# Nginx Configuration for Video to Image Formatter

Since nginx is already running on port 80, we'll configure it as a reverse proxy to forward requests to the Flask app.

## Setup Instructions

### 1. Find your nginx configuration file

The nginx config is typically located at one of these locations:
- `/opt/homebrew/etc/nginx/nginx.conf` (Homebrew on Apple Silicon)
- `/usr/local/etc/nginx/nginx.conf` (Homebrew on Intel)
- `/etc/nginx/nginx.conf` (System installation)

### 2. Add the proxy configuration

Open your nginx configuration file and find the `server` block (usually in `nginx.conf` or a file included from it, like `servers/default.conf` or `servers/localhost.conf`).

Add this location block inside your `server` block:

```nginx
location /v2p-formatter {
    proxy_pass http://127.0.0.1:5000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    
    # Increase timeouts for file uploads
    proxy_read_timeout 300s;
    proxy_connect_timeout 300s;
    proxy_send_timeout 300s;
    
    # Increase body size for large video files
    client_max_body_size 0;  # No limit
}
```

### 3. Test and reload nginx

```bash
# Test the configuration
sudo nginx -t

# If test passes, reload nginx
sudo nginx -s reload
```

### 4. Start the Flask application

```bash
cd /Users/rom/Documents/nvq/apps/v2p-formatter
source venv/bin/activate
python run.py
```

The Flask app will run on port 5000, and nginx will proxy requests from `http://localhost/v2p-formatter` to it.

## Quick Setup Script

If your nginx config is at `/opt/homebrew/etc/nginx/nginx.conf`, you can use this:

```bash
# Backup your config first!
sudo cp /opt/homebrew/etc/nginx/nginx.conf /opt/homebrew/etc/nginx/nginx.conf.backup

# Add the location block (you'll need to edit manually or use sed)
# Then test and reload
sudo nginx -t && sudo nginx -s reload
```

## Troubleshooting

- **502 Bad Gateway**: Make sure Flask app is running on port 5000
- **404 Not Found**: Check that the location block is inside the correct server block
- **413 Request Entity Too Large**: The `client_max_body_size` might need to be increased in the main nginx config as well

