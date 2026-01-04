import requests
import time

def test_services():
    print("Testing NCERT Doubt Solver Services...")
    
    print("\n1. Testing Backend API (localhost:8000)...")
    try:
        response = requests.get('http://localhost:8000/api/languages', timeout=5)
        if response.status_code == 200:
            print("   ✅ Backend API is running")
            print("   Supported languages:", response.json().get('languages', []))
        else:
            print("   ❌ Backend API returned status:", response.status_code)
    except requests.exceptions.ConnectionError:
        print("   ❌ Backend API is not accessible")
    except Exception as e:
        print("   ❌ Backend API error:", str(e))
    
    print("\n2. Testing Frontend Service (localhost:3000)...")
    try:
        response = requests.get('http://localhost:3000', timeout=5)
        if response.status_code == 200:
            print("   ✅ Frontend service is running")
            if '<title>NCERT Doubt Solver</title>' in response.text:
                print("   ✅ Correct frontend page loaded")
            else:
                print("   ⚠️  Frontend page loaded but may be incorrect")
        else:
            print("   ❌ Frontend service returned status:", response.status_code)
    except requests.exceptions.ConnectionError:
        print("   ❌ Frontend service is not accessible")
    except Exception as e:
        print("   ❌ Frontend service error:", str(e))
    
    print("\n3. Instructions:")
    print("   - Backend API: http://localhost:8000")
    print("   - Frontend UI: http://localhost:3000")
    print("   - To test the chat API, send POST request to http://localhost:8000/api/chat")

if __name__ == "__main__":
    test_services()