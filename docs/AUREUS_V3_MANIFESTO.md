# AUREUS X1 V3: The Premium Interceptor Spec

## 1. The Design Vision (Premium UI)
AUREUS V3 moves away from "floating buttons" to a **Native Smart Overlay**.
- **The Widget:** A glassmorphism bar with a blurred background (`backdrop-filter: blur(10px)`) that slides out from the right side of the YouTube player.
- **Micro-Animations:** Use CSS transitions for status updates. When a stage is active (e.g., [2/4] Transcribing), the icon should "pulse."
- **Typography:** Use **Inter** or **Roboto** (Google Fonts) for a clean, modern look. Avoid system fonts.

## 2. User Experience (The "Magic" Flow)
- **Automatic Sync:** When the user clicks "Intercept," the video pauses automatically. When the dub is ready, the video resumes at 1.0x speed, original volume ducks to 10%, and the Dub plays.
- **The Control Pod:**
  - **Volume Slider:** Dedicated slider for the English dub.
  - **Original Ducking Toggle:** Toggle between "Silent Original" and "Ducked Original."
  - **Status Stepper:** Visual icons (🎙️ -> 🧠 -> 🗣️ -> ✨) showing live progress.

## 3. Engineering Hardening (The "Solid Fix")
- **Persistent Ear:** The `faster-whisper` model must be a singleton in `app.state`. This removes the 5s startup lag.
- **Parallel Synthesis:** Synthesize English segments in parallel using `asyncio.gather`.
- **WebSocket Robustness:** Implementation of a heartbeat every 3 seconds to prevent "Socket Closed" red errors in Chrome.
- **Port Lock:** Force all communication to Port 8005.

## 4. Bottleneck Audit (Current Status)
- **Bottleneck 1:** Model Loading (5s). **Solution:** Move to app-startup singleton.
- **Bottleneck 2:** Audio Ripping (4s). **Solution:** Use `--post-processor-args` to speed up FFmpeg.
- **Bottleneck 3:** Extension Port Mismatch. **Solution:** Global Port Sync to 8005.
