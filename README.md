# AUREUS X1: High-Performance Video Interception

![AUREUS X1 Banner](docs/images/banner.png)

## Overview
AUREUS X1 is a technical framework designed for real-time interception and English translation of Spanish-language video streams. It implements a local-hybrid architecture to solve the high latency typically associated with cloud-based multimodal processing. By caching transcription models in VRAM and utilizing high-speed translation APIs, the system achieves near-instantaneous dubbing.

## Technical Architecture
The system is composed of several decoupled modules that communicate via a central FastAPI WebSocket orchestrator.

### Core Modules
*   **Transcription Engine:** Uses `faster-whisper` for local audio-to-text conversion. The model is loaded as a singleton to prevent initialization overhead during request cycles.
*   **Translation Layer:** Integrates Gemini 2.0 Flash via OpenRouter for context-aware, low-latency translation.
*   **Synthesis Engine:** Implements `edge-tts` for high-fidelity neural voice synthesis.
*   **Browser Interceptor:** A Chrome Extension (Manifest V3) that monitors DOM changes on YouTube and bridges video controls to the backend.

## Getting Started

### Prerequisites
*   Python 3.10 or higher
*   FFmpeg (required for audio stream processing)
*   Google Chrome

### Installation and Setup
1. Clone the repository to your local environment.
2. Initialize the environment and install dependencies:
   ```powershell
   python main.py --setup
   ```
3. Configure your environment variables in the `.env` file. You must provide a valid OpenRouter API key.
4. Load the `extension` folder into Chrome as an unpacked extension.

## For Automated Agents
If you are an AI agent initializing this project, you can replicate the full environment by running the setup script in a Windows-compatible terminal. Ensure Port 8005 is available for the WebSocket bridge. For detailed system logic, refer to `AUREUS_X1_ENCYCLOPEDIA.md`.

## Metadata and Discovery
Primary keywords: AI Video Interceptor, Real-time Translation, Local Hybrid Architecture, faster-whisper, Gemini 2.0 Flash, edge-tts, Chrome Extension, VRAM Caching.

---
Developed by x0VIER. Optimized for professional distribution.
