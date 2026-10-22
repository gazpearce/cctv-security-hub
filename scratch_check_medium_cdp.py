import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def check():
    ws_url = "ws://127.0.0.1:9223/devtools/page/D554E1EBFF4A9880047E634AA7A9937D"
    async with websockets.connect(ws_url) as ws:
        url = "https://medium.com/@garypearce.homesecurity/hikvision-or-dahua-honest-breakdown-after-installing-both-for-years-9ae766765cfc"
        await ws.send(json.dumps({'id': 1, 'method': 'Page.navigate', 'params': {'url': url}}))
        await ws.recv()
        await asyncio.sleep(4)
        script = """
        (() => {
            const links = Array.from(document.querySelectorAll('a')).map(a => a.href);
            return links.filter(l => l.includes('adicommunications') || l.includes('tvandhomesecurity') || l.includes('google'));
        })()
        """
        await ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': script, 'returnByValue': True}}))
        res = json.loads(await ws.recv())
        print("Outbound links in article 1:", res.get('result', {}).get('result', {}).get('value'))

if __name__ == '__main__':
    asyncio.run(check())
