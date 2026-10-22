import json
import os

user_data = r"C:\Users\Gary\AppData\Local\Google\Chrome\User Data"
profiles = [d for d in os.listdir(user_data) if os.path.isdir(os.path.join(user_data, d)) and (d.startswith("Profile") or d == "Default")]

for p in sorted(profiles):
    pref_path = os.path.join(user_data, p, "Preferences")
    if os.path.exists(pref_path):
        try:
            with open(pref_path, "r", encoding="utf-8", errors="ignore") as f:
                data = json.load(f)
                account_info = data.get("account_info", [])
                email = account_info[0].get("email", "N/A") if account_info else "N/A"
                name = data.get("profile", {}).get("name", "N/A")
                print(f"{p}: Profile Name = '{name}', Account Email = '{email}'")
        except Exception as e:
            print(f"{p}: Error {e}")
