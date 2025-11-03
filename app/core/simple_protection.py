"""
Simple in-memory rate limiting for hackathon demo
No Redis needed - uses Python dict (resets on restart)
"""

from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, Tuple
from fastapi import HTTPException, Request
import asyncio
import re

# In-memory storage (will reset on server restart - perfect for hackathon!)
request_history: Dict[str, list] = defaultdict(list)
daily_costs: Dict[str, float] = defaultdict(float)

# Simple limits
MAX_REQUESTS_PER_MINUTE = 20
MAX_REQUESTS_PER_HOUR = 200
MAX_MESSAGE_LENGTH = 2000
MAX_DAILY_COST = 5.0  # $5 per user per day (you have GCP credits!)


def get_client_id(request: Request) -> str:
    """Get client identifier (IP address for hackathon)"""
    return request.client.host if request.client else "unknown"


def check_rate_limit(client_id: str) -> Tuple[bool, str]:
    """
    Check if client has exceeded rate limits
    Returns: (is_allowed, error_message)
    """
    now = datetime.now()
    
    # Clean old entries (older than 1 hour)
    request_history[client_id] = [
        req_time for req_time in request_history[client_id]
        if now - req_time < timedelta(hours=1)
    ]
    
    requests = request_history[client_id]
    
    # Check last minute
    recent_requests = [r for r in requests if now - r < timedelta(minutes=1)]
    if len(recent_requests) >= MAX_REQUESTS_PER_MINUTE:
        return False, f"Rate limit: Max {MAX_REQUESTS_PER_MINUTE} requests per minute"
    
    # Check last hour
    if len(requests) >= MAX_REQUESTS_PER_HOUR:
        return False, f"Rate limit: Max {MAX_REQUESTS_PER_HOUR} requests per hour"
    
    # Add this request
    request_history[client_id].append(now)
    
    return True, ""


def validate_message(message: str) -> Tuple[bool, str]:
    """
    Basic message validation
    Returns: (is_valid, error_message)
    """
    if not message or not message.strip():
        return False, "Message cannot be empty"
    
    if len(message) > MAX_MESSAGE_LENGTH:
        return False, f"Message too long (max {MAX_MESSAGE_LENGTH} characters)"
    
    # Block obvious spam/injection attempts
    dangerous_patterns = [
        r'<script',
        r'javascript:',
        r'DROP TABLE',
        r'DELETE FROM',
        r'{{',  # Template injection
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, message, re.IGNORECASE):
            return False, "Invalid message format"
    
    return True, ""


def track_cost(client_id: str, tokens_used: int) -> bool:
    """
    Track costs (rough estimate)
    Gemini Flash: ~$0.0001 per 1K tokens
    Returns: True if under budget
    """
    cost = (tokens_used / 1000) * 0.0001
    daily_costs[client_id] += cost
    
    if daily_costs[client_id] > MAX_DAILY_COST:
        return False
    
    return True


def estimate_tokens(text: str) -> int:
    """Rough token estimate: ~4 chars = 1 token"""
    return len(text) // 4


def get_stats() -> dict:
    """Get current usage stats"""
    return {
        "active_clients": len(request_history),
        "total_requests": sum(len(reqs) for reqs in request_history.values()),
        "total_cost_usd": round(sum(daily_costs.values()), 4),
        "status": "healthy"
    }


async def cleanup_old_data():
    """Background task to clean up old data (run daily)"""
    while True:
        await asyncio.sleep(86400)  # 24 hours
        daily_costs.clear()
        for client_id in list(request_history.keys()):
            request_history[client_id] = []
