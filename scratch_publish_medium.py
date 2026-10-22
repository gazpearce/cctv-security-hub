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
title_text = "Crown Prosecution Service (CPS) CCTV Evidence Standards: Why 82% of UK Footage Fails BS EN 62676-4 DORI Identification"

async def publish_medium():
    ws_url = "ws://127.0.0.1:9223/devtools/page/D554E1EBFF4A9880047E634AA7A9937D"
    async with websockets.connect(ws_url, max_size=25*1024*1024) as ws:
        # Step 1: Set Title
        set_title = f"""
        (() => {{
            const titleEl = document.querySelector('h3[data-default-value="Title"]') || document.querySelector('h3');
            if (titleEl) {{
                titleEl.focus();
                document.execCommand('selectAll', false, null);
                document.execCommand('insertText', false, {json.dumps(title_text)});
                return 'Title set successfully';
            }}
            return 'Title element not found';
        }})()
        """
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': set_title}}))
        res1 = json.loads(await ws.recv())
        print("Set Title:", res1.get('result', {}).get('result', {}).get('value'))
        
        await asyncio.sleep(2)
        
        # Step 2: Set Body
        set_body = f"""
        (() => {{
            const bodyEl = document.querySelector('p[data-default-value="Tell your story…"]') || document.querySelector('section p') || document.querySelector('article p');
            if (bodyEl) {{
                bodyEl.focus();
                const dt = new DataTransfer();
                dt.setData('text/plain', {json.dumps(body_text)});
                const pasteEvent = new ClipboardEvent('paste', {{
                    clipboardData: dt,
                    bubbles: true,
                    cancelable: true
                }});
                bodyEl.dispatchEvent(pasteEvent);
                return 'Body pasted to Medium editor';
            }}
            return 'Body element not found';
        }})()
        """
        await ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': set_body}}))
        res2 = json.loads(await ws.recv())
        print("Set Body:", res2.get('result', {}).get('result', {}).get('value'))
        
        await asyncio.sleep(4)
        
        # Step 3: Click Publish button to open publish panel
        click_pub = """
        (() => {
            const btns = Array.from(document.querySelectorAll('button'));
            const pubBtn = btns.find(b => b.innerText.trim() === 'Publish');
            if (pubBtn) {
                pubBtn.click();
                return 'Clicked top Publish button';
            }
            return 'Publish button not found';
        })()
        """
        await ws.send(json.dumps({'id': 3, 'method': 'Runtime.evaluate', 'params': {'expression': click_pub}}))
        res3 = json.loads(await ws.recv())
        print("Click Publish:", res3.get('result', {}).get('result', {}).get('value'))
        
        await asyncio.sleep(4)
        
        # Step 4: Check publish panel state
        panel_state = """
        (() => {
            const btns = Array.from(document.querySelectorAll('button')).map(b => b.innerText.trim()).filter(Boolean);
            const inputs = Array.from(document.querySelectorAll('input')).map(i => ({placeholder: i.placeholder, value: i.value}));
            return { buttons: btns, inputs: inputs };
        })()
        """
        await ws.send(json.dumps({'id': 4, 'method': 'Runtime.evaluate', 'params': {'expression': panel_state, 'returnByValue': True}}))
        res4 = json.loads(await ws.recv())
        print("Panel state:", res4.get('result', {}).get('result', {}).get('value'))

if __name__ == '__main__':
    asyncio.run(publish_medium())
