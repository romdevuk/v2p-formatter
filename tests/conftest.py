"""
Pytest configuration and fixtures for Selenium tests
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from app import create_app
import threading
import time
import os

# Test configuration
BASE_URL = "http://localhost"
TEST_PORT = 5000
TEST_HOST = "127.0.0.1"

@pytest.fixture(scope="session")
def app():
    """Create application for testing"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    return app

@pytest.fixture(scope="session")
def flask_server(app):
    """Check if Flask server is already running, or start one for testing"""
    import requests
    
    # Check if server is already running
    try:
        response = requests.get(f"http://{TEST_HOST}:{TEST_PORT}/v2p-formatter/", timeout=1)
        if response.status_code == 200:
            print(f"✅ Using existing Flask server on port {TEST_PORT}")
            yield app
            return
    except:
        pass
    
    # If not running, start a new server
    print(f"🚀 Starting Flask server on port {TEST_PORT}")
    def run_server():
        app.run(host=TEST_HOST, port=TEST_PORT, debug=False, use_reloader=False)
    
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Wait for server to start
    max_attempts = 30
    for _ in range(max_attempts):
        try:
            response = requests.get(f"http://{TEST_HOST}:{TEST_PORT}/v2p-formatter/", timeout=1)
            if response.status_code == 200:
                print("✅ Flask server started successfully")
                break
        except:
            time.sleep(0.5)
    else:
        pytest.fail("Flask server did not start in time")
    
    yield app
    
    # Server will be stopped when thread dies (daemon=True)

@pytest.fixture(scope="function")
def driver():
    """Create and configure Chromium WebDriver"""
    chrome_options = Options()
    
    # Add options for headless mode (can be toggled)
    if os.getenv('HEADLESS', 'false').lower() == 'true':
        chrome_options.add_argument('--headless')
    
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    
    # Try to use Chrome first (more reliable on macOS), then Chromium
    # Chrome is Chromium-based and works identically for testing
    import shutil
    
    # Priority order: Chrome -> Chromium -> System default
    # Chrome is preferred because it's more reliable on macOS (no Gatekeeper issues)
    browser_paths = [
        # Chrome paths (Chromium-based, works the same, more reliable on macOS)
        '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        '/opt/homebrew/bin/google-chrome',
        '/usr/local/bin/google-chrome',
        # Chromium paths
        '/Applications/Chromium.app/Contents/MacOS/Chromium',
        '/opt/homebrew/bin/chromium',
        '/usr/local/bin/chromium',
        '/usr/bin/chromium',
        '/usr/bin/chromium-browser',
    ]
    
    browser_executable = None
    browser_name = None
    
    # Check installed paths first
    for path in browser_paths:
        if os.path.exists(path):
            browser_executable = path
            if 'Chromium' in path:
                browser_name = 'Chromium'
            else:
                browser_name = 'Chrome'
            break
    
    # If not found in paths, try which command (Chrome first, then Chromium)
    if not browser_executable:
        chrome_cmd = shutil.which('google-chrome') or shutil.which('chrome')
        if chrome_cmd:
            browser_executable = chrome_cmd
            browser_name = 'Chrome'
        else:
            chrome_cmd = shutil.which('chromium') or shutil.which('chromium-browser')
            if chrome_cmd:
                browser_executable = chrome_cmd
                browser_name = 'Chromium'
    
    if browser_executable:
        chrome_options.binary_location = browser_executable
        print(f"✅ Using {browser_name} at: {browser_executable}")
    else:
        print("⚠️  Chromium/Chrome not found, using system default")
        print("   Note: Chrome works identically to Chromium for testing")
    
    # Use webdriver-manager to handle ChromeDriver (works with Chromium too)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    yield driver
    
    # Cleanup
    driver.quit()

@pytest.fixture
def wait(driver):
    """WebDriverWait instance with default timeout"""
    return WebDriverWait(driver, 10)

@pytest.fixture
def base_url():
    """Base URL for the application"""
    return BASE_URL

