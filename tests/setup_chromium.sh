#!/bin/bash
# Script to help set up Chromium for Selenium tests

echo "Chromium Browser Setup for Selenium Tests"
echo "=========================================="
echo ""

# Check if Chromium is already installed
if command -v chromium &> /dev/null; then
    echo "✅ Chromium found at: $(which chromium)"
    exit 0
fi

if command -v chromium-browser &> /dev/null; then
    echo "✅ Chromium found at: $(which chromium-browser)"
    exit 0
fi

# Check common installation paths
CHROMIUM_PATHS=(
    "/Applications/Chromium.app/Contents/MacOS/Chromium"
    "/opt/homebrew/bin/chromium"
    "/usr/bin/chromium"
    "/usr/bin/chromium-browser"
)

for path in "${CHROMIUM_PATHS[@]}"; do
    if [ -f "$path" ]; then
        echo "✅ Chromium found at: $path"
        exit 0
    fi
done

echo "❌ Chromium not found"
echo ""
echo "To install Chromium:"
echo ""
echo "macOS (Homebrew):"
echo "  brew install chromium"
echo ""
echo "Linux (Ubuntu/Debian):"
echo "  sudo apt-get install chromium-browser"
echo ""
echo "Linux (Fedora):"
echo "  sudo dnf install chromium"
echo ""

exit 1

