import requests
import json
import time
from typing import Dict, Any

class BMOTestClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.chat_url = f"{base_url}/chat/"
        self.status_url = f"{base_url}/chat/status"
        self.reset_url = f"{base_url}/chat/reset"
    
    def check_status(self) -> Dict[str, Any]:
        """Check if BMO is ready"""
        try:
            response = requests.get(self.status_url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"status": "error", "message": str(e), "ready": False}
    
    def chat_with_bmo(self, message: str, max_tokens: int = 150, temperature: float = 0.8) -> Dict[str, Any]:
        """Send a message to BMO"""
        payload = {
            "prompt": message,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        try:
            start_time = time.time()
            response = requests.post(self.chat_url, json=payload, timeout=30)
            end_time = time.time()
            
            response.raise_for_status()
            result = response.json()
            result["response_time"] = end_time - start_time
            return result
            
        except requests.exceptions.Timeout:
            return {
                "response": "BMO took too long to respond! Maybe try a simpler question?",
                "error": "timeout"
            }
        except Exception as e:
            return {
                "response": f"Error talking to BMO: {str(e)}",
                "error": str(e)
            }
    
    def reset_conversation(self) -> Dict[str, Any]:
        """Reset BMO's memory"""
        try:
            response = requests.post(self.reset_url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"status": "error", "message": str(e)}

def run_bmo_tests():
    """Run comprehensive BMO tests"""
    print("BMO Test Suite")
    print("=" * 50)
    
    client = BMOTestClient()
    
    # 1. Check status
    print("\nChecking BMO status...")
    status = client.check_status()
    print(f"Status: {status}")
    
    if not status.get("ready", False):
        print("BMO is not ready. Please start the server and wait for BMO to load.")
        return
    
    print("BMO is ready!")
    
    # 2. Test conversations
    test_conversations = [
        {
            "message": "Hi BMO! How are you?",
            "max_tokens": 50,
            "temperature": 0.8
        },
        {
            "message": "Want to play a game?",
            "max_tokens": 60,
            "temperature": 0.9
        },
        {
            "message": "Tell me about Finn and Jake!",
            "max_tokens": 80,
            "temperature": 0.7
        },
        {
            "message": "What's your favorite song?",
            "max_tokens": 50,
            "temperature": 0.8
        },
        {
            "message": "Can you help me with math? What's 5 + 3?",
            "max_tokens": 30,
            "temperature": 0.3
        }
    ]
    
    print(f"\nTesting {len(test_conversations)} conversations...")
    
    for i, test in enumerate(test_conversations, 1):
        print(f"\n--- Test {i} ---")
        print(f"Human: {test['message']}")
        
        result = client.chat_with_bmo(**test)
        
        if "error" in result:
            print(f"Error: {result['error']}")
        else:
            print(f"BMO: {result['response']}")
            print(f"Mood: {result.get('bmo_mood', 'unknown')}")
            print(f"Tokens: {result.get('tokens_used', 0)}")
            print(f"Time: {result.get('response_time', 0):.2f}s")
            
            # Check response quality
            response_text = result['response'].lower()
            if any(word in response_text for word in ['mathematical', 'beep', 'bmo', 'finn', 'jake', 'adventure']):
                print("Response seems BMO-like!")
            else:
                print("Response might not be in BMO character")
    
    # 3. Test conversation reset
    print(f"\nTesting conversation reset...")
    reset_result = client.reset_conversation()
    print(f"Reset result: {reset_result}")
    
    # 4. Test conversation memory
    print(f"\nTesting conversation memory...")
    
    # First message
    result1 = client.chat_with_bmo("My name is Finn!", max_tokens=30)
    print(f"Human: My name is Finn!")
    print(f"BMO: {result1.get('response', 'Error')}")
    
    time.sleep(1)  # Small delay
    
    # Follow-up message
    result2 = client.chat_with_bmo("What's my name?", max_tokens=20)
    print(f"Human: What's my name?")
    print(f"BMO: {result2.get('response', 'Error')}")
    
    if "finn" in result2.get('response', '').lower():
        print("BMO remembered the name!")
    else:
        print("BMO might not have remembered the name")
    
    print(f"\nTest suite complete!")
    print(f"Check the logs for detailed performance information.")

if __name__ == "__main__":
    run_bmo_tests()
