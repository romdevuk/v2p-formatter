#!/usr/bin/env python3
"""
CLI test: Deface a video (intro.mp4) for qualification=Deco, learner=arjom.
Uses the API only (list_images -> apply_deface). Passes only when the server
actually defaces the file and returns success with processed items.
Run with: python test_deface_video_cli.py
Requires: app running at BASE_URL (e.g. http://localhost/v2p-formatter via nginx or http://localhost:5001/v2p-formatter).
"""

import json
import sys
import urllib.request
import urllib.error

BASE_URL = "http://localhost/v2p-formatter"
QUALIFICATION = "Deco"
LEARNER = "arjom"
VIDEO_NAME = "intro.mp4"  # must exist under OUTPUT_FOLDER/Deco/arjom/ (or in a subfolder)


def request(method, path, data=None):
    url = f"{BASE_URL}{path}"
    req = urllib.request.Request(url, method=method)
    req.add_header("Content-Type", "application/json")
    if data is not None:
        req.data = json.dumps(data).encode("utf-8")
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            return r.getcode(), json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        try:
            out = json.loads(body)
        except Exception:
            out = {"error": body[:500]}
        return e.code, out
    except Exception as e:
        return 0, {"error": str(e)}


def main():
    print(f"1. GET list_images?qualification={QUALIFICATION}&learner={LEARNER}")
    code, data = request("GET", f"/list_images?qualification={QUALIFICATION}&learner={LEARNER}")
    if code != 200:
        print(f"   FAIL list_images: {code} {data}")
        return 1
    if not data.get("success") or "files" not in data:
        print(f"   FAIL list_images: success={data.get('success')} files missing")
        return 1
    files = data["files"]
    video = None
    for f in files:
        if f.get("type") == "video" and (f.get("name") == VIDEO_NAME or VIDEO_NAME in (f.get("name") or "") or (f.get("path") or "").endswith(VIDEO_NAME)):
            video = f
            break
    if not video and files:
        first_video = next((f for f in files if f.get("type") == "video"), None)
        if first_video:
            video = first_video
            print(f"   (intro.mp4 not found, using first video: {video.get('name')})")
    if not video:
        names = [f.get("name") for f in files if f.get("type") == "video"][:10]
        print(f"   FAIL no video named like {VIDEO_NAME!r}. Video names: {names}")
        return 1
    path = video.get("path")
    if not path:
        print("   FAIL video entry has no path")
        return 1
    print(f"   OK found video: {video.get('name')} path={path[:60]}...")

    print("2. POST apply_deface (approve_video_processing=true). This may take several minutes for video...")
    payload = {
        "image_paths": [path],
        "quality": 95,
        "max_size": "640x480",
        "replacewith": "blur",
        "boxes": False,
        "thresh": 0.2,
        "scale": "original",
        "mosaicsize": 20,
        "draw_scores": False,
        "approve_video_processing": True,
    }
    code, data = request("POST", "/apply_deface", data=payload)
    if code != 200:
        print(f"   FAIL apply_deface: HTTP {code} {data.get('error', data)}")
        return 1
    if not data.get("success"):
        print(f"   FAIL apply_deface: success=False error={data.get('error', data)}")
        return 1
    processed = data.get("processed") or []
    if not processed:
        print("   FAIL apply_deface: success=True but processed is empty")
        return 1
    print(f"   OK defaced: session_id={data.get('session_id')} processed={len(processed)} item(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
