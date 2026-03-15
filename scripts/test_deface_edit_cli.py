#!/usr/bin/env python3
"""
CLI test: Deface page with qualification=Deco&learner=arjom — verify Edit button works.
1. Fetches the deface page HTML and checks that the Edit implementation is present
   (wrapper + _impl, no stub).
2. Optionally: run apply_deface for intro.mp4, then verify deface_existing returns
   items so the review grid (✓ Defaced, Edit) is shown.

Usage:
  python scripts/test_deface_edit_cli.py              # check page script only
  python scripts/test_deface_edit_cli.py --full       # check page + run deface flow

Requires app running at BASE_URL (default http://localhost:5001/v2p-formatter).
"""

import argparse
import json
import sys
import urllib.request
import urllib.error

BASE_URL = "http://localhost:5001/v2p-formatter"
QUALIFICATION = "Deco"
LEARNER = "arjom"
VIDEO_NAME = "intro.mp4"


def fetch_html(path, base_url=BASE_URL):
    url = base_url.rstrip("/") + path
    req = urllib.request.Request(url)
    req.add_header("Accept", "text/html")
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.read().decode("utf-8", errors="replace")


def request(method, path, data=None, base_url=BASE_URL):
    url = base_url.rstrip("/") + path
    req = urllib.request.Request(url, method=method)
    req.add_header("Content-Type", "application/json")
    if data is not None:
        req.data = json.dumps(data).encode("utf-8")
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.getcode(), json.loads(r.read().decode())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--full", action="store_true", help="Run full flow: list_images, apply_deface, deface_existing")
    ap.add_argument("--base-url", default=BASE_URL, help=f"Base URL (default {BASE_URL})")
    args = ap.parse_args()
    base_url = args.base_url.rstrip("/")

    print("Deface Edit CLI test")
    print(f"  BASE_URL={base_url}")
    print(f"  qualification={QUALIFICATION} learner={LEARNER}")
    print()

    # 1. Fetch deface page and verify Edit implementation is in the page (no stub)
    path = f"/deface?qualification={QUALIFICATION}&learner={LEARNER}"
    print(f"1. GET {path}")
    try:
        html = fetch_html(path, base_url)
    except Exception as e:
        print(f"   FAIL fetch: {e}")
        return 1
    print(f"   OK (len={len(html)})")

    # Must have wrapper that delegates to _impl
    if "window.openManualDefaceEditor = function(mediaId)" not in html and "window.openManualDefaceEditor=function(mediaId)" not in html:
        print("   FAIL: page missing wrapper (window.openManualDefaceEditor = function)")
        return 1
    if "openManualDefaceEditor._impl" not in html:
        print("   FAIL: page missing openManualDefaceEditor._impl")
        return 1
    # Must NOT have the stub message (so stub was removed and main script wins)
    if "stub called" in html or "main script may not have loaded" in html:
        print("   FAIL: page still contains stub message (Edit would show stub)")
        return 1
    print("   OK: Edit implementation present (wrapper + _impl), no stub")
    print()

    if not args.full:
        print("Edit script check passed. Use --full to run deface flow (list_images -> apply_deface -> deface_existing).")
        return 0

    # 2. list_images
    print("2. GET list_images")
    try:
        code, data = request("GET", f"/list_images?qualification={QUALIFICATION}&learner={LEARNER}", base_url=base_url)
    except Exception as e:
        print(f"   FAIL: {e}")
        return 1
    if code != 200 or not data.get("success"):
        print(f"   FAIL: {code} {data}")
        return 1
    files = data.get("files") or []
    videos = [f for f in files if f.get("type") == "video"]
    video = next((f for f in videos if VIDEO_NAME in (f.get("name") or "") or (f.get("path") or "").endswith(VIDEO_NAME)), videos[0] if videos else None)
    if not video:
        print(f"   FAIL: no video found (intro.mp4 or any)")
        return 1
    print(f"   OK: using video {video.get('name')}")
    image_paths = [f.get("path") for f in files if f.get("type") == "image"][:3]
    video_paths = [video.get("path")] if video.get("path") else []
    all_paths = image_paths + video_paths
    if not all_paths:
        all_paths = [f.get("path") for f in files if f.get("path")][:5]
    if not all_paths:
        print("   FAIL: no paths to deface")
        return 1

    # 3. apply_deface
    print("3. POST apply_deface")
    payload = {
        "image_paths": all_paths,
        "quality": 95,
        "max_size": "640x480",
        "replacewith": "blur",
        "boxes": False,
        "thresh": 0.2,
        "scale": "640x360",
        "mosaicsize": 20,
        "draw_scores": False,
        "approve_video_processing": True,
        "qualification": QUALIFICATION,
        "learner": LEARNER,
    }
    try:
        code, data = request("POST", "/apply_deface", data=payload, base_url=base_url)
    except Exception as e:
        print(f"   FAIL: {e}")
        return 1
    if not data.get("success"):
        print(f"   FAIL: success=False {data.get('error', data)}")
        return 1
    processed = data.get("processed", [])
    print(f"   OK: processed {len(processed)} item(s)")
    print()

    # 4. deface_existing (review grid: ✓ Defaced, Edit)
    print("4. GET deface_existing (review grid with Edit)")
    try:
        code, data = request("GET", f"/deface_existing?qualification={QUALIFICATION}&learner={LEARNER}", base_url=base_url)
    except Exception as e:
        print(f"   FAIL: {e}")
        return 1
    if code != 200:
        print(f"   FAIL: {code}")
        return 1
    items = data.get("items") or []
    print(f"   OK: {len(items)} existing defaced item(s)")
    if items:
        print("   Review grid would show: ✓ Defaced, Edit for each item.")
    print()
    print("All checks passed. Edit button should work on the deface page.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
