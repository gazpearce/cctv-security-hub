import json

with open("master_1000_publishing_registry.json", "r", encoding="utf-8") as f:
    m1000 = json.load(f)

platforms = m1000.get("platforms", [])
print(f"Total platforms: {len(platforms)}")
if platforms:
    print("First platform keys:", list(platforms[0].keys()))
    print("First platform content:", json.dumps(platforms[0], indent=2))
