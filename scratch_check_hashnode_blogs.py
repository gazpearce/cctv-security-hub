import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def check_settings_pubs():
    ws_url = "ws://127.0.0.1:9223/devtools/page/45AD4F7EB5D4BF0E59AD5CA3F91B7817"
    async with websockets.connect(ws_url) as ws:
        msg = {
            "id": 1,
            "method": "Page.navigate",
            "params": {"url": "https://hashnode.com/settings/blogs"}
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
                    const links = Array.from(document.querySelectorAll('a[href]')).map(a => ({href: a.href, text: a.innerText.trim()}));
                    return JSON.stringify({url: window.location.href, links: links, body: document.body.innerText.slice(0, 500)});
                })()
                """
            }
        }
        await ws.send(json.dumps(msg2))
        res2 = await ws.recv()
        print("Blogs settings:", json.loads(res2).get("result", {}).get("result", {}).get("value"))

asyncio.run(check_settings_pubs())
