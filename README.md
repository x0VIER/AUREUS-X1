# AUREUS X1

![AUREUS X1 Banner](docs/images/banner.png)

<p align="center">
    <img src="https://img.shields.io/github/languages/top/x0VIER/AUREUS-X1?style=flat-square" alt="Top Language">
    <img src="https://img.shields.io/github/repo-size/x0VIER/AUREUS-X1?style=flat-square" alt="Repo Size">
    <img src="https://img.shields.io/github/commit-activity/m/x0VIER/AUREUS-X1?style=flat-square" alt="Commit Activity">
    <img src="https://img.shields.io/github/license/x0VIER/AUREUS-X1?style=flat-square" alt="License">
</p>

AUREUS X1 is a high-performance framework for real-time interception and English translation of Spanish video streams. It implements a local-hybrid architecture to achieve zero-latency dubbing through VRAM model caching and high-speed API orchestration.

---

## Table of Contents
- [Overview](#overview)
- [Technical Specifications](#technical-specifications)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
- [Roadmap](#roadmap)

---

## Overview
AUREUS X1 addresses the latency bottleneck in AI video translation. By moving the transcription layer locally (Faster-Whisper) and maintaining persistent model singletons, it removes the cold-start lag found in cloud-only implementations.

---

## Technical Specifications

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Transcription** | `faster-whisper` | Local VRAM-cached STT |
| **Translation** | `Gemini 2.0 Flash` | Context-aware LLM translation |
| **Synthesis** | `edge-tts` | Neural voice generation |
| **Frontend** | `Chrome Extension` | Manifest V3 DOM Interceptor |
| **Backend** | `FastAPI` | WebSocket Orchestrator |

---

## Architecture
The system operates as a decoupled bridge between the browser DOM and local inference engines.

*   **Persistent Singletons:** Whisper models remain in VRAM to ensure instantaneous processing.
*   **WebSocket Bridge:** Zero-latency communication on Port 8005.
*   **Dynamic Volume Control:** Automated ducking of original audio during translation overlay.

---

## Getting Started

### Prerequisites
*   Python 3.10+
*   FFmpeg
*   Google Chrome

### Quick Setup
```powershell
git clone https://github.com/x0VIER/AUREUS-X1.git
cd AUREUS-X1
python main.py --setup
```

---

## Roadmap
- [x] Initial local-hybrid architecture implementation
- [x] Chrome Extension (Manifest V3) interception
- [x] Multi-model singleton caching
- [ ] Real-time lip-syncing integration
- [ ] Multi-language support (Extended beyond Spanish)
- [ ] Native Electron wrapper for standalone use

---

Developed by x0VIER. Optimized for professional engineering standards.
