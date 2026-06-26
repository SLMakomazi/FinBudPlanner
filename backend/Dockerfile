# Use Python 3.11 slim image as base (minimal Debian with Python)
FROM python:3.11-slim

# Set working directory to /app inside the container
WORKDIR /app

# Install system dependencies required for SQLite database support
# - apt-get update: Update package lists
# - install sqlite3: Install SQLite command-line tool
# - rm -rf /var/lib/apt/lists/*: Clean up apt cache to reduce image size
RUN apt-get update && apt-get install -y sqlite3 && rm -rf /var/lib/apt/lists/*

# Copy Python requirements file from host to container
COPY requirements.txt .

# Install Python dependencies from requirements.txt
# --no-cache-dir: Don't cache pip downloads to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy all backend application code from host to container
# This includes main.py, models.py, routers/, etc.
COPY . .

# Create persistent runtime directory for database storage
# This ensures the database directory exists when the container starts
RUN mkdir -p /app/database

# Expose port 8000 for FastAPI backend (default FastAPI port)
# Note: This is for documentation, actual port mapping done at runtime
EXPOSE 8000

# Set environment variable for database path
# This tells the application where to find/create the SQLite database
ENV DATABASE_PATH=/app/database/finbud.db

# Default command to run when container starts
# This launches the FastAPI backend server
CMD ["python", "main.py"]
