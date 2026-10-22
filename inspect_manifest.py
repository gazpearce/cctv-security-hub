import json

with open("master_profile_manifest.json", "r", encoding="utf-8") as f:
    m = json.load(f)

cs = m.get("category_stacks_11", {})
for k, v in cs.items():
    print(f"{k}: id={v.get('id')} name='{v.get('name')}' apex='{v.get('apex_url')}' agent='{v.get('agent')}'")
