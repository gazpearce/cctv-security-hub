import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def switch_hashnode_markdown():
    ws_url = "ws://127.0.0.1:9223/devtools/page/45AD4F7EB5D4BF0E59AD5CA3F91B7817"
    async with websockets.connect(ws_url) as ws:
        script = """
        (() => {
            const btns = Array.from(document.querySelectorAll('button'));
            const mdBtn = btns.find(b => b.innerText.trim() === 'Markdown');
            if (mdBtn) {
                mdBtn.click();
                return 'Clicked Markdown button';
            }
            return 'No Markdown button';
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
        
        await asyncio.sleep(2)
        
        # Check inputs now
        msg2 = {
            "id": 2,
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
                    return JSON.stringify(inputs);
                })()
                """
            }
        }
        await ws.send(json.dumps(msg2))
        res2 = await ws.recv()
        print("Inputs after markdown switch:", json.loads(res2).get("result", {}).get("result", {}).get("value"))

asyncio.run(switch_hashnode_markdown())
