/**
 * Frontend Telemetry Client
 * Collects anonymous usage analytics and sends to telemetry service
 * Always enabled - no opt-out functionality
 */

import crypto from 'crypto';

// Telemetry configuration
const TELEMETRY_ENDPOINT = 'https://cementaitelemetry.codygon.com/telemetry';
const SESSION_STORAGE_KEY = 'cement_ai_session_id';
const INSTANCE_STORAGE_KEY = 'cement_ai_instance_id';

/**
 * NOTE: Frontend telemetry does NOT use request signatures like backend
 * Reason: Any secret in browser JavaScript is visible to users
 * Protection: Telemetry service uses rate limiting + anomaly detection instead
 * This is similar to how Google Analytics, Mixpanel, etc. work
 */

interface TelemetryEvent {
  instance_id: string;
  session_id: string;
  event_type: 'page_view' | 'interaction' | 'error' | 'performance' | 'startup' | 'shutdown';
  timestamp: string;
  
  // Browser/Device info
  browser_name?: string;
  browser_version?: string;
  os_type?: string;
  screen_width?: number;
  screen_height?: number;
  device_type?: string;
  language?: string;
  timezone?: string;
  
  // Configuration
  api_endpoint?: string;
  use_mock_data?: boolean;
  app_version?: string;
  
  // Event-specific data
  page_path?: string;
  page_title?: string;
  referrer?: string;
  interaction_type?: string;
  interaction_target?: string;
  error_message?: string;
  error_stack?: string;
  performance_metric?: string;
  performance_value?: number;
  
  // Custom event data
  event_data?: Record<string, unknown>;
}

/**
 * Telemetry Client - Always enabled
 */
class TelemetryClient {
  private instanceId: string;
  private sessionId: string;
  private isInitialized: boolean = false;
  
  constructor() {
    this.instanceId = '';
    this.sessionId = '';
  }
  
  /**
   * Initialize telemetry (call on app startup)
   */
  async initialize(): Promise<void> {
    if (this.isInitialized) return;
    
    try {
      // Get or create instance ID (persistent across sessions)
      this.instanceId = this.getOrCreateInstanceId();
      
      // Get or create session ID (new for each browser session)
      this.sessionId = this.getOrCreateSessionId();
      
      this.isInitialized = true;
      
      // Send startup event
      await this.trackEvent('startup', {
        event_data: {
          initialization_time: new Date().toISOString(),
        },
      });
      
      // Track page unload
      if (typeof window !== 'undefined') {
        window.addEventListener('beforeunload', () => {
          this.trackEvent('shutdown', {}, true); // Synchronous for unload
        });
      }
    } catch (error) {
      console.error('Failed to initialize telemetry:', error);
    }
  }
  
  /**
   * Get or create persistent instance ID
   */
  private getOrCreateInstanceId(): string {
    if (typeof window === 'undefined') return 'server-render';
    
    let instanceId = localStorage.getItem(INSTANCE_STORAGE_KEY);
    
    if (!instanceId) {
      // Generate UUID v4
      instanceId = this.generateUUID();
      localStorage.setItem(INSTANCE_STORAGE_KEY, instanceId);
    }
    
    return instanceId;
  }
  
  /**
   * Get or create session ID (expires when browser closes)
   */
  private getOrCreateSessionId(): string {
    if (typeof window === 'undefined') return 'server-render';
    
    let sessionId = sessionStorage.getItem(SESSION_STORAGE_KEY);
    
    if (!sessionId) {
      sessionId = this.generateUUID();
      sessionStorage.setItem(SESSION_STORAGE_KEY, sessionId);
    }
    
    return sessionId;
  }
  
  /**
   * Generate UUID v4
   */
  private generateUUID(): string {
    if (typeof crypto !== 'undefined' && crypto.randomUUID) {
      return crypto.randomUUID();
    }
    
    // Fallback for older browsers
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
      const r = Math.random() * 16 | 0;
      const v = c === 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
  }
  
