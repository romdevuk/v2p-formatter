#!/bin/bash
# Test observation-media route until it returns 200

echo "🧪 Testing observation-media route..."
echo "Make sure Flask is running and nginx is reloaded!"
echo ""

# Start Flask if not running
if ! lsof -i :5001 > /dev/null 2>&1; then
    echo "Starting Flask on port 5001..."
    cd /Users/rom/Documents/nvq/apps/v2p-formatter
    source venv/bin/activate
    python3 run.py > /tmp/flask_test.log 2>&1 &
    FLASK_PID=$!
    echo "Flask started (PID: $FLASK_PID)"
    sleep 6
fi

# Test loop
MAX_ATTEMPTS=10
ATTEMPT=1

while [ $ATTEMPT -le $MAX_ATTEMPTS ]; do
    echo "Attempt $ATTEMPT/$MAX_ATTEMPTS..."
    
    # Test direct Flask
    FLASK_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:5001/v2p-formatter/observation-media 2>/dev/null)
    echo "  Direct Flask (5001): $FLASK_STATUS"
    
    # Test through nginx
    NGINX_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/v2p-formatter/observation-media 2>/dev/null)
    echo "  Through nginx (80): $NGINX_STATUS"
    
    if [ "$NGINX_STATUS" = "200" ]; then
        echo ""
        echo "✅ SUCCESS! Route is working!"
        echo ""
        echo "Testing full response:"
        curl -s http://localhost/v2p-formatter/observation-media | head -10
        exit 0
    fi
    
    if [ $ATTEMPT -lt $MAX_ATTEMPTS ]; then
        echo "  ⏳ Waiting 3 seconds before retry..."
        sleep 3
    fi
    
    ATTEMPT=$((ATTEMPT + 1))
done

echo ""
echo "❌ Still getting 403 after $MAX_ATTEMPTS attempts"
echo ""
echo "Please check:"
echo "1. Flask is running: lsof -i :5001"
echo "2. Nginx is reloaded: sudo nginx -s reload"
echo "3. Nginx config: grep '5001' /opt/homebrew/etc/nginx/servers/apps.conf"
exit 1




