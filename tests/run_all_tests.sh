#!/bin/bash
# Run all Selenium tests with HTML report generation

set -e

echo "=========================================="
echo "Running v2p-formatter Selenium Tests"
echo "=========================================="
echo ""

# Activate virtual environment
cd "$(dirname "$0")/.."
source venv/bin/activate

# Create reports directory
mkdir -p tests/reports

# Run tests with HTML report
echo "Running tests..."
pytest tests/test_complete_workflow.py \
    -v \
    --html=tests/reports/test_report.html \
    --self-contained-html \
    --capture=no \
    -s

echo ""
echo "=========================================="
echo "Tests completed!"
echo "=========================================="
echo ""
echo "📊 Test report: tests/reports/test_report.html"
echo ""
echo "To view the report, open:"
echo "  open tests/reports/test_report.html"
echo ""
