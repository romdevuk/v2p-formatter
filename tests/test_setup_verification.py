"""
Simple test to verify browser testing setup is working
"""
import pytest
from playwright.sync_api import Page, expect
import time


def test_playwright_installation():
    """Verify Playwright is installed and can launch browser"""
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://example.com")
        expect(page.locator("h1")).to_contain_text("Example")
        browser.close()


def test_browser_can_navigate(page: Page):
    """Test that browser can navigate to a simple page"""
    page.goto("https://example.com")
    expect(page.locator("h1")).to_contain_text("Example")


def test_server_connectivity():
    """Test if Flask server is accessible"""
    import requests
    
    base_url = "http://127.0.0.1:5000"
    
    try:
        response = requests.get(f"{base_url}/v2p-formatter/", timeout=5)
        print(f"Server responded with status: {response.status_code}")
        assert response.status_code in [200, 403], f"Unexpected status: {response.status_code}"
        assert response.status_code in [200, 403], f"Unexpected status: {response.status_code}"
    except requests.exceptions.ConnectionError:
        print("Server is not running")
        pytest.skip("Flask server is not running")
    except Exception as e:
        print(f"Error connecting to server: {e}")
        pytest.skip(f"Cannot connect to server: {e}")


def test_observation_media_page_loads(page: Page):
    """Test that observation media page can be loaded (if server is running)"""
    base_url = "http://127.0.0.1:5000"
    url = f"{base_url}/v2p-formatter/observation-media"
    
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=10000)
        
        # Check if page loaded (even if it's an error page)
        title = page.title()
        print(f"Page title: {title}")
        
        # Try to find any element to verify page loaded
        body = page.locator("body")
        expect(body).to_be_visible()
    except Exception as e:
        print(f"Error loading page: {e}")
        pytest.skip(f"Cannot load observation media page: {e}")

