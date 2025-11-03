#!/usr/bin/env python3
"""
Quick test script for simple chat protection
Run this while your backend is running
"""

import requests
import time

BASE_URL = "http://localhost:8000/api"


def test_normal_request():
    """Test a normal chat request"""
    print("\n🧪 Test 1: Normal request")
    response = requests.post(
        f"{BASE_URL}/chat",
        json={"message": "What is the current kiln temperature?"}
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✅ Success! Got response")
    else:
        print(f"   ❌ Failed: {response.json()}")


def test_rate_limit():
    """Test rate limiting"""
    print("\n🧪 Test 2: Rate limiting (sending 25 requests quickly)")
    rate_limited = False
    
    for i in range(25):
        response = requests.post(
            f"{BASE_URL}/chat",
            json={"message": f"Test {i+1}"}
        )
        
        if response.status_code == 429:
            print(f"   ✅ Rate limit triggered at request #{i+1}")
            print(f"   Message: {response.json().get('detail')}")
            rate_limited = True
            break
        elif i < 5 or i % 5 == 0:
            print(f"   Request #{i+1}: OK")
    
    if not rate_limited:
        print(f"   ⚠️  No rate limit hit (maybe increase request count)")


def test_message_validation():
    """Test message validation"""
    print("\n🧪 Test 3: Message validation")
    
    # Test long message
    print("   Testing long message...")
    response = requests.post(
        f"{BASE_URL}/chat",
        json={"message": "x" * 2500}
    )
    if response.status_code == 400:
        print(f"   ✅ Long message blocked: {response.json().get('detail')}")
    else:
        print(f"   ❌ Long message not blocked")
    
    # Test empty message
    print("   Testing empty message...")
    response = requests.post(
        f"{BASE_URL}/chat",
        json={"message": "   "}
    )
    if response.status_code == 400:
        print(f"   ✅ Empty message blocked: {response.json().get('detail')}")
    else:
        print(f"   ❌ Empty message not blocked")
    
    # Test injection attempt
    print("   Testing SQL injection...")
    response = requests.post(
        f"{BASE_URL}/chat",
        json={"message": "'; DROP TABLE users; --"}
    )
    if response.status_code == 400:
        print(f"   ✅ SQL injection blocked: {response.json().get('detail')}")
    else:
        print(f"   ❌ SQL injection not blocked")


def test_stats_endpoint():
    """Test stats endpoint"""
    print("\n🧪 Test 4: Stats endpoint")
    response = requests.get(f"{BASE_URL}/chat/stats")
    if response.status_code == 200:
        stats = response.json()
        print(f"   ✅ Stats retrieved:")
        print(f"      Active clients: {stats.get('active_clients')}")
        print(f"      Total requests: {stats.get('total_requests')}")
        print(f"      Total cost: ${stats.get('total_cost_usd')}")
        print(f"      Status: {stats.get('status')}")
    else:
        print(f"   ❌ Failed to get stats")


def main():
    print("=" * 60)
    print("  Simple Chat Protection Test Suite")
    print("  Make sure your backend is running on port 8000")
    print("=" * 60)
    
    try:
        # Check if backend is running
        response = requests.get(f"{BASE_URL.replace('/api', '')}/")
        print("✅ Backend is running\n")
    except requests.exceptions.ConnectionError:
        print("❌ Backend is not running!")
        print("   Start it with: cd backend && uvicorn app.main:main --reload")
        return
    
    # Run tests
    test_normal_request()
    time.sleep(1)
    
    test_message_validation()
    time.sleep(1)
    
    test_rate_limit()
    time.sleep(1)
    
    test_stats_endpoint()
    
    print("\n" + "=" * 60)
    print("  Tests complete! 🎉")
    print("=" * 60)


if __name__ == "__main__":
    main()
