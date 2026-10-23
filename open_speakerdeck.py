import urllib.request
import json

try:
    # Open new tab for speakerdeck
    req = urllib.request.Request('http://localhost:9223/json/new?https://speakerdeck.com/', method='PUT')
    with urllib.request.urlopen(req, timeout=5) as resp:
        data = json.loads(resp.read().decode())
    print('Opened tab:', data.get('id'), data.get('url'))
except Exception as e:
    print('Error:', e)
