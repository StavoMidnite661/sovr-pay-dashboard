#!/usr/bin/env python3
"""
SOVR Pay Backend Server Starter
Starts the FastAPI backend server with proper configuration
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def start_backend():
    """Start the FastAPI backend server"""
    print("🚀 Starting SOVR Pay Backend Server...")
    
    # Change to backend directory
    backend_dir = Path(__file__).parent.parent / "backend"
    os.chdir(backend_dir)
    
    # Check if requirements are installed
    try:
        import fastapi
        import uvicorn
        print("✅ Dependencies verified")
    except ImportError:
        print("📦 Installing dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Start the server
    print("🌐 Starting FastAPI server on http://localhost:8000")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("❤️  Health Check: http://localhost:8000/health")
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "main:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload",
            "--log-level", "info"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Backend server stopped")

if __name__ == "__main__":
    start_backend()
