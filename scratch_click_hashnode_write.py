import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def click_hashnode_write():
    ws_url = "ws://127.0.0.1:9223/devtools/page/45AD4F7EB5D4BF0E59AD5CA3F91B7817"
    async with websockets.connect(ws_url) as ws:
        script = """
        (() => {
            const btns = Array.from(document.querySelectorAll('button'));
            const writeBtn = btns.find(b => b.innerText.trim() === 'Write');
            if (writeBtn) {
                writeBtn.click();
                return 'Clicked Write button';
            }
            return 'No Write button';
        })()
        """
        msg = {
            "id": 1,
            "method": "Runtime.evaluate",
            "params": {"expression": script}
        }
        await ws.send(json.dumps(msg))
        res = await ws.recv()
        print("Click result:", json.loads(res).get("result", {}).get("result", {}).get("value"))
        
        await asyncio.sleep(4)
        
        msg2 = {
            "id": 2,
            "method": "Runtime.evaluate",
            "params": {"expression": "JSON.stringify({url: window.location.href, title: document.title, body: document.body.innerText.slice(0, 400)})"}
        }
        await ws.send(json.dumps(msg2))
        res2 = await ws.recv()
        print("After click:", json.loads(res2).get("result", {}).get("result", {}).get("value"))

asyncio.run(click_hashnode_write())
