import os
import sys
import yt_dlp


def get_ffmpeg_path():
    if getattr(sys, 'frozen', False):
        base = sys._MEIPASS
        name = 'ffmpeg.exe' if sys.platform == 'win32' else 'ffmpeg'
        path = os.path.join(base, 'bin', name)
        if os.path.isfile(path):
            return path
    return None


def download_mp3(url, output_dir, on_progress, on_done, on_error):
    def hook(d):
        if d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            downloaded = d.get('downloaded_bytes', 0)
            pct = (downloaded / total) if total > 0 else 0
            on_progress(pct, 'Downloading...')
        elif d['status'] == 'finished':
            on_progress(1.0, 'Converting to MP3...')

    opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'progress_hooks': [hook],
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
    }

    ffmpeg = get_ffmpeg_path()
    if ffmpeg:
        opts['ffmpeg_location'] = ffmpeg

    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])
        on_done()
    except yt_dlp.utils.DownloadError as e:
        on_error(str(e).replace('ERROR: ', '', 1))
    except Exception as e:
        on_error(str(e))
