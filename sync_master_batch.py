import json
import csv

def sync_all():
    with open('master_cloud_signup_tracker.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Master map of all verified joined platforms
    verified_updates = {
        "Netlify": {
            "status": "JOINED",
            "url": "https://app.netlify.com/start"
        },
        "Replit": {
            "status": "JOINED",
            "url": "https://replit.com/~"
        },
        "Turso (libSQL / SQLite Edge)": {
            "status": "JOINED",
            "url": "https://app.turso.tech/aiagent1510"
        },
        "Upstash Serverless Redis": {
            "status": "JOINED",
            "url": "https://console.upstash.com/home"
        },
        "Upstash Vector Database": {
            "status": "JOINED",
            "url": "https://console.upstash.com/home"
        },
        "Upstash QStash": {
            "status": "JOINED",
            "url": "https://console.upstash.com/home"
        },
        "MongoDB Atlas Cloud": {
            "status": "JOINED",
            "url": "https://account.mongodb.com/account/register/success"
        },
        "Prisma Data Platform": {
            "status": "JOINED",
            "url": "https://console.prisma.io/wc60cot7ebta5tscx52poatm/onboarding"
        },
        "Make.com (Integromat)": {
            "status": "JOINED",
            "url": "https://eu1.make.com/organization/9179329/dashboard"
        },
        "Kaggle Cloud Notebooks": {
            "status": "JOINED",
            "url": "https://www.kaggle.com/"
        },
        "Sentry": {
            "rank": "104",
            "name": "Sentry",
            "domain": "sentry.io",
            "da": 90,
            "category": "Cloud Telemetry & APM",
            "free_tier": "5,000 errors, 10,000 performance units/mo",
            "sso_method": "GitHub OAuth",
            "signup_url": "https://sentry.io/signup/",
            "status": "JOINED",
            "active_tenant_url": "https://adi-communications-ltd.sentry.io/onboarding/welcome/"
        },
        "CircleCI": {
            "rank": "103",
            "name": "CircleCI",
            "domain": "circleci.com",
            "da": 91,
            "category": "CI/CD & Automation",
            "free_tier": "6,000 build mins/mo free",
            "sso_method": "GitHub / Email",
            "signup_url": "https://app.circleci.com/login",
            "status": "JOINED",
            "active_tenant_url": "https://app.circleci.com/home"
        }
    }

    # Update in data['platforms']
    existing_names = set()
    for p in data['platforms']:
        name = p.get('name')
        existing_names.add(name)
        if name in verified_updates:
            p['status'] = verified_updates[name].get('status', 'JOINED')
            p['active_tenant_url'] = verified_updates[name].get('url', verified_updates[name].get('active_tenant_url', ''))
            print(f"Updated {name} -> {p['status']} ({p['active_tenant_url']})")

    for special_key in ['Sentry', 'CircleCI']:
        if special_key not in existing_names:
            data['platforms'].append(verified_updates[special_key])
            print(f"Appended {special_key} -> JOINED")

    joined_list = [p for p in data['platforms'] if p.get('status') == 'JOINED']
    data['total_platforms'] = len(data['platforms'])
    data['joined_count'] = len(joined_list)
    avg_da = sum(int(p.get('da', 0)) for p in joined_list) / len(joined_list) if joined_list else 0

    print(f"\n================ SUMMARY ================")
    print(f"Total Platforms Tracked: {data['total_platforms']}")
    print(f"Verified Joined Platforms: {len(joined_list)}")
    print(f"Average Stack DA: {avg_da:.1f}")

    with open('master_cloud_signup_tracker.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

    # Generate updated CLOUD_STACK_ONBOARDING_REPORT.md
    report_md = f"""# Master Cloud Stack Onboarding & Authority Matrix (Wave 5 Verified)
**Business**: ADI Communications / Gary Pearce (07860 244 274)  
**Total Platforms**: {data['total_platforms']} | **Verified Active Tenants**: {len(joined_list)} | **Stack Average DA**: {avg_da:.1f}  
**Architecture Rule**: Rule 45 (Google Shield Buffer & E-E-A-T Trade Invariant)

---

## 1. Verified Active Cloud Tenants ({len(joined_list)} Platforms)

| # | Platform | Category | DA | SSO Method | Verified Active Tenant / Endpoint |
|---|---|---|---|---|---|
"""
    for idx, p in enumerate(joined_list, 1):
        report_md += f"| {idx} | **{p.get('name')}** | {p.get('category')} | **{p.get('da')}** | {p.get('sso_method')} | `{p.get('active_tenant_url')}` |\n"

    report_md += """
---

## 2. Strategic Reciprocal Linking & Authority Invariants
1. **Google Shield Buffer (Rule 45)**:
   - All external cloud repos, packages, and calculators link upward to **Google Shield Blogger** (`https://tvandhomesecurity.blogspot.com/`), **Google Drive CAD Vault** (`1jkTPHdni9Bki3kwNbna5d5oK2ejPJf88`), and pillar money pages (`adicommunications.co.uk/starlink-internet-installation/`).
   - Zero raw root linking prevents algorithmic link dilution or spam triggers.
2. **Trade E-E-A-T Authority**:
   - Every cloud package embeds authentic engineering credentials: Gary Pearce, 25+ years hands-on physical security & telecom experience, £10M Public Liability Insurance, 07860 244 274.
3. **Telemetry & Multi-Cloud Ingress**:
   - Live metrics stream into Grafana Cloud (`purplemyrtle460.grafana.net`) and Sentry (`adi-communications-ltd.sentry.io`).
   - High-performance state backed by Supabase Postgres, Neon, Turso libSQL, and Upstash Redis.
"""

    with open('CLOUD_STACK_ONBOARDING_REPORT.md', 'w', encoding='utf-8') as f:
        f.write(report_md)
    print("Updated CLOUD_STACK_ONBOARDING_REPORT.md successfully.")

if __name__ == '__main__':
    sync_all()
