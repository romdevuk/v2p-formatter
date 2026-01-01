#!/bin/bash

# Observation Report - Test Runner Script
# Runs all observation report tests with screenshots and reporting

set -e

echo "🧪 Observation Report - Test Runner"
echo "===================================="
echo ""

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Virtual environment not activated. Activating..."
    source venv/bin/activate
fi

# Create directories
mkdir -p test_screenshots/observation_report_workflows
mkdir -p test_screenshots/observation_report_visual
mkdir -p reports

echo "📁 Directories created"
echo ""

# Check if Flask server is running
echo "🔍 Checking Flask server..."
if ! curl -s http://localhost/v2p-formatter/observation-report > /dev/null; then
    echo "⚠️  WARNING: Flask server may not be running"
    echo "   Start server with: python run.py"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✅ Flask server is running"
fi

echo ""
echo "🧪 Running Tests..."
echo ""

# Run tests with options
HEADLESS="${HEADLESS:-true}"
VERBOSE="${VERBOSE:-true}"

if [ "$VERBOSE" = "true" ]; then
    VERBOSE_FLAG="-v -s"
else
    VERBOSE_FLAG=""
fi

if [ "$HEADLESS" = "false" ]; then
    export HEADLESS=false
    echo "🖥️  Running in visible browser mode"
else
    export HEADLESS=true
    echo "🖥️  Running in headless mode"
fi

echo ""

# Run test suites
echo "1️⃣  Running E2E Workflow Tests..."
pytest tests/test_observation_report_workflow_e2e.py $VERBOSE_FLAG \
    --html=reports/observation_report_e2e_report.html \
    --self-contained-html || true

echo ""
echo "2️⃣  Running Visual Verification Tests..."
pytest tests/test_observation_report_visual_verification.py $VERBOSE_FLAG \
    --html=reports/observation_report_visual_report.html \
    --self-contained-html || true

echo ""
echo "3️⃣  Running Backend Unit Tests..."
pytest tests/test_observation_report_backend.py $VERBOSE_FLAG || true

echo ""
echo "4️⃣  Running API Integration Tests..."
pytest tests/test_observation_report_api.py $VERBOSE_FLAG || true

echo ""
echo "5️⃣  Running Critical Feature Tests (Drag-and-Drop & Reshuffle)..."
pytest tests/test_observation_report_drag_drop.py \
       tests/test_observation_report_reshuffle.py \
       $VERBOSE_FLAG || true

echo ""
echo "✅ Test Run Complete!"
echo ""
echo "📊 Reports Generated:"
echo "   - reports/observation_report_e2e_report.html"
echo "   - reports/observation_report_visual_report.html"
echo ""
echo "📸 Screenshots:"
echo "   - test_screenshots/observation_report_workflows/"
echo "   - test_screenshots/observation_report_visual/"
echo ""
echo "🎯 View Reports:"
echo "   open reports/observation_report_e2e_report.html"



