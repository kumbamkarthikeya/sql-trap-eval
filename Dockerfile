# Use official lightweight Python image
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*

# Copy requirements/dependency list & install python packages
COPY requirements.txt* ./
RUN pip install --no-cache-dir-r requirements.txt

# Copy application source code into container
COPY . .

# Expose Flask port
EXPOSE 5000

# Default command to run the Flask web dashboard
CMD ["python", "app.py"]