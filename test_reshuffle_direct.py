#!/usr/bin/env python3
"""Direct test of array manipulation"""
from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    page.goto("http://127.0.0.1:5000/v2p-formatter/observation-media", wait_until="domcontentloaded")
    time.sleep(2)
    
    # Set up test data
    result = page.evaluate("""
        () => {
            window.observationMediaAssignments = {
                'test_placeholder': [
                    { name: 'test1.jpg', path: '/test1.jpg' },
                    { name: 'test2.jpg', path: '/test2.jpg' },
                    { name: 'test3.jpg', path: '/test3.jpg' }
                ]
            };
            
            const arr = window.observationMediaAssignments['test_placeholder'];
            console.log('Before:', arr.map(m => m.name));
            
            // Direct array manipulation
            const media = arr[0];
            arr.splice(0, 1);
            arr.splice(1, 0, media);
            
            console.log('After:', arr.map(m => m.name));
            console.log('Assignments:', window.observationMediaAssignments);
            
            return {
                before: ['test1.jpg', 'test2.jpg', 'test3.jpg'],
                after: arr.map(m => m.name),
                assignments: window.observationMediaAssignments['test_placeholder'].map(m => m.name)
            };
        }
    """)
    
    print("Result:", result)
    
    # Check if modification persisted
    check = page.evaluate("""
        () => {
            return window.observationMediaAssignments['test_placeholder'].map(m => m.name);
        }
    """)
    print("Check:", check)
    
    time.sleep(3)
    browser.close()





