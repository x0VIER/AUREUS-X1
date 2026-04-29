import requests
import os
import json
import time
from dotenv import load_dotenv
from faster_whisper import WhisperModel

load_dotenv()

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Global model instance for efficiency (loads once)
print("Loading Local Whisper Model (faster-whisper base)...")
whisper_model = WhisperModel("base", device="cpu", compute_type="int8")

def transcribe_local(audio_path):
    """Uses faster-whisper to transcribe Mexican Spanish locally."""
    print(f"--- Local Transcription Phase: {audio_path} ---")
    segments, info = whisper_model.transcribe(audio_path, beam_size=5, language="es")
    
    transcription_data = []
    for segment in segments:
        transcription_data.append({
            "start": segment.start,
            "end": segment.end,
            "text": segment.text
        })
    
    print(f"Detected language: {info.language} with probability {info.language_probability}")
    return transcription_data

def translate_audio(audio_file_path):
    """
    Hybrid Engine: Local Transcription -> Cloud Translation.
    """
    # 1. Local Transcription
    transcription = transcribe_local(audio_file_path)
    if not transcription:
        return None

    # 2. Cloud Translation (Text-only)
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key: return None

    return call_translation_cloud(transcription, "google/gemini-2.0-flash-lite-001", api_key)

def call_translation_cloud(transcription_data, model, api_key):
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    
    prompt = f"""
    You are a Bilingual Cultural Expert. I have a transcription of Mexican Spanish audio with timestamps.
    
    TRANSCRIPTION:
    {json.dumps(transcription_data, indent=2)}
    
    TASKS:
    1. Translate the Mexican Spanish dialogue into natural, professional English.
    2. Maintain the exact timestamps provided.
    3. Output a JSON OBJECT with:
       - "segments": List of {{ "speaker": "Speaker 1", "start": start, "end": end, "text": "English text", "original": "Spanish text" }}.
       - "srt": Valid SRT formatted string of the English translation.
       - "clean_text": Single string of full English translation for TTS.

    Return ONLY the raw JSON object.
    """
    
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "response_format": { "type": "json_object" }
    }

    try:
        res = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=300)
        if res.status_code == 200:
            return res.json()['choices'][0]['message']['content']
        print(f"Cloud Translation failed: {res.text}")
    except Exception as e:
        print(f"Error calling Cloud AI: {e}")
    return None

def check_openrouter_health():
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key: return False
    headers = {"Authorization": f"Bearer {api_key}"}
    try:
        res = requests.get("https://openrouter.ai/api/v1/models", headers=headers, timeout=10)
        return res.status_code == 200
    except:
        return False

def extract_json(text):
    try:
        text = text.replace("```json", "").replace("```", "").strip()
        start = text.find('{')
        end = text.rfind('}')
        if start != -1 and end != -1:
            return json.loads(text[start:end+1])
    except Exception as e:
        print(f"Extraction Error: {e}")
    return None
