import asyncio
import websockets
import urllib.request
import json
import time

CHROME_DEBUG_PORT = 9223

def open_new_tab(url):
    req = urllib.request.Request(f"http://127.0.0.1:{CHROME_DEBUG_PORT}/json/new?{url}", method="PUT")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

def get_tabs():
    req = urllib.request.Request(f"http://127.0.0.1:{CHROME_DEBUG_PORT}/json")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

async def cdp_call(ws, method, params=None):
    msg_id = int(time.time() * 1000) % 1000000
    await ws.send(json.dumps({'id': msg_id, 'method': method, 'params': params or {}}))
    while True:
        resp = json.loads(await ws.recv())
        if resp.get('id') == msg_id:
            return resp.get('result', {})

async def create_profile_repo():
    print("Navigating to GitHub New Repo...")
    tab = open_new_tab("https://github.com/new")
    await asyncio.sleep(4)
    
    tabs = get_tabs()
    gh_tab = next((t for t in tabs if 'github.com/new' in t.get('url', '')), None)
    if not gh_tab:
        print("Tab not found")
        return

    async with websockets.connect(gh_tab['webSocketDebuggerUrl']) as ws:
        expr = """(() => {
            const nameInput = document.querySelector('input[data-testid=\"repository-name-input\"], input[name=\"repository[name]\"]');
            if (nameInput) {
                nameInput.value = 'aiagent1510';
                nameInput.dispatchEvent(new Event('input', { bubbles: true }));
                nameInput.dispatchEvent(new Event('change', { bubbles: true }));
            }
            
            // Check public radio
            const publicRadio = document.querySelector('input[value=\"public\"]');
            if (publicRadio) publicRadio.checked = true;
            
            // Check README checkbox
            const readmeCb = document.querySelector('input[name=\"repository[auto_init]\"]');
            if (readmeCb) readmeCb.checked = true;
            
            return 'Filled repo details';
        })()"""
        res = await cdp_call(ws, 'Runtime.evaluate', {'expression': expr, 'returnByValue': True})
        print(res.get('result', {}).get('value'))
        
        await asyncio.sleep(3)
        
        # Click Create repository
        submit_expr = """(() => {
            const btn = Array.from(document.querySelectorAll('button')).find(b => (b.innerText || '').toLowerCase().includes('create repository') && !b.disabled);
            if (btn) {
                btn.click();
                return 'Clicked Create Repository';
            }
            return 'Create button disabled or not found';
        })()"""
        res2 = await cdp_call(ws, 'Runtime.evaluate', {'expression': submit_expr, 'returnByValue': True})
        print(res2.get('result', {}).get('value'))

if __name__ == '__main__':
    asyncio.run(create_profile_repo())
