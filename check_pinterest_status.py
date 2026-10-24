import asyncio
import websockets
import json

async def check():
    uri = "ws://127.0.0.1:9223/devtools/page/A2DC8F183A11791FEB284DC5B78D1861"
    async with websockets.connect(uri) as ws:
        # Check current status
        await ws.send(json.dumps({
            "id": 1,
            "method": "Runtime.evaluate",
            "params": {
                "expression": "JSON.stringify({ title: document.title, url: window.location.href, body: document.body.innerText.slice(0, 500) })",
                "returnByValue": True
            }
        }))
        res = json.loads(await ws.recv())
        val = res.get("result", {}).get("result", {}).get("value")
        print("Pinterest Status:\n", val)

if __name__ == "__main__":
    asyncio.run(check())
