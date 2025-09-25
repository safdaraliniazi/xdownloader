from fastapi import FastAPI, Request
from .downloader import stream_twitter_video
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI()


# CORS configuration for production deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://xaudiovideodownloader.netlify.app",
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "*"  # Allow all origins as fallback
    ],
    allow_credentials=False,  # Set to False when using wildcard origins
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=[
        "Accept",
        "Accept-Language",
        "Content-Language",
        "Content-Type",
        "Authorization",
        "X-Requested-With",
        "Origin",
        "Access-Control-Request-Method",
        "Access-Control-Request-Headers"
    ],
)

class URLRequest(BaseModel):
    url: str
    


@app.get("/")
def read_root():
    return {"Hello": "World", "status": "running", "version": "1.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "API is running correctly"}

@app.options("/download/twitter")
def twitter_options():
    """Handle preflight OPTIONS request for CORS"""
    return {"message": "OK"}

@app.post("/download/twitter")
def twitter_download(request : URLRequest):
    return stream_twitter_video(request.url)

