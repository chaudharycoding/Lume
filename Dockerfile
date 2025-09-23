# Use Python 3.11 slim image
FROM python:3.11-slim

# Install minimal system dependencies for opencv-python-headless
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p uploads/track
RUN mkdir -p static/uploads

# Set environment variables
ENV PYTHONPATH=/app
ENV FLASK_ENV=production
ENV PORT=8080

# Expose the port that Railway expects
EXPOSE $PORT

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:$PORT/ || exit 1

# Start the application with gunicorn
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 300 --max-requests 1000 --max-requests-jitter 100 app:app
