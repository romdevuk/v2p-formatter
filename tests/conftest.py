"""
Pytest configuration and fixtures for browser testing
"""
import pytest
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext
import os


@pytest.fixture(scope="session")
def browser():
    """Launch browser for testing"""
    with sync_playwright() as p:
        # Install browsers if needed
        # p.chromium.install()  # Uncomment if browsers not installed
        
        browser = p.chromium.launch(
            headless=os.getenv("HEADLESS", "true").lower() == "true",
            slow_mo=100 if os.getenv("SLOW_MO") else 0
        )
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def context(browser: Browser):
    """Create a new browser context for each test"""
    context = browser.new_context(
        viewport={"width": 1280, "height": 720},
        # Enable console logging
        ignore_https_errors=True
    )
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext):
    """Create a new page for each test"""
    page = context.new_page()
    
    # Listen to console messages for debugging
    def handle_console(msg):
        if msg.type in ["error", "warning"]:
            print(f"\n[Browser {msg.type.upper()}] {msg.text}")
    
    page.on("console", handle_console)
    
    # Listen to page errors
    def handle_page_error(error):
        print(f"\n[Page Error] {error}")
    
    page.on("pageerror", handle_page_error)
    
    yield page
    page.close()
