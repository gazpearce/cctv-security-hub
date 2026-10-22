import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def inspect_hashnode_publish_panel():
    ws_url = "ws://127.0.0.1:9223/devtools/page/45AD4F7EB5D4BF0E59AD5CA3F91B7817"
    async with websockets.connect(ws_url) as ws:
        msg = {
            "id": 1,
            "method": "Runtime.evaluate",
            "params": {
                "expression": """
                (() => {
                    const btns = Array.from(document.querySelectorAll('button')).map(b => ({text: b.innerText.trim(), disabled: b.disabled, class: b.className})).filter(b => b.text);
                    const dialogs = Array.from(document.querySelectorAll('[role=dialog], [role=menu], .modal')).map(d => d.innerText.slice(0, 300));
                    return JSON.stringify({buttons: btns, dialogs: dialogs});
                })()
                """
            }
        }
        await ws.send(json.dumps(msg))
        res = await ws.recv()
        print("Hashnode panel:", json.loads(res).get("result", {}).get("result", {}).get("value"))

asyncio.run(inspect_hashnode_publish_panel())
