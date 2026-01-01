# Fix 403 Error - Command Line Instructions

## Problem
- Port 5000 is intercepted by macOS AirPlay Receiver
- Nginx is configured to proxy to port 5000
- Flask app is now configured to run on port 5001

## Solution Applied
✅ Nginx config file updated: `/opt/homebrew/etc/nginx/servers/apps.conf`
✅ Changed `proxy_pass http://127.0.0.1:5000` → `http://127.0.0.1:5001`
✅ Flask code updated to use port 5001

## Commands to Run

### Step 1: Test Nginx Configuration
```bash
sudo nginx -t
```
**Expected output:** `nginx: configuration file ... test is successful`

### Step 2: Reload Nginx
```bash
sudo nginx -s reload
```
**Expected output:** (no output = success)

### Step 3: Start Flask App (if not running)
```bash
cd /Users/rom/Documents/nvq/apps/v2p-formatter
source venv/bin/activate
python3 run.py
```
**Expected output:** 
```
Starting Video to Image Formatter...
Access the application at: http://localhost/v2p-formatter
(Flask running on port 5001, proxied by nginx on port 80)
```

**Note:** Keep this terminal open. Flask will run in foreground. To run in background, use:
```bash
python3 run.py > /tmp/flask.log 2>&1 &
```

### Step 4: Test the Route
Open a **new terminal** and run:
```bash
curl http://localhost/v2p-formatter/observation-media
```

**Expected:** HTML content (status 200)

Or test status code only:
```bash
curl -s -o /dev/null -w "Status: %{http_code}\n" http://localhost/v2p-formatter/observation-media
```

**Expected:** `Status: 200`

## Quick One-Liner Test
After reloading nginx and starting Flask:
```bash
curl -s -o /dev/null -w "Status: %{http_code}\n" http://localhost/v2p-formatter/observation-media && echo "✅ Working!" || echo "❌ Still 403"
```

## Troubleshooting

### If still getting 403:
1. **Check Flask is running:**
   ```bash
   lsof -i :5001
   ```
   Should show Python process listening on port 5001

2. **Check nginx config was updated:**
   ```bash
   grep "5001" /opt/homebrew/etc/nginx/servers/apps.conf
   ```
   Should show: `proxy_pass http://127.0.0.1:5001/v2p-formatter;`

3. **Check nginx error logs:**
   ```bash
   tail -20 /var/log/nginx/nvq_apps_error.log
   ```

4. **Test Flask directly (bypass nginx):**
   ```bash
   curl http://127.0.0.1:5001/v2p-formatter/observation-media
   ```
   Should return HTML (200 OK)

### If Flask won't start:
```bash
cd /Users/rom/Documents/nvq/apps/v2p-formatter
source venv/bin/activate
python3 -c "from app import create_app; app = create_app(); print('✅ App created')"
```

## All Commands in Sequence
```bash
# 1. Test and reload nginx
sudo nginx -t && sudo nginx -s reload

# 2. Start Flask (in background)
cd /Users/rom/Documents/nvq/apps/v2p-formatter
source venv/bin/activate
python3 run.py > /tmp/flask.log 2>&1 &

# 3. Wait a few seconds for Flask to start
sleep 5

# 4. Test the route
curl -s -o /dev/null -w "Status: %{http_code}\n" http://localhost/v2p-formatter/observation-media
```




