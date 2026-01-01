#!/usr/bin/env python3
"""
Test script to verify observation-media route is working
"""
import subprocess
import time
import requests
import sys
from pathlib import Path

def test_observation_media_route():
    """Test the observation-media route"""
    print("🧪 Testing observation-media route...")
    
    # Start Flask app in background
    print("📦 Starting Flask app on port 5001...")
    flask_process = subprocess.Popen(
        ['python3', 'run.py'],
        cwd=Path(__file__).parent,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env={**dict(os.environ), 'PYTHONPATH': str(Path(__file__).parent)}
    )
    
    # Wait for Flask to start
    print("⏳ Waiting for Flask to start...")
    time.sleep(5)
    
    # Test direct connection to Flask
    print("\n🔍 Test 1: Direct connection to Flask (port 5001)")
    try:
        response = requests.get('http://127.0.0.1:5001/v2p-formatter/observation-media', timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ SUCCESS - Route is working!")
            print(f"   Content length: {len(response.text)} bytes")
        else:
            print(f"   ❌ FAILED - Status: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
    
    # Test through nginx proxy
    print("\n🔍 Test 2: Through nginx proxy (port 80)")
    try:
        response = requests.get('http://localhost/v2p-formatter/observation-media', timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ SUCCESS - Nginx proxy is working!")
        else:
            print(f"   ❌ FAILED - Status: {response.status_code}")
            print(f"   Response headers: {dict(response.headers)}")
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
    
    # Cleanup
    print("\n🧹 Stopping Flask app...")
    flask_process.terminate()
    flask_process.wait(timeout=5)
    
    print("\n✅ Test complete!")

if __name__ == '__main__':
    import os
    # Activate venv
    venv_python = Path(__file__).parent / 'venv' / 'bin' / 'python3'
    if venv_python.exists():
        os.execv(str(venv_python), [str(venv_python)] + sys.argv)
    else:
        test_observation_media_route()




