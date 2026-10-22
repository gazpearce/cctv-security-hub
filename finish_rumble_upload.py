import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def finish_rumble():
    tab_id = 'B05DD5FD31627A501BCF11412B0DA3C8'
    async with websockets.connect(f'ws://127.0.0.1:9223/devtools/page/{tab_id}') as ws:
        # Wait for 100%
        print("Waiting for 100% upload...")
        for i in range(30):
            await ws.send(json.dumps({
                'id': 100 + i,
                'method': 'Runtime.evaluate',
                'params': {
                    'expression': '({ text: document.body.innerText.slice(0, 300), disabled: document.getElementById("submitForm") ? document.getElementById("submitForm").disabled : null })',
                    'returnByValue': True
                }
            }))
            raw = await ws.recv()
            val = json.loads(raw).get('result', {}).get('result', {}).get('value', {})
            text = val.get('text', '')
            print(f"[{i*2}s] Status:", text.split('\n')[5:8], "Disabled:", val.get('disabled'))
            if '100%' in text or 'Complete' in text or 'Ready' in text or val.get('disabled') is False:
                # Double check upload percentage
                if '100%' in text or not any(f'{p}%' in text for p in range(1, 100)):
                    print("Upload ready to submit!")
                    break
            await asyncio.sleep(2)

        # Click submitForm
        print("Clicking submitForm...")
        await ws.send(json.dumps({
            'id': 200,
            'method': 'Runtime.evaluate',
            'params': {
                'expression': 'document.getElementById("submitForm").click()',
                'returnByValue': True
            }
        }))
        await ws.recv()
        await asyncio.sleep(3)

        # Check Step 2 terms
        print("Submitting Step 2 terms...")
        step2_expr = """
        (() => {
            const terms = document.getElementById('cterms');
            if (terms) { terms.checked = true; terms.dispatchEvent(new Event('change', { bubbles: true })); }
            const rights = document.getElementById('crights');
            if (rights) { rights.checked = true; rights.dispatchEvent(new Event('change', { bubbles: true })); }
            
            const submit2 = document.getElementById('submitForm2');
            if (submit2) {
                submit2.disabled = false;
                submit2.click();
                return 'Clicked submitForm2';
            }
            return 'submitForm2 not found';
        })()
        """
        await ws.send(json.dumps({
            'id': 201,
            'method': 'Runtime.evaluate',
            'params': {'expression': step2_expr, 'returnByValue': True}
        }))
        raw = await ws.recv()
        print("Step 2 response:", json.loads(raw).get('result', {}).get('result', {}).get('value'))

        await asyncio.sleep(6)

        # Check final output
        final_expr = """
        (() => {
            const direct = document.getElementById('direct');
            const embed = document.getElementById('embed');
            return {
                url: window.location.href,
                directShareUrl: direct ? direct.value : null,
                embedCode: embed ? embed.value : null,
                snippet: document.body.innerText.slice(0, 400)
            };
        })()
        """
        await ws.send(json.dumps({
            'id': 202,
            'method': 'Runtime.evaluate',
            'params': {'expression': final_expr, 'returnByValue': True}
        }))
        raw = await ws.recv()
        print("Final Published Result:\n", json.dumps(json.loads(raw).get('result', {}).get('result', {}).get('value'), indent=2))

if __name__ == '__main__':
    asyncio.run(finish_rumble())
