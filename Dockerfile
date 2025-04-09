FROM python:3.10-slim

# Install ffmpeg (includes ffprobe)
RUN apt update && apt install -y ffmpeg

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run FastAPI app
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
