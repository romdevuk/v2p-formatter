#!/bin/bash
# Run Complete Workflow Test for Observation Report

set -e

echo "🧪 Running Complete Workflow Test..."
echo ""

cd "$(dirname "$0")/.."

source venv/bin/activate

echo "📋 Test: Complete End-to-End Workflow"
echo "   Steps: Open Draft → Add Media → Header → Feedback → Save → Export DOCX"
echo ""

pytest tests/test_observation_report_complete_workflow.py -v -s --tb=short

echo ""
echo "✅ Test complete!"
echo ""
echo "📸 Screenshots: test_screenshots/observation_report_complete_workflow/"
echo "📊 HTML Report: reports/report.html"



