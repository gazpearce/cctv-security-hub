import os
import re
import posixpath
import urllib.parse

root_dir = r"C:\Users\Gary\github-cctv-seo"
violations = []

ROOT_LINK_REGEX = re.compile(
    r"(?:https?:)?//(?:www\.)?adicommunications\.co\.uk\.?(?::\d+)?(?:/([^\s\"\'<>)]*)|(?=$|[?#\"'\s<>,;)\]}]))",
    re.IGNORECASE
)

def is_raw_root_violation(raw_line: str) -> bool:
    """Normalize, unquote, and check for raw root links to adicommunications.co.uk."""
    unquoted = urllib.parse.unquote(raw_line)
    for m in ROOT_LINK_REGEX.finditer(unquoted):
        path = m.group(1) or ""
        path = re.split(r"[?#]", path)[0]
        norm_path = posixpath.normpath("/" + path.lstrip("/"))
        if norm_path == "/" or norm_path in ("/index.html", "/index.htm", "/index.php"):
            return True
    return False

if __name__ == "__main__":
    for root, dirs, files in os.walk(root_dir):
        if ".git" in dirs:
            dirs.remove(".git")
        for f in files:
            if f.endswith((".html", ".json", ".csv", ".xml", ".yml", ".yaml", ".toml")):
                p = os.path.join(root, f)
                with open(p, "r", encoding="utf-8", errors="ignore") as fp:
                    for line_no, line in enumerate(fp, 1):
                        if is_raw_root_violation(line):
                            violations.append((p, line_no, line.strip()))

    if violations:
        print(f"FAILED: Found {len(violations)} raw root links:")
        for v in violations[:10]:
            print(f"{v[0]}:{v[1]} -> {v[2]}")
        exit(1)
    else:
        print("RULE 45 PASS: 100% compliant. Zero raw root links found across all files!")
        exit(0)

