import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r"C:\Users\Gary\github-cctv-seo\syndication\articles\cps_cctv_evidence_guide.md", "r", encoding="utf-8") as f:
    raw_md = f.read()

lines = raw_md.splitlines()
body_lines = []
fm_count = 0
for l in lines:
    if l.strip() == "---":
        fm_count += 1
        if fm_count <= 2:
            continue
    if fm_count < 2:
        continue
    body_lines.append(l)

body_text = "\n".join(body_lines).strip()
title_text = "Crown Prosecution Service (CPS) CCTV Evidence Standards: Why 82% of UK Footage Fails BS EN 62676-4 DORI Identification (250 px/m)"

async def fill_hashnode():
    ws_url = "ws://127.0.0.1:9223/devtools/page/45AD4F7EB5D4BF0E59AD5CA3F91B7817"
    async with websockets.connect(ws_url, max_size=25*1024*1024) as ws:
        script = f"""
        (() => {{
            function setNativeValue(element, value) {{
                let prototype = Object.getPrototypeOf(element);
                let descriptor = Object.getOwnPropertyDescriptor(prototype, 'value');
                descriptor.set.call(element, value);
                element.dispatchEvent(new Event('input', {{ bubbles: true }}));
                element.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}
            
            const titleArea = document.querySelector('textarea[placeholder="Article title..."]');
            if (titleArea) {{
                setNativeValue(titleArea, {json.dumps(title_text)});
            }}
            
            // For ProseMirror, paste or set content
            const pm = document.querySelector('.ProseMirror');
            if (pm) {{
                pm.focus();
                // Set innerText or dispatch paste event
                const dt = new DataTransfer();
                dt.setData('text/plain', {json.dumps(body_text[:1000])});
                const pasteEvent = new ClipboardEvent('paste', {{
                    clipboardData: dt,
                    bubbles: true,
                    cancelable: true
                }});
                pm.dispatchEvent(pasteEvent);
            }}
            
            return 'Filled title and triggered paste on ProseMirror';
        }})()
        """
        msg = {
            "id": 1,
            "method": "Runtime.evaluate",
            "params": {"expression": script}
        }
        await ws.send(json.dumps(msg))
        res = await ws.recv()
        print("Fill result:", json.loads(res).get("result", {}).get("result", {}).get("value"))
        
        await asyncio.sleep(3)
        
        msg2 = {
            "id": 2,
            "method": "Runtime.evaluate",
            "params": {"expression": "document.querySelector('.ProseMirror')?.innerText.slice(0, 300)"}
        }
        await ws.send(json.dumps(msg2))
        res2 = await ws.recv()
        print("ProseMirror text:", json.loads(res2).get("result", {}).get("result", {}).get("value"))

asyncio.run(fill_hashnode())
