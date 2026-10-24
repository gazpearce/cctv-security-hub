#!/usr/bin/env python3
"""
upload_tiktok_reels.py
======================
Autonomous TikTok Upload Agent for @cctv_services7 / Gary Pearce (ADI Communications).
Follows tiktok-trend-agent 2026 FYP algorithms, 9:16 safe zones, viral hooks, and SEO tagging.

Connects via Chrome CDP (port 9223).
"""

import os
import sys
import json
import time
import argparse
import asyncio
import urllib.request
from pathlib import Path
from typing import Dict, List, Optional, Any

REPO_ROOT = Path(__file__).resolve().parent
REELS_DIR = REPO_ROOT / "assets" / "reels"
AUDIT_LOG = REPO_ROOT / "hourly_trend_audit.json"
TIKTOK_EVIDENCE = REPO_ROOT / "assets" / "evidence" / "tiktok"
TIKTOK_EVIDENCE.mkdir(parents=True, exist_ok=True)

class TikTokUploader:
    def __init__(self, cdp_port: int = 9223):
        self.cdp_port = cdp_port
        self.cdp_base = f"http://127.0.0.1:{cdp_port}"

    def is_cdp_active(self) -> bool:
        try:
            with urllib.request.urlopen(f"{self.cdp_base}/json", timeout=2.0) as resp:
                return resp.status == 200
        except Exception:
            return False

    async def check_login_state(self) -> Dict[str, Any]:
        """Checks whether the active Chrome session is logged into TikTok."""
        import websockets
        req = urllib.request.Request(f"{self.cdp_base}/json", headers={"User-Agent": "Mozilla/5.0"})
        tabs = json.loads(urllib.request.urlopen(req).read().decode("utf-8"))
        
        tab = next((t for t in tabs if "tiktok.com" in t.get("url", "").lower()), None)
        if not tab:
            put_req = urllib.request.Request(f"{self.cdp_base}/json/new?https://www.tiktok.com/creator-center/upload", method="PUT")
            tab = json.loads(urllib.request.urlopen(put_req).read().decode("utf-8"))
            await asyncio.sleep(4)

        ws_url = tab["webSocketDebuggerUrl"]
        async with websockets.connect(ws_url, max_size=25 * 1024 * 1024) as ws:
            # Check login indicators
            expr = """
            (() => {
                const body = document.body ? document.body.innerText : '';
                const url = window.location.href;
                const isLoginPage = url.includes('/login');
                const hasUploadContainer = !!document.querySelector('input[type="file"], div[class*="upload-container"], div[class*="uploader"]');
                const hasAvatar = !!document.querySelector('div[data-e2e="profile-icon"], img[class*="avatar"]');
                const loggedIn = !isLoginPage && (hasUploadContainer || hasAvatar);
                return { loggedIn, url, isLoginPage, hasUploadContainer, hasAvatar };
            })()
            """
            msg = {"id": 1, "method": "Runtime.evaluate", "params": {"expression": expr, "returnByValue": True}}
            await ws.send(json.dumps(msg))
            resp = json.loads(await ws.recv())
            return resp.get("result", {}).get("result", {}).get("value", {})

    async def login_with_credentials(self, username: str = "cctv_services7", password: str = "") -> bool:
        """Enters username and password into TikTok login screen if provided."""
        import websockets, base64
        req = urllib.request.Request(f"{self.cdp_base}/json", headers={"User-Agent": "Mozilla/5.0"})
        tabs = json.loads(urllib.request.urlopen(req).read().decode("utf-8"))
        tab = next((t for t in tabs if "tiktok.com" in t.get("url", "").lower()), None)
        if not tab:
            return False

        ws_url = tab["webSocketDebuggerUrl"]
        async with websockets.connect(ws_url, max_size=25 * 1024 * 1024) as ws:
            # Navigate to email/username login
            await ws.send(json.dumps({"id": 1, "method": "Page.navigate", "params": {"url": "https://www.tiktok.com/login/phone-or-email/email"}}))
            await asyncio.sleep(3.5)

            fill_expr = f"""
            (() => {{
                const u = document.querySelector('input[name="username"]');
                const p = document.querySelector('input[type="password"]');
                if (u && p) {{
                    u.focus();
                    u.value = {json.dumps(username)};
                    u.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    u.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    
                    p.focus();
                    p.value = {json.dumps(password)};
                    p.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    p.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    
                    const btn = document.querySelector('button[type="submit"], button:has-text("Log in")');
                    if (btn) btn.click();
                    return true;
                }}
                return false;
            }})()
            """
            await ws.send(json.dumps({"id": 2, "method": "Runtime.evaluate", "params": {"expression": fill_expr, "returnByValue": True}}))
            res = json.loads(await ws.recv())
            success = res.get("result", {}).get("result", {}).get("value", False)
            await asyncio.sleep(4.0)

            # Screenshot result
            await ws.send(json.dumps({"id": 3, "method": "Page.captureScreenshot", "params": {"format": "png"}}))
            s_res = json.loads(await ws.recv())
            raw_b64 = s_res.get("result", {}).get("data", "")
            if raw_b64:
                with open(TIKTOK_EVIDENCE / "login_attempt.png", "wb") as f:
                    f.write(base64.b64decode(raw_b64))

            return success

    async def upload_reel(self, video_path: Path, caption: str, tags: str) -> bool:
        """Uploads a single 9:16 vertical reel to TikTok creator center via CDP."""
        import websockets, base64
        print(f"\n[TIKTOK UPLOADER] Processing: {video_path.name}")
        print(f"Caption: {caption}")
        print(f"Hashtags: {tags}")

        req = urllib.request.Request(f"{self.cdp_base}/json", headers={"User-Agent": "Mozilla/5.0"})
        tabs = json.loads(urllib.request.urlopen(req).read().decode("utf-8"))
        tab = next((t for t in tabs if "tiktok.com" in t.get("url", "").lower()), None)
        if not tab:
            put_req = urllib.request.Request(f"{self.cdp_base}/json/new?https://www.tiktok.com/creator-center/upload", method="PUT")
            tab = json.loads(urllib.request.urlopen(put_req).read().decode("utf-8"))
            await asyncio.sleep(5)
        else:
            ws_url = tab["webSocketDebuggerUrl"]
            async with websockets.connect(ws_url) as ws:
                await ws.send(json.dumps({"id": 1, "method": "Page.navigate", "params": {"url": "https://www.tiktok.com/creator-center/upload"}}))
                await asyncio.sleep(5)

        ws_url = tab["webSocketDebuggerUrl"]
        async with websockets.connect(ws_url, max_size=25 * 1024 * 1024) as ws:
            await ws.send(json.dumps({"id": 1, "method": "DOM.enable"}))
            await ws.send(json.dumps({"id": 2, "method": "Page.enable"}))
            await ws.send(json.dumps({"id": 3, "method": "Runtime.enable"}))

            # Find file input
            get_doc = {"id": 4, "method": "DOM.getDocument"}
            await ws.send(json.dumps(get_doc))
            doc_res = json.loads(await ws.recv())

            query_file = {"id": 5, "method": "DOM.querySelector", "params": {"nodeId": doc_res["result"]["root"]["nodeId"], "selector": "input[type='file']"}}
            await ws.send(json.dumps(query_file))
            file_node = json.loads(await ws.recv())
            node_id = file_node.get("result", {}).get("nodeId")

            if not node_id:
                print("[ERROR] Could not locate file input on creator upload page.")
                return False

            print(f"[ATTACH] Attaching file via CDP: {video_path}")
            set_file = {"id": 6, "method": "DOM.setFileInputFiles", "params": {"files": [str(video_path)], "nodeId": node_id}}
            await ws.send(json.dumps(set_file))
            await asyncio.sleep(8.0)

            # Inject caption and hashtags
            full_text = f"{caption} • Gary Pearce ADI Communications 07860 244 274 {tags}"
            cap_expr = f"""
            (() => {{
                const editor = document.querySelector('div[contenteditable="true"], textarea, div[class*="caption-editor"]');
                if (editor) {{
                    editor.focus();
                    if (editor.tagName === 'TEXTAREA') {{
                        editor.value = {json.dumps(full_text)};
                        editor.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    }} else {{
                        editor.innerText = {json.dumps(full_text)};
                        editor.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    }}
                    return true;
                }}
                return false;
            }})()
            """
            await ws.send(json.dumps({"id": 7, "method": "Runtime.evaluate", "params": {"expression": cap_expr, "returnByValue": True}}))
            await asyncio.sleep(4.0)

            # Click Post / Publish button
            post_expr = """
            (() => {
                const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Post' || b.innerText.trim() === 'Publish');
                if (btn) {
                    btn.click();
                    return true;
                }
                return false;
            })()
            """
            await ws.send(json.dumps({"id": 8, "method": "Runtime.evaluate", "params": {"expression": post_expr, "returnByValue": True}}))
            await asyncio.sleep(6.0)

            # Verification screenshot
            slug = video_path.stem
            ev_img = TIKTOK_EVIDENCE / f"{slug}_uploaded.png"
            await ws.send(json.dumps({"id": 9, "method": "Page.captureScreenshot", "params": {"format": "png"}}))
            s_res = json.loads(await ws.recv())
            raw_b64 = s_res.get("result", {}).get("data", "")
            if raw_b64:
                with open(ev_img, "wb") as f:
                    f.write(base64.b64decode(raw_b64))
                print(f"[VERIFIED] Screenshot saved to {ev_img.name}")

            return True

