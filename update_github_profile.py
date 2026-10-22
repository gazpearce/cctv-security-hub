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

async def update_github_profile():
    print("Navigating to GitHub Profile Settings...")
    tab = open_new_tab("https://github.com/settings/profile")
    await asyncio.sleep(4)
    
    tabs = get_tabs()
    gh_tab = next((t for t in tabs if 'github.com/settings/profile' in t.get('url', '')), None)
    if not gh_tab:
        print("Settings tab not found")
        return

    async with websockets.connect(gh_tab['webSocketDebuggerUrl']) as ws:
        expr = """(() => {
            const nameInput = document.getElementById('user_profile_name');
            const bioInput = document.getElementById('user_profile_bio');
            const companyInput = document.getElementById('user_profile_company');
            const locationInput = document.getElementById('user_profile_location');
            const blogInput = document.getElementById('user_profile_blog');
            
            if (nameInput) {
                nameInput.value = 'Gary Pearce';
                nameInput.dispatchEvent(new Event('input', { bubbles: true }));
            }
            if (bioInput) {
                bioInput.value = 'Director at ADI Communications | Physical Security, Starlink Telecom & CCTV Specialist (25+ yrs). £10M Public Liability. Direct: 07860 244 274.';
                bioInput.dispatchEvent(new Event('input', { bubbles: true }));
            }
            if (companyInput) {
                companyInput.value = 'ADI Communications';
                companyInput.dispatchEvent(new Event('input', { bubbles: true }));
            }
            if (locationInput) {
                locationInput.value = 'West Yorkshire, England, UK';
                locationInput.dispatchEvent(new Event('input', { bubbles: true }));
            }
            if (blogInput) {
                blogInput.value = 'https://tvandhomesecurity.blogspot.com/';
                blogInput.dispatchEvent(new Event('input', { bubbles: true }));
            }
            
            const submitBtn = Array.from(document.querySelectorAll('button[type=submit], input[type=submit]')).find(b => (b.innerText || b.value || '').toLowerCase().includes('update profile'));
            if (submitBtn) {
                submitBtn.click();
                return 'Updated GitHub profile and clicked submit';
            }
            return 'Submit button not found';
        })()"""
        res = await cdp_call(ws, 'Runtime.evaluate', {'expression': expr, 'returnByValue': True})
        print(res.get('result', {}).get('value'))

if __name__ == '__main__':
    asyncio.run(update_github_profile())
