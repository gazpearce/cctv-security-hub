import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def open_devto_editor():
    ws_url = "ws://127.0.0.1:9223/devtools/page/3C6B7FB0CD5048B1044C5EE2CC7EE407"
    async with websockets.connect(ws_url) as ws:
        msg = {
            "id": 1,
            "method": "Page.navigate",
            "params": {"url": "https://dev.to/new"}
        }
        await ws.send(json.dumps(msg))
        await ws.recv()
        await asyncio.sleep(4)
        
        msg2 = {
            "id": 2,
            "method": "Runtime.evaluate",
            "params": {
                "expression": """
                (() => {
                    return JSON.stringify({
                        url: window.location.href,
                        title: document.title,
                        inputs: Array.from(document.querySelectorAll('input, textarea')).map(i => ({name: i.name, id: i.id, placeholder: i.placeholder})),
                        buttons: Array.from(document.querySelectorAll('button')).map(b => b.innerText.trim()).filter(Boolean)
                    });
                })()
                """
            }
        }
        await ws.send(json.dumps(msg2))
        res = await ws.recv()
        print("DEV.to editor state:", json.loads(res).get("result", {}).get("result", {}).get("value"))

asyncio.run(open_devto_editor())
