import urllib.request
import json
import asyncio
import websockets
import base64

async def main():
    req = urllib.request.Request("http://127.0.0.1:9223/json", headers={"User-Agent": "Mozilla/5.0"})
    tabs = json.loads(urllib.request.urlopen(req).read().decode("utf-8"))
    
    pin_tab = None
    for t in tabs:
        if "pinterest" in t.get("url", "").lower():
            pin_tab = t
            break
            
    if not pin_tab:
        print("No Pinterest tab found! Opening a new tab...")
        put_req = urllib.request.Request("http://127.0.0.1:9223/json/new?https://www.pinterest.co.uk/", method="PUT")
        pin_tab = json.loads(urllib.request.urlopen(put_req).read().decode("utf-8"))
        await asyncio.sleep(3)

    ws_url = pin_tab["webSocketDebuggerUrl"]
    print(f"Connecting to Pinterest via: {ws_url}")
    
    async with websockets.connect(ws_url, max_size=25 * 1024 * 1024) as ws:
        # Check title, URL, login state
        expr = """
        (() => {
            return {
                title: document.title,
                url: window.location.href,
                hasCreateButton: !!document.querySelector('a[href*="/pin-creation-tool/"], button[aria-label*="Create"], div[data-test-id*="create"]'),
                hasUserMenu: !!document.querySelector('div[data-test-id*="header-profile"], a[href*="/cctv_services"]'),
                bodySnippet: document.body.innerText.slice(0, 300)
            };
        })()
        """
        await ws.send(json.dumps({"id": 1, "method": "Runtime.evaluate", "params": {"expression": expr, "returnByValue": True}}))
        res = json.loads(await ws.recv())
        val = res.get("result", {}).get("result", {}).get("value")
        print("Pinterest Status Result:", json.dumps(val, indent=2))
        
        # Take screenshot
        await ws.send(json.dumps({"id": 2, "method": "Page.captureScreenshot", "params": {"format": "png"}}))
        s_res = json.loads(await ws.recv())
        img_b64 = s_res.get("result", {}).get("data")
        if img_b64:
            with open("pinterest_screen.png", "wb") as f:
                f.write(base64.b64decode(img_b64))
            print("Saved screenshot to pinterest_screen.png")

if __name__ == "__main__":
    asyncio.run(main())
