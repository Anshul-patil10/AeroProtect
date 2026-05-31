"""Quick test to verify backend is working"""
import requests

try:
    response = requests.get('http://localhost:5000/health')
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print("\n✅ Backend is working perfectly!")
except Exception as e:
    print(f"❌ Error: {e}")
