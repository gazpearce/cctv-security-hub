import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def test_input():
    ws_url = "ws://127.0.0.1:9223/devtools/page/D554E1EBFF4A9880047E634AA7A9937D"
    async with websockets.connect(ws_url) as ws:
        script = """
        (() => {
            // Clear appended elements
            const editor = document.querySelector('.postArticle-content');
            const h3 = editor.querySelector('h3');
            editor.innerHTML = '';
            editor.appendChild(h3);
            
            // Add initial paragraph
            const p = document.createElement('p');
            p.className = 'graf graf--p';
            editor.appendChild(p);
            
            p.focus();
            const range = document.createRange();
            range.selectNodeContents(p);
            const sel = window.getSelection();
            sel.removeAllRanges();
            sel.addRange(range);
            
            document.execCommand('insertText', false, 'Official technical masterclass on UK Crown Prosecution Service CCTV evidence standards by Gary Pearce (07860 244 274). Full specifications: https://tvandhomesecurity.blogspot.com/');
            
            return {
                text: editor.innerText,
                canPublish: !document.body.innerText.includes('Publishing will become available')
            };
        })()
        """
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': script, 'returnByValue': True}}))
        res = json.loads(await ws.recv())
        print(res.get('result', {}).get('result', {}).get('value'))

if __name__ == '__main__':
    asyncio.run(test_input())
