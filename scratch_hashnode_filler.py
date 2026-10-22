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

async def run():
    ws_url = "ws://127.0.0.1:9223/devtools/page/45AD4F7EB5D4BF0E59AD5CA3F91B7817"
    async with websockets.connect(ws_url, max_size=25*1024*1024) as ws:
        # First switch to Markdown tab
        switch_md = """
        (() => {
            const btns = Array.from(document.querySelectorAll('button'));
            const mdBtn = btns.find(b => b.innerText.trim() === 'Markdown');
            if (mdBtn) {
                mdBtn.click();
                return 'Clicked Markdown tab';
            }
            return 'Markdown button not found';
        })()
        """
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': switch_md}}))
        print("Switch MD:", json.loads(await ws.recv()).get('result', {}).get('result', {}).get('value'))
        
        await asyncio.sleep(2)
        
        # Fill Title and Body
        fill_script = f"""
        (() => {{
            function setNativeValue(element, value) {{
                let prototype = Object.getPrototypeOf(element);
                let descriptor = Object.getOwnPropertyDescriptor(prototype, 'value');
                descriptor.set.call(element, value);
                element.dispatchEvent(new Event('input', {{ bubbles: true }}));
                element.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}
            
            const titleArea = document.querySelector('textarea[placeholder*="title"], textarea[placeholder*="Title"]');
            if (titleArea) {{
                setNativeValue(titleArea, {json.dumps(title_text)});
            }}
            
            const bodyArea = document.querySelector('textarea[placeholder*="Write your story"], textarea[placeholder*="content"], textarea[placeholder*="markdown"], .CodeMirror textarea, textarea:not([placeholder*="title"])');
            if (bodyArea) {{
                setNativeValue(bodyArea, {json.dumps(body_text)});
                return 'Set title and body via textarea';
            }}
            
            // If ProseMirror or other editor
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
                return 'Set title and pasted body to ProseMirror';
            }}
            
            return 'No suitable body editor found';
        }})()
        """
        await ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': fill_script}}))
        print("Fill:", json.loads(await ws.recv()).get('result', {}).get('result', {}).get('value'))
        
        await asyncio.sleep(3)
        
        # Click Publish button
        click_pub = """
        (() => {
            const btns = Array.from(document.querySelectorAll('button'));
            const pubBtn = btns.find(b => b.innerText.trim() === 'Publish');
            if (pubBtn) {
                pubBtn.click();
                return 'Clicked Publish';
            }
            return 'Publish not found';
        })()
        """
        await ws.send(json.dumps({'id': 3, 'method': 'Runtime.evaluate', 'params': {'expression': click_pub}}))
        print("Click Publish:", json.loads(await ws.recv()).get('result', {}).get('result', {}).get('value'))
        
        await asyncio.sleep(3)
        
        # Check what dialog or modal opened
        modal_state = """
        (() => {
            const btns = Array.from(document.querySelectorAll('button, a'));
            return btns.map(b => b.innerText.trim()).filter(Boolean).slice(0, 15);
        })()
        """
        await ws.send(json.dumps({'id': 4, 'method': 'Runtime.evaluate', 'params': {'expression': modal_state, 'returnByValue': True}}))
        print("Buttons in modal/view:", json.loads(await ws.recv()).get('result', {}).get('result', {}).get('value'))

if __name__ == '__main__':
    asyncio.run(run())
