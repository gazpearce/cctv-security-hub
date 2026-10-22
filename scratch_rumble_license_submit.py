import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def finalize_rumble_licensing():
    tab_id = "B05DD5FD31627A501BCF11412B0DA3C8"
    async with websockets.connect(f"ws://127.0.0.1:9223/devtools/page/{tab_id}", max_size=25*1024*1024) as ws:
        expr = """
        (() => {
            // 1. Select Rumble Only licensing
            const radios = Array.from(document.querySelectorAll('input[type="radio"]'));
            const rumbleRadio = radios.find(r => r.value === 'rumble' || r.id === 'rumble' || (r.labels && Array.from(r.labels).some(l => l.innerText.includes('Rumble Only'))));
            if (rumbleRadio) {
                rumbleRadio.checked = true;
                rumbleRadio.dispatchEvent(new Event('change', { bubbles: true }));
                rumbleRadio.dispatchEvent(new MouseEvent('click', { bubbles: true }));
            }
            
            // 2. Check terms and rights
            const terms = document.getElementById('cterms');
            if (terms) {
                terms.checked = true;
                terms.dispatchEvent(new Event('change', { bubbles: true }));
            }
            const rights = document.getElementById('crights');
            if (rights) {
                rights.checked = true;
                rights.dispatchEvent(new Event('change', { bubbles: true }));
            }
            
            // 3. Click submitForm2
            const submit2 = document.getElementById('submitForm2');
            if (submit2) {
                submit2.disabled = false;
                submit2.click();
                return {
                    status: 'Clicked submitForm2',
                    rumbleChecked: rumbleRadio ? rumbleRadio.checked : false,
                    termsChecked: terms ? terms.checked : false,
                    rightsChecked: rights ? rights.checked : false
                };
            }
            return { error: 'submitForm2 not found' };
        })()
        """
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
        res = json.loads(await ws.recv())
        print("Finalize result:", json.dumps(res.get('result', {}).get('result', {}).get('value'), indent=2))
        
        # Wait 8 seconds for Rumble to process and redirect to published video URL
        print("Waiting 8 seconds for final publishing...")
        await asyncio.sleep(8)
        
        status_expr = """
        (() => {
            const links = Array.from(document.querySelectorAll('a')).map(a => a.href).filter(h => h.includes('rumble.com/v'));
            const direct = document.getElementById('direct');
            const embed = document.getElementById('embed');
            return {
                currentUrl: window.location.href,
                title: document.title,
                publishedVideoLinks: links,
                directShareUrl: direct ? direct.value : null,
                embedCode: embed ? embed.value : null,
                bodyText: document.body.innerText.slice(0, 600)
            };
        })()
        """
        await ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': status_expr, 'returnByValue': True}}))
        res2 = json.loads(await ws.recv())
        print("Published Video Status:\n", json.dumps(res2.get('result', {}).get('result', {}).get('value'), indent=2))

if __name__ == '__main__':
    asyncio.run(finalize_rumble_licensing())
