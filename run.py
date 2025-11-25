#!/usr/bin/env python3
"""
Run script for Video to Image Formatter
"""
from app import create_app

if __name__ == '__main__':
    app = create_app()
    print("Starting Video to Image Formatter...")
    print("Access the application at: http://localhost/v2p-formatter")
    print("(Flask running on port 5000, proxied by nginx on port 80)")
    # Run on port 5000 - nginx will proxy port 80 to this
    app.run(debug=True, host='127.0.0.1', port=5000)

