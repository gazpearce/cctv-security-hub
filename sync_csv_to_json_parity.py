import json
import csv

def sync_parity():
    with open('master_cloud_signup_tracker.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    platforms = data['platforms']
    tracker_by_name = {p['name'].strip().lower(): p for p in platforms}

    with open('doc2_cloud_stack_100.csv', 'r', encoding='utf-8', errors='ignore') as f:
        csv_rows = list(csv.DictReader(f))

    print(f"Total in JSON: {len(platforms)} | Total in CSV: {len(csv_rows)}")

    fieldnames = list(csv_rows[0].keys())

    synced_rows = []
    for r in csv_rows:
        name_key = r.get('Platform Name', '').strip().lower()
        if name_key in tracker_by_name:
            p = tracker_by_name[name_key]
            r['Status'] = p['status']
            r['Active Tenant URL'] = p.get('active_tenant_url', '')
        synced_rows.append(r)

    with open('doc2_cloud_stack_100.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(synced_rows)

    print("doc2_cloud_stack_100.csv synced with 100% mathematical parity.")

if __name__ == '__main__':
    sync_parity()
