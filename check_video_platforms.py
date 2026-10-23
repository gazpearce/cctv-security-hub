import json

with open('video_stack_registry.json', 'r', encoding='utf-8') as f:
    reg = json.load(f)

platforms = reg.get('platforms', [])
print(f"Total Video Platforms in Sovereign Registry: {len(platforms)}")

status_counts = {}
tier_counts = {}
for p in platforms:
    s = p.get('status', 'PENDING')
    status_counts[s] = status_counts.get(s, 0) + 1
    t = p.get('tier', 'Unknown')
    tier_counts[t] = tier_counts.get(t, 0) + 1

print("By Status:", status_counts)
print("By Tier:", tier_counts)

print("\n--- All 50 Video Platforms by Tier ---")
for p in platforms:
    da = str(p.get('domain_authority') or 'N/A')
    st = str(p.get('status') or 'PENDING')
    auth = str(p.get('auth_type') or 'N/A')
    print(f"{p.get('id')} | {p.get('name', ''):<28} | Tier: {p.get('tier')} | DA: {da:<3} | Status: {st:<10} | Type: {auth}")
