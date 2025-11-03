"""Quick API test"""
import requests

print("Testing backend API...")
try:
    # Test root endpoint
    resp = requests.get('http://localhost:8000/', timeout=2)
    print(f"✅ Root endpoint: {resp.status_code}")
    
    # Test alternative fuels endpoint
    resp = requests.get('http://localhost:8000/api/data/alternative-fuels?limit=5', timeout=2)
    print(f"✅ Alternative fuels endpoint: {resp.status_code}")
    
    if resp.status_code == 200:
        data = resp.json()
        print(f"   Records returned: {len(data)}")
        if data:
            tsr_values = [item.get('tsr') for item in data if item.get('tsr') is not None]
            if tsr_values:
                avg = sum(tsr_values) / len(tsr_values)
                print(f"   ✅ Average TSR: {avg:.2f}%")
            else:
                print(f"   ❌ No TSR values in response")
except requests.Timeout:
    print("❌ Request timed out - backend might be slow or not running")
except requests.ConnectionError:
    print("❌ Cannot connect - backend is not running on port 8000")
except Exception as e:
    print(f"❌ Error: {e}")
