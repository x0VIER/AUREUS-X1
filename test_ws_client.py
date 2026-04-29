import asyncio
import websockets
import json

async def test_interceptor():
    uri = "ws://127.0.0.1:8005/ws"
    url_to_test = "https://www.youtube.com/watch?v=x8miXaZ2bco"
    
    print(f"Connecting to {uri}...")
    try:
        async with websockets.connect(uri, ping_timeout=None) as websocket:
            print("Connected. Sending start message...")
            await websocket.send(json.dumps({
                "type": "start",
                "url": url_to_test
            }))
            
            while True:
                response = await websocket.recv()
                data = json.loads(response)
                print(f"[WS RECEIVE] {data}")
                
                if data.get("type") == "result":
                    print("Test SUCCESS: Result received.")
                    break
                if data.get("type") == "error":
                    print(f"Test FAILED: {data.get('message')}")
                    break
    except Exception as e:
        print(f"Connection Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_interceptor())
