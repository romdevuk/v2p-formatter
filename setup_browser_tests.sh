#!/bin/bash
# Setup script for browser testing environment

echo "🔧 Setting up browser testing environment..."

# Install Python test dependencies
echo "📦 Installing Python test dependencies..."
pip install -r requirements-test.txt

# Install Playwright browsers
echo "🌐 Installing Playwright browsers..."
python -m playwright install chromium

echo "✅ Browser testing environment setup complete!"
echo ""
echo "To run tests:"
echo "  1. Start Flask server: python app.py"
echo "  2. Run tests: pytest tests/test_observation_media_drag_drop.py -v"
echo ""
echo "For debugging, run with visible browser:"
echo "  HEADLESS=false pytest tests/test_observation_media_drag_drop.py -v"

