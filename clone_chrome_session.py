import os
import shutil

src_root = r"C:\Users\Gary\AppData\Local\Google\Chrome\User Data"
dst_root = r"C:\Users\Gary\.chrome_automated_agent"

os.makedirs(dst_root, exist_ok=True)

# Copy Local State
if os.path.exists(os.path.join(src_root, "Local State")):
    try:
        shutil.copy2(os.path.join(src_root, "Local State"), os.path.join(dst_root, "Local State"))
        print("[OK] Copied Local State")
    except Exception as e:
        print("[WARN] Local State copy error:", e)

# Target profile to copy: Default
src_profile = os.path.join(src_root, "Default")
dst_profile = os.path.join(dst_root, "Default")
os.makedirs(dst_profile, exist_ok=True)

# Files critical for session / cookies / logins
critical_items = [
    "Preferences", "Secure Preferences", "Network", "Cookies", "Login Data", "Web Data",
    "Storage", "Session Storage", "Local Storage", "IndexedDB"
]

for item in critical_items:
    s = os.path.join(src_profile, item)
    d = os.path.join(dst_profile, item)
    if os.path.exists(s):
        try:
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)
            print(f"[OK] Copied {item}")
        except Exception as e:
            print(f"[WARN] Failed {item}: {e}")

print("Cloning complete!")
