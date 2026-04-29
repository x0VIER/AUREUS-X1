import asyncio
import os
import signal
import sys
import subprocess
import time

def monitor():
    print("--- AUREUS X1: Autonomous Quality Monitor ---")
    log_file = "monitor.log"
    
    # Clean old log
    if os.path.exists(log_file):
        os.remove(log_file)

    print("Starting server process...")
    # Start server and redirect everything to log
    process = subprocess.Popen(
        ["python", "-u", "server.py"],
        stdout=open(log_file, "a"),
        stderr=subprocess.STDOUT,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
    )

    try:
        print(f"Server started (PID: {process.pid}). Monitoring logs...")
        while True:
            if os.path.exists(log_file):
                with open(log_file, "r") as f:
                    f.seek(0, 2) # Go to end
                    last_pos = f.tell()
                    
                    while True:
                        line = f.readline()
                        if line:
                            if "Error" in line or "fail" in line.lower():
                                print(f"⚠️ [LOG ALERT] {line.strip()}")
                            elif "Synthesizing Professional Dub" in line:
                                print(f"✅ [SUCCESS] Dub phase reached!")
                        else:
                            time.sleep(1)
                            # Check if process is still alive
                            if process.poll() is not None:
                                print("❌ Server process died unexpectedly.")
                                return
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping monitor...")
        os.kill(process.pid, signal.SIGTERM)

if __name__ == "__main__":
    monitor()
