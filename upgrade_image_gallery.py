import json
import re

print("Loading image_stack_manifest.json...")
with open("image_stack_manifest.json", "r", encoding="utf-8") as f:
    manifest = json.load(f)

# Map by filename and by id
manifest_by_target = {}
for img in manifest.get("images", []):
    manifest_by_target[img["filename"]] = img

print(f"Loaded {len(manifest_by_target)} images from manifest.")

with open("image-gallery.html", "r", encoding="utf-8") as f:
    html = f.read()

# Extract the existing imageDatabase JSON
db_match = re.search(r'const imageDatabase = (\{.*?\});', html, re.DOTALL)
if not db_match:
    print("Error: Could not find imageDatabase in image-gallery.html")
    exit(1)

current_db = json.loads(db_match.group(1))
print(f"Current imageDatabase has {len(current_db)} entries.")

# Enrich current_db entries with manifest metadata
for img_id, item in current_db.items():
    target = item.get("target", "")
    man = manifest_by_target.get(target)
    if not man:
        # Try matching by filename without extension or fuzzy
        for k, v in manifest_by_target.items():
            if k == item.get("local_rel_path", "").split("/")[-1]:
                man = v
                break

    if man:
        item["about"] = man.get("about_section_markdown", item.get("desc", ""))
        item["seo_tags"] = man.get("seo_tags", [])
        item["top_of_stack_google_url"] = man.get("top_of_stack_google_url", "https://drive.google.com/drive/folders/1jkTPHdni9Bki3kwNbna5d5oK2ejPJf88")
        item["top_of_stack_youtube_url"] = man.get("top_of_stack_youtube_url", "https://www.youtube.com/@CCTV.services")
        item["companion_blogger_url"] = man.get("companion_blogger_url", "https://tvandhomesecurity.blogspot.com/")
        item["money_post_url"] = man.get("money_post_url", "https://adicommunications.co.uk/news/")
    else:
        # Default topic mapping
        cat = item.get("cat", "cctv")
        if cat == "starlink":
            item["about"] = f"{item.get('title')} — Professional UK installation by Gary Pearce (ADI Communications, Direct: 07860 244 274). High-tensile stainless steel strapping, 90mph Pennine gale rated, zero brickwork drilling. Verified low-loss solid copper Cat6 cabling and 0.00% sky obstruction."
            item["seo_tags"] = ["#StarlinkInstallation", "#StarlinkUK", "#ChimneyMount", "#PennineGales", "#GaryPearce", "#ADISecurity"]
            item["top_of_stack_google_url"] = "https://drive.google.com/drive/folders/1jkTPHdni9Bki3kwNbna5d5oK2ejPJf88"
            item["top_of_stack_youtube_url"] = "https://www.youtube.com/@CCTV.services"
            item["companion_blogger_url"] = "https://tvandhomesecurity.blogspot.com/2026/10/starlink-installation-uk-chimney-mount.html"
            item["money_post_url"] = "https://adicommunications.co.uk/news/starlink-chimney-mount-vs-roof-apex-brackets/"
        elif cat == "ajax":
            item["about"] = f"{item.get('title')} — Grade 2 wireless security engineering by Gary Pearce (ADI Communications, 07860 244 274). 868MHz Jeweller frequency hopping with anti-jamming detection, 9-second photo verification, and 16-hour backup battery power."
            item["seo_tags"] = ["#AjaxAlarms", "#SmartAlarmsUK", "#Grade2Security", "#MotionCamPhOD", "#GaryPearce", "#ADISecurity"]
            item["top_of_stack_google_url"] = "https://drive.google.com/drive/folders/1jkTPHdni9Bki3kwNbna5d5oK2ejPJf88"
            item["top_of_stack_youtube_url"] = "https://www.youtube.com/@CCTV.services"
            item["companion_blogger_url"] = "https://tvandhomesecurity.blogspot.com/2026/10/ajax-smart-alarms-uk-masterclass-2026.html"
            item["money_post_url"] = "https://adicommunications.co.uk/news/ajax-wireless-alarm-grade-2-installation/"
        elif cat == "cctv":
            item["about"] = f"{item.get('title')} — Police evidence grade CCTV engineering by Gary Pearce (ADI Communications, 07860 244 274). Full BS EN 62676-4 DORI 250 px/m facial identification compliance, F1.0 ColorVu night vision, and hardwired solid copper PoE."
            item["seo_tags"] = ["#CCTVInstallation", "#HikvisionColorVu", "#PoliceEvidence", "#DORIStandards", "#GaryPearce", "#ADISecurity"]
            item["top_of_stack_google_url"] = "https://drive.google.com/drive/folders/1jkTPHdni9Bki3kwNbna5d5oK2ejPJf88"
            item["top_of_stack_youtube_url"] = "https://www.youtube.com/@CCTV.services"
            item["companion_blogger_url"] = "https://tvandhomesecurity.blogspot.com/2026/10/hikvision-colorvu-vs-infrared-cctv-4k.html"
            item["money_post_url"] = "https://adicommunications.co.uk/news/hikvision-colorvu-vs-infrared-cctv/"
        elif cat == "doorbell":
            item["about"] = f"{item.get('title')} — Smart doorbell and access engineering by Gary Pearce (ADI Communications, 07860 244 274). Hardwired 24V 30VA DIN-rail transformer upgrades and precision diamond-drilled masonry wedge fittings for historic stone and composite doors."
            item["seo_tags"] = ["#SmartDoorbell", "#RingPro2", "#ReolinkPoE", "#YorkshireStone", "#GaryPearce", "#ADISecurity"]
            item["top_of_stack_google_url"] = "https://drive.google.com/drive/folders/1jkTPHdni9Bki3kwNbna5d5oK2ejPJf88"
            item["top_of_stack_youtube_url"] = "https://www.youtube.com/@CCTV.services"
            item["companion_blogger_url"] = "https://tvandhomesecurity.blogspot.com/2026/10/how-to-get-ethernet-upstairs-without-running-cables.html"
            item["money_post_url"] = "https://adicommunications.co.uk/news/how-to-get-ethernet-upstairs-without-running-cables/"
        else:
            item["about"] = f"{item.get('title')} — Architectural TV and masonry mounting by Gary Pearce (ADI Communications, 07860 244 274). Corefix steel core fixings transferring 100kg shear load into solid masonry behind dot-and-dab drywall with 40°C thermal protection."
            item["seo_tags"] = ["#TVMounting", "#CorefixAnchors", "#SamsungTheFrame", "#OLEDThermalSafety", "#GaryPearce", "#ADISecurity"]
            item["top_of_stack_google_url"] = "https://drive.google.com/drive/folders/1jkTPHdni9Bki3kwNbna5d5oK2ejPJf88"
            item["top_of_stack_youtube_url"] = "https://www.youtube.com/@CCTV.services"
            item["companion_blogger_url"] = "https://tvandhomesecurity.blogspot.com/2026/10/tv-mounting-above-fireplaces-in-uk.html"
            item["money_post_url"] = "https://adicommunications.co.uk/news/tv-above-fireplace-safe-installation/"

