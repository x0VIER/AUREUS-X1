import asyncio
import aiohttp
import sys

async def check_engine():
    print(f"--- AUREUS X1: Autonomous Diagnostic ---")
    url = "http://127.0.0.1:8005/audio/"
    print(f"Pinging Engine at: {url}")
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=5) as response:
                if response.status in [200, 404, 403]: # Any response means port is open
                    print(f"[OK] Port 8005 is RESPONDING (Status: {response.status})")
                    return True
                else:
                    print(f"[FAIL] Unexpected response: {response.status}")
        except Exception as e:
            print(f"[FAIL] Connection Refused: {e}")
    return False

if __name__ == "__main__":
    success = asyncio.run(check_engine())
    if not success:
        sys.exit(1)
    sys.exit(0)
