#!/bin/bash
# Start script for Video to Image Formatter
# This script activates the virtual environment and starts the Flask app on port 5000
# Nginx on port 80 will proxy requests to this Flask app

cd "$(dirname "$0")"

echo "Starting Video to Image Formatter..."
echo ""

# Activate virtual environment
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found. Please run: python3 -m venv venv"
    exit 1
fi

source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import flask" 2>/dev/null; then
    echo "Error: Dependencies not installed. Please run: pip install -r requirements.txt"
    exit 1
fi

echo "Starting Flask application on port 5000..."
echo "Access the application at: http://localhost/v2p-formatter"
echo ""
echo "Note: Make sure nginx is configured to proxy /v2p-formatter to port 5000"
echo "See NGINX_SETUP.md for configuration instructions"
echo ""

# Run without sudo (port 5000 doesn't require privileges)
python run.py

