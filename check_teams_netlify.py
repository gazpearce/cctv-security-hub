import asyncio
import json
import urllib.request
import websockets

CDP_BASE = "http://127.0.0.1:9223"

async def check():
    req = urllib.request.Request(f"{CDP_BASE}/json/list")
    with urllib.request.urlopen(req) as resp:
        tabs = json.loads(resp.read().decode())
    target = next((t for t in tabs if "netlify" in t.get("url", "") or "stripe.network" in t.get("url", "")), None)
    if not target:
        print("No Netlify tab found")
        return
    ws_url = target.get("webSocketDebuggerUrl")
    async with websockets.connect(ws_url, max_size=20*1024*1024) as ws:
        msg = {
            "id": 1,
            "method": "Runtime.evaluate",
            "params": {"expression": "window.top.location.href = 'https://app.netlify.com/teams';", "returnByValue": True}
        }
        await ws.send(json.dumps(msg))
        await ws.recv()
        await asyncio.sleep(6)
        msg["id"] = 2
        msg["params"]["expression"] = "window.top.location.href"
        await ws.send(json.dumps(msg))
        r2 = await ws.recv()
        val = json.loads(r2).get("result", {}).get("result", {}).get("value")
        print("Navigated Netlify URL:", val)

if __name__ == "__main__":
    asyncio.run(check())
