# Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p models/trained data/raw data/processed data/live

# Set environment variables
ENV PYTHONPATH=/app
ENV FLASK_APP=api/app.py

# Expose ports
# 5000 for API, 8080 for dashboard
EXPOSE 5000 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/health')"

# Default command (can be overridden)
CMD ["python", "api/app.py", "--host", "0.0.0.0", "--port", "5000"]
