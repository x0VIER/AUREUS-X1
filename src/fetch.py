import yt_dlp
import os

def download_media(url, output_dir="downloads"):
    """
    Downloads both the audio stream and the video from a URL using yt-dlp.
    Returns (audio_path, video_path).
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Base options for both
    base_opts = {
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'ffmpeg_location': os.getenv("FFMPEG_PATH", "ffmpeg"),
    }

    # Audio options
    audio_opts = base_opts.copy()
    audio_opts.update({
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    })

    # Video options (best video + best audio merged into mp4)
    video_opts = base_opts.copy()
    video_opts.update({
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
    })

    try:
        audio_path = None
        video_path = None

        # Download Audio
        with yt_dlp.YoutubeDL(audio_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            base, _ = os.path.splitext(filename)
            audio_path = f"{base}.mp3"

        # Download Video
        with yt_dlp.YoutubeDL(video_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_path = ydl.prepare_filename(info)

        return audio_path, video_path
    except Exception as e:
        print(f"Error downloading media: {e}")
        return None, None

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python fetch.py <URL>")
    else:
        url = sys.argv[1]
        a_path, v_path = download_media(url)
        if a_path and v_path:
            print(f"Audio: {a_path}")
            print(f"Video: {v_path}")
