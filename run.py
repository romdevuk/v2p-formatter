#!/usr/bin/env python3
"""
Run script for Video to Image Formatter
"""
from app import create_app

if __name__ == '__main__':
    app = create_app()
    print("Starting Video to Image Formatter...")
    print("Access the application at: http://localhost/v2p-formatter")
    # Use port 5001 to avoid macOS AirPlay Receiver conflict on port 5000
    print("(Flask running on port 5001, proxied by nginx on port 80)")
    # Run on port 5001 - nginx will proxy port 80 to this
    # Note: Changed from 5000 to avoid macOS AirPlay Receiver conflict
    # use_reloader=False to prevent server restarts that clear in-memory sessions
    app.run(debug=True, host='127.0.0.1', port=5001, use_reloader=False)

