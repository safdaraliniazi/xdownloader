from yt_dlp import YoutubeDL
from fastapi.responses import JSONResponse
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def stream_twitter_video(url):
    try:
        # Validate URL
        if not url or not isinstance(url, str):
            return JSONResponse(
                content={"error": "Invalid URL provided"}, 
                status_code=400,
                headers={
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                    "Access-Control-Allow-Headers": "*"
                }
            )
        
        logger.info(f"Processing URL: {url}")
        
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'age_limit': None,
            'no_warnings': True,
            'extractaudio': False,
            'format': 'best[ext=mp4]/best',
        }
        
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
        # Clean up the info to only include necessary data
        if info:
            cleaned_info = {
                'title': info.get('title', 'Unknown'),
                'url': info.get('url', ''),
                'thumbnail': info.get('thumbnail', ''),
                'duration': info.get('duration', 0),
                'formats': info.get('formats', []),
                'webpage_url': info.get('webpage_url', url)
            }
            logger.info(f"Successfully extracted info for: {cleaned_info.get('title')}")
            
            return JSONResponse(
                content=cleaned_info,
                headers={
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                    "Access-Control-Allow-Headers": "*"
                }
            )
        else:
            return JSONResponse(
                content={"error": "No video information found"}, 
                status_code=404,
                headers={
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                    "Access-Control-Allow-Headers": "*"
                }
            )

    except Exception as e:
        logger.error(f"Error processing URL {url}: {str(e)}")
        return JSONResponse(
            content={"error": f"Failed to process video: {str(e)}"}, 
            status_code=500,
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "*"
            }
        )
