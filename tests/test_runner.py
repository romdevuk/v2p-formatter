"""
Test runner script for browser tests
Can be used to run tests programmatically or from CI/CD
"""
import subprocess
import sys
import os
import time
import requests
from pathlib import Path


def check_server_running(base_url: str = "http://127.0.0.1:5000", timeout: int = 10) -> bool:
    """Check if Flask server is running"""
    try:
        response = requests.get(f"{base_url}/v2p-formatter/", timeout=timeout)
        return response.status_code == 200
    except:
        return False


def run_tests(
    base_url: str = "http://127.0.0.1:5000",
    headless: bool = True,
    slow_mo: int = 0,
    test_file: str = "tests/test_observation_media_drag_drop.py"
):
    """Run browser tests with specified configuration"""
    
    # Check if server is running
    print(f"🔍 Checking if server is running at {base_url}...")
    if not check_server_running(base_url):
        print(f"❌ Server is not running at {base_url}")
        print("   Please start the Flask server first:")
        print("   python app.py")
        return False
    
    print(f"✅ Server is running at {base_url}")
    
    # Set environment variables
    env = os.environ.copy()
    env["TEST_BASE_URL"] = base_url
    env["HEADLESS"] = "true" if headless else "false"
    if slow_mo > 0:
        env["SLOW_MO"] = str(slow_mo)
    
    # Build pytest command
    cmd = [
        "pytest",
        test_file,
        "-v",
        "--html=reports/browser_test_report.html",
        "--self-contained-html"
    ]
    
    if not headless:
        cmd.append("--headed")
    
    print(f"\n🚀 Running tests...")
    print(f"   Command: {' '.join(cmd)}")
    print(f"   Base URL: {base_url}")
    print(f"   Headless: {headless}")
    if slow_mo > 0:
        print(f"   Slow motion: {slow_mo}ms")
    print()
    
    # Run tests
    result = subprocess.run(cmd, env=env)
    
    return result.returncode == 0


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run browser tests for Observation Media")
    parser.add_argument(
        "--url",
        default="http://localhost:5000",
        help="Base URL for the Flask server (default: http://localhost:5000)"
    )
    parser.add_argument(
        "--headed",
        action="store_true",
        help="Run tests with visible browser (for debugging)"
    )
    parser.add_argument(
        "--slow-mo",
        type=int,
        default=0,
        help="Add delay between actions in milliseconds (for debugging)"
    )
    parser.add_argument(
        "--test-file",
        default="tests/test_observation_media_drag_drop.py",
        help="Test file to run"
    )
    
    args = parser.parse_args()
    
    success = run_tests(
        base_url=args.url,
        headless=not args.headed,
        slow_mo=args.slow_mo,
        test_file=args.test_file
    )
    
    sys.exit(0 if success else 1)

