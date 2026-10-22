import json
import os

cat_path = 'master_multicategory_platform_catalog.json'
with open(cat_path, 'r', encoding='utf-8') as f:
    cat = json.load(f)

updated_platforms = []
newly_joined = [
    {
        'match': 'speaker deck',
        'url': 'https://speakerdeck.com/',
        'status': 'JOINED'
    },
    {
        'match': 'replicate',
        'url': 'https://replicate.com/aiagent1510',
        'status': 'JOINED'
    },
    {
        'match': 'val town',
        'url': 'https://www.val.town/u/aiagent1510',
        'status': 'JOINED'
    },
    {
        'match': 'zenodo',
        'url': 'https://zenodo.org/',
        'status': 'JOINED'
    },
    {
        'match': 'resend',
        'url': 'https://resend.com/overview',
        'status': 'JOINED'
    }
]

joined_count = 0
for p in cat.get('platforms', []):
    name_lower = p.get('name', '').lower()
    for nj in newly_joined:
        if nj['match'] in name_lower:
            p['status'] = 'JOINED'
            p['active_tenant_url'] = nj['url']
            p['failure_reason'] = None
            p['failure_detail'] = None
            joined_count += 1
            print(f"Updated {p.get('name')} to JOINED: {nj['url']}")
            break

with open(cat_path, 'w', encoding='utf-8') as f:
    json.dump(cat, f, indent=2, ensure_ascii=False)

print(f"Updated {joined_count} platforms in catalog.")
