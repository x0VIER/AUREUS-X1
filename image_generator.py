import os
import requests
import sys

def generate_image(prompt, output_path):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set.")
        sys.exit(1)

    print(f"Generating image for prompt: {prompt}")
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    data = {
        "model": "dall-e-3",
        "prompt": prompt,
        "n": 1,
        "size": "1024x1024" # DALL-E 3 default, we can resize if needed
    }
    
    response = requests.post("https://api.openai.com/v1/images/generations", headers=headers, json=data)
    
    if response.status_code == 200:
        image_url = response.json()["data"][0]["url"]
        print(f"Image generated! Downloading from {image_url}")
        
        img_data = requests.get(image_url).content
        with open(output_path, 'wb') as handler:
            handler.write(img_data)
        print(f"Success: Image saved to {output_path}")
    else:
        print(f"Error: {response.status_code} - {response.text}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python image_generator.py '<prompt>' <output_path>")
        sys.exit(1)
    
    generate_image(sys.argv[1], sys.argv[2])
