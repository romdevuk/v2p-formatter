#!/bin/bash
# Script to test and reload nginx configuration

echo "Testing nginx configuration..."
sudo nginx -t

if [ $? -eq 0 ]; then
    echo "✅ Nginx configuration is valid"
    echo "Reloading nginx..."
    sudo nginx -s reload
    echo "✅ Nginx reloaded"
    echo ""
    echo "Testing observation-media route..."
    sleep 2
    curl -s -o /dev/null -w "Status: %{http_code}\n" http://localhost/v2p-formatter/observation-media
else
    echo "❌ Nginx configuration has errors - please fix before reloading"
    exit 1
fi
