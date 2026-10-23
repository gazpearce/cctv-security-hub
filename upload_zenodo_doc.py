import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def test_set_file():
    tab_id = 'C8AC94E331D5E7707203F724DC068AD7'
    async with websockets.connect(f'ws://127.0.0.1:9223/devtools/page/{tab_id}') as ws:
        # Get objectId of input[type="file"]
        expr = "document.querySelector('input[type=\"file\"]')"
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': expr}}))
        raw = await ws.recv()
        resp = json.loads(raw)
        obj_id = resp.get('result', {}).get('result', {}).get('objectId')
        print('objectId of file input:', obj_id)
        
        pdf_path = r'C:\Users\Gary\github-cctv-seo\stack_assets\documents\UK_Police_CCTV_Evidence_Admissibility_and_DORI_Standard_Guide.pdf'
        
        # Call DOM.setFileInputFiles with objectId
        await ws.send(json.dumps({
            'id': 2,
            'method': 'DOM.setFileInputFiles',
            'params': {
                'files': [pdf_path],
                'objectId': obj_id
            }
        }))
        raw2 = await ws.recv()
        print('setFileInputFiles response:', raw2)
        
        await asyncio.sleep(4)
        
        # Check UI to see if file is listed
        expr_check = """
        (() => {
            const files = Array.from(document.querySelectorAll('.file-item, .item, tr, .filename')).map(e => e.innerText.trim()).filter(t => t.includes('UK_Police_CCTV') || t.includes('.pdf'));
            return {
                filesFound: files,
                bodyText: document.body.innerText.slice(0, 1000)
            };
        })()
        """
        await ws.send(json.dumps({'id': 3, 'method': 'Runtime.evaluate', 'params': {'expression': expr_check, 'returnByValue': True}}))
        raw3 = await ws.recv()
        val = json.loads(raw3).get('result', {}).get('result', {}).get('value', {})
        print('Files in UI:', json.dumps(val, indent=2))

if __name__ == '__main__':
    asyncio.run(test_set_file())
