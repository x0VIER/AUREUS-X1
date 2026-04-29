from fastapi import FastAPI, HTTPException, BackgroundTasks, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import uuid
import yt_dlp
import asyncio
import json
from typing import Dict, List
from src.translate import translate_audio, extract_json, check_openrouter_health, whisper_model
from src.synthesize import synthesize_audio, check_tts_health

app = FastAPI()

# AUREUS V3: Persistent Model State
app.state.whisper = whisper_model

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DOWNLOADS_DIR = "downloads"
if not os.path.exists(DOWNLOADS_DIR):
    os.makedirs(DOWNLOADS_DIR)

app.mount("/audio", StaticFiles(directory=DOWNLOADS_DIR), name="audio")

# In-memory cache for preloaded audio
preload_cache: Dict[str, dict] = {}

class TranslationRequest(BaseModel):
    url: str

@app.on_event("startup")
async def startup_event():
    print("--- AUREUS X1 Pre-flight Health Check ---")
    if check_openrouter_health(): print("[OK] OpenRouter API Connection")
    else: print("[FAIL] OpenRouter API Connection")
    if await check_tts_health(): print("[OK] Edge TTS Service Reachable")
    else: print("[FAIL] Edge TTS Service")
    # Use 'ffmpeg' from PATH or override via environment variable
    ffmpeg_path = os.getenv("FFMPEG_PATH", "ffmpeg")
    if os.path.exists(ffmpeg_path): print("[OK] FFmpeg found")
    else: print("[FAIL] FFmpeg NOT found")
    print("------------------------------------------")

async def run_download(video_url: str, session_id: str, ws: WebSocket = None):
    """Background task to extract audio using mp3."""
    if ws: await ws.send_json({"type": "status", "message": "📥 Intercepting Audio Stream..."})
    
    preload_cache[video_url] = {"status": "pending", "path": None}
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '128',
        }],
        'outtmpl': os.path.join(DOWNLOADS_DIR, f"{session_id}.%(ext)s"),
        'ffmpeg_location': os.getenv("FFMPEG_PATH", "ffmpeg"),
        'quiet': True,
        'no_warnings': True
    }

    try:
        def download():
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                filename = ydl.prepare_filename(info)
                base, _ = os.path.splitext(filename)
                return f"{base}.mp3"
        
        loop = asyncio.get_event_loop()
        file_path = await loop.run_in_executor(None, download)
        
        preload_cache[video_url] = {"status": "completed", "path": file_path}
        if ws: await ws.send_json({"type": "status", "message": "✅ Audio Intercepted."})
        return file_path
    except Exception as e:
        print(f"[PRELOAD] Error: {e}")
        preload_cache[video_url] = {"status": "error", "error": str(e)}
        if ws: await ws.send_json({"type": "error", "message": f"Download failed: {str(e)}"})
        return None

async def process_translation(video_url: str, ws: WebSocket = None):
    """Core logic for translation and synthesis, shared by HTTP and WS."""
    session_id = str(uuid.uuid4())
    
    # 1. Download/Fetch from Cache
    audio_path = None
    if video_url in preload_cache:
        cache = preload_cache[video_url]
        if cache["status"] == "pending":
            if ws: await ws.send_json({"type": "status", "message": "⏳ Waiting for Preload..."})
            while cache["status"] == "pending":
                await asyncio.sleep(0.5)
                cache = preload_cache[video_url]
        
        if cache["status"] == "completed":
            audio_path = cache["path"]
    
    if not audio_path:
        audio_path = await run_download(video_url, session_id, ws)
        if not audio_path: return None

    # 2. Translate
    if ws: await ws.send_json({"type": "status", "message": "🧠 Consulting Local Whisper + Gemini..."})
    
    loop = asyncio.get_event_loop()
    raw_response = await loop.run_in_executor(None, translate_audio, audio_path)
    if ws: await ws.send_json({"type": "status", "message": "🌎 [3/4] Translating (Gemini)..."})
    
    if not raw_response:
        if ws: await ws.send_json({"type": "error", "message": "Translation service failed."})
        return None

    translation_data = extract_json(raw_response)
    if not translation_data:
        if ws: await ws.send_json({"type": "error", "message": "Failed to parse translation."})
        return None

    srt_content = translation_data.get("srt")
    clean_text = translation_data.get("clean_text")

    # 3. Synthesize
    if ws: await ws.send_json({"type": "status", "message": "🗣️ Synthesizing Professional Dub..."})
    session_id_actual = os.path.basename(audio_path).split('.')[0]
    dub_filename = f"{session_id_actual}_dub.mp3"
    dub_path = os.path.join(DOWNLOADS_DIR, dub_filename)
    
    text_to_speak = str(clean_text) if clean_text else "Translation complete."
    if len(text_to_speak) < 5:
        text_to_speak = "I have translated the video for you."

    print(f"[{session_id_actual}] Synthesizing text (len {len(text_to_speak)}): {text_to_speak[:100]}...")
    if not await synthesize_audio(text_to_speak, dub_path):
        if ws: await ws.send_json({"type": "error", "message": "Speech synthesis failed."})
        return None

    result = {
        "audio_url": f"http://127.0.0.1:8005/audio/{dub_filename}",
        "srt": srt_content,
        "status": "success"
    }
    
    if ws: await ws.send_json({"type": "result", **result})
    return result

@app.post("/preload")
async def preload_video(request: TranslationRequest, background_tasks: BackgroundTasks):
    url = request.url
    if url in preload_cache and preload_cache[url]["status"] != "error":
        return {"status": "already_cached"}
    
    session_id = str(uuid.uuid4())
    background_tasks.add_task(run_download, url, session_id)
    return {"status": "started", "session_id": session_id}

@app.post("/translate")
async def translate_video(request: TranslationRequest):
    result = await process_translation(request.url)
    if not result:
        raise HTTPException(status_code=500, detail="Processing failed.")
    return result

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            if message.get("type") == "start":
                url = message.get("url")
                # AUREUS V3: Run as background task so the loop can answer pings!
                asyncio.create_task(process_translation(url, websocket))
            elif message.get("type") == "ping":
                await websocket.send_json({"type": "pong"})
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"WS Error: {e}")
        try:
            await websocket.send_json({"type": "error", "message": str(e)})
        except:
            pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8005)

