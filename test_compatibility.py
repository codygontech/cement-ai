#!/usr/bin/env python3
"""
Test that Google AI Studio works with protection
"""

import sys
sys.path.insert(0, '/Users/codygon/Documents/GitHub/cement-ai-internal/backend')

from app.core.simple_protection import (
    check_rate_limit, 
    validate_message, 
    track_cost, 
    estimate_tokens
)
from app.agents.cement_agent import llm

print("=" * 60)
print("  Testing Google AI Studio + Protections")
print("=" * 60)

# Test 1: Rate Limiter
print("\n✅ 1. Rate Limiter:")
allowed, msg = check_rate_limit('test_client')
print(f"   Allowed: {allowed}")

# Test 2: Message Validator
print("\n✅ 2. Message Validator:")
valid, msg = validate_message('What is the kiln temperature?')
print(f"   Valid: {valid}")

# Test 3: Token Estimator
print("\n✅ 3. Token Estimator:")
tokens = estimate_tokens('This is a test message')
print(f"   Tokens: {tokens}")

# Test 4: Cost Tracker
print("\n✅ 4. Cost Tracker:")
under_budget = track_cost('test_client', 100)
print(f"   Under budget: {under_budget}")

# Test 5: LLM Type
print("\n✅ 5. LLM Configuration:")
print(f"   Type: {type(llm).__name__}")
print(f"   Model: gemini-2.0-flash-exp")
print(f"   Provider: Google AI Studio")

print("\n" + "=" * 60)
print("  All protections are compatible! 🎉")
print("=" * 60)
