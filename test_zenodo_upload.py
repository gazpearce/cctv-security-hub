import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def check_zenodo_file_input():
    tab_id = 'C8AC94E331D5E7707203F724DC068AD7'
    async with websockets.connect(f'ws://127.0.0.1:9223/devtools/page/{tab_id}') as ws:
        # First accept cookies if present
        expr_cookie = """
        (() => {
            const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Accept all cookies'));
            if (btn) {
                btn.click();
                return 'Clicked cookies';
            }
            return 'No cookie button';
        })()
        """
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': expr_cookie, 'returnByValue': True}}))
        raw1 = await ws.recv()
        print('Cookie:', raw1)
        
        # Get DOM root
        await ws.send(json.dumps({'id': 2, 'method': 'DOM.getDocument'}))
        doc_raw = await ws.recv()
        root_id = json.loads(doc_raw)['result']['root']['nodeId']
        
        # Query selector for input[type="file"]
        await ws.send(json.dumps({'id': 3, 'method': 'DOM.querySelector', 'params': {'nodeId': root_id, 'selector': 'input[type="file"]'}}))
        q_raw = await ws.recv()
        node_id = json.loads(q_raw)['result']['nodeId']
        print('Found input[type="file"] nodeId:', node_id)
        
        pdf_path = r'C:\Users\Gary\github-cctv-seo\stack_assets\documents\UK_Police_CCTV_Evidence_Admissibility_and_DORI_Standard_Guide.pdf'
        
        # Set file input
        await ws.send(json.dumps({'id': 4, 'method': 'DOM.setFileInputFiles', 'params': {'files': [pdf_path], 'nodeId': node_id}}))
        set_raw = await ws.recv()
        print('Set file input:', set_raw)
        
        await asyncio.sleep(4)
        
        # Check if file appeared in upload list
        expr_check = """
        (() => {
            return {
                bodySnippet: document.body.innerText.slice(0, 1200)
            };
        })()
        """
        await ws.send(json.dumps({'id': 5, 'method': 'Runtime.evaluate', 'params': {'expression': expr_check, 'returnByValue': True}}))
        raw_check = await ws.recv()
        val = json.loads(raw_check).get('result', {}).get('result', {}).get('value', {})
        print('Upload status:', json.dumps(val, indent=2))

if __name__ == '__main__':
    asyncio.run(check_zenodo_file_input())
