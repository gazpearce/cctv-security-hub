import os
import re

root_dir = r"C:\Users\Gary\github-cctv-seo"
fixed_count = 0

# Map calculators to their corresponding /news/ buffer post or Google Shield
calculator_buffer_map = {
    "ethernet-upstairs-calculator.html": "https://adicommunications.co.uk/news/how-to-get-ethernet-upstairs-without-running-cables/",
    "tv-fireplace-thermal-safety-calculator.html": "https://adicommunications.co.uk/news/tv-above-fireplace-safe-installation/",
    "starlink-obstruction-windload-calculator.html": "https://adicommunications.co.uk/news/starlink-chimney-mount-vs-roof-apex/",
    "starlink-vs-fibre-speed-cost-analyzer.html": "https://adicommunications.co.uk/news/starlink-chimney-mount-vs-roof-apex/",
    "starlink-roof-chimney-quiz.html": "https://adicommunications.co.uk/news/starlink-chimney-mount-vs-roof-apex/",
    "ajax-alarm-grade-selector.html": "https://adicommunications.co.uk/news/ajax-wireless-alarm-grade-2-installation/",
    "ajax-system-builder.html": "https://adicommunications.co.uk/news/ajax-wireless-alarm-grade-2-installation/",
    "ajax-wireless-range-calculator.html": "https://adicommunications.co.uk/news/ajax-wireless-alarm-grade-2-installation/",
    "cctv-dori-lens-calculator.html": "https://tvandhomesecurity.blogspot.com/",
    "cctv-storage-bandwidth-calculator.html": "https://tvandhomesecurity.blogspot.com/",
    "garden-office-wifi-bridge-calculator.html": "https://adicommunications.co.uk/news/how-to-get-ethernet-upstairs-without-running-cables/",
    "poe-voltage-drop-calculator.html": "https://tvandhomesecurity.blogspot.com/",
    "uk-postcode-crime-risk-checker.html": "https://tvandhomesecurity.blogspot.com/",
    "image-gallery.html": "https://tvandhomesecurity.blogspot.com/"
}

for f in os.listdir(root_dir):
    if f.endswith((".html", ".xml", ".json")):
        p = os.path.join(root_dir, f)
        with open(p, "r", encoding="utf-8") as fp:
            content = fp.read()

        # Find target replacement for this file
        shield_target = calculator_buffer_map.get(f, "https://tvandhomesecurity.blogspot.com/")
        
        # Replace raw root domain occurrences: "https://adicommunications.co.uk/" or "https://adicommunications.co.uk"
        # Only when not followed by news/, assets/, or feed
        def replacer(m):
            global fixed_count
            fixed_count += 1
            return shield_target

        pattern = re.compile(r'https?://(?:www\.)?adicommunications\.co\.uk/?(?=[\"\',;>\s])')
        new_content = pattern.sub(replacer, content)

        if new_content != content:
            with open(p, "w", encoding="utf-8") as fp:
                fp.write(new_content)
            print(f"Patched Rule 45 in: {f} -> {shield_target}")

print(f"Total replacements made: {fixed_count}")
