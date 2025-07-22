#!/usr/bin/env python3
"""
SOVR Pay Unified Service Orchestrator
Starts all services in the correct order with proper coordination
"""

import os
import sys
import subprocess
import time
import signal
from pathlib import Path
import threading
import requests

class ServiceOrchestrator:
    def __init__(self):
        self.processes = []
        self.running = True
        
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print("\n🛑 Shutting down all services...")
        self.running = False
        for process in self.processes:
            try:
                process.terminate()
            except:
                pass
        sys.exit(0)
    
    def check_service_health(self, url, timeout=5):
        """Check if a service is healthy"""
        try:
            response = requests.get(url, timeout=timeout)
            return response.status_code == 200
        except:
            return False
    
    def start_backend(self):
        """Start the FastAPI backend"""
        print("🚀 Starting backend server...")
        backend_dir = Path(__file__).parent.parent / "backend"
        
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn",
            "main:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload"
        ], cwd=backend_dir)
        
        self.processes.append(process)
        
        # Wait for backend to be ready
        for _ in range(30):
            if self.check_service_health("http://localhost:8000/health"):
                print("✅ Backend server ready")
                return True
            time.sleep(1)
        
        print("❌ Backend failed to start")
        return False
    
    def start_ngrok(self):
        """Start ngrok tunnel"""
        print("🌐 Starting ngrok tunnel...")
        
        # Import ngrok manager
        sys.path.append(str(Path(__file__).parent))
        from start_ngrok_tunnel import NgrokManager
        
        manager = NgrokManager()
        url = manager.start_ngrok(8000)
        
        if url:
            print(f"✅ Ngrok tunnel active: {url}")
            return url
        else:
            print("❌ Failed to start ngrok")
            return None
    
    def start_dashboard(self):
        """Start the local dashboard"""
        print("📊 Starting local dashboard...")
        dashboard_path = Path(__file__).parent.parent / "dashboard" / "dashboard.html"
        
        if dashboard_path.exists():
            print(f"📋 Dashboard available at: file://{dashboard_path.absolute()}")
            return True
        else:
            print("⚠️  Dashboard file not found")
            return False
    
    def run(self):
        """Run all services"""
        print("🎯 SOVR Pay Service Orchestrator")
        print("=" * 50)
        
        # Set up signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Start services in order
        if not self.start_backend():
            sys.exit(1)
        
        time.sleep(2)
        
        ngrok_url = self.start_ngrok()
        if not ngrok_url:
            print("⚠️  Continuing without ngrok...")
        
        time.sleep(1)
        
        self.start_dashboard()
        
        print("\n" + "=" * 50)
        print("🎉 All services started successfully!")
        print(f"📖 API Docs: {ngrok_url or 'http://localhost:8000'}/docs")
        print(f"❤️  Health: {ngrok_url or 'http://localhost:8000'}/health")
        print("🛑 Press Ctrl+C to stop all services")
        
        # Keep running
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.signal_handler(None, None)

if __name__ == "__main__":
    orchestrator = ServiceOrchestrator()
    orchestrator.run()
