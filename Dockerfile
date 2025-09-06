# Use official Python image
FROM python:3.10-slim

# Install Octave
RUN apt-get update && \
    apt-get install -y octave && \
    rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy dependencies first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose port (Render will inject $PORT)
EXPOSE 10000

# Start Flask app with Gunicorn (bind to Render's $PORT)
CMD ["gunicorn", "-b", "0.0.0.0:${PORT}", "api:app"]
