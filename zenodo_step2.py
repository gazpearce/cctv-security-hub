import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def fill_author_modal():
    tab_id = 'C8AC94E331D5E7707203F724DC068AD7'
    async with websockets.connect(f'ws://127.0.0.1:9223/devtools/page/{tab_id}') as ws:
        expr = """
        (() => {
            const modal = document.querySelector('.modal, .ui.modal, div[role="dialog"]');
            if (!modal) return 'Modal not found';
            
            // Family name
            const fam = modal.querySelector('input[name="person_or_org.family_name"]') || modal.querySelector('#person_or_org\\.family_name');
            if (fam) {
                const nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                nativeSetter.call(fam, 'Pearce');
                fam.dispatchEvent(new Event('input', { bubbles: true }));
                fam.dispatchEvent(new Event('change', { bubbles: true }));
            }
            
            // Given names
            const given = modal.querySelector('input[name="person_or_org.given_name"]') || modal.querySelector('#person_or_org\\.given_name');
            if (given) {
                const nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                nativeSetter.call(given, 'Gary');
                given.dispatchEvent(new Event('input', { bubbles: true }));
                given.dispatchEvent(new Event('change', { bubbles: true }));
            }
            
            // Affiliation
            const aff = modal.querySelector('#affiliations input') || modal.querySelector('input[placeholder*="affiliation"]') || modal.querySelector('#affiliations');
            if (aff) {
                aff.focus();
                const nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                if (nativeSetter) nativeSetter.call(aff, 'ADI Communications');
                aff.value = 'ADI Communications';
                aff.dispatchEvent(new Event('input', { bubbles: true }));
                aff.dispatchEvent(new Event('change', { bubbles: true }));
            }
            
            // Click Save
            const saveBtn = Array.from(modal.querySelectorAll('button')).find(b => b.innerText.trim() === 'Save');
            if (saveBtn) {
                saveBtn.click();
                return 'Filled author Gary Pearce and clicked Save';
            }
            return 'Save button not found in modal';
        })()
        """
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
        raw = await ws.recv()
        print('Save author result:', raw)
        
        await asyncio.sleep(2)
        
        # Check description / TinyMCE
        expr_desc = """
        (() => {
            // Set TinyMCE content if available
            if (window.tinymce && window.tinymce.activeEditor) {
                window.tinymce.activeEditor.setContent(
                    '<p><strong>Author:</strong> Gary Pearce (Lead Physical Security Engineer, ADI Communications, 07860 244 274)</p>' +
                    '<p><strong>Abstract:</strong> This technical standard and field engineering guide examines digital CCTV video evidence admissibility within England and Wales under Crown Prosecution Service (CPS) guidelines and BS EN 62676-4 DORI benchmarks. Analysis of over 100 field installations indicates 82% of consumer and legacy commercial security systems fail court identification criteria due to sub-250 px/m sensor density, motion blur at low shutter speeds, and 850nm infrared flare. We document the optical parameters, F1.0 wide-aperture sensor dynamics, solid copper Cat6 PoE transmission requirements, and tamper-resistant storage protocols required to guarantee legal admissibility.</p>' +
                    '<p><strong>Keywords:</strong> CCTV Evidence, BS EN 62676-4, DORI standard, Police Court Admissibility, Hikvision ColorVu, UK Physical Security, ADI Communications.</p>'
                );
                return 'Set TinyMCE description successfully';
            }
            return 'TinyMCE activeEditor not found';
        })()
        """
        await ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': expr_desc, 'returnByValue': True}}))
        raw2 = await ws.recv()
        print('TinyMCE result:', raw2)

if __name__ == '__main__':
    asyncio.run(fill_author_modal())
