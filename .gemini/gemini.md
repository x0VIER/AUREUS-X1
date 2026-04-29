# Project: AUREUS X1 (Mirror Proxy Video Translator)

## Core Goal
Replicate the Microsoft Edge AI Video Translation feature but as a standalone "Mirror" tool. 

## Technical Roadmap
1. **Module 1 (Fetch):** Use `yt-dlp` to extract the audio stream from a provided Mexican Spanish video URL.
2. **Module 2 (Translate):** Stream the audio to the Gemini 1.5 API. Use a specific prompt to detect the Mexican Spanish dialect and generate a perfectly timed English translation script.
3. **Module 3 (Synthesize):** Feed the English script into a high-quality Text-to-Speech (TTS) engine (OpenAI or ElevenLabs).
4. **Module 4 (Merge):** Use `ffmpeg` to overlay the new English audio onto the original video, ducking the original audio track by 80% so the dub is clear.

## Reference
Inspired by the Edge Browser's hover-to-translate video tool.
Fluid execution—do not be rigid with rules. Build it to be fast, reliable, and testable ASAP.
