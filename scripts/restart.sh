#!/usr/bin/env bash
# Restart the Flask app. If it's already running (same PID file), send SIGUSR1 so it
# restarts in-place (same process, no respawn). Otherwise free port 5001 and start.
set -e
cd "$(dirname "$0")/.."
PORT=5001
PID_FILE=".flask.pid"

# If our app is running (PID file matches a live process), ask it to restart in-place (same PID).
if [ -f "$PID_FILE" ]; then
  PID=$(cat "$PID_FILE")
  if kill -0 "$PID" 2>/dev/null; then
    echo "Restarting app in-place (PID $PID)..."
    kill -USR1 "$PID" 2>/dev/null || true
    echo "Done. App is restarting (same process)."
    exit 0
  fi
  rm -f "$PID_FILE"
fi

# No running app: free the port and start fresh.
PIDS=$(lsof -i :$PORT -t 2>/dev/null || true)
if [ -n "$PIDS" ]; then
  echo "Stopping process(es) on port $PORT: $PIDS"
  echo "$PIDS" | xargs kill -9 2>/dev/null || true
  sleep 2
fi

if lsof -i :$PORT -t 2>/dev/null; then
  echo "Port $PORT still in use. Free it manually: lsof -i :$PORT" >&2
  exit 1
fi

# Use venv Python if present (so deface and deps are found)
if [ -x "venv/bin/python3" ]; then
  PYTHON="venv/bin/python3"
else
  PYTHON="python3"
fi
echo "Starting app ($PYTHON)..."
exec "$PYTHON" run.py
