import os
import re
import subprocess

REPO_DIR = r"C:\Users\Gary\github-cctv-seo"

AUTHORITY_FOOTER = '''
<!-- ================= ADI COMMUNICATIONS CLOUD AUTHORITY & TRADE ENGINEERING NETWORK ================= -->
<section id="cloud-authority-network" class="border-t border-slate-800 bg-space-950/95 text-slate-300 py-12 px-4 sm:px-6 lg:px-8 font-sans mt-16">
    <div class="max-w-7xl mx-auto space-y-10">
        
        <!-- Authority Header -->
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800/80 pb-6">
            <div>
                <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-cyan-500/10 text-cyan-400 font-mono text-xs border border-cyan-500/30 mb-2">
                    <i class="fa-solid fa-network-wired"></i> UK Telecommunications & Physical Security Authority Network
                </span>
                <h3 class="text-xl sm:text-2xl font-black text-white tracking-tight">ADI Communications Open-Source Engineering Stack</h3>
                <p class="text-xs sm:text-sm text-slate-400 max-w-3xl mt-1">
                    Free, mathematically verified trade calculators, BS EN 62676-4 video surveillance models, and Pennine 90mph storm-rated mounting telemetry engineered by <strong>Gary Pearce</strong> (25+ years hands-on trade experience, £10M Public Liability Insurance).
                </p>
            </div>
            <div class="flex items-center gap-3 shrink-0">
                <a href="tel:07860244274" class="px-4 py-2.5 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-space-950 font-bold text-xs transition shadow-lg shadow-cyan-500/20 flex items-center gap-2">
                    <i class="fa-solid fa-phone"></i> Call Gary: 07860 244 274
                </a>
            </div>
        </div>

        <!-- 3-Column Authority Hub Grid -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 text-xs">
            
            <!-- Col 1: Interactive Tool Suite -->
            <div class="bg-space-900/60 p-5 rounded-2xl border border-slate-800/80 space-y-3">
                <div class="flex items-center gap-2 text-cyan-400 font-bold text-sm">
                    <i class="fa-solid fa-calculator"></i> Verified Trade Calculators
                </div>
                <ul class="space-y-2 text-slate-300">
                    <li><a href="https://gazpearce.github.io/starlink-mount-finder/" class="hover:text-cyan-400 transition flex items-center gap-1.5"><i class="fa-solid fa-satellite-dish text-slate-500"></i> Starlink Roof Mount & Obstacle Finder</a></li>
                    <li><a href="https://gazpearce.github.io/starlink-wind-load-calculator/" class="hover:text-cyan-400 transition flex items-center gap-1.5"><i class="fa-solid fa-wind text-slate-500"></i> Pennine 90mph Gale Wind Load Calculator</a></li>
                    <li><a href="https://gazpearce.github.io/uk-postcode-crime-checker/" class="hover:text-cyan-400 transition flex items-center gap-1.5"><i class="fa-solid fa-shield-halved text-slate-500"></i> UK Postcode Police Crime Risk Checker</a></li>
                    <li><a href="https://gazpearce.github.io/cctv-lens-dori-tool/" class="hover:text-cyan-400 transition flex items-center gap-1.5"><i class="fa-solid fa-video text-slate-500"></i> BS EN 62676-4 DORI Camera Distance Tool</a></li>
                    <li><a href="https://gazpearce.github.io/ajax-smart-alarms-selector/" class="hover:text-cyan-400 transition flex items-center gap-1.5"><i class="fa-solid fa-bell text-slate-500"></i> Grade 2 Ajax Wireless Alarm System Selector</a></li>
                    <li><a href="https://gazpearce.github.io/poe-voltage-drop-calculator/" class="hover:text-cyan-400 transition flex items-center gap-1.5"><i class="fa-solid fa-bolt text-slate-500"></i> Cat6 Pure Copper PoE Voltage Drop Tool</a></li>
                </ul>
            </div>

            <!-- Col 2: High-Authority Cloud Stack & Telemetry -->
            <div class="bg-space-900/60 p-5 rounded-2xl border border-slate-800/80 space-y-3">
                <div class="flex items-center gap-2 text-emerald-400 font-bold text-sm">
                    <i class="fa-solid fa-cloud"></i> Decentralized Cloud & Telemetry
                </div>
                <ul class="space-y-2 text-slate-300">
                    <li><a href="https://purplemyrtle460.grafana.net/" target="_blank" rel="noopener" class="hover:text-emerald-400 transition flex items-center gap-1.5"><i class="fa-solid fa-chart-line text-slate-500"></i> Grafana Cloud Live Telemetry Dashboards</a></li>
                    <li><a href="https://gary-pearce-forensic-hub.web.app/" target="_blank" rel="noopener" class="hover:text-emerald-400 transition flex items-center gap-1.5"><i class="fa-solid fa-fire text-slate-500"></i> Google Firebase Global Edge Hub</a></li>
                    <li><a href="https://adi-starlink-mount-finder.surge.sh/" target="_blank" rel="noopener" class="hover:text-emerald-400 transition flex items-center gap-1.5"><i class="fa-solid fa-bolt-lightning text-slate-500"></i> Surge.sh Dedicated Edge CDN</a></li>
                    <li><a href="https://github.com/gazpearce/cctv-security-hub" target="_blank" rel="noopener" class="hover:text-emerald-400 transition flex items-center gap-1.5"><i class="fa-brands fa-github text-slate-500"></i> Open-Source GitHub Repository</a></li>
                    <li><a href="https://gitlab.com/gazpearce" target="_blank" rel="noopener" class="hover:text-emerald-400 transition flex items-center gap-1.5"><i class="fa-brands fa-gitlab text-slate-500"></i> GitLab Cloud CI/CD Pipeline</a></li>
                    <li><a href="https://huggingface.co/datasets/gazpearce" target="_blank" rel="noopener" class="hover:text-emerald-400 transition flex items-center gap-1.5"><i class="fa-solid fa-brain text-slate-500"></i> Hugging Face Security Datasets</a></li>
                </ul>
            </div>

            <!-- Col 3: Research Whitepapers & Commercial Services -->
            <div class="bg-space-900/60 p-5 rounded-2xl border border-slate-800/80 space-y-3">
                <div class="flex items-center gap-2 text-orange-400 font-bold text-sm">
                    <i class="fa-solid fa-graduation-cap"></i> Research Debriefs & Commercial Services
                </div>
                <ul class="space-y-2 text-slate-300">
                    <li><a href="https://adicommunications.co.uk/starlink-internet-installation/" target="_blank" rel="noopener" class="hover:text-orange-400 font-semibold text-white transition flex items-center gap-1.5"><i class="fa-solid fa-screwdriver-wrench text-orange-400"></i> Professional UK Starlink Installation</a></li>
                    <li><a href="https://tvandhomesecurity.blogspot.com/" target="_blank" rel="noopener" class="hover:text-orange-400 transition flex items-center gap-1.5"><i class="fa-solid fa-newspaper text-slate-500"></i> ADI Technical Engineering Debriefs (UK Trade Blog)</a></li>
                    <li><a href="https://drive.google.com/drive/folders/1jkTPHdni9Bki3kwNbna5d5oK2ejPJf88" target="_blank" rel="noopener" class="hover:text-orange-400 transition flex items-center gap-1.5"><i class="fa-brands fa-google-drive text-slate-500"></i> Google Drive CAD & Engineering Whitepapers</a></li>
                    <li><a href="https://www.youtube.com/@GaryPearceADI" target="_blank" rel="noopener" class="hover:text-orange-400 transition flex items-center gap-1.5"><i class="fa-brands fa-youtube text-slate-500"></i> YouTube Field Engineering Masterclasses</a></li>
                </ul>
                <div class="pt-2 border-t border-slate-800/80 text-[11px] text-slate-400">
                    Need turnkey physical installation? Direct engineer support across Yorkshire, Lancashire & Greater Manchester.
                </div>
            </div>

        </div>

        <!-- Semantic Co-Citation & Trade E-E-A-T Block -->
        <div class="border-t border-slate-800/80 pt-6 text-[11px] text-slate-500 leading-relaxed space-y-2">
            <p>
                <strong>Engineering Citation & Attribution:</strong> All interactive models, load calculations, and impedance charts are maintained by physical installation engineer Gary Pearce for ADI Communications. Equipment conforms to British Standard BS EN 62676-4 (video surveillance), BS 6701 / BS 7671 (telecommunications and electrical cabling), and CAI benchmarked double-shielded copper standards.
            </p>
            <div class="flex flex-wrap items-center justify-between gap-4 pt-2">
                <div>
                    &copy; 2026 ADI Communications &bull; Gary Pearce &bull; 07860 244 274 &bull; £10M Public Liability Insurance.
                </div>
                <div class="flex items-center gap-3">
                    <span class="inline-block w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                    <span class="font-mono text-slate-400">Multi-Cloud Edge Sync Active</span>
                </div>
            </div>
        </div>

    </div>
</section>
<!-- ================= END ADI COMMUNICATIONS CLOUD AUTHORITY NETWORK ================= -->
'''

