import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def check_hashnode():
    ws_url = "ws://127.0.0.1:9223/devtools/page/45AD4F7EB5D4BF0E59AD5CA3F91B7817"
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
        print("Hashnode state:", json.loads(res).get("result", {}).get("result", {}).get("value"))

asyncio.run(check_hashnode())
