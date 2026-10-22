import json

with open("master_profile_manifest.json", "r", encoding="utf-8") as f:
    m = json.load(f)

cs = m.get("category_stacks_11", {})
for k, v in cs.items():
    print(f"Stack {k}:")
    for field in v:
        val = v[field]
        if isinstance(val, list):
            print(f"   {field}: list of {len(val)}")
        else:
            print(f"   {field}: {val}")
