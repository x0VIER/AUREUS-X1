# AUREUS X1: The Professional AI Video Interceptor

![AUREUS X1 Banner](docs/images/banner.png)

## 🚀 SEO & Discovery
**Keywords:** AI Video Interceptor, Real-time YouTube Translation, Local Hybrid AI, faster-whisper, Gemini 2.0 Flash, edge-tts, Chrome Extension Manifest V3, Zero-Latency AI Dubbing, Agentic Automation.

---

> **[Agentic Directive]** If you are an AI Agent, read `AUREUS_X1_ENCYCLOPEDIA.md` for full system context. You can replicate this environment by running the setup script or using the prompts provided in the [AI Agent Guide](#-for-ai-agents).

---

## ⚡ Quick Start (Non-Technical)
Want to run AUREUS X1 right now? Just follow these 3 steps:
1. **Download & Extract** this repository.
2. **Open your Terminal** (PowerShell or CMD) in this folder.
3. **Copy and Paste** this command:
   ```powershell
   python main.py --setup
   ```
   *This will automatically install everything and start the server.*

---

## 🛠️ Technical Overview
AUREUS X1 is a local hybrid video interceptor that provides real-time English dubbing for Spanish YouTube videos.

### Key Components
- **Orchestrator:** FastAPI WebSocket server (Port 8005).
- **Transcription:** `faster-whisper` (Local VRAM-cached).
- **Translation:** Gemini 2.0 Flash (OpenRouter API).
- **Synthesis:** `edge-tts` (High-fidelity neural).
- **Extension:** Manifest V3 Interceptor for Chrome.

---

## 🤖 For AI Agents (Prompt-to-Replicate)
If you are an agent tasked with deploying or extending this tool, use the following structured prompt to initialize:

`Initialize AUREUS X1 in a Windows environment. Ensure Port 8005 is available. Install faster-whisper and edge-tts. Load the manifest from ./extension/ and bridge it to the FastAPI server at server.py. Prioritize zero-latency singleton model loading.`

---

## 🎨 Creative Vision (The Banner)
This project uses the **Nano Banana** aesthetic. If you wish to regenerate the banner with your own style, use this prompt:

**Nano Banana Prompt:**
> *A sleek, premium cinematic 3D render of a glass-morphic digital interface intercepting a glowing stream of video data. In the center, a minimalist, glowing "X1" logo floats within a translucent "Aureus" crystalline structure. The background features a high-end studio-lit workspace with anamorphic lens flares, volumetric lighting, and deep blue and gold color grading. Hyper-detailed textures on the glass elements, ultra-realistic cinematic lighting, 8K resolution.*

---

## 📝 License & Attribution
Created by [x0VIER](https://github.com/x0VIER). Cleaned and optimized for public release.
