import json

with open('master_cloud_signup_tracker.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

pending = [p for p in data['platforms'] if p.get('status') == 'PENDING']
print(f"Total pending: {len(pending)}")
pending.sort(key=lambda x: int(x.get('da', 0)), reverse=True)
for p in pending[:20]:
    name = p.get('name')
    da = p.get('da')
    cat = p.get('category')
    sso = p.get('sso_method')
    url = p.get('signup_url')
    print(f"- {name} (DA {da}) [{cat}] | SSO: {sso} | {url}")
