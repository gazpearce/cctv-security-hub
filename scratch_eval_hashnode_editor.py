import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def inspect_hashnode_editor():
    ws_url = "ws://127.0.0.1:9223/devtools/page/45AD4F7EB5D4BF0E59AD5CA3F91B7817"
    async with websockets.connect(ws_url) as ws:
        msg = {
            "id": 1,
            "method": "Runtime.evaluate",
            "params": {
                "expression": """
                (() => {
                    const inputs = Array.from(document.querySelectorAll('input, textarea, [contenteditable=true]')).map(el => ({
                        tag: el.tagName,
                        placeholder: el.placeholder || el.getAttribute('data-placeholder'),
                        id: el.id,
                        className: el.className
                    }));
                    const buttons = Array.from(document.querySelectorAll('button')).map(b => b.innerText.trim()).filter(Boolean);
                    return JSON.stringify({inputs: inputs, buttons: buttons.slice(0, 20)});
                })()
                """
            }
        }
        await ws.send(json.dumps(msg))
        res = await ws.recv()
        print("Hashnode editor fields:", json.loads(res).get("result", {}).get("result", {}).get("value"))

asyncio.run(inspect_hashnode_editor())
