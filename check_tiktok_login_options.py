import urllib.request
import json
import asyncio
import websockets
import base64

async def check():
    req = urllib.request.Request("http://127.0.0.1:9223/json", headers={"User-Agent": "Mozilla/5.0"})
    tabs = json.loads(urllib.request.urlopen(req).read().decode("utf-8"))
    tt = [t for t in tabs if "tiktok" in t.get("url", "").lower()][0]
    ws_url = tt["webSocketDebuggerUrl"]
    async with websockets.connect(ws_url) as ws:
        await ws.send(json.dumps({"id": 1, "method": "Page.captureScreenshot", "params": {"format": "png"}}))
        res = json.loads(await ws.recv())
        img_b64 = res.get("result", {}).get("data", "")
        with open("tiktok_login_screen.png", "wb") as f:
            f.write(base64.b64decode(img_b64))
        print("Saved tiktok_login_screen.png!")
        
        expr = """
        (() => {
            const btns = Array.from(document.querySelectorAll('a, button, div[role="button"]')).map(b => b.innerText.trim()).filter(Boolean);
            return btns;
        })()
        """
        await ws.send(json.dumps({"id": 2, "method": "Runtime.evaluate", "params": {"expression": expr, "returnByValue": True}}))
        b_res = json.loads(await ws.recv())
        print("Available buttons on screen:", b_res.get("result", {}).get("result", {}).get("value", [])[:20])

if __name__ == "__main__":
    asyncio.run(check())