TARGET_FILES = [
    "starlink-mount-obstacle-finder.html",
    "starlink-tool.html",
    "starlink-wind-load-calculator.html",
    "uk-postcode-crime-risk-checker.html",
    "cctv-dori-lens-calculator.html",
    "ajax-alarm-grade-selector.html",
    "poe-voltage-drop-calculator.html",
    "starlink-vs-5g-cost-calculator.html",
    "garden-office-wifi-bridge-calculator.html",
    "smart-doorbell-transformer-calculator.html",
    "tv-fireplace-thermal-calculator.html",
    "cctv-storage-bandwidth-calculator.html",
    "poe-switch-budget-calculator.html"
]

def update_file(filename):
    path = os.path.join(REPO_DIR, filename)
    if not os.path.exists(path):
        print(f"[SKIP] File not found: {filename}")
        return False
        
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Remove existing authority network section if present
    content = re.sub(r'<!-- ================= ADI COMMUNICATIONS CLOUD AUTHORITY.*?<!-- ================= END ADI COMMUNICATIONS CLOUD AUTHORITY NETWORK ================= -->', '', content, flags=re.DOTALL)
    
    # Inject before </body> or </html>
    if "</body>" in content:
        content = content.replace("</body>", f"{AUTHORITY_FOOTER}\n</body>")
    elif "</html>" in content:
        content = content.replace("</html>", f"{AUTHORITY_FOOTER}\n</html>")
    else:
        content += f"\n{AUTHORITY_FOOTER}"
        
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"[OK] Injected Authority Network into {filename}")
    return True

def main():
    print("--- INJECTING MASTER CLOUD AUTHORITY NETWORK ---")
    for f in TARGET_FILES:
        update_file(f)
        
    print("\n--- SYNCING DIST_SURGE DIRECTORY ---")
    dist_surge = os.path.join(REPO_DIR, "dist_surge")
    os.makedirs(dist_surge, exist_ok=True)
    
    # Copy main tools into dist_surge
    import shutil
    for f in TARGET_FILES:
        src = os.path.join(REPO_DIR, f)
        if os.path.exists(src):
            dst = os.path.join(dist_surge, f)
            shutil.copy2(src, dst)
            
    # Also copy starlink-mount-obstacle-finder.html as index.html in dist_surge for the dedicated Starlink domain
    shutil.copy2(
        os.path.join(REPO_DIR, "starlink-mount-obstacle-finder.html"),
        os.path.join(dist_surge, "index.html")
    )
    print("[OK] dist_surge populated with updated tools & index.html")

if __name__ == "__main__":
    main()
