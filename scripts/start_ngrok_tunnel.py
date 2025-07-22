#!/usr/bin/env python3
"""
SOVR Pay Ngrok Tunnel Manager
Handles dynamic ngrok URL management and environment updates
"""

import requests
import json
import time
import os
from pathlib import Path
import subprocess
import sys

class NgrokManager:
    def __init__(self):
        self.ngrok_api = "http://localhost:4040/api"
        self.env_files = [
            ".env.production",
            ".env.development"
        ]
        
    def get_ngrok_url(self):
        """Get current ngrok URL from API"""
        try:
            response = requests.get(f"{self.ngrok_api}/tunnels", timeout=5)
            if response.status_code == 200:
                tunnels = response.json().get("tunnels", [])
                for tunnel in tunnels:
                    if tunnel.get("proto") == "https":
                        return tunnel.get("public_url")
            return None
        except:
            return None
    
    def update_env_files(self, ngrok_url):
        """Update environment files with new ngrok URL"""
        env_content = f"VITE_API_BASE_URL={ngrok_url}\n"
        env_content += "ENVIRONMENT=production\n"
        env_content += "PORT=8000\n"
        
        for env_file in self.env_files:
            file_path = Path(__file__).parent.parent / env_file
            with open(file_path, 'w') as f:
                f.write(env_content)
            print(f"✅ Updated {env_file} with URL: {ngrok_url}")
    
    def start_ngrok(self, port=8000):
        """Start ngrok tunnel for specified port"""
        print("🌐 Starting ngrok tunnel...")
        
        # Check if ngrok is already running
        try:
            url = self.get_ngrok_url()
            if url:
                print(f"✅ Ngrok already running: {url}")
                self.update_env_files(url)
                return url
        except:
            pass
        
        # Start ngrok
        try:
            subprocess.Popen([
                "ngrok", "http", str(port),
                "--log=stdout",
                "--log-level=info"
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Wait for ngrok to start
            for _ in range(30):
                url = self.get_ngrok_url()
                if url:
                    self.update_env_files(url)
                    print(f"🎯 Ngrok tunnel active: {url}")
                    return url
                time.sleep(1)
            
            print("❌ Failed to start ngrok tunnel")
            return None
            
        except FileNotFoundError:
            print("❌ Ngrok not found. Please install ngrok: https://ngrok.com/download")
            return None

if __name__ == "__main__":
    manager = NgrokManager()
    url = manager.start_ngrok()
    if url:
        print(f"🚀 Ngrok URL: {url}")
        print("📋 Environment files updated")
    else:
        sys.exit(1)
