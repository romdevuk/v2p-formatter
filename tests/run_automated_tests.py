#!/usr/bin/env python3
"""
Automated test runner for Observation Report
Can be executed by agents to verify code changes
"""
import subprocess
import sys
import os
from pathlib import Path

def check_flask_server():
    """Check if Flask server is running"""
    import urllib.request
    try:
        urllib.request.urlopen("http://localhost/v2p-formatter/observation-report", timeout=2)
        print("✅ Flask server is running")
        return True
    except Exception:
        print("❌ ERROR: Flask server is not running")
        print("   Please start with: python run.py")
        return False

def run_tests(test_pattern="test_observation_report*.py", verbose=True):
    """Run pytest tests"""
    cmd = ["pytest", test_pattern]
    
    if verbose:
        cmd.append("-v")
    
    cmd.extend([
        "--tb=short",
        "--html=reports/automated_test_report.html",
        "--self-contained-html"
    ])
    
    result = subprocess.run(cmd, cwd=Path(__file__).parent.parent)
    return result.returncode == 0

def main():
    """Main function"""
    print("🧪 Observation Report - Automated Test Runner")
    print("=" * 60)
    print()
    
    # Check Flask server
    if not check_flask_server():
        sys.exit(1)
    
    print()
    print("🧪 Running automated tests...")
    print()
    
    # Run tests
    success = run_tests()
    
    print()
    print("=" * 60)
    if success:
        print("✅ All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed")
        sys.exit(1)

if __name__ == "__main__":
    main()



