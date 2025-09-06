# syntax=docker/dockerfile:1

FROM python:3.10-slim

# Install Octave (and clean apt cache)
RUN apt-get update && \
    apt-get install -y --no-install-recommends octave && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Helpful for logs
ENV PYTHONUNBUFFERED=1

# Render assigns a dynamic port via $PORT; EXPOSE is informational
EXPOSE 10000

# IMPORTANT: run via a shell so $PORT expands at runtime
CMD ["sh","-c","gunicorn -b 0.0.0.0:$PORT app:app"]
