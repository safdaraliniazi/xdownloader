from fastapi import FastAPI, Request
from .downloader import stream_twitter_video
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI()


## cors error
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class URLRequest(BaseModel):
    url: str
    


@app.post("/download/twitter")
def twitter_download(request : URLRequest):
    return stream_twitter_video(request.url)

@app.get("/")
def read_root():
    return {"Hello": "World"}

