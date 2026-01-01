#!/bin/bash
# Run all Observation Report tests (Backend + Frontend + UX/QA)
# Designed for automated agent execution

set -e

echo "🧪 Observation Report - Complete Test Suite"
echo "============================================"
echo ""

# Configuration
BASE_URL="${BASE_URL:-http://localhost/v2p-formatter}"
REPORT_DIR="reports"
EXIT_CODE=0

# Create directories
mkdir -p "$REPORT_DIR"
mkdir -p "test_screenshots"

# Check Flask server
echo "🔍 Checking Flask server..."
if ! curl -s "$BASE_URL/observation-report" > /dev/null 2>&1; then
    echo "❌ ERROR: Flask server is not running"
    echo "   Start with: python run.py"
    exit 1
fi
echo "✅ Flask server is running"
echo ""

# Activate venv if needed
if [ -z "$VIRTUAL_ENV" ] && [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run test suites
echo "📋 Running test suites..."
echo ""

# 1. Backend tests
echo "1️⃣  Backend Tests..."
if pytest tests/test_observation_report_backend.py -v --tb=short; then
    echo "✅ Backend tests passed"
else
    echo "❌ Backend tests failed"
    EXIT_CODE=1
fi
echo ""

# 2. API tests
echo "2️⃣  API Tests..."
if pytest tests/test_observation_report_api.py -v --tb=short; then
    echo "✅ API tests passed"
else
    echo "❌ API tests failed"
    EXIT_CODE=1
fi
echo ""

# 3. UX/QA tests
echo "3️⃣  UX/QA Tests..."
if ./tests/run_observation_report_qa_automated.sh; then
    echo "✅ UX/QA tests passed"
else
    echo "❌ UX/QA tests failed"
    EXIT_CODE=1
fi
echo ""

# 4. Workflow tests
echo "4️⃣  Workflow Tests..."
if pytest tests/test_observation_report_screenshots.py -v --tb=short; then
    echo "✅ Workflow tests passed"
else
    echo "❌ Workflow tests failed"
    EXIT_CODE=1
fi
echo ""

# Generate summary
echo "============================================"
if [ "$EXIT_CODE" -eq 0 ]; then
    echo "✅ ALL TESTS PASSED!"
else
    echo "❌ SOME TESTS FAILED"
fi
echo ""
echo "📊 Reports: $REPORT_DIR/"
echo "📸 Screenshots: test_screenshots/"
echo ""

exit $EXIT_CODE



