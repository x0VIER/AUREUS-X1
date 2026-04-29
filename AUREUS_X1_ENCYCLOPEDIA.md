# AUREUS X1: The Mirror Engine Encyclopedia

## 1. Overview
AUREUS X1 is a high-performance "Mirror Proxy" system designed for real-time video translation. Unlike traditional downloaders, AUREUS X1 operates as a browser-side companion that injects translated audio (dubs) directly into the web player, creating a seamless multi-lingual viewing experience.

## 2. Architecture
The system follows a Decoupled Proxy Architecture:
- **Frontend:** Chrome Extension (Manifest V3) that monitors the DOM for video elements and handles UI injection.
- **Backend:** Python FastAPI server that orchestrates the heavy lifting (Extraction, AI Translation, Neural Synthesis).

## 3. Core Engine Components (src/)
### 3.1 Fetch Engine (`fetch.py`)
Responsible for retrieving raw media streams. It primarily wraps `yt-dlp` to extract high-quality audio tracks without downloading the entire video file.

### 3.2 Translation Engine (`translate.py`)
The "Cultural Expert" layer. 
- **Provider:** OpenRouter (Gemini 1.5/2.0 Flash).
- **Capability:** Multimodal audio analysis. It doesn't just transcribe; it understands Mexican Spanish slang, detects speaker genders, and translates for dubbing.
- **Output:** Structured JSON containing timestamps and translated text.

### 3.3 Synthesis Engine (`synthesize.py`)
Powered by **Edge-TTS**. 
- **Technology:** Microsoft Edge's neural voices.
- **Advantage:** High-quality, low-latency, and zero-cost (no API keys required).

### 3.4 Merge Engine (`merge.py`)
Provides offline merging capabilities.
- **Function:** Uses FFmpeg to mix synthesized audio with the original video, applying "audio ducking" (original audio at 20% volume).
- **Use Case:** Creating hard-coded dubbed versions of videos for offline use.

## 4. Backend API (`server.py`)
- `POST /preload`: Background task to start audio extraction as soon as a user lands on a video page.
- `POST /translate`: Final orchestration. Waits for preload, sends audio to AI, and triggers TTS synthesis.
- `/audio`: Static mount for serving generated MP3 dubs.

## 5. Frontend Integration (`extension/`)
### 5.1 Injection Logic
The extension uses a `MutationObserver` (and `setInterval` fallback) to watch for YouTube's dynamic page transitions. It targets the `.html5-video-player` container for button placement.

### 5.2 Sync Protocol
The extension maintains a high-frequency sync loop:
- Adjusts dub playback to match `video.currentTime`.
- Synchronizes Play/Pause states.
- Dampens volume of the original video to 15% during dubbing.

## 6. Critical Paths & Dependencies
- **FFmpeg:** Required for audio transcoding. Ensure `ffmpeg` is in your system PATH or set the `FFMPEG_PATH` environment variable.
- **OpenRouter API Key:** Must be present in `.env`.
- **yt-dlp:** Must be up-to-date to handle YouTube's rotating signatures.

## 7. Troubleshooting
- **Button not appearing:** Check if YouTube changed its DOM classes. Verify extension is loaded in `chrome://extensions`.
- **No Audio:** Ensure the backend server is running (`python server.py`) and FFmpeg path is correct.
- **CORS Errors:** The backend is configured with `allow_origins=["*"]`, but check browser security settings if using a strict environment.
