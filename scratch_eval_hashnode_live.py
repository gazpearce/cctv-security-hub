import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def find_published_url():
    ws_url = "ws://127.0.0.1:9223/devtools/page/45AD4F7EB5D4BF0E59AD5CA3F91B7817"
    async with websockets.connect(ws_url) as ws:
        msg = {
            "id": 1,
            "method": "Runtime.evaluate",
            "params": {
                "expression": """
                (() => {
                    const links = Array.from(document.querySelectorAll('a[href]')).map(a => a.href);
                    const viewLive = links.find(l => !l.includes('hashnode.com/edit') && !l.includes('hashnode.com/settings') && (l.includes('crown-prosecution') || l.includes('hashnode.dev')));
                    return JSON.stringify({live: viewLive, all: links.slice(0, 15)});
                })()
                """
            }
        }
        await ws.send(json.dumps(msg))
        res = await ws.recv()
        print("Hashnode live link:", json.loads(res).get("result", {}).get("result", {}).get("value"))

asyncio.run(find_published_url())
