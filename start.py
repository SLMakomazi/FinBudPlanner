#!/usr/bin/env python3
"""
Start script to run both backend and frontend servers simultaneously.

This script starts the FastAPI backend on port 8000 and the Angular frontend
on port 4200. It handles cleanup when the script is interrupted.
"""

import subprocess
import sys
import os
import signal
import time

# Paths to backend and frontend
BACKEND_DIR = os.path.join(os.path.dirname(__file__), 'backend')
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), 'frontend')

# Process references
backend_process = None
frontend_process = None

def signal_handler(sig, frame):
    """Handle interrupt signals to cleanup processes."""
    print('\n\nShutting down servers...')
    if backend_process:
        backend_process.terminate()
    if frontend_process:
        frontend_process.terminate()
    sys.exit(0)

def check_env_file():
    """Check if .env file exists in backend directory."""
    env_file = os.path.join(BACKEND_DIR, '.env')
    if not os.path.exists(env_file):
        print("⚠️  WARNING: .env file not found in backend directory!")
        print("Please copy .env.example to .env and set your SECRET_KEY:")
        print("  cd backend")
        print("  cp .env.example .env")
        print("  # Edit .env and set SECRET_KEY")
        print("  cd ..")
        print()
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            print("Setup cancelled. Please configure .env file first.")
            sys.exit(1)

def start_backend():
    """Start the FastAPI backend server."""
    print("🚀 Starting FastAPI backend on port 8000...")
    os.chdir(BACKEND_DIR)
    backend_process = subprocess.Popen(
        [sys.executable, 'main.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )
    os.chdir(os.path.dirname(__file__))
    return backend_process

def start_frontend():
    """Start the Angular frontend development server."""
    print("🎨 Starting Angular frontend on port 4200...")
    os.chdir(FRONTEND_DIR)
    frontend_process = subprocess.Popen(
        ['npm', 'start'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )
    os.chdir(os.path.dirname(__file__))
    return frontend_process

def main():
    """Main function to start both servers."""
    global backend_process, frontend_process
    
    # Register signal handler for cleanup
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("=" * 60)
    print("FinBudPlanner - Starting Development Servers")
    print("=" * 60)
    print()
    
    # Check for .env file
    check_env_file()
    
    # Check if directories exist
    if not os.path.exists(BACKEND_DIR):
        print(f"❌ Backend directory not found: {BACKEND_DIR}")
        sys.exit(1)
    
    if not os.path.exists(FRONTEND_DIR):
        print(f"❌ Frontend directory not found: {FRONTEND_DIR}")
        sys.exit(1)
    
    # Start backend
    try:
        backend_process = start_backend()
        print("✅ Backend started")
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        sys.exit(1)
    
    # Wait a moment for backend to initialize
    time.sleep(2)
    
    # Start frontend
    try:
        frontend_process = start_frontend()
        print("✅ Frontend started")
    except Exception as e:
        print(f"❌ Failed to start frontend: {e}")
        if backend_process:
            backend_process.terminate()
        sys.exit(1)
    
    print()
    print("=" * 60)
    print("✨ Both servers are running!")
    print("=" * 60)
    print()
    print("📡 Backend API:  http://localhost:8000")
    print("🌐 Frontend:     http://localhost:4200")
    print("📚 API Docs:    http://localhost:8000/docs")
    print()
    print("Press Ctrl+C to stop both servers")
    print("=" * 60)
    print()
    
    # Keep script running and monitor processes
    try:
        while True:
            # Check if processes are still running
            if backend_process.poll() is not None:
                print("❌ Backend process stopped unexpectedly")
                if frontend_process:
                    frontend_process.terminate()
                sys.exit(1)
            
            if frontend_process.poll() is not None:
                print("❌ Frontend process stopped unexpectedly")
                if backend_process:
                    backend_process.terminate()
                sys.exit(1)
            
            time.sleep(1)
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)

if __name__ == "__main__":
    main()
