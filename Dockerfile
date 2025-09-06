# syntax=docker/dockerfile:1

FROM python:3.10-slim

# Install Octave
RUN apt-get update && \
    apt-get install -y --no-install-recommends octave && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all app files
COPY . .

# Render injects $PORT at runtime
EXPOSE 10000

# Use Gunicorn, binding to $PORT
CMD ["sh","-c","gunicorn -b 0.0.0.0:$PORT api:app"]
