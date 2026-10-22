import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def check_devto():
    ws_url = "ws://127.0.0.1:9223/devtools/page/3C6B7FB0CD5048B1044C5EE2CC7EE407"
    async with websockets.connect(ws_url) as ws:
        msg = {
            "id": 1,
            "method": "Runtime.evaluate",
            "params": {
                "expression": """
                (() => {
                    return JSON.stringify({
                        url: window.location.href,
                        title: document.title,
                        body: document.body.innerText.slice(0, 400)
                    });
                })()
                """
            }
        }
        await ws.send(json.dumps(msg))
        res = await ws.recv()
        print("DEV.to state:", json.loads(res).get("result", {}).get("result", {}).get("value"))

asyncio.run(check_devto())
