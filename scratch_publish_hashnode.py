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

async def publish_full_hashnode():
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
            
            const pm = document.querySelector('.ProseMirror');
            if (pm) {{
                pm.innerHTML = '';
                pm.focus();
                const dt = new DataTransfer();
                dt.setData('text/plain', {json.dumps(body_text)});
                const pasteEvent = new ClipboardEvent('paste', {{
                    clipboardData: dt,
                    bubbles: true,
                    cancelable: true
                }});
                pm.dispatchEvent(pasteEvent);
            }}
            
            return 'Pasted full body to ProseMirror';
        }})()
        """
        msg = {
            "id": 1,
            "method": "Runtime.evaluate",
            "params": {"expression": script}
        }
        await ws.send(json.dumps(msg))
        res = await ws.recv()
        print("Paste full body:", json.loads(res).get("result", {}).get("result", {}).get("value"))
        
        await asyncio.sleep(4)
        
        # Click Publish button
        pub_script = """
        (() => {
            const btns = Array.from(document.querySelectorAll('button'));
            const pubBtn = btns.find(b => b.innerText.trim() === 'Publish');
            if (pubBtn) {
                pubBtn.click();
                return 'Clicked Publish button on Hashnode';
            }
            return 'No Publish button found';
        })()
        """
        msg2 = {
            "id": 2,
            "method": "Runtime.evaluate",
            "params": {"expression": pub_script}
        }
        await ws.send(json.dumps(msg2))
        res2 = await ws.recv()
        print("Publish click:", json.loads(res2).get("result", {}).get("result", {}).get("value"))
        
        await asyncio.sleep(4)
        
        # Check modal or second publish button if Hashnode shows confirmation modal
        modal_script = """
        (() => {
            const btns = Array.from(document.querySelectorAll('button'));
            // Look for 'Publish now' in modal
            const pubNow = btns.find(b => b.innerText.toLowerCase().includes('publish now'));
            if (pubNow) {
                pubNow.click();
                return 'Clicked Publish now in modal';
            }
            return 'No Publish now button. Active buttons: ' + btns.map(b => b.innerText.trim()).filter(Boolean).slice(0, 10).join(', ');
        })()
        """
        msg3 = {
            "id": 3,
            "method": "Runtime.evaluate",
            "params": {"expression": modal_script}
        }
        await ws.send(json.dumps(msg3))
        res3 = await ws.recv()
        print("Modal state:", json.loads(res3).get("result", {}).get("result", {}).get("value"))
        
        await asyncio.sleep(6)
        
        # Check current URL
        msg4 = {
            "id": 4,
            "method": "Runtime.evaluate",
            "params": {"expression": "JSON.stringify({url: window.location.href, title: document.title})"}
        }
        await ws.send(json.dumps(msg4))
        res4 = await ws.recv()
        print("Final Hashnode state:", json.loads(res4).get("result", {}).get("result", {}).get("value"))

asyncio.run(publish_full_hashnode())
