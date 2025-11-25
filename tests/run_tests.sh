#!/bin/bash
# Script to run Selenium tests

set -e

echo "=========================================="
echo "Running Selenium Tests"
echo "=========================================="
echo ""

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Activating virtual environment..."
    source ../venv/bin/activate
fi

# Check if Flask app is running
echo "Checking if Flask app is running..."
if ! curl -s http://localhost:5000/v2p-formatter/ > /dev/null 2>&1; then
    echo "⚠️  Warning: Flask app doesn't seem to be running on port 5000"
    echo "   Please start it with: python run.py"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Create reports directory
mkdir -p ../reports

# Run tests
echo "Running tests..."
echo ""

# Check for headless mode
if [ "$1" == "--headless" ] || [ "$HEADLESS" == "true" ]; then
    echo "Running in headless mode..."
    HEADLESS=true pytest . -v --html=../reports/report.html --self-contained-html
else
    pytest . -v --html=../reports/report.html --self-contained-html
fi

echo ""
echo "=========================================="
echo "Tests completed!"
echo "Report: reports/report.html"
echo "=========================================="