  /**
   * Get browser information
   */
  private getBrowserInfo() {
    if (typeof window === 'undefined') return {};
    
    const ua = navigator.userAgent;
    let browserName = 'Unknown';
    let browserVersion = 'Unknown';
    
    // Detect browser
    if (ua.indexOf('Chrome') > -1 && ua.indexOf('Edg') === -1) {
      browserName = 'Chrome';
      browserVersion = ua.match(/Chrome\/(\d+\.\d+)/)?.[1] || 'Unknown';
    } else if (ua.indexOf('Safari') > -1 && ua.indexOf('Chrome') === -1) {
      browserName = 'Safari';
      browserVersion = ua.match(/Version\/(\d+\.\d+)/)?.[1] || 'Unknown';
    } else if (ua.indexOf('Firefox') > -1) {
      browserName = 'Firefox';
      browserVersion = ua.match(/Firefox\/(\d+\.\d+)/)?.[1] || 'Unknown';
    } else if (ua.indexOf('Edg') > -1) {
      browserName = 'Edge';
      browserVersion = ua.match(/Edg\/(\d+\.\d+)/)?.[1] || 'Unknown';
    }
    
    // Get additional browser capabilities
    const additionalInfo: Record<string, unknown> = {};
    
    // Memory info (Chrome only)
    if ('memory' in performance) {
      const perfWithMemory = performance as Performance & { 
        memory?: { 
          usedJSHeapSize: number; 
          jsHeapSizeLimit: number; 
        } 
      };
      if (perfWithMemory.memory) {
        additionalInfo.heap_size_mb = Math.round(perfWithMemory.memory.usedJSHeapSize / 1024 / 1024);
        additionalInfo.heap_limit_mb = Math.round(perfWithMemory.memory.jsHeapSizeLimit / 1024 / 1024);
      }
    }
    
    // Network info (if available)
    if ('connection' in navigator) {
      const navWithConnection = navigator as Navigator & {
        connection?: {
          effectiveType?: string;
          downlink?: number;
          rtt?: number;
          saveData?: boolean;
        }
      };
      if (navWithConnection.connection) {
        const conn = navWithConnection.connection;
        additionalInfo.network_type = conn.effectiveType; // '4g', '3g', '2g', 'slow-2g'
        additionalInfo.network_downlink = conn.downlink; // Mbps
        additionalInfo.network_rtt = conn.rtt; // Round trip time in ms
        additionalInfo.network_save_data = conn.saveData; // Data saver enabled?
      }
    }
    
    // Hardware concurrency (logical CPU cores available to browser)
    if ('hardwareConcurrency' in navigator) {
      additionalInfo.logical_cores = navigator.hardwareConcurrency;
    }
    
    // Device pixel ratio (for detecting high-DPI displays)
    additionalInfo.pixel_ratio = window.devicePixelRatio;
    
    // Viewport size (visible area, different from screen size)
    additionalInfo.viewport_width = window.innerWidth;
    additionalInfo.viewport_height = window.innerHeight;
    
    // Color depth
    additionalInfo.color_depth = window.screen.colorDepth;
    
    // WebGL/GPU info (limited in browsers for privacy)
    try {
      const canvas = document.createElement('canvas');
      const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
      if (gl && gl instanceof WebGLRenderingContext) {
        const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
        if (debugInfo) {
          additionalInfo.gpu_vendor = gl.getParameter(debugInfo.UNMASKED_VENDOR_WEBGL);
          additionalInfo.gpu_renderer = gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL);
        }
      }
    } catch {
      // GPU detection not available
    }
    
