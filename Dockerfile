# Use official Python image
FROM python:3.10-slim

# Install Octave
RUN apt-get update && \
    apt-get install -y octave && \
    rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy app files
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Expose port
EXPOSE 5000

# Start Flask app
CMD ["python", "api.py"]
