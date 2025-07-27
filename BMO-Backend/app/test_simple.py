import requests
import json
import time

def test_api():
    base_url = "http://localhost:8000"
    
    # Wait for server to start
    print("Waiting for server to start...")
    for i in range(10):
        try:
            response = requests.get(f"{base_url}/health", timeout=5)
            if response.status_code == 200:
                print("Server is ready!")
                break
        except:
            time.sleep(1)
            print(f"Waiting... ({i+1}/10)")
    else:
        print("Server failed to start")
        return
    
    # Test chat
    print("\nTesting chat endpoint...")
    test_data = {"prompt": "What is 2+2?", "max_tokens": 50}
    
    try:
        response = requests.post(f"{base_url}/chat", json=test_data, timeout=30)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Chat test failed: {e}")
    
    # Test direct endpoint
    print("\nTesting direct endpoint...")
    try:
        response = requests.post(f"{base_url}/test-direct", json=test_data, timeout=30)
        print(f"Status: {response.status_code}")
        result = response.json()
        for test_result in result["test_results"]:
            print(f"Format {test_result['format']}: {test_result.get('response', test_result.get('error'))}")
    except Exception as e:
        print(f"Direct test failed: {e}")

if __name__ == "__main__":
    test_api()