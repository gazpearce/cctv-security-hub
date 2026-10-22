import json, csv

# 1. Load current master_cloud_signup_tracker.json
with open('master_cloud_signup_tracker.json', 'r', encoding='utf-8') as f:
    tracker = json.load(f)

platforms = tracker['platforms']

# Define verified updates
updates = {
    "2": {  # Cloudflare Pages
        "status": "JOINED",
        "active_tenant_url": "https://gary-pearce-home-services.pages.dev/"
    },
    "28": {  # Google Cloud Storage (GCS)
        "status": "JOINED",
        "active_tenant_url": "https://console.cloud.google.com/storage/browser/gary-pearce-forensic-hub.appspot.com"
    },
    "29": {  # Microsoft OneDrive
        "status": "JOINED",
        "active_tenant_url": "https://onedrive.live.com/ (Local Vault: C:\\Users\\Gary\\OneDrive)"
    },
    "51": {  # Cloudflare Workers
        "status": "JOINED",
        "active_tenant_url": "https://aionui-free-ai.aiagent1510.workers.dev/"
    },
    "52": {  # Google Cloud Run
        "status": "JOINED",
        "active_tenant_url": "https://console.cloud.google.com/run?project=gary-pearce-forensic-hub"
    },
    "53": {  # Google Cloud Functions
        "status": "JOINED",
        "active_tenant_url": "https://console.cloud.google.com/functions?project=gary-pearce-forensic-hub"
    },
    "58": {  # GitHub Container Registry (GHCR)
        "status": "JOINED",
        "active_tenant_url": "https://ghcr.io/gazpearce"
    },
    "59": {  # GitLab Container Registry
        "status": "JOINED",
        "active_tenant_url": "https://gitlab.com/aiagent1510/cctv-security-hub/container_registry"
    },
    "63": {  # Google Colab Cloud
        "status": "JOINED",
        "active_tenant_url": "https://colab.research.google.com/drive/"
    },
    "73": {  # Zapier Central Cloud
        "status": "JOINED",
        "active_tenant_url": "https://zapier.com/app/dashboard (Editor: 383285081)"
    }
}

joined_count = 0
for p in platforms:
    rank = str(p.get('rank'))
    if rank in updates:
        p['status'] = updates[rank]['status']
        p['active_tenant_url'] = updates[rank]['active_tenant_url']
    if p.get('status', '').upper() == 'JOINED':
        joined_count += 1

tracker['joined_count'] = joined_count
tracker['total_platforms'] = len(platforms)

with open('master_cloud_signup_tracker.json', 'w', encoding='utf-8') as f:
    json.dump(tracker, f, indent=2)

print(f"Updated master_cloud_signup_tracker.json: {joined_count} joined out of {len(platforms)}")

# 2. Update doc2_cloud_stack_100.csv with Status and Active Tenant URL
platform_by_rank = {str(p.get('rank')): p for p in platforms}

with open('doc2_cloud_stack_100.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    rows = list(reader)

header = rows[0]
has_status = "Status" in header
has_tenant = "Active Tenant URL" in header

new_header = list(header)
if not has_status:
    new_header.append("Status")
if not has_tenant:
    new_header.append("Active Tenant URL")

new_rows = [new_header]
for row in rows[1:]:
    if not row: continue
    rank = str(row[0]).strip()
    p_info = platform_by_rank.get(rank, {})
    status = p_info.get('status', 'PENDING')
    tenant = p_info.get('active_tenant_url', '')
    
    new_row = list(row)
    if not has_status and not has_tenant:
        new_row.extend([status, tenant])
    elif has_status and not has_tenant:
        status_idx = new_header.index("Status")
        new_row[status_idx] = status
        new_row.append(tenant)
    else:
        status_idx = new_header.index("Status")
        tenant_idx = new_header.index("Active Tenant URL")
        new_row[status_idx] = status
        new_row[tenant_idx] = tenant
    new_rows.append(new_row)

with open('doc2_cloud_stack_100.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(new_rows)

print(f"Updated doc2_cloud_stack_100.csv with verified status and tenant URLs ({len(new_rows)-1} rows).")
