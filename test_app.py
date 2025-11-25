#!/usr/bin/env python3
"""Test script to verify the Flask app works"""
from app import create_app

if __name__ == '__main__':
    app = create_app()
    print("=" * 50)
    print("Testing Flask application")
    print("=" * 50)
    print("\nRegistered routes:")
    for rule in app.url_map.iter_rules():
        print(f"  {rule}")
    print("\n" + "=" * 50)
    print("Starting server on port 5000 for testing...")
    print("Access at: http://localhost:5000/v2p-formatter")
    print("Press Ctrl+C to stop")
    print("=" * 50 + "\n")
    app.run(debug=True, host='127.0.0.1', port=5000)

