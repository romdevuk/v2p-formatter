"""
In-memory buffer and logger for video deface processing debug.
Used so the UI or a separate tab can show live progress when a request is stuck.
Also holds current run progress (total, completed, current_item) for polling during apply_deface.
"""
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional

# In-memory ring buffer (max 300 lines) for GET /deface_video_log
VIDEO_DEBUG_LINES: List[str] = []
_MAX_LINES = 300

# Current deface run progress (set by apply_deface, read by polling)
_DEFACE_PROGRESS: Dict[str, Any] = {
    "total": 0,
    "completed": 0,
    "current_item": None,
    "status": "idle",  # idle | processing | complete | error
    "phase": None,     # images | videos | None
    "elapsed_seconds": 0,  # during video subprocess, updated by heartbeat
    "current_item_pct": None,  # 0-100 from deface CLI (e.g. 23) when parsing stderr
    "item_names": [],  # ordered list of names (images then videos) for queue UI
    "completed_item_urls": [],  # ordered list of defaced URLs as each item completes (for detailed page links)
}

_video_logger = None


def _get_logger():
    global _video_logger
    if _video_logger is None:
        _video_logger = logging.getLogger("app.deface_video")
    return _video_logger


def append_video_log(message: str) -> None:
    """Append a line to the video debug log (file via logger + in-memory buffer)."""
    ts = datetime.utcnow().strftime("%H:%M:%S.%f")[:-3]
    line = f"[{ts}] {message}"
    VIDEO_DEBUG_LINES.append(line)
    if len(VIDEO_DEBUG_LINES) > _MAX_LINES:
        VIDEO_DEBUG_LINES.pop(0)
    _get_logger().info(message)


def get_recent_lines(limit: int = 200) -> List[str]:
    """Return the most recent lines (for API)."""
    return list(VIDEO_DEBUG_LINES[-limit:])


def set_deface_queue_item_names(names: List[str]) -> None:
    """Set the ordered list of item names (images then videos) for queue UI."""
    _DEFACE_PROGRESS["item_names"] = list(names)


def add_deface_completed_item_url(url: str) -> None:
    """Append the defaced URL when an item completes (so detailed page can show link)."""
    _DEFACE_PROGRESS["completed_item_urls"].append(url)


def set_deface_progress(
    total: Optional[int] = None,
    completed: Optional[int] = None,
    current_item: Optional[str] = None,
    status: Optional[str] = None,
    phase: Optional[str] = None,
    elapsed_seconds: Optional[int] = None,
    current_item_pct: Optional[int] = None,
    item_names: Optional[List[str]] = None,
) -> None:
    """Update current deface run progress (for polling during apply_deface)."""
    if total is not None:
        _DEFACE_PROGRESS["total"] = total
    if item_names is not None:
        _DEFACE_PROGRESS["item_names"] = list(item_names)
    if completed is not None:
        _DEFACE_PROGRESS["completed"] = completed
    if current_item is not None:
        _DEFACE_PROGRESS["current_item"] = current_item
        _DEFACE_PROGRESS["current_item_pct"] = None  # reset when starting new item
    if status is not None:
        _DEFACE_PROGRESS["status"] = status
    if phase is not None:
        _DEFACE_PROGRESS["phase"] = phase
    if elapsed_seconds is not None:
        _DEFACE_PROGRESS["elapsed_seconds"] = elapsed_seconds
    if current_item_pct is not None:
        _DEFACE_PROGRESS["current_item_pct"] = current_item_pct


def set_deface_current_item_pct(pct: int) -> None:
    """Update current item percentage from deface CLI output (0-100)."""
    _DEFACE_PROGRESS["current_item_pct"] = max(0, min(100, pct))


def set_deface_elapsed(seconds: int) -> None:
    """Update elapsed seconds during video subprocess (called by heartbeat)."""
    _DEFACE_PROGRESS["elapsed_seconds"] = seconds


def get_deface_progress() -> Dict[str, Any]:
    """Return current deface progress (for API). Includes queue with name+state for UI."""
    out = dict(_DEFACE_PROGRESS)
    names = out.get("item_names") or []
    total = out.get("total") or 0
    completed = out.get("completed") or 0
    current = out.get("current_item")
    status = out.get("status") or "idle"
    # Build queue: [{ name, state }] for main and detailed page
    queue = []
    current_idx = None  # index of item in progress (when current_item doesn't match a name, use completed)
    if current and status == "processing":
        for i, name in enumerate(names):
            if name == current:
                current_idx = i
                break
        if current_idx is None and completed < len(names):
            current_idx = completed  # e.g. parallel videos: generic "Videos (up to N in parallel)"
    completed_urls = out.get("completed_item_urls") or []
    for i, name in enumerate(names):
        if i < completed:
            state = "done"
            url = completed_urls[i] if i < len(completed_urls) else None
        elif current_idx is not None and i == current_idx:
            state = "in_progress"
            url = None
        elif current and name == current:
            state = "in_progress"
            url = None
        else:
            state = "pending"
            url = None
        queue.append({"name": name, "state": state, "url": url})
    out["queue"] = queue
    return out


def clear_deface_progress() -> None:
    """Reset progress after run completes or errors."""
    _DEFACE_PROGRESS["total"] = 0
    _DEFACE_PROGRESS["completed"] = 0
    _DEFACE_PROGRESS["current_item"] = None
    _DEFACE_PROGRESS["status"] = "idle"
    _DEFACE_PROGRESS["phase"] = None
    _DEFACE_PROGRESS["elapsed_seconds"] = 0
    _DEFACE_PROGRESS["current_item_pct"] = None
    _DEFACE_PROGRESS["item_names"] = []
    _DEFACE_PROGRESS["completed_item_urls"] = []
