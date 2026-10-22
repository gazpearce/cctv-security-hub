import os
import subprocess

surge_sites = [
    ("adi-cctv-crime-checker.surge.sh", "uk-postcode-crime-risk-checker.html"),
    ("adi-starlink-wind-calculator.surge.sh", "starlink-wind-load-calculator.html"),
    ("adi-sound-system-music.surge.sh", "music-showcase.html"),
    ("adi-cctv-dori-lens.surge.sh", "cctv-dori-lens-calculator.html"),
    ("adi-ajax-alarm-selector.surge.sh", "ajax-alarm-grade-selector.html")
]

base_dir = os.path.dirname(os.path.abspath(__file__))
dist_surge = os.path.join(base_dir, "dist_surge")
os.makedirs(dist_surge, exist_ok=True)

for domain, html_src in surge_sites:
    site_dir = os.path.join(dist_surge, domain)
    os.makedirs(site_dir, exist_ok=True)
    
    src_path = os.path.join(base_dir, html_src)
    dst_path = os.path.join(site_dir, "index.html")
    
    with open(src_path, "r", encoding="utf-8") as f_in:
        content = f_in.read()
    with open(dst_path, "w", encoding="utf-8") as f_out:
        f_out.write(content)
        
    print(f"Deploying {domain}...")
    try:
        res = subprocess.run(
            f"npx --yes surge \"{site_dir}\" {domain}",
            shell=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=True
        )
        print(f"SUCCESS: https://{domain}/")
    except subprocess.CalledProcessError as e:
        print(f"FAILED on {domain}: {e.stderr or e.stdout}")

print("Surge deployments completed!")
