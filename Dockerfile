# Use Python 3.11 slim image (Debian Bullseye for better compatibility)
FROM python:3.11-slim-bullseye

# Install system dependencies for opencv-python-headless
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libgomp1 \
    libgl1-mesa-glx \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libfontconfig1 \
    libice6 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies with optimizations
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --find-links https://download.pytorch.org/whl/cpu/torch_stable.html -r requirements.txt && \
    pip cache purge

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p uploads/track
RUN mkdir -p static/uploads

# Set environment variables
ENV PYTHONPATH=/app
ENV FLASK_ENV=production
ENV PORT=8080
ENV DISPLAY=:99
ENV QT_QPA_PLATFORM=offscreen

# Expose the port that Railway expects
EXPOSE $PORT

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:$PORT/ || exit 1

# Start the application with gunicorn
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 600 --max-requests 100 --max-requests-jitter 10 app:app
