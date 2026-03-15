#!/usr/bin/env python3
"""
Run script for Video to Image Formatter
"""
import os
import signal
import sys
from pathlib import Path

from app import create_app

PORT = 5001
PID_FILE = Path(__file__).resolve().parent / ".flask.pid"
RUN_PY = str(Path(__file__).resolve())


def write_pid():
    PID_FILE.write_text(str(os.getpid()))


def remove_pid():
    if PID_FILE.exists():
        try:
            PID_FILE.unlink()
        except OSError:
            pass


def _restart_self(signum, frame):
    """SIGUSR1: replace this process with a fresh run (same PID, no respawn)."""
    os.execv(sys.executable, [sys.executable, RUN_PY])


if __name__ == '__main__':
    signal.signal(signal.SIGUSR1, _restart_self)
    app = create_app()
    try:
        write_pid()
        print("Starting Video to Image Formatter...")
        print("Access the application at: http://localhost/v2p-formatter")
        print("(Flask running on port {}, proxied by nginx on port 80)".format(PORT))
        print("(PID file: {}). Send SIGUSR1 or run ./scripts/restart.sh to restart.".format(PID_FILE))
        app.run(debug=True, host='127.0.0.1', port=PORT, use_reloader=False, threaded=True)
    finally:
        remove_pid()

