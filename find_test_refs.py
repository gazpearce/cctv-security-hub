import os, re

repo = r"C:\Users\Gary\github-cctv-seo\tests"
patterns = [
    r"doc2_established_profiles_list",
    r"doc3_published_asset_links",
    r"master_cloud_signup_tracker",
    r"doc2_cloud_stack_100",
    r"master_profile_manifest"
]

for root, dirs, files in os.walk(repo):
    for f in files:
        if f.endswith(".py"):
            path = os.path.join(root, f)
            with open(path, "r", encoding="utf-8", errors="ignore") as fp:
                lines = fp.readlines()
            for i, line in enumerate(lines, 1):
                for p in patterns:
                    if re.search(p, line):
                        # print surrounding assertion if nearby
                        print(f"{os.path.relpath(path, repo)}:{i} [{p}] -> {line.strip()}")
