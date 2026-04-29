import requests
import time
import sys
import os
import subprocess

# Standard GitHub CLI Client ID (used for device flow)
CLIENT_ID = "01782d817878343843a9" 

def get_device_code():
    res = requests.post("https://github.com/login/device/code", 
                        data={"client_id": CLIENT_ID, "scope": "repo"},
                        headers={"Accept": "application/json"})
    return res.json()

def poll_for_token(device_code, interval):
    print("\n[WAITING] Waiting for you to authorize in the browser...")
    while True:
        res = requests.post("https://github.com/login/oauth/access_token",
                            data={
                                "client_id": CLIENT_ID,
                                "device_code": device_code,
                                "grant_type": "urn:ietf:params:oauth:grant-type:device_code"
                            },
                            headers={"Accept": "application/json"})
        data = res.json()
        
        if "access_token" in data:
            return data["access_token"]
        elif data.get("error") == "authorization_pending":
            time.sleep(interval + 1)
        else:
            print(f"Error: {data.get('error_description')}")
            sys.exit(1)

def create_repo(token, repo_name):
    print(f"\n[ACTION] Creating repository '{repo_name}' on GitHub...")
    res = requests.post("https://api.github.com/user/repos",
                        json={"name": repo_name, "private": False},
                        headers={
                            "Authorization": f"Bearer {token}",
                            "Accept": "application/vnd.github+json"
                        })
    if res.status_code == 201:
        data = res.json()
        print(f"✅ Successfully created: {data['html_url']}")
        return data['clone_url']
    elif res.status_code == 422:
        print(f"ℹ️ Repository '{repo_name}' already exists or name is unavailable.")
        # Try to get the existing repo URL
        user_res = requests.get("https://api.github.com/user", headers={"Authorization": f"Bearer {token}"})
        username = user_res.json()['login']
        return f"https://github.com/{username}/{repo_name}.git"
    else:
        print(f"❌ Failed to create repo: {res.json()}")
        sys.exit(1)

def push_code(token, repo_url):
    print("\n[ACTION] Pushing code to GitHub...")
    # Inject token into URL for authentication
    auth_url = repo_url.replace("https://", f"https://oauth2:{token}@")
    
    try:
        # Update remote
        subprocess.run(["git", "remote", "set-url", "origin", auth_url], check=True)
        # Push
        result = subprocess.run(["git", "push", "-u", "origin", "master", "--force"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Code pushed successfully!")
            # Clean up token from remote URL
            subprocess.run(["git", "remote", "set-url", "origin", repo_url], check=True)
        else:
            print(f"❌ Push failed: {result.stderr}")
    except Exception as e:
        print(f"❌ Error during push: {e}")

if __name__ == "__main__":
    print("--- AUREUS X1 GitHub Publisher ---")
    
    device_data = get_device_code()
    if "error" in device_data:
        print(f"Error starting auth: {device_data}")
        sys.exit(1)

    print(f"\n1. Open your browser and go to: {device_data['verification_uri']}")
    print(f"2. Enter this code: {device_data['user_code']}")
    
    # Try to open browser automatically
    os.system(f"start {device_data['verification_uri']}")

    token = poll_for_token(device_data['device_code'], device_data['interval'])
    
    repo_url = create_repo(token, "AUREUS-X1")
    push_code(token, repo_url)
    
    print("\n🎉 All done! Your project is now live.")
