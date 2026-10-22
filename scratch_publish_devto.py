import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r"C:\Users\Gary\github-cctv-seo\syndication\articles\cps_cctv_evidence_guide.md", "r", encoding="utf-8") as f:
    raw_md = f.read()

# Strip frontmatter if present since title/tags have dedicated fields
lines = raw_md.splitlines()
body_lines = []
in_fm = False
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

async def publish_devto():
    ws_url = "ws://127.0.0.1:9223/devtools/page/3C6B7FB0CD5048B1044C5EE2CC7EE407"
    async with websockets.connect(ws_url, max_size=25*1024*1024) as ws:
        # Fill title and body
        script = f"""
        (() => {{
            function setNativeValue(element, value) {{
                let prototype = Object.getPrototypeOf(element);
                let descriptor = Object.getOwnPropertyDescriptor(prototype, 'value');
                descriptor.set.call(element, value);
                element.dispatchEvent(new Event('input', {{ bubbles: true }}));
                element.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}
            
            const titleInput = document.getElementById('article-form-title');
            if (titleInput) {{
                setNativeValue(titleInput, {json.dumps(title_text)});
            }}
            
            const tagInput = document.getElementById('tag-input');
            if (tagInput) {{
                setNativeValue(tagInput, 'cctv, security, networking, engineering');
            }}
            
            const bodyInput = document.getElementById('article_body_markdown');
            if (bodyInput) {{
                setNativeValue(bodyInput, {json.dumps(body_text)});
            }}
            
            return 'Filled title, tags, and body successfully!';
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
        
        # Click Publish button
        pub_script = """
        (() => {
            const btns = Array.from(document.querySelectorAll('button'));
            const pubBtn = btns.find(b => b.innerText.trim() === 'Publish');
            if (pubBtn) {
                pubBtn.click();
                return 'Clicked Publish button!';
            }
            return 'Publish button not found';
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
        
        await asyncio.sleep(6)
        
        # Check URL after publish
        msg3 = {
            "id": 3,
            "method": "Runtime.evaluate",
            "params": {"expression": "JSON.stringify({url: window.location.href, title: document.title})"}
        }
        await ws.send(json.dumps(msg3))
        res3 = await ws.recv()
        print("After publish:", json.loads(res3).get("result", {}).get("result", {}).get("value"))

asyncio.run(publish_devto())
