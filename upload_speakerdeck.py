import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def upload_speakerdeck():
    tab_id = 'C48DFADC6D68706DAF5E12B0F783F8AE'
    pdf_path = r'C:\Users\Gary\github-cctv-seo\stack_assets\documents\UK_Police_CCTV_Evidence_Admissibility_and_DORI_Standard_Guide.pdf'
    
    async with websockets.connect(f'ws://127.0.0.1:9223/devtools/page/{tab_id}') as ws:
        # Get objectId of #upload-field
        expr_find = "document.querySelector('input#upload-field')"
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': expr_find}}))
        raw = await ws.recv()
        obj_id = json.loads(raw).get('result', {}).get('result', {}).get('objectId')
        print('objectId of upload field:', obj_id)
        
        # Attach file
        await ws.send(json.dumps({
            'id': 2,
            'method': 'DOM.setFileInputFiles',
            'params': {
                'files': [pdf_path],
                'objectId': obj_id
            }
        }))
        raw2 = await ws.recv()
        print('Attached file response:', raw2)
        
        await asyncio.sleep(4)
        
        # Fill title, description, category, video URL
        expr_fill = """
        (() => {
            const title = document.querySelector('input#talk_name') || document.querySelector('input[name="talk[name]"]');
            if (title) {
                title.value = 'UK Police CCTV Evidence Admissibility & BS EN 62676-4 DORI Standard Specification';
                title.dispatchEvent(new Event('input', { bubbles: true }));
                title.dispatchEvent(new Event('change', { bubbles: true }));
            }
            
            const desc = document.querySelector('textarea#talk_description') || document.querySelector('textarea[name="talk[description]"]');
            if (desc) {
                desc.value = 'Comprehensive field engineering guide to UK digital CCTV evidence admissibility under Crown Prosecution Service (CPS) guidelines and BS EN 62676-4 DORI benchmarks (250 px/m identification).\\n\\nAuthored by Gary Pearce, Lead Engineer at ADI Communications (25+ years hands-on experience, 07860 244 274).\\n\\nPermanent CERN DOI: https://doi.org/10.5281/zenodo.23581566\\nOfficial Technical Guide: https://tvandhomesecurity.blogspot.com/';
                desc.dispatchEvent(new Event('input', { bubbles: true }));
                desc.dispatchEvent(new Event('change', { bubbles: true }));
            }
            
            // Category: Technology (usually option value 9 or similar, let's select option with text Technology)
            const cat = document.querySelector('select#talk_category_id');
            if (cat) {
                const opt = Array.from(cat.options).find(o => o.text.includes('Technology'));
                if (opt) {
                    cat.value = opt.value;
                    cat.dispatchEvent(new Event('change', { bubbles: true }));
                }
            }
            
            // Companion YouTube video
            const videoUrl = document.querySelector('input#talk_video_url');
            if (videoUrl) {
                videoUrl.value = 'https://www.youtube.com/@CCTV.services';
                videoUrl.dispatchEvent(new Event('input', { bubbles: true }));
                videoUrl.dispatchEvent(new Event('change', { bubbles: true }));
            }
            
            return {
                titleVal: title ? title.value : null,
                descVal: desc ? desc.value.slice(0, 100) : null,
                catVal: cat ? cat.value : null
            };
        })()
        """
        await ws.send(json.dumps({'id': 3, 'method': 'Runtime.evaluate', 'params': {'expression': expr_fill, 'returnByValue': True}}))
        raw3 = await ws.recv()
        val3 = json.loads(raw3).get('result', {}).get('result', {}).get('value', {})
        print('Filled metadata:', json.dumps(val3, indent=2))
        
        await asyncio.sleep(2)
        
        # Click "Save this deck" or "Save"
        expr_save = """
        (() => {
            const btn = Array.from(document.querySelectorAll('button, input[type="submit"]')).find(b => {
                const t = (b.innerText || b.value || '').trim();
                return t === 'Save this deck' || t === 'Save';
            });
            if (btn) {
                btn.click();
                return 'Clicked save button: ' + (btn.innerText || btn.value);
            }
            return 'Save button not found';
        })()
        """
        await ws.send(json.dumps({'id': 4, 'method': 'Runtime.evaluate', 'params': {'expression': expr_save, 'returnByValue': True}}))
        raw4 = await ws.recv()
        print('Save button click:', raw4)
        
        await asyncio.sleep(6)
        
        expr_after = """
        (() => {
            return {
                url: window.location.href,
                title: document.title,
                bodySnippet: document.body.innerText.slice(0, 500)
            };
        })()
        """
        await ws.send(json.dumps({'id': 5, 'method': 'Runtime.evaluate', 'params': {'expression': expr_after, 'returnByValue': True}}))
        raw5 = await ws.recv()
        val5 = json.loads(raw5).get('result', {}).get('result', {}).get('value', {})
        print('After save:', json.dumps(val5, indent=2))

if __name__ == '__main__':
    asyncio.run(upload_speakerdeck())
