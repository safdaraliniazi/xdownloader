from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import logging
import sys

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="XDownloader API",
    description="Video downloader API for social media platforms",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Pydantic model for request
class URLRequest(BaseModel):
    url: str

# Import yt-dlp only when needed to avoid startup issues
def get_video_info(url: str):
    try:
        from yt_dlp import YoutubeDL
        
        logger.info(f"Processing URL: {url}")
        
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'no_warnings': True,
        }
        
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
        if info:
            # Return cleaned info
            return {
                'title': info.get('title', 'Unknown'),
                'url': info.get('url', ''),
                'thumbnail': info.get('thumbnail', ''),
                'duration': info.get('duration', 0),
                'webpage_url': info.get('webpage_url', url),
                'status': 'success'
            }
        else:
            return {'error': 'No video information found', 'status': 'error'}
            
    except ImportError as e:
        logger.error(f"yt-dlp not available: {e}")
        return {'error': 'Video processing service unavailable', 'status': 'error'}
    except Exception as e:
        logger.error(f"Error processing URL {url}: {str(e)}")
        return {'error': f'Failed to process video: {str(e)}', 'status': 'error'}

# Routes
@app.get("/")
def root():
    return {
        "message": "XDownloader API is running", 
        "status": "healthy",
        "python_version": sys.version,
        "endpoints": ["/", "/health", "/download/twitter"]
    }

@app.get("/health")
def health():
    return {
        "status": "healthy", 
        "message": "API is running correctly",
        "python_version": sys.version
    }

@app.options("/download/twitter")
def twitter_options():
    return {"message": "OK"}

@app.post("/download/twitter")
def download_twitter(request: URLRequest):
    try:
        if not request.url:
            return JSONResponse(
                content={"error": "URL is required", "status": "error"}, 
                status_code=400
            )
        
        result = get_video_info(request.url)
        
        if result.get('status') == 'error':
            return JSONResponse(
                content=result, 
                status_code=400 if 'unavailable' in result.get('error', '') else 500
            )
        
        return JSONResponse(content=result)
        
    except Exception as e:
        logger.error(f"Endpoint error: {str(e)}")
        return JSONResponse(
            content={"error": f"Internal server error: {str(e)}", "status": "error"}, 
            status_code=500
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)