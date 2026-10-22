import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def click_modal_publish():
    ws_url = "ws://127.0.0.1:9223/devtools/page/45AD4F7EB5D4BF0E59AD5CA3F91B7817"
    async with websockets.connect(ws_url) as ws:
        script = """
        (() => {
            const dialog = document.querySelector('[role=dialog]') || document.querySelector('.modal') || document.body;
            const btns = Array.from(dialog.querySelectorAll('button'));
            const pubBtn = btns.find(b => b.innerText.trim() === 'Publish' && b.className.includes('bg-primary'));
            if (pubBtn) {
                pubBtn.click();
                return 'Clicked Publish in Draft settings modal!';
            }
            return 'Publish button in modal not found';
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
        
        await asyncio.sleep(6)
        
        msg2 = {
            "id": 2,
            "method": "Runtime.evaluate",
            "params": {"expression": "JSON.stringify({url: window.location.href, title: document.title, body: document.body.innerText.slice(0, 300)})"}
        }
        await ws.send(json.dumps(msg2))
        res2 = await ws.recv()
        print("After modal publish:", json.loads(res2).get("result", {}).get("result", {}).get("value"))

asyncio.run(click_modal_publish())
