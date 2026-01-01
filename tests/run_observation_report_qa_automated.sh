#!/bin/bash
# Automated UX/QA Test Runner for Observation Report
# This script is designed to be run by agents automatically

set -e

echo "🧪 Observation Report - Automated UX/QA Testing"
echo "================================================"
echo ""

# Configuration
BASE_URL="${BASE_URL:-http://localhost/v2p-formatter}"
HEADLESS="${HEADLESS:-true}"
SCREENSHOT_DIR="test_screenshots/observation_report_ux_qa"
REPORT_DIR="reports"

# Create directories
mkdir -p "$SCREENSHOT_DIR"
mkdir -p "$REPORT_DIR"

# Check if Flask server is running
echo "🔍 Checking Flask server..."
if ! curl -s "$BASE_URL/observation-report" > /dev/null 2>&1; then
    echo "❌ ERROR: Flask server is not running at $BASE_URL"
    echo "   Please start the server with: python run.py"
    exit 1
fi
echo "✅ Flask server is running"
echo ""

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    if [ -d "venv" ]; then
        echo "🔧 Activating virtual environment..."
        source venv/bin/activate
    else
        echo "⚠️  Warning: No virtual environment found"
    fi
fi

# Run UX/QA tests
echo "🧪 Running UX/QA tests..."
echo ""

pytest tests/test_observation_report_ux_qa.py \
    -v \
    --tb=short \
    --html="$REPORT_DIR/observation_report_ux_qa.html" \
    --self-contained-html \
    --junitxml="$REPORT_DIR/observation_report_ux_qa.xml" \
    || TEST_EXIT_CODE=$?

echo ""
echo "================================================"

if [ -z "$TEST_EXIT_CODE" ] || [ "$TEST_EXIT_CODE" -eq 0 ]; then
    echo "✅ All UX/QA tests passed!"
    echo ""
    echo "📊 Reports generated:"
    echo "   - $REPORT_DIR/observation_report_ux_qa.html"
    echo "   - $REPORT_DIR/observation_report_ux_qa.xml"
    echo ""
    echo "📸 Screenshots: $SCREENSHOT_DIR/"
    exit 0
else
    echo "❌ Some UX/QA tests failed"
    echo ""
    echo "📊 Check reports:"
    echo "   - $REPORT_DIR/observation_report_ux_qa.html"
    echo ""
    echo "📸 Screenshots: $SCREENSHOT_DIR/"
    exit 1
fi



