import os
import re

root_dir = r"C:\Users\Gary\github-cctv-seo"
violations = []

for root, dirs, files in os.walk(root_dir):
    if ".git" in dirs:
        dirs.remove(".git")
    for f in files:
        if f.endswith((".html", ".json", ".xml", ".yml", ".yaml", ".toml")):
            p = os.path.join(root, f)
            with open(p, "r", encoding="utf-8", errors="ignore") as fp:
                for line_no, line in enumerate(fp, 1):
                    # Check for direct money site root
                    if re.search(r"https?://(?:www\.)?adicommunications\.co\.uk/?[\"\'\s>]", line):
                        # Ensure it's not a /news/ or specific subpath
                        if not re.search(r"adicommunications\.co\.uk/(?:news|assets|feed)", line):
                            violations.append((p, line_no, line.strip()))

if violations:
    print(f"FAILED: Found {len(violations)} raw root links:")
    for v in violations[:10]:
        print(f"{v[0]}:{line_no} -> {v[2]}")
    exit(1)
else:
    print("RULE 45 PASS: 100% compliant. Zero raw root links found across all files!")
    exit(0)
