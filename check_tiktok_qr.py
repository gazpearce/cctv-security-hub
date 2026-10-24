import asyncio
import websockets
import json
import urllib.request
import base64

resp = urllib.request.urlopen("http://127.0.0.1:9223/json")
tabs = json.loads(resp.read().decode())
tt_tab = [t for t in tabs if "tiktok.com" in t.get("url", "")][0]
ws_url = tt_tab["webSocketDebuggerUrl"]

async def main():
    async with websockets.connect(ws_url, max_size=20*1024*1024) as ws:
        click_js = """
        (() => {
            const boxes = Array.from(document.querySelectorAll('div[class*="DivBoxContainer"]'));
            for (const b of boxes) {
                if ((b.innerText || '').includes('Use QR code')) {
                    b.click();
                    return 'CLICKED_BOX';
                }
            }
            return 'NOT_FOUND';
        })()
        """
        await ws.send(json.dumps({"id": 1, "method": "Runtime.evaluate", "params": {"expression": click_js, "returnByValue": True}}))
        await asyncio.sleep(2.5)
        await ws.send(json.dumps({"id": 2, "method": "Page.captureScreenshot", "params": {"format": "png"}}))
        while True:
            msg = await ws.recv()
            data = json.loads(msg)
            if data.get("id") == 2:
                with open("tiktok_qr_view.png", "wb") as f:
                    f.write(base64.b64decode(data["result"]["data"]))
                print("Saved tiktok_qr_view.png")
                break

if __name__ == "__main__":
    asyncio.run(main())