def main():
    parser = argparse.ArgumentParser(description="Autonomous TikTok Uploader for cctv_services7")
    parser.add_argument("--check", action="store_true", help="Check current login state")
    parser.add_argument("--login", action="store_true", help="Attempt login with username/password")
    parser.add_argument("--username", type=str, default="cctv_services7")
    parser.add_argument("--password", type=str, default="")
    parser.add_argument("--upload-latest", action="store_true", help="Upload the latest generated trend reel")
    parser.add_argument("--upload-all-queued", action="store_true", help="Upload all queued trend reels")
    args = parser.parse_args()

    uploader = TikTokUploader()
    if not uploader.is_cdp_active():
        print("[ERROR] Chrome CDP is not active on port 9223.")
        sys.exit(1)

    if args.check:
        state = asyncio.run(uploader.check_login_state())
        print("TikTok Session State:", json.dumps(state, indent=2))
        sys.exit(0)

    if args.login:
        if not args.password:
            print("[INFO] Please provide --password to log into TikTok as cctv_services7.")
            sys.exit(1)
        res = asyncio.run(uploader.login_with_credentials(args.username, args.password))
        print("Login attempt result:", res)
        sys.exit(0)

    if args.upload_latest or args.upload_all_queued:
        # Check login first
        state = asyncio.run(uploader.check_login_state())
        if not state.get("loggedIn"):
            print("\n[AUTH NOTICE] TikTok session is not currently logged in on Chrome (port 9223).")
            print("Please log into TikTok on Chrome (either scan the QR code or enter credentials).")
            print("Current page is at: https://www.tiktok.com/login/qrcode")
            sys.exit(1)

        # Process upload
        if AUDIT_LOG.exists():
            with open(AUDIT_LOG, "r", encoding="utf-8") as f:
                audit = json.load(f)
            
            reels_to_upload = [item for item in audit if item.get("tiktok_status") == "READY_FOR_UPLOAD"]
            if args.upload_latest:
                reels_to_upload = reels_to_upload[-1:]

            print(f"[QUEUE] Found {len(reels_to_upload)} reel(s) ready for TikTok upload.")
            for r in reels_to_upload:
                rp = Path(r["reel_path"])
                if rp.exists():
                    topic = r.get("topic", "UK Trade Solutions")
                    tags = r.get("tiktok_tags", "#CCTV #Tradesman #Yorkshire")
                    ok = asyncio.run(uploader.upload_reel(rp, topic, tags))
                    if ok:
                        r["tiktok_status"] = "PUBLISHED"
                        r["tiktok_published"] = True
                        with open(AUDIT_LOG, "w", encoding="utf-8") as f:
                            json.dump(audit, f, indent=2)

if __name__ == "__main__":
    main()
