import glob
import os

files = sorted(glob.glob("*.html"))
print(f"Total HTML files to inspect: {len(files)}")
missing_schema = []

for f in files:
    with open(f, "r", encoding="utf-8", errors="ignore") as fp:
        content = fp.read()
    has_schema = "application/ld+json" in content
    has_meta = "name=\"description\"" in content or 'name="description"' in content
    print(f"{f:42} | Schema: {str(has_schema):5} | Meta: {str(has_meta):5}")
    if not has_schema:
        missing_schema.append(f)

print(f"\nMissing Schema count: {len(missing_schema)}")
if missing_schema:
    print("Files missing schema:", missing_schema)