    return {
      browser_name: browserName,
      browser_version: browserVersion,
      os_type: this.getOSType(ua),
      screen_width: window.screen.width,
      screen_height: window.screen.height,
      device_type: this.getDeviceType(),
      language: navigator.language,
      timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
      event_data: additionalInfo, // Additional info goes into event_data
    };
  }
  
  /**
   * Detect OS type from user agent
   */
  private getOSType(ua: string): string {
    if (ua.indexOf('Win') > -1) return 'Windows';
    if (ua.indexOf('Mac') > -1) return 'MacOS';
    if (ua.indexOf('Linux') > -1) return 'Linux';
    if (ua.indexOf('Android') > -1) return 'Android';
    if (ua.indexOf('iOS') > -1 || ua.indexOf('iPhone') > -1 || ua.indexOf('iPad') > -1) return 'iOS';
    return 'Unknown';
  }
  
  /**
   * Detect device type (desktop, tablet, mobile)
   */
  private getDeviceType(): string {
    if (typeof window === 'undefined') return 'Unknown';
    
    const width = window.screen.width;
    if (width >= 1024) return 'Desktop';
    if (width >= 768) return 'Tablet';
    return 'Mobile';
  }
  
  /**
   * Get configuration info
   */
  private getConfigInfo() {
    return {
      api_endpoint: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
      use_mock_data: process.env.NEXT_PUBLIC_USE_MOCK_DATA === 'true',
      app_version: process.env.NEXT_PUBLIC_APP_VERSION || '0.1.0',
    };
  }
  
  /**
   * Track an event
   */
  async trackEvent(
    eventType: TelemetryEvent['event_type'],
    data: Partial<TelemetryEvent> = {},
    synchronous: boolean = false
  ): Promise<void> {
    if (!this.isInitialized && eventType !== 'startup') {
      console.warn('Telemetry not initialized, skipping event:', eventType);
      return;
    }
    
    try {
      const event: TelemetryEvent = {
        instance_id: this.instanceId,
        session_id: this.sessionId,
        event_type: eventType,
        timestamp: new Date().toISOString(),
        ...this.getBrowserInfo(),
        ...this.getConfigInfo(),
        ...data,
      };
      
      const payload = JSON.stringify(event);
      
      const sendData = () => {
        if (synchronous && typeof navigator !== 'undefined' && 'sendBeacon' in navigator) {
          // Use sendBeacon for synchronous events (like page unload)
          const blob = new Blob([payload], { type: 'application/json' });
          navigator.sendBeacon(TELEMETRY_ENDPOINT, blob);
        } else {
          // Regular async fetch - no signature needed for frontend
          fetch(TELEMETRY_ENDPOINT, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: payload,
            keepalive: synchronous, // Keep connection alive for unload events
          }).catch(error => {
            console.error('Failed to send telemetry:', error);
          });
        }
      };
      
      sendData();
    } catch (error) {
      console.error('Failed to track event:', error);
    }
  }
  
  /**
   * Track page view
   */
  async trackPageView(path?: string, title?: string): Promise<void> {
    if (typeof window === 'undefined') return;
    
    await this.trackEvent('page_view', {
      page_path: path || window.location.pathname,
      page_title: title || document.title,
      referrer: document.referrer || 'direct',
    });
  }
  
  /**
   * Track user interaction
   */
  async trackInteraction(type: string, target: string, data?: Record<string, unknown>): Promise<void> {
    await this.trackEvent('interaction', {
      interaction_type: type,
      interaction_target: target,
      event_data: data,
    });
  }
  
  /**
   * Track error
   */
  async trackError(error: Error | string, context?: string): Promise<void> {
    const errorMessage = typeof error === 'string' ? error : error.message;
    const errorStack = typeof error === 'string' ? undefined : error.stack;
    
    await this.trackEvent('error', {
      error_message: errorMessage,
      error_stack: errorStack,
      event_data: { context },
    });
  }
  
  /**
   * Track performance metric
   */
  async trackPerformance(metric: string, value: number, data?: Record<string, unknown>): Promise<void> {
    await this.trackEvent('performance', {
      performance_metric: metric,
      performance_value: value,
      event_data: data,
    });
  }
}

// Export singleton instance
export const telemetry = new TelemetryClient();

// Export for use in components
export default telemetry;
