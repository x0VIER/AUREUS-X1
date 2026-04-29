import requests
import time
import os

def run_autonomous_test():
    """
    Simulates a translation request to the local server.
    Verifies:
    1. Server reachability.
    2. Successful audio extraction.
    3. Multimodal or Decoupled translation.
    4. Edge-TTS synthesis.
    """
    print("--- STARTING AUTONOMOUS TEST ---")
    
    # Target video (A Mexican Spanish clip)
    test_url = "https://www.youtube.com/watch?v=YN-uwAi4skY"
    server_url = "http://127.0.0.1:8000/translate"
    
    start_time = time.time()
    
    try:
        print(f"Testing URL: {test_url}")
        response = requests.post(server_url, json={"url": test_url}, timeout=300)
        
        if response.status_code == 200:
            data = response.json()
            audio_url = data.get("audio_url")
            srt = data.get("srt")
            
            print("\n[VERIFICATION SUCCESS]")
            print(f"Time Taken: {round(time.time() - start_time, 2)}s")
            print(f"Dub Audio URL: {audio_url}")
            print(f"SRT Preview: {srt[:100]}...")
            
            # Check if file exists on disk
            filename = audio_url.split("/")[-1]
            local_path = os.path.join("downloads", filename)
            if os.path.exists(local_path):
                print(f"Local file verified at: {local_path}")
                return True
            else:
                print("Error: Dub file not found on disk despite success response.")
        else:
            print(f"\n[VERIFICATION FAILED]")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"\n[ERROR] Test crashed: {e}")
        
    return False

if __name__ == "__main__":
    success = run_autonomous_test()
    if not success:
        exit(1)
