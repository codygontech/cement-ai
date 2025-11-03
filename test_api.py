"""Test the API endpoint"""
import requests


def test_api():
    try:
        resp = requests.get('http://localhost:8000/api/data/alternative-fuels', timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            print(f"\n✅ API Response: {len(data)} records")
            print(f"\nFirst 3 records:")
            for i, item in enumerate(data[:3]):
                print(f"\n  Record {i+1}:")
                print(f"    fuel_type: {item.get('fuel_type')}")
                print(f"    tsr: {item.get('tsr')}")
                print(f"    timestamp: {item.get('timestamp')}")
            
            # Calculate average
            tsr_values = [item.get('tsr', 0) for item in data if item.get('tsr')]
            if tsr_values:
                avg = sum(tsr_values) / len(tsr_values)
                print(f"\n  Average TSR from API: {avg:.2f}%")
            else:
                print(f"\n  ❌ No TSR values found in API response")
        else:
            print(f"❌ API returned status {resp.status_code}")
    except requests.ConnectionError:
        print("❌ Cannot connect to API. Is the backend running on port 8000?")
        print("   Start it with: cd backend && uvicorn app.main:app --reload")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    test_api()
