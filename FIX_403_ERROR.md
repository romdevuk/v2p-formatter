# Fix 403 Error on observation-media

## Problem
- Port 5000 is intercepted by macOS AirPlay Receiver
- Flask app needs to run on port 5001
- Nginx is still configured to proxy to port 5000

## Solution Applied
✅ Changed Flask to use port 5001 (in `run.py` and `app/__init__.py`)
✅ Fixed duplicate route function names (`get_learners` → `get_input_learners`, `get_observation_media_learners`)
✅ Added missing logger import

## What You Need to Do

### 1. Update Nginx Configuration

Find your nginx configuration file (usually in one of these locations):
- `/etc/nginx/sites-enabled/your-site`
- `/usr/local/etc/nginx/nginx.conf`
- `/opt/homebrew/etc/nginx/nginx.conf`

Look for this line:
```nginx
proxy_pass http://127.0.0.1:5000;
```

Change it to:
```nginx
proxy_pass http://127.0.0.1:5001;
```

### 2. Reload Nginx

After updating the config, reload nginx:
```bash
sudo nginx -t  # Test configuration
sudo nginx -s reload  # Reload nginx
```

### 3. Restart Flask App

Stop the current Flask process and restart it:
```bash
# Find and kill the old process
ps aux | grep "run.py" | grep v2p-formatter
kill <PID>

# Start Flask (it will now use port 5001)
cd /Users/rom/Documents/nvq/apps/v2p-formatter
source venv/bin/activate
python3 run.py
```

### 4. Test

```bash
# Test direct Flask connection
curl http://127.0.0.1:5001/v2p-formatter/observation-media

# Test through nginx
curl http://localhost/v2p-formatter/observation-media
```

Both should return 200 OK.

## Current Status
- ✅ Flask route works (tested - returns 200)
- ✅ Flask runs on port 5001
- ❌ Nginx still proxying to port 5000 (needs update)




