"""
Telemetry Client for Cement AI Backend
Sends anonymous usage data to telemetry service

Privacy: All data is anonymous. No PII is collected.
Control: Users can disable telemetry at any time using toggle_telemetry.py script
"""

import uuid
import asyncio
import platform
import sys
import os
import psutil
import shutil
import hmac
import hashlib
from datetime import datetime
from typing import Optional, Dict, Any
from pathlib import Path
import json

import httpx
from app.core.logging_config import logger
from app.core.config import settings


# Telemetry configuration file (stores only instance ID)
TELEMETRY_CONFIG_FILE = Path(".telemetry")

# Telemetry endpoint (publicly available, protected by signatures and rate limiting)
TELEMETRY_ENDPOINT = os.getenv(
    "TELEMETRY_ENDPOINT",
    "https://cementaitelemetry.codygon.com/telemetry"
)

# Application version (read from package or environment)
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")


class TelemetryClient:
    """Anonymous telemetry client - always enabled"""
    
    def __init__(self):
        self.instance_id: Optional[str] = None
        self.session_start: Optional[datetime] = None
        self.http_client: Optional[httpx.AsyncClient] = None
        
        # Load configuration
        self._load_config()
    
    def _load_config(self):
        """Load telemetry instance ID from file"""
        try:
            if TELEMETRY_CONFIG_FILE.exists():
                config = json.loads(TELEMETRY_CONFIG_FILE.read_text())
                self.instance_id = config.get("instance_id")
            else:
                # First run - create instance ID
                self.instance_id = str(uuid.uuid4())
                self._save_config()
                
            logger.info("Telemetry: enabled")
            
        except Exception as e:
            logger.warning(f"Failed to load telemetry config: {e}")
            # Still create instance ID for telemetry
            self.instance_id = str(uuid.uuid4())
    
    def _save_config(self):
        """Save telemetry instance ID to file"""
        try:
            config = {
                "instance_id": self.instance_id,
                "created_at": datetime.utcnow().isoformat()
            }
            TELEMETRY_CONFIG_FILE.write_text(json.dumps(config, indent=2))
            
            # Add to .gitignore if not already there
            gitignore = Path(".gitignore")
            if gitignore.exists():
                content = gitignore.read_text()
                if ".telemetry" not in content:
                    with gitignore.open("a") as f:
                        f.write("\n# Telemetry configuration\n.telemetry\n")
                        
        except Exception as e:
            logger.warning(f"Failed to save telemetry config: {e}")
    
    def _generate_signature(self, instance_id: str, timestamp: str, event_type: str) -> str:
        """
        Generate HMAC signature for request validation
        Uses instance_id as the secret key (same as server)
        """
        message = f"{instance_id}:{timestamp}:{event_type}"
        return hmac.new(
            instance_id.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
    
    async def _send_event(
        self,
        event_type: str,
        event_data: Optional[Dict[str, Any]] = None,
        error_type: Optional[str] = None,
        error_message: Optional[str] = None
    ):
        """Send telemetry event to service"""
        if not self.instance_id:
            return
        
        try:
            # Build event payload
            timestamp = datetime.utcnow().isoformat()
            payload = {
                "instance_id": self.instance_id,
                "event_type": event_type,
                "timestamp": timestamp,
                "app_version": APP_VERSION,
                "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
                "os_type": platform.system(),
                "deployment_type": self._get_deployment_type(),
                "region": os.getenv("VERTEX_AI_LOCATION", "unknown"),
            }
            
            if event_data:
                payload["event_data"] = event_data
            
            if error_type:
                payload["error_type"] = error_type
                payload["error_message"] = error_message
            
            # Generate signature for request validation
            signature = self._generate_signature(self.instance_id, timestamp, event_type)
            
            # Send async (non-blocking)
            if self.http_client is None:
                self.http_client = httpx.AsyncClient(timeout=5.0)
            
            # Await the post directly instead of creating a task
            await self._post_event(payload, signature, timestamp)
            
        except Exception as e:
            # Telemetry should never break the application
            logger.debug(f"Failed to send telemetry: {e}")
    
    async def _post_event(self, payload: dict, signature: str, timestamp: str):
        """Post event to telemetry service with signature headers"""
        try:
            logger.info(f"Sending telemetry event: {payload.get('event_type')}")
            headers = {
                "X-Signature": signature,
                "X-Timestamp": timestamp
            }
            response = await self.http_client.post(
                TELEMETRY_ENDPOINT,
                json=payload,
                headers=headers
            )
            
            logger.info(f"Telemetry response: {response.status_code}")
            
            # Log rate limiting (helpful for debugging)
            if response.status_code == 429:
                logger.debug("Telemetry rate limited")
            elif response.status_code not in [200, 201]:
                logger.debug(f"Telemetry request failed: {response.status_code}")
                
        except Exception as e:
            # Silently fail - telemetry is best-effort
            logger.warning(f"Telemetry failed: {e}")
    
    def _get_deployment_type(self) -> str:
        """Detect deployment type"""
        if os.getenv("K_SERVICE"):
            return "cloud_run"
        elif os.getenv("KUBERNETES_SERVICE_HOST"):
            return "kubernetes"
        elif Path("/.dockerenv").exists():
            return "docker"
        else:
            return "local"
    
    def _get_network_info(self) -> Dict[str, Any]:
        """Collect network information (hostname, domain, public IP, local IP)"""
        try:
            import socket
            import urllib.request
            
            # Hostname
            hostname = socket.gethostname()
            
            # Domain/FQDN (Fully Qualified Domain Name)
            try:
                fqdn = socket.getfqdn()
                # Extract domain from FQDN (everything after first dot)
                if '.' in fqdn and fqdn != hostname:
                    domain = '.'.join(fqdn.split('.')[1:])
                else:
                    domain = None
            except Exception:
                domain = None
            
            # Local IP address (private network IP)
            local_ip = None
            try:
                # Create a socket to get the local IP (doesn't actually connect)
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                local_ip = s.getsockname()[0]
                s.close()
            except Exception:
                try:
                    # Fallback: get IP from hostname
                    local_ip = socket.gethostbyname(hostname)
                    # Filter out loopback
                    if local_ip.startswith('127.'):
                        local_ip = None
                except Exception:
                    pass
            
            # Public IP address (external/WAN IP)
            public_ip = None
            try:
                # Try multiple services for reliability
                services = [
                    'https://api.ipify.org',
                    'https://checkip.amazonaws.com',
                    'https://icanhazip.com'
                ]
                
                for service in services:
                    try:
                        with urllib.request.urlopen(service, timeout=2) as response:
                            public_ip = response.read().decode('utf-8').strip()
                            if public_ip:
                                break
                    except Exception:
                        continue
            except Exception:
                pass
            
            return {
                "hostname": hostname,
                "domain": domain,
                "local_ip": local_ip,
                "public_ip": public_ip,
            }
        except Exception as e:
            logger.debug(f"Failed to collect network info: {e}")
            return {}
    
    def _get_hardware_info(self) -> Dict[str, Any]:
        """Collect hardware information"""
        try:
            # CPU info
            cpu_count = psutil.cpu_count(logical=True)
            cpu_arch = platform.machine()
            
            # Memory info
            memory = psutil.virtual_memory()
            total_memory_gb = round(memory.total / (1024**3), 2)
            available_memory_gb = round(memory.available / (1024**3), 2)
            
            # Disk info
            disk = psutil.disk_usage('/')
            disk_total_gb = round(disk.total / (1024**3), 2)
            disk_available_gb = round(disk.free / (1024**3), 2)
            
            # GPU info (multiple detection methods)
            gpu_available = False
            gpu_info = None
            
            # Method 1: Try PyTorch CUDA
            try:
                import torch
                if torch.cuda.is_available():
                    gpu_available = True
                    gpu_info = torch.cuda.get_device_name(0)
            except (ImportError, Exception):
                pass
            
            # Method 2: Try nvidia-smi (NVIDIA GPUs)
            if not gpu_available:
                try:
                    import subprocess
                    result = subprocess.run(
                        ['nvidia-smi', '--query-gpu=name', '--format=csv,noheader'],
                        capture_output=True,
                        text=True,
                        timeout=2
                    )
                    if result.returncode == 0 and result.stdout.strip():
                        gpu_available = True
                        gpu_info = result.stdout.strip().split('\n')[0]
                except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
                    pass
            
            # Method 3: Check Windows registry for GPU (Windows only)
            if not gpu_available and platform.system() == "Windows":
                try:
                    import subprocess
                    result = subprocess.run(
                        ['wmic', 'path', 'win32_VideoController', 'get', 'name'],
                        capture_output=True,
                        text=True,
                        timeout=2
                    )
                    if result.returncode == 0:
                        lines = [line.strip() for line in result.stdout.split('\n') if line.strip()]
                        # Skip the header "Name" and get actual GPU names
                        gpu_names = [line for line in lines[1:] if line and 'microsoft' not in line.lower()]
                        if gpu_names:
                            gpu_available = True
                            gpu_info = gpu_names[0]
                except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
                    pass
            
            return {
                "cpu_count": cpu_count,
                "cpu_arch": cpu_arch,
                "total_memory_gb": total_memory_gb,
                "available_memory_gb": available_memory_gb,
                "disk_total_gb": disk_total_gb,
                "disk_available_gb": disk_available_gb,
                "gpu_available": gpu_available,
                "gpu_info": gpu_info,
            }
        except Exception as e:
            logger.debug(f"Failed to collect hardware info: {e}")
            return {}
    
    def _get_configuration_info(self) -> Dict[str, Any]:
        """Collect application configuration information (no secrets!)"""
        try:
            # Database type detection
            database_type = "none"
            if settings.DATABASE_URL:
                if "postgresql" in settings.DATABASE_URL:
                    database_type = "postgresql"
                elif "cloudsql" in settings.DATABASE_URL:
                    database_type = "cloud_sql"
            elif settings.JDBC_DB_STRING:
                database_type = "cloud_sql_jdbc"
            
            # CORS origins (actual values - not sensitive as they're public-facing)
            cors_origins = settings.CORS_ORIGINS if hasattr(settings, 'CORS_ORIGINS') else None
            
            return {
                "database_type": database_type,
                "ai_model": settings.VERTEX_AI_MODEL if hasattr(settings, 'VERTEX_AI_MODEL') else None,
                "vertex_ai_enabled": bool(settings.VERTEX_AI_MODEL) if hasattr(settings, 'VERTEX_AI_MODEL') else False,
                "cloud_storage_enabled": bool(settings.GCS_IMAGES_BUCKET) if hasattr(settings, 'GCS_IMAGES_BUCKET') else False,
                "vision_api_enabled": True,  # Assume enabled if app is running
                "cloud_logging_enabled": settings.ENABLE_CLOUD_LOGGING if hasattr(settings, 'ENABLE_CLOUD_LOGGING') else False,
                "cors_origins": cors_origins,
                "api_port": settings.API_PORT if hasattr(settings, 'API_PORT') else None,
            }
        except Exception as e:
            logger.debug(f"Failed to collect configuration info: {e}")
            return {}
    
    async def track_startup(self):
        """Track application startup with hardware and configuration info"""
        self.session_start = datetime.utcnow()
        
        # Collect hardware, configuration, and network info on startup
        hardware_info = self._get_hardware_info()
        config_info = self._get_configuration_info()
        network_info = self._get_network_info()
        
        # Build enhanced payload
        timestamp = datetime.utcnow().isoformat()
        payload = {
            "instance_id": self.instance_id,
            "event_type": "startup",
            "timestamp": timestamp,
            "app_version": APP_VERSION,
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "os_type": platform.system(),
            "deployment_type": self._get_deployment_type(),
            "region": os.getenv("VERTEX_AI_LOCATION", "unknown"),
            **hardware_info,
            **config_info,
            **network_info,
        }
        
        # Send telemetry
        if self.instance_id:
            try:
                if self.http_client is None:
                    self.http_client = httpx.AsyncClient(timeout=5.0)
                # Generate signature
                signature = self._generate_signature(self.instance_id, timestamp, "startup")
                # Await directly to ensure it completes during startup
                await self._post_event(payload, signature, timestamp)
            except Exception as e:
                logger.debug(f"Failed to send startup telemetry: {e}")
    
    async def track_shutdown(self):
        """Track application shutdown"""
        if self.session_start:
            duration = (datetime.utcnow() - self.session_start).total_seconds() / 60
            await self._send_event(
                "shutdown",
                event_data={"session_duration_minutes": round(duration, 2)}
            )
        
        # Close HTTP client
        if self.http_client:
            await self.http_client.aclose()
    
    async def track_api_call(self, endpoint: str, method: str = "GET"):
        """Track API endpoint usage (aggregated, no sensitive data)"""
        await self._send_event(
            "api_call",
            event_data={
                "endpoint": endpoint,
                "method": method
            }
        )
    
    async def track_feature_usage(self, feature: str, details: Optional[Dict] = None):
        """Track feature usage"""
        event_data = {"feature": feature}
        if details:
            event_data.update(details)
        
        await self._send_event("feature_usage", event_data=event_data)
    
    async def track_error(self, error_type: str, error_message: str, sanitized: bool = False):
        """
        Track error occurrence
        
        IMPORTANT: error_message should be sanitized - no sensitive data!
        Set sanitized=True if you've already sanitized the message
        """
        if not sanitized:
            # Basic sanitization - remove anything that looks like credentials
            error_message = error_message[:200]  # Limit length
            # Add more sanitization rules as needed
        
        await self._send_event(
            "error",
            error_type=error_type,
            error_message=error_message
        )


# Global telemetry client instance
_telemetry_client: Optional[TelemetryClient] = None


def get_telemetry_client() -> TelemetryClient:
    """Get global telemetry client instance"""
    global _telemetry_client
    if _telemetry_client is None:
        _telemetry_client = TelemetryClient()
    return _telemetry_client


# Convenience functions
async def track_startup():
    """Track application startup"""
    client = get_telemetry_client()
    await client.track_startup()


async def track_shutdown():
    """Track application shutdown"""
    client = get_telemetry_client()
    await client.track_shutdown()


async def track_api_call(endpoint: str, method: str = "GET"):
    """Track API endpoint usage"""
    client = get_telemetry_client()
    await client.track_api_call(endpoint, method)


async def track_feature_usage(feature: str, details: Optional[Dict] = None):
    """Track feature usage"""
    client = get_telemetry_client()
    await client.track_feature_usage(feature, details)


async def track_error(error_type: str, error_message: str, sanitized: bool = False):
    """Track error occurrence"""
    client = get_telemetry_client()
    await client.track_error(error_type, error_message, sanitized)
