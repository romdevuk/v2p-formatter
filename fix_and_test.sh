#!/bin/bash
# Fix 403 error - Run this script in your terminal

set -e

echo "🔧 Fixing 403 Error on observation-media"
echo "========================================"
echo ""

# Step 1: Test nginx config
echo "Step 1: Testing nginx configuration..."
sudo nginx -t

if [ $? -ne 0 ]; then
    echo "❌ Nginx configuration test failed!"
    exit 1
fi

echo "✅ Nginx configuration is valid"
echo ""

# Step 2: Reload nginx
echo "Step 2: Reloading nginx..."
sudo nginx -s reload
echo "✅ Nginx reloaded"
echo ""

# Step 3: Check if Flask is running
echo "Step 3: Checking Flask status..."
if lsof -i :5001 > /dev/null 2>&1; then
    echo "✅ Flask is already running on port 5001"
    FLASK_PID=$(lsof -ti :5001)
    echo "   PID: $FLASK_PID"
else
    echo "⚠️  Flask is not running. Starting Flask..."
    cd /Users/rom/Documents/nvq/apps/v2p-formatter
    source venv/bin/activate
    python3 run.py > /tmp/flask_fix.log 2>&1 &
    FLASK_PID=$!
    echo "✅ Flask started (PID: $FLASK_PID)"
    echo "   Waiting for Flask to initialize..."
    sleep 6
fi
echo ""

# Step 4: Test the route
echo "Step 4: Testing observation-media route..."
echo ""

# Test direct Flask connection
echo "Testing direct Flask connection (port 5001):"
FLASK_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:5001/v2p-formatter/observation-media 2>/dev/null || echo "000")
if [ "$FLASK_STATUS" = "200" ]; then
    echo "   ✅ Direct Flask: Status $FLASK_STATUS"
else
    echo "   ❌ Direct Flask: Status $FLASK_STATUS"
fi

# Test through nginx
echo "Testing through nginx (port 80):"
NGINX_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/v2p-formatter/observation-media 2>/dev/null || echo "000")
if [ "$NGINX_STATUS" = "200" ]; then
    echo "   ✅ Through nginx: Status $NGINX_STATUS"
    echo ""
    echo "🎉 SUCCESS! Route is working!"
    echo ""
    echo "You can now access: http://localhost/v2p-formatter/observation-media"
else
    echo "   ❌ Through nginx: Status $NGINX_STATUS"
    echo ""
    echo "⚠️  Still getting $NGINX_STATUS. Checking..."
    echo ""
    echo "Debug info:"
    echo "  - Flask running: $(lsof -i :5001 > /dev/null 2>&1 && echo 'Yes' || echo 'No')"
    echo "  - Nginx config: $(grep -c '5001' /opt/homebrew/etc/nginx/servers/apps.conf && echo 'Updated' || echo 'Not updated')"
    echo ""
    echo "Try:"
    echo "  1. Check Flask logs: tail -20 /tmp/flask_fix.log"
    echo "  2. Check nginx logs: tail -20 /var/log/nginx/nvq_apps_error.log"
    echo "  3. Test Flask directly: curl http://127.0.0.1:5001/v2p-formatter/observation-media"
fi

echo ""
echo "Done!"




