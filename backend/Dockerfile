# ==============================
# Base Image
# ==============================
FROM python:3.11-slim

# ==============================
# Working Directory
# ==============================
WORKDIR /app

# ==============================
# System dependencies
# ==============================
RUN apt-get update && apt-get install -y \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# ==============================
# Python dependencies
# ==============================
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# ==============================
# Copy application code
# ==============================
COPY . .

# ==============================
# Ensure runtime directories exist
# ==============================
RUN mkdir -p /app/database

# ==============================
# Environment variables
# ==============================
ENV PYTHONUNBUFFERED=1
ENV DATABASE_PATH=/app/database/finbud.db

# ==============================
# Expose FastAPI port
# ==============================
EXPOSE 8000

# ==============================
# Start application
# ==============================
CMD ["python", "main.py"]