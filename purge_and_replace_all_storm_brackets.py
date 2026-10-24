import os
import re

REPO_DIR = r"C:\Users\Gary\github-cctv-seo"

REPLACEMENTS = [
    # Specific compound terms
    (re.compile(r"Heavy-Duty Chimney Lashing Brackets in High-Wind Valleys", re.IGNORECASE), "Heavy-Duty Chimney Lashing Brackets in High-Wind Valleys"),
    (re.compile(r"Heavy-Duty Chimney Lashing Brackets", re.IGNORECASE), "Heavy-Duty Chimney Lashing Brackets"),
    (re.compile(r"Heavy-Duty Chimney Lashing Bracket", re.IGNORECASE), "Heavy-Duty Chimney Lashing Bracket"),
    (re.compile(r"Heavy-Duty Galvanised Starlink Chimney Brackets", re.IGNORECASE), "Heavy-Duty Galvanised Starlink Chimney Brackets"),
    (re.compile(r"Heavy-Duty Galvanised Starlink Chimney Bracket", re.IGNORECASE), "Heavy-Duty Galvanised Starlink Chimney Bracket"),
    (re.compile(r"heavy-duty galvanised Starlink chimney brackets", re.IGNORECASE), "heavy-duty galvanised Starlink chimney brackets"),
    (re.compile(r"heavy-duty galvanised Starlink chimney bracket", re.IGNORECASE), "heavy-duty galvanised Starlink chimney bracket"),
    (re.compile(r"Heavy-Duty Galvanised Starlink Chimney Brackets", re.IGNORECASE), "heavy-duty galvanised Starlink chimney brackets"),
    (re.compile(r"Heavy-Duty Galvanised Starlink Chimney Bracket", re.IGNORECASE), "heavy-duty galvanised Starlink chimney bracket"),
    (re.compile(r"Heavy-Duty Starlink Chimney Brackets", re.IGNORECASE), "Heavy-Duty Starlink Chimney Brackets"),
    (re.compile(r"Heavy-Duty Starlink Chimney Bracket", re.IGNORECASE), "Heavy-Duty Starlink Chimney Bracket"),
    (re.compile(r"Heavy-Duty Starlink Chimney Brackets", re.IGNORECASE), "heavy-duty Starlink chimney brackets"),
    (re.compile(r"Heavy-Duty Starlink Chimney Bracket", re.IGNORECASE), "heavy-duty Starlink chimney bracket"),
    (re.compile(r"Heavy-Duty Starlink Chimney Brackets", re.IGNORECASE), "heavy-duty Starlink chimney brackets"),
    (re.compile(r"Heavy-Duty Starlink Chimney Bracket", re.IGNORECASE), "heavy-duty Starlink chimney bracket"),
    (re.compile(r"heavy-duty-starlink-chimney-bracket", re.IGNORECASE), "heavy-duty-starlink-chimney-bracket"),
    (re.compile(r"90mph High Winds", re.IGNORECASE), "90mph High Winds"),
    (re.compile(r"90MPH HIGH WINDS!", re.IGNORECASE), "90MPH HIGH WINDS!"),
    (re.compile(r"90MPH HIGH-WIND RATED", re.IGNORECASE), "90MPH HIGH-WIND RATED"),
]

EXTENSIONS = {'.html', '.json', '.py', '.md', '.csv', '.js', '.txt'}

updated_files = []
total_replacements = 0

for root, dirs, files in os.walk(REPO_DIR):
    # skip .git
    if ".git" in dirs:
        dirs.remove(".git")
    for file in files:
        ext = os.path.splitext(file)[1].lower()
        if ext in EXTENSIONS:
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
            except UnicodeDecodeError:
                try:
                    with open(filepath, 'r', encoding='latin1') as f:
                        content = f.read()
                except Exception:
                    continue

            new_content = content
            file_replacements = 0
            for pattern, replacement in REPLACEMENTS:
                matches = len(pattern.findall(new_content))
                if matches > 0:
                    new_content = pattern.sub(replacement, new_content)
                    file_replacements += matches

            if file_replacements > 0:
                try:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    updated_files.append((filepath, file_replacements))
                    total_replacements += file_replacements
                except Exception as e:
                    print(f"Error writing {filepath}: {e}")

print(f"=== PURGE COMPLETE ===")
print(f"Total files updated: {len(updated_files)}")
print(f"Total occurrences replaced: {total_replacements}")
for path, count in updated_files[:25]:
    rel = os.path.relpath(path, REPO_DIR)
    print(f" - {rel}: {count} replacements")
if len(updated_files) > 25:
    print(f" ... and {len(updated_files) - 25} more files.")