# New Lightbox Modal HTML
new_modal_html = """    <!-- Modal Lightbox Dialog -->
    <div id="lightbox-modal" class="fixed inset-0 z-50 bg-black/90 backdrop-blur-md hidden items-center justify-center p-4">
        <div class="bg-darkCard border border-borderMuted max-w-5xl w-full rounded-2xl overflow-hidden shadow-2xl flex flex-col max-h-[92vh]" onclick="event.stopPropagation()">
            <!-- Modal Header -->
            <div class="p-4 border-b border-borderMuted flex items-center justify-between">
                <div class="flex items-center gap-2">
                    <span id="modal-category" class="text-xs font-mono uppercase bg-brand/20 text-brand px-2.5 py-1 rounded font-bold"></span>
                    <span id="modal-town" class="text-xs font-mono text-slate-400"></span>
                    <span class="inline-flex items-center gap-1 text-[11px] font-mono px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                        <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
                        Top-of-Stack Apex Verified
                    </span>
                </div>
                <button onclick="closeLightbox()" class="text-slate-400 hover:text-white p-1 rounded-lg hover:bg-slate-800 transition" aria-label="Close modal">
                    <svg class="w-6 h-6 fill-current" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/></svg>
                </button>
            </div>
            
            <div class="overflow-y-auto p-4 sm:p-6 space-y-6">
                <!-- Image Display -->
                <div class="bg-black rounded-xl overflow-hidden flex items-center justify-center border border-slate-800">
                    <img id="modal-img" src="" alt="" class="max-h-[48vh] w-auto object-contain">
                </div>

                <!-- Title & Tags -->
                <div>
                    <h3 id="modal-title" class="text-xl sm:text-2xl font-black text-white mb-2 tracking-tight"></h3>
                    <div id="modal-tags-container" class="flex flex-wrap gap-1.5 pt-1"></div>
                </div>

                <!-- About & Installation Forensics (Gary Pearce) -->
                <div class="bg-slate-950 p-5 rounded-xl border border-slate-800 space-y-3">
                    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-1 pb-2 border-b border-slate-800/80">
                        <div class="flex items-center gap-2">
                            <span class="w-2.5 h-2.5 rounded-full bg-[#FF5500] animate-pulse"></span>
                            <h4 class="text-xs font-mono uppercase text-[#FF5500] font-bold tracking-wider">About This Installation & Engineering Forensics</h4>
                        </div>
                        <span class="text-[11px] font-mono text-slate-400">Gary Pearce • 25+ Yrs Field Experience • £10M Insurance</span>
                    </div>
                    <div id="modal-about-content" class="text-xs sm:text-sm text-slate-300 leading-relaxed font-sans whitespace-pre-line space-y-2"></div>
                </div>

                <!-- Top of Stack Apex Google & Authority Links -->
                <div class="bg-slate-950 p-5 rounded-xl border border-slate-800 space-y-3">
                    <div class="flex items-center justify-between pb-2 border-b border-slate-800/80">
                        <h4 class="text-xs font-mono uppercase text-emerald-400 font-bold tracking-wider flex items-center gap-2">
                            <svg class="w-4 h-4 fill-current text-emerald-400" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M12.586 4.586a2 2 0 112.828 2.828l-3 3a2 2 0 01-2.828 0 1 1 0 00-1.414 1.414 4 4 0 005.656 0l3-3a4 4 0 00-5.656-5.656l-1.5 1.5a1 1 0 101.414 1.414l1.5-1.5zm-5 5a2 2 0 012.828 0 1 1 0 101.414-1.414 4 4 0 00-5.656 0l-3 3a4 4 0 105.656 5.656l1.5-1.5a1 1 0 10-1.414-1.414l-1.5 1.5a2 2 0 11-2.828-2.828l3-3z" clip-rule="evenodd"/></svg>
                            Top of Stack Apex Google & Companion Guides (DA 99–100)
                        </h4>
                        <span class="text-[11px] font-mono text-slate-400">Rule 45 Google Shield Air-Gap</span>
                    </div>
                    <p class="text-xs text-slate-400">
                        Direct verifiable authority destinations linking physical trade hardware to Google Drive Vaults, YouTube Masterclasses, and Blogger companion studies:
                    </p>
                    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-2 pt-1">
                        <a id="modal-link-drive" href="#" target="_blank" rel="noopener" class="flex items-center gap-2 px-3 py-2 rounded-lg bg-blue-500/10 hover:bg-blue-500/20 border border-blue-500/30 text-blue-300 font-mono text-xs transition">
                            <svg class="w-4 h-4 shrink-0 fill-current text-blue-400" viewBox="0 0 24 24"><path d="M19.35 10.04C18.67 6.59 15.64 4 12 4 9.11 4 6.6 5.64 5.35 8.04 2.34 8.36 0 10.91 0 14c0 3.31 2.69 6 6 6h13c2.76 0 5-2.24 5-5 0-2.64-2.05-4.78-4.65-4.96z"/></svg>
                            <span class="truncate">Google Drive (DA 100)</span>
                        </a>
                        <a id="modal-link-youtube" href="#" target="_blank" rel="noopener" class="flex items-center gap-2 px-3 py-2 rounded-lg bg-red-500/10 hover:bg-red-500/20 border border-red-500/30 text-red-300 font-mono text-xs transition">
                            <svg class="w-4 h-4 shrink-0 fill-current text-red-400" viewBox="0 0 24 24"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
                            <span class="truncate">YouTube (DA 100)</span>
                        </a>
                        <a id="modal-link-blogger" href="#" target="_blank" rel="noopener" class="flex items-center gap-2 px-3 py-2 rounded-lg bg-amber-500/10 hover:bg-amber-500/20 border border-amber-500/30 text-amber-300 font-mono text-xs transition">
                            <svg class="w-4 h-4 shrink-0 fill-current text-amber-400" viewBox="0 0 20 20"><path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z"/><path fill-rule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h6a1 1 0 100-2H7zm0 4a1 1 0 100 2h6a1 1 0 100-2H7z" clip-rule="evenodd"/></svg>
                            <span class="truncate">Blogger Hub (DA 99)</span>
                        </a>
                        <a id="modal-link-buffer" href="#" target="_blank" rel="noopener" class="flex items-center gap-2 px-3 py-2 rounded-lg bg-orange-500/10 hover:bg-orange-500/20 border border-orange-500/30 text-orange-300 font-mono text-xs transition">
                            <svg class="w-4 h-4 shrink-0 fill-current text-[#FF5500]" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-8.707l-3-3a1 1 0 00-1.414 1.414L10.586 9H7a1 1 0 100 2h3.586l-1.293 1.293a1 1 0 101.414 1.414l3-3a1 1 0 000-1.414z" clip-rule="evenodd"/></svg>
                            <span class="truncate">ADI Field Guide</span>
                        </a>
                    </div>
                    <div class="pt-3 flex flex-col sm:flex-row items-center justify-between gap-3 border-t border-slate-800 text-xs">
                        <span class="text-slate-400">Speak directly with Gary Pearce for installation and commissioning advice:</span>
                        <a href="tel:07860244274" class="px-4 py-2 rounded-lg bg-[#FF5500] hover:bg-orange-600 text-white font-mono font-bold transition flex items-center gap-2 shrink-0">
                            <svg class="w-4 h-4 fill-current" viewBox="0 0 20 20"><path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 4V3z"/></svg>
                            <span>Call Gary: 07860 244 274</span>
                        </a>
                    </div>
                </div>

                <!-- Technical Specs & Metadata -->
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs font-mono bg-slate-950 p-4 rounded-xl border border-slate-800">
                    <div>
                        <span class="text-slate-500 block mb-1">Trade Engineering Specification:</span>
                        <span id="modal-specs" class="text-slate-200 font-semibold"></span>
                    </div>
                    <div>
                        <span class="text-slate-500 block mb-1">Geographic Coordinates:</span>
                        <span id="modal-coords" class="text-slate-200"></span>
                    </div>
                    <div>
                        <span class="text-slate-500 block mb-1">Resolution & Dimensions:</span>
                        <span id="modal-dims" class="text-emerald-400"></span>
                    </div>
                    <div>
                        <span class="text-slate-500 block mb-1">Lead Engineer:</span>
                        <span class="text-slate-200">Gary Pearce (07860 244 274)</span>
                    </div>
                </div>

                <!-- Direct CDN Copy -->
                <div>
                    <label class="block text-xs font-mono text-slate-400 mb-1.5">Direct jsDelivr CDN URL (Open-Source Embed):</label>
                    <div class="flex gap-2">
                        <input id="modal-cdn-input" type="text" readonly class="flex-grow bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-xs font-mono text-slate-300 focus:outline-none">
                        <button id="modal-copy-btn" onclick="copyModalCdn()" class="bg-brand hover:bg-brandHover text-white px-4 py-2 rounded-lg text-xs font-mono font-bold transition">
                            Copy
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>"""

