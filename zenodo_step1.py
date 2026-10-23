import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def fill_zenodo_metadata():
    tab_id = 'C8AC94E331D5E7707203F724DC068AD7'
    async with websockets.connect(f'ws://127.0.0.1:9223/devtools/page/{tab_id}') as ws:
        expr = """
        (() => {
            const results = {};
            
            // 1. Set Resource Type
            const rtInput = document.querySelector('div[name="metadata.resource_type"] input.search');
            if (rtInput) {
                rtInput.focus();
                rtInput.value = 'Report';
                rtInput.dispatchEvent(new Event('input', { bubbles: true }));
                
                // Click option from dropdown if opened
                const options = Array.from(document.querySelectorAll('.visible.menu .item, .dropdown .menu .item'));
                const reportOpt = options.find(o => o.innerText.includes('Report') || o.innerText.includes('Technical note') || o.innerText.includes('Working paper'));
                if (reportOpt) {
                    reportOpt.click();
                    results.resourceType = 'Selected ' + reportOpt.innerText;
                } else {
                    results.resourceType = 'Typed Report';
                }
            }
            
            // 2. Set Title
            const titleInput = document.querySelector('input[name="metadata.title"]') || document.getElementById('metadata.title');
            if (titleInput) {
                const nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                nativeSetter.call(titleInput, 'Crown Prosecution Service (CPS) CCTV Evidence Standards & BS EN 62676-4 DORI Technical Standard Specification');
                titleInput.dispatchEvent(new Event('input', { bubbles: true }));
                titleInput.dispatchEvent(new Event('change', { bubbles: true }));
                results.title = titleInput.value;
            }
            
            // 3. Set Publication Date
            const dateInput = document.querySelector('input[name="metadata.publication_date"]') || document.getElementById('metadata.publication_date');
            if (dateInput) {
                const nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                nativeSetter.call(dateInput, '2026-10-22');
                dateInput.dispatchEvent(new Event('input', { bubbles: true }));
                dateInput.dispatchEvent(new Event('change', { bubbles: true }));
                results.publicationDate = dateInput.value;
            }
            
            // 4. Click Add Author
            const addAuthorBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Add author');
            if (addAuthorBtn) {
                addAuthorBtn.click();
                results.clickedAddAuthor = true;
            }
            
            return results;
        })()
        """
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
        raw = await ws.recv()
        val = json.loads(raw).get('result', {}).get('result', {}).get('value', {})
        print('Step 1 results:', json.dumps(val, indent=2))
        
        await asyncio.sleep(2)
        
        # Check modal for Add Author
        expr_author = """
        (() => {
            const modal = document.querySelector('.modal, .ui.modal, div[role="dialog"]');
            return {
                modalFound: !!modal,
                modalText: modal ? modal.innerText.slice(0, 500) : null,
                modalInputs: modal ? Array.from(modal.querySelectorAll('input')).map(i => ({name: i.name, id: i.id, placeholder: i.placeholder})) : []
            };
        })()
        """
        await ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': expr_author, 'returnByValue': True}}))
        raw2 = await ws.recv()
        val2 = json.loads(raw2).get('result', {}).get('result', {}).get('value', {})
        print('Modal info:', json.dumps(val2, indent=2))

if __name__ == '__main__':
    asyncio.run(fill_zenodo_metadata())
