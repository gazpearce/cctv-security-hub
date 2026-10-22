import json

def update_tracker():
    with open('master_cloud_signup_tracker.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Updates map
    updates = {
        "Netlify": {
            "status": "JOINED",
            "active_tenant_url": "https://app.netlify.com/start"
        },
        "Replit": {
            "status": "JOINED",
            "active_tenant_url": "https://replit.com/~"
        },
        "Sentry": {
            "status": "JOINED",
            "active_tenant_url": "https://adi-communications-ltd.sentry.io/onboarding/welcome/"
        },
        "Turso": {
            "status": "JOINED",
            "active_tenant_url": "https://app.turso.tech/aiagent1510"
        },
        "Upstash": {
            "status": "JOINED",
            "active_tenant_url": "https://console.upstash.com/home"
        },
        "MongoDB Atlas Cloud": {
            "status": "JOINED",
            "active_tenant_url": "https://account.mongodb.com/account/register/success"
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

    found_circleci = False
    for p in data['platforms']:
        name = p.get('name')
        if name in updates:
            p['status'] = updates[name]['status']
            p['active_tenant_url'] = updates[name]['active_tenant_url']
            print(f"Updated {name} -> JOINED ({p['active_tenant_url']})")
        if name == 'CircleCI':
            found_circleci = True

    if not found_circleci:
        data['platforms'].append(updates['CircleCI'])
        data['total_platforms'] = len(data['platforms'])
        print("Appended CircleCI -> JOINED (https://app.circleci.com/home)")

    # Recount joined
    joined = sum(1 for p in data['platforms'] if p.get('status') == 'JOINED')
    data['joined_count'] = joined
    print(f"\nTotal Platforms: {data['total_platforms']} | Total Joined: {joined}")

    with open('master_cloud_signup_tracker.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

if __name__ == '__main__':
    update_tracker()
