import json

cat = json.load(open('master_multicategory_platform_catalog.json', encoding='utf-8'))
platforms = cat.get('platforms', [])
pending = [p for p in platforms if p.get('status') != 'JOINED']
print('Total pending platforms:', len(pending))

github_oauth = [p for p in pending if 'GitHub' in str(p.get('sso_method', ''))]
print(f'Pending with GitHub OAuth ({len(github_oauth)}):')
for p in github_oauth:
    print(p.get('platform_id'), '|', p.get('name'), '|', p.get('signup_url'))
