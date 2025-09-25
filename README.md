# XDownloader API

A FastAPI-based video downloader service for social media platforms.

## Features

- Download videos from Twitter/X and other social media platforms
- RESTful API with automatic documentation
- CORS support for web applications
- Built with FastAPI and yt-dlp

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the development server:
```bash
uvicorn app.main:app --reload
```

3. Access the API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

- `GET /` - Health check
- `GET /health` - Detailed health status
- `POST /download/twitter` - Download Twitter/X videos

### Example Usage

```bash
curl -X POST "http://localhost:8000/download/twitter" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://twitter.com/username/status/123456789"}'
```

## Deployment

### Render

1. Connect your GitHub repository to Render
2. Use the following settings:
   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Environment Variables

- `PORT` - Server port (automatically set by Render)
- `PYTHON_VERSION` - Python version (optional, defaults to 3.11.4)

## Tech Stack

- **FastAPI** - Modern, fast web framework for building APIs
- **yt-dlp** - YouTube downloader with support for many sites
- **Uvicorn** - ASGI web server
- **Pydantic** - Data validation using Python type annotations
