# AUREUS X1: The Professional AI Video Interceptor

![AUREUS X1 Banner](docs/images/banner.png)

## Project Overview
AUREUS X1 is a high-performance, real-time video interceptor and translator designed to provide a "Zero-Touch" dubbing experience. It pivots from traditional cloud-only multimodal processing to a **Local Hybrid Architecture**, achieving significant latency reductions while maintaining semantic precision.

## The Evolution: From V1 to V3
This repository showcases the engineering journey of solving the "Latency Wall" in AI dubbing:
1. **V1 (Cloud-Only):** Initial prototype using remote multimodal models. High fidelity but high latency (45s+).
2. **V2 (API-Hybrid):** First introduction of local transcription. Reduced wait times but suffered from model-loading bottlenecks.
3. **V3 (The Interceptor):** Current version. Features **Persistent Model Caching (Singleton)** and a **Glassmorphism Floating UI** that intercepts YouTube traffic on the fly.

## Component Highlights
### 🎙️ The Local Ear (faster-whisper)
Optimized local transcription engine using `faster-whisper`. By caching the model in VRAM, AUREUS removes the 5-8 second startup lag found in standard implementations.

### 🧠 The Global Brain (Gemini 2.0 Flash)
Leverages Gemini 2.0 Flash Lite via OpenRouter for high-speed, slang-aware text-to-text translation. This ensures that cultural nuances and technical jargon are preserved during the dubbing process.

### 🗣️ The Neural Voice (edge-tts)
High-fidelity neural synthesis providing a natural English voice overlay with automatic volume ducking of the original Spanish audio.

## Architecture
- **Persistent Backend:** FastAPI WebSocket orchestrator running on Port 8005.
- **Frontend Interceptor:** Chrome Extension (Manifest V3) with a native YouTube Floating Control Bar.
- **Auto-Sync Logic:** Automated `video.pause()` and `video.play()` orchestration with dynamic volume control.

## Installation & Setup
### Prerequisites
- Python 3.10+
- FFmpeg
- Chrome Browser

### Getting Started
1. **Clone the repository:**
   ```bash
   git clone https://github.com/x0VIER/AUREUS-X1.git
   cd AUREUS-X1
   ```
2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure API Keys:**
   Create a `.env` file (see `.env.example`) and add your OpenRouter API Key.
4. **Load the Extension:**
   Go to `chrome://extensions`, enable Developer Mode, and click "Load Unpacked". Select the `extension/` folder.

## Mission Alignment
This project demonstrates the technical foundation required for **Agentic Interception**—building tools that don't just react to data, but actively intercept and transform it in real-time to augment human understanding.

---
*Created by [x0VIER](https://github.com/x0VIER)*
