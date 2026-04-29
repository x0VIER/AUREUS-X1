import os
import sys
import json
from src.fetch import download_media
from src.translate import translate_audio
from src.synthesize import synthesize_audio
from src.merge import merge_audio_video

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <Video_URL>")
        sys.exit(1)

    url = sys.argv[1]
    
    print(f"--- Step 1: Fetch Media ---")
    audio_path, video_path = download_media(url)
    
    if not audio_path or not video_path:
        print("Failed to download media. Please check the URL and ensure FFmpeg is accessible.")
        sys.exit(1)
    
    print(f"--- Step 2: Translate Audio ---")
    raw_response = translate_audio(audio_path)
    
    if not raw_response:
        print("Failed to generate translation.")
        sys.exit(1)
    
    try:
        # Gemini might wrap JSON in code blocks
        clean_json = raw_response.strip()
        if clean_json.startswith("```json"):
            clean_json = clean_json[7:-3].strip()
        elif clean_json.startswith("```"):
            clean_json = clean_json[3:-3].strip()
            
        translation_data = json.loads(clean_json)
        srt_content = translation_data.get("srt")
        clean_text = translation_data.get("clean_text")
    except Exception as e:
        print(f"Error parsing Gemini response: {e}")
        print(f"Raw response: {raw_response}")
        sys.exit(1)
    
    # Save SRT
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    srt_path = os.path.join("downloads", f"{base_name}.srt")
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write(srt_content)
    print(f"SRT saved to: {srt_path}")
    
    print(f"--- Step 3: Synthesize Dub Audio ---")
    dub_audio_path = os.path.join("downloads", f"{base_name}_dub.mp3")
    if not synthesize_audio(clean_text, dub_audio_path):
        print("Failed to synthesize audio.")
        sys.exit(1)
    
    print(f"--- Step 4: Merge Dub with Video ---")
    final_video_path = os.path.join("downloads", f"{base_name}_translated.mp4")
    if not merge_audio_video(video_path, dub_audio_path, final_video_path):
        print("Failed to merge audio and video.")
        sys.exit(1)
    
    print(f"\nSUCCESS! Translated video created: {final_video_path}")

if __name__ == "__main__":
    main()
