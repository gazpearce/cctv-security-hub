import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def find_hashnode_write():
    ws_url = "ws://127.0.0.1:9223/devtools/page/45AD4F7EB5D4BF0E59AD5CA3F91B7817"
    async with websockets.connect(ws_url) as ws:
        msg = {
            "id": 1,
            "method": "Runtime.evaluate",
            "params": {
                "expression": """
                (() => {
                    const links = Array.from(document.querySelectorAll('a, button')).map(el => ({
                        tag: el.tagName,
                        text: el.innerText.trim(),
                        href: el.href || null
                    }));
                    return JSON.stringify(links.filter(l => l.text.toLowerCase().includes('write')));
                })()
                """
            }
        }
        await ws.send(json.dumps(msg))
        res = await ws.recv()
        print("Write elements:", json.loads(res).get("result", {}).get("result", {}).get("value"))

asyncio.run(find_hashnode_write())
