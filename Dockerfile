# Use official Python image
FROM python:3.10-slim

# Install Octave
RUN apt-get update && \
    apt-get install -y octave && \
    rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy dependencies first (for better build cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all app files
COPY . .

# Expose Render's dynamic port
EXPOSE 10000

# Start Flask app with Gunicorn bound to $PORT
CMD ["gunicorn", "-b", "0.0.0.0:${PORT}", "app:app"]
