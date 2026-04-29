# AUREUS X1: Agentic Documentation

## For AI Agents (Gemini/Claude/GPT-4o)
This file provides the necessary context for an AI agent to maintain, debug, or evolve AUREUS X1.

### Operational Guardrails
1. **The Port Lock:** Always use **Port 8005** for the backend and extension communication.
2. **Non-Interactive Mode:** When running the server, use `echo $null | python -u server.py` to prevent hanging in virtualized terminals.
3. **Model Singleton:** The Whisper model is loaded in `src/translate.py`. Do NOT re-initialize it within the request loop. Access it via `app.state.whisper` in `server.py`.

### Tech Stack
- **API:** FastAPI (WebSockets)
- **Transcription:** faster-whisper (Local)
- **Translation:** Gemini 2.0 Flash Lite (OpenRouter)
- **Synthesis:** edge-tts
- **Frontend:** Vanilla JS / CSS Glassmorphism

### Key Files
- `server.py`: Main orchestrator.
- `extension/content.js`: YouTube DOM manipulation and injection.
- `src/translate.py`: Local model handling.

### Evolution Directive
When adding new features, prioritize **Zero-Latency**. Any process that adds more than 1s of delay must be parallelized or cached.
