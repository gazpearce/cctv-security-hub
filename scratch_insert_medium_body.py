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

# Group lines into paragraphs
paragraphs = []
cur_p = []
for l in body_lines:
    if not l.strip():
        if cur_p:
            paragraphs.append("\n".join(cur_p))
            cur_p = []
    else:
        cur_p.append(l)
if cur_p:
    paragraphs.append("\n".join(cur_p))

async def run():
    ws_url = "ws://127.0.0.1:9223/devtools/page/D554E1EBFF4A9880047E634AA7A9937D"
    async with websockets.connect(ws_url, max_size=25*1024*1024) as ws:
        # Insert paragraphs into Medium editor
        insert_script = f"""
        (() => {{
            const editor = document.querySelector('.postArticle-content');
            if (!editor) return 'Editor container not found';
            
            const ps = {json.dumps(paragraphs)};
            let count = 0;
            for (const text of ps) {{
                if (text.startsWith('# ')) continue; // skip h1
                
                const p = document.createElement('p');
                p.className = 'graf graf--p';
                if (text.startsWith('## ')) {{
                    const h4 = document.createElement('h4');
                    h4.className = 'graf graf--h4';
                    h4.innerText = text.replace(/^##\s+/, '');
                    editor.appendChild(h4);
                }} else if (text.startsWith('### ')) {{
                    const h4 = document.createElement('h4');
                    h4.className = 'graf graf--h4';
                    h4.innerText = text.replace(/^###\s+/, '');
                    editor.appendChild(h4);
                }} else {{
                    p.innerText = text;
                    editor.appendChild(p);
                }}
                count++;
            }}
            editor.dispatchEvent(new Event('input', {{ bubbles: true }}));
            return 'Appended ' + count + ' sections to Medium editor';
        }})()
        """
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': insert_script}}))
        res = json.loads(await ws.recv())
        print(res.get('result', {}).get('result', {}).get('value'))
        
        await asyncio.sleep(3)
        
        # Click Publish button
        click_pub = """
        (() => {
            const btns = Array.from(document.querySelectorAll('button'));
            const pubBtn = btns.find(b => b.innerText.trim() === 'Publish');
            if (pubBtn) {
                pubBtn.click();
                return 'Clicked Publish button';
            }
            return 'Publish button not found';
        })()
        """
        await ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': click_pub}}))
        res2 = json.loads(await ws.recv())
        print(res2.get('result', {}).get('result', {}).get('value'))
        
        await asyncio.sleep(3)
        
        # Check active buttons and inputs in Publish drawer
        drawer_script = """
        (() => {
            const btns = Array.from(document.querySelectorAll('button')).map(b => b.innerText.trim()).filter(Boolean);
            const inputs = Array.from(document.querySelectorAll('input')).map(i => ({placeholder: i.placeholder, value: i.value}));
            return { buttons: btns, inputs: inputs };
        })()
        """
        await ws.send(json.dumps({'id': 3, 'method': 'Runtime.evaluate', 'params': {'expression': drawer_script, 'returnByValue': True}}))
        res3 = json.loads(await ws.recv())
        print("Drawer elements:", res3.get('result', {}).get('result', {}).get('value'))

if __name__ == '__main__':
    asyncio.run(run())
