import urllib.request
import json
import asyncio
import websockets

async def check_tiktok():
    req = urllib.request.Request("http://127.0.0.1:9223/json", headers={"User-Agent": "Mozilla/5.0"})
    tabs = json.loads(urllib.request.urlopen(req).read().decode("utf-8"))
    
    tiktok_tab = None
    for t in tabs:
        if "tiktok.com" in t.get("url", "").lower():
            tiktok_tab = t
            break

    if not tiktok_tab:
        print("No TikTok tab open currently. Opening https://www.tiktok.com/@cctv_services7...")
        put_req = urllib.request.Request("http://127.0.0.1:9223/json/new?https://www.tiktok.com/@cctv_services7", method="PUT")
        tiktok_tab = json.loads(urllib.request.urlopen(put_req).read().decode("utf-8"))
        await asyncio.sleep(4)

    ws_url = tiktok_tab["webSocketDebuggerUrl"]
    print(f"Connecting to TikTok tab via CDP: {ws_url}")

    async with websockets.connect(ws_url, max_size=25 * 1024 * 1024) as ws:
        expr = """
        (() => {
            const body = document.body ? document.body.innerText : '';
            const title = document.title;
            const url = window.location.href;
            const hasUploadBtn = !!document.querySelector('a[href*="/upload"], a[href*="/creator-center"]');
            const hasProfile = !!document.querySelector('div[data-e2e="profile-icon"], img[class*="avatar"]');
            const isLoggedIn = !body.includes('Log in to TikTok') && (hasUploadBtn || hasProfile);
            return {
                title,
                url,
                hasUploadBtn,
                hasProfile,
                isLoggedIn,
                snippet: body.slice(0, 300)
            };
        })()
        """
        msg = {"id": 1, "method": "Runtime.evaluate", "params": {"expression": expr, "returnByValue": True}}
        await ws.send(json.dumps(msg))
        resp = json.loads(await ws.recv())
        val = resp.get("result", {}).get("result", {}).get("value")
        print("TikTok Status:", json.dumps(val, indent=2))

if __name__ == "__main__":
    asyncio.run(check_tiktok())
