"""Test API response format"""
import requests
import json

try:
    resp = requests.get('http://localhost:8000/api/data/alternative-fuels?limit=5', timeout=5)
    print(f"Status: {resp.status_code}")
    print(f"Content-Type: {resp.headers.get('content-type')}")
    
    if resp.status_code == 200:
        data = resp.json()
        print(f"\nData type: {type(data)}")
        print(f"Data length: {len(data) if isinstance(data, list) else 'N/A'}")
        print(f"\nFull response:")
        print(json.dumps(data, indent=2, default=str))
    else:
        print(f"Error: {resp.text}")
except Exception as e:
    print(f"Error: {e}")
