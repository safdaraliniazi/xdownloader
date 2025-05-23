from yt_dlp import YoutubeDL
from fastapi.responses import JSONResponse
import logging
import os

def stream_twitter_video(url):
    try:
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'age_limit' : None,
            
        }
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        return JSONResponse(info)

    except Exception as e:
        logging.error(f"Error: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)
