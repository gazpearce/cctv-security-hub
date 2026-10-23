import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def inspect_fields():
    tab_id = 'C8AC94E331D5E7707203F724DC068AD7'
    async with websockets.connect(f'ws://127.0.0.1:9223/devtools/page/{tab_id}') as ws:
        expr = """
        (() => {
            // Find inputs and dropdowns in the form
            const inputs = Array.from(document.querySelectorAll('input, select, textarea')).map(el => ({
                tag: el.tagName,
                type: el.type,
                name: el.name,
                id: el.id,
                placeholder: el.placeholder,
                ariaLabel: el.getAttribute('aria-label')
            }));
            const resourceTypeDropdown = document.querySelector('.resource-type, [name="metadata.resource_type"]');
            return {
                inputs: inputs.filter(i => i.name || i.id || i.placeholder),
                resourceTypeDropdown: resourceTypeDropdown ? resourceTypeDropdown.outerHTML.slice(0, 300) : null
            };
        })()
        """
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
        raw = await ws.recv()
        val = json.loads(raw).get('result', {}).get('result', {}).get('value', {})
        print(json.dumps(val, indent=2))

if __name__ == '__main__':
    asyncio.run(inspect_fields())
