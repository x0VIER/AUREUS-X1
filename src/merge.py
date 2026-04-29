import subprocess
import os

FFMPEG_PATH = os.getenv("FFMPEG_PATH", "ffmpeg")

def merge_audio_video(video_path, dub_audio_path, output_path):
    """
    Merges synthesized audio with original video, ducking original audio.
    """
    if not os.path.exists(video_path):
        print(f"Error: Video file not found at {video_path}")
        return False
    
    if not os.path.exists(dub_audio_path):
        print(f"Error: Dub audio file not found at {dub_audio_path}")
        return False

    # Filter complex explanation:
    # [0:a] is original audio, volume reduced to 0.2 (80% ducking)
    # [1:a] is new dub audio, volume kept at 1.0
    # [a0][a1]amix mixes them. duration=first keeps it the length of the original video.
    filter_complex = "[0:a]volume=0.2[a0];[1:a]volume=1.0[a1];[a0][a1]amix=inputs=2:duration=first[aout]"
    
    command = [
        FFMPEG_PATH,
        '-y', # Overwrite output
        '-i', video_path,
        '-i', dub_audio_path,
        '-filter_complex', filter_complex,
        '-map', '0:v', # Use video from first input
        '-map', '[aout]', # Use mixed audio
        '-c:v', 'copy', # Copy video codec (fast)
        '-c:a', 'aac', # Encode audio to AAC
        '-shortest', # Finish when the shortest stream ends
        output_path
    ]

    try:
        print(f"Merging audio and video into: {output_path}...")
        subprocess.run(command, check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error during ffmpeg execution: {e.stderr}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 4:
        print("Usage: python merge.py <video_path> <dub_audio_path> <output_path>")
    else:
        v_path = sys.argv[1]
        a_path = sys.argv[2]
        o_path = sys.argv[3]
        if merge_audio_video(v_path, a_path, o_path):
            print("Merging complete.")
