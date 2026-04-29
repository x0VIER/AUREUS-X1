import edge_tts
import asyncio
import os

async def synthesize_audio(text, output_path, voice="en-US-GuyNeural"):
    """
    Synthesizes English text into speech using Microsoft Edge TTS.
    Includes validation to ensure the voice is available.
    """
    try:
        # Validate voice list (quick check)
        voices = await edge_tts.VoicesManager.create()
        voice_data = voices.find(ShortName=voice)
        
        if not voice_data:
            print(f"Warning: Voice {voice} not found. Falling back to en-US-AriaNeural.")
            voice = "en-US-AriaNeural"

        print(f"Synthesizing speech to: {output_path} using voice: {voice}...")
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_path)
        return True
    except Exception as e:
        print(f"Error synthesizing audio with edge-tts: {e}")
        return False

async def check_tts_health():
    """Quick check to see if Edge TTS service is reachable."""
    try:
        voices = await edge_tts.VoicesManager.create()
        return len(voices.voices) > 0
    except:
        return False
