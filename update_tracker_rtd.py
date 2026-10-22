import json
import csv

def update_rtd():
    with open('master_cloud_signup_tracker.json', 'r', encoding='utf-8') as f:
        d = json.load(f)

    for p in d['platforms']:
        if 'read the docs' in p['name'].lower():
            p['status'] = 'JOINED'
            p['active_tenant_url'] = 'https://home-security-guide.readthedocs.io/en/latest/'
            print('Updated tracker JSON:', p['name'], p['status'], p['active_tenant_url'])

    joined = sum(1 for p in d['platforms'] if p['status'] == 'JOINED')
    pending = sum(1 for p in d['platforms'] if p['status'] == 'PENDING')
    d['joined_count'] = joined
    d['pending_count'] = pending
    print(f"Total: {len(d['platforms'])} | Joined: {joined} | Pending: {pending}")

    with open('master_cloud_signup_tracker.json', 'w', encoding='utf-8') as f:
        json.dump(d, f, indent=2)

    with open('doc2_cloud_stack_100.csv', 'r', encoding='utf-8', errors='ignore') as f:
        rows = list(csv.DictReader(f))

    for r in rows:
        if 'read the docs' in r.get('Platform Name', '').lower():
            r['Status'] = 'JOINED'
            r['Active Tenant URL'] = 'https://home-security-guide.readthedocs.io/en/latest/'
            print('Updated CSV row:', r['Platform Name'], r['Status'])

    fieldnames = list(rows[0].keys())
    with open('doc2_cloud_stack_100.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print('Updated doc2_cloud_stack_100.csv cleanly.')

if __name__ == '__main__':
    update_rtd()