# Replace the modal in HTML
modal_pattern = r'<!-- Modal Lightbox Dialog -->.*?</div>\s*</div>\s*</div>\s*(?=<!-- Footer -->)'
html = re.sub(modal_pattern, new_modal_html + "\n\n    ", html, flags=re.DOTALL)

# New JS openLightbox function
new_open_lightbox = """        function openLightbox(id) {
            const item = imageDatabase[id];
            if (!item) return;

            document.getElementById('modal-img').src = item.local_rel_path;
            document.getElementById('modal-img').alt = item.alt;
            document.getElementById('modal-title').textContent = item.title;
            document.getElementById('modal-category').textContent = item.category_label;
            document.getElementById('modal-town').textContent = item.town + ', ' + item.county;
            document.getElementById('modal-specs').textContent = item.specs;
            document.getElementById('modal-coords').textContent = item.lat + '° N, ' + Math.abs(item.lon) + '° W';
            document.getElementById('modal-dims').textContent = item.width + ' × ' + item.height + ' px (' + item.file_size_kb + ' KB WebP)';
            document.getElementById('modal-cdn-input').value = item.jsdelivr_cdn_url;

            // Populate About Section
            const aboutEl = document.getElementById('modal-about-content');
            if (aboutEl) {
                aboutEl.textContent = item.about || item.desc || '';
            }

            // Populate SEO Tags
            const tagsContainer = document.getElementById('modal-tags-container');
            if (tagsContainer) {
                tagsContainer.innerHTML = '';
                const tags = item.seo_tags || [];
                tags.forEach(tag => {
                    const span = document.createElement('span');
                    span.className = 'text-[11px] font-mono px-2 py-0.5 rounded bg-white/5 border border-white/10 text-[#FF5500] font-semibold';
                    span.textContent = tag.startsWith('#') ? tag : '#' + tag;
                    tagsContainer.appendChild(span);
                });
            }

            // Populate Top of Stack Apex Links
            const linkDrive = document.getElementById('modal-link-drive');
            if (linkDrive) linkDrive.href = item.top_of_stack_google_url || 'https://drive.google.com/drive/folders/1jkTPHdni9Bki3kwNbna5d5oK2ejPJf88';

            const linkYt = document.getElementById('modal-link-youtube');
            if (linkYt) linkYt.href = item.top_of_stack_youtube_url || 'https://www.youtube.com/@CCTV.services';

            const linkBlogger = document.getElementById('modal-link-blogger');
            if (linkBlogger) linkBlogger.href = item.companion_blogger_url || 'https://tvandhomesecurity.blogspot.com/';

            const linkBuffer = document.getElementById('modal-link-buffer');
            if (linkBuffer) linkBuffer.href = item.money_post_url || 'https://adicommunications.co.uk/news/';

            const modal = document.getElementById('lightbox-modal');
            modal.classList.remove('hidden');
            modal.classList.add('flex');
            document.body.style.overflow = 'hidden';
        }"""

# Replace openLightbox function in HTML
fn_pattern = r'function openLightbox\(id\) \{.*?\n        \}'
html = re.sub(fn_pattern, new_open_lightbox, html, flags=re.DOTALL)

# Replace imageDatabase using lambda to avoid backslash escape issues
new_db_str = "const imageDatabase = " + json.dumps(current_db, ensure_ascii=False) + ";"
html = re.sub(r'const imageDatabase = \{.*?\};', lambda m: new_db_str, html, flags=re.DOTALL)

with open("image-gallery.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Successfully upgraded image-gallery.html with About sections, SEO tags, and Apex Google links!")
