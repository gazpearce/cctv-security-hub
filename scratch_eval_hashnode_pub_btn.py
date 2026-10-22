import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def find_publication_url():
    ws_url = "ws://127.0.0.1:9223/devtools/page/45AD4F7EB5D4BF0E59AD5CA3F91B7817"
    async with websockets.connect(ws_url) as ws:
        msg = {
            "id": 1,
            "method": "Runtime.evaluate",
            "params": {
                "expression": """
                (() => {
                    const btns = Array.from(document.querySelectorAll('button, a')).map(el => ({text: el.innerText.trim(), href: el.href || null}));
                    return JSON.stringify(btns.filter(b => b.text.includes('CCTV') || b.text.includes('Manage') || b.text.includes('View')));
                })()
                """
            }
        }
        await ws.send(json.dumps(msg))
        res = await ws.recv()
        print("Publication buttons:", json.loads(res).get("result", {}).get("result", {}).get("value"))

asyncio.run(find_publication_url())
