#!/bin/bash
# Script to reload nginx with the new v2p-formatter configuration

echo "Testing nginx configuration..."
sudo nginx -t

if [ $? -eq 0 ]; then
    echo ""
    echo "Configuration is valid. Reloading nginx..."
    sudo nginx -s reload
    echo ""
    echo "✅ Nginx reloaded successfully!"
    echo ""
    echo "Now start the Flask app:"
    echo "  cd /Users/rom/Documents/nvq/apps/v2p-formatter"
    echo "  source venv/bin/activate"
    echo "  python run.py"
    echo ""
    echo "Then access: http://localhost/v2p-formatter"
else
    echo ""
    echo "❌ Nginx configuration test failed. Please check the errors above."
    exit 1
fi

