import json

def generate_html():
    with open("master_1000_publishing_registry.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    platforms = data["platforms"]
    total_count = len(platforms)

    # Categories list
    categories = sorted(list(set(p["category"] for p in platforms)))

    hosted_count = sum(1 for p in platforms if "Free Hosted" in p["hosting_type"])
    selfhost_count = sum(1 for p in platforms if "Self-Host" in p["hosting_type"] or "Docker" in p["hosting_type"])

    html = f'''<!DOCTYPE html>
<html lang="en-GB" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Master 1,000 Free Publishing & Automation Directory | ADI Communications</title>
  <meta name="description" content="Forensic directory of 1,000 free public publishing destinations, APIs, MCP servers, and automation routes for Google Stacking and Tier-2 authority syndication.">
  <meta name="robots" content="index, follow">
  <!-- Tailwind CSS -->
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
  <script>
    tailwind.config = {{
      theme: {{
        extend: {{
          fontFamily: {{
            sans: ['"Plus Jakarta Sans"', 'sans-serif'],
            mono: ['"JetBrains Mono"', 'monospace']
          }},
          colors: {{
            brand: {{
              orange: '#FF5500',
              glow: 'rgba(255, 85, 0, 0.15)',
              dark: '#08080c',
              card: 'rgba(18, 18, 26, 0.85)',
              border: 'rgba(255, 255, 255, 0.08)'
            }}
          }}
        }}
      }}
    }}
  </script>
  <style>
    body {{ background: #08080c; color: #e2e8f0; font-family: 'Plus Jakarta Sans', sans-serif; }}
    .glass-card {{ background: rgba(18, 18, 26, 0.85); backdrop-filter: blur(16px); border: 1px solid rgba(255, 255, 255, 0.08); }}
    .brand-glow {{ box-shadow: 0 0 35px -5px rgba(255, 85, 0, 0.25); }}
    .custom-scrollbar::-webkit-scrollbar {{ width: 6px; height: 6px; }}
    .custom-scrollbar::-webkit-scrollbar-track {{ background: #0c0c14; }}
    .custom-scrollbar::-webkit-scrollbar-thumb {{ background: #262638; border-radius: 3px; }}
  </style>
</head>
<body class="min-h-screen flex flex-col selection:bg-brand-orange selection:text-white">

  <!-- Top Sticky Navigation -->
  <header class="sticky top-0 z-50 glass-card border-b border-white/5 bg-[#08080c]/90 backdrop-blur-md">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <a href="https://gary-pearce-forensic-hub.web.app/" class="flex items-center space-x-2">
          <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-brand-orange to-amber-500 flex items-center justify-center font-black text-white text-base shadow-lg">
            GP
          </div>
          <div>
            <span class="font-extrabold text-white text-sm tracking-tight block">ADI Communications</span>
            <span class="text-[10px] text-neutral-400 font-mono tracking-wider uppercase block">Master 1,000 Publishing Directory</span>
          </div>
        </a>
      </div>

      <nav class="hidden md:flex items-center space-x-6 text-xs font-medium text-neutral-300">
        <a href="property-asset-tracker.html" class="hover:text-brand-orange transition">Property Tracker</a>
        <a href="public_backlink_ledger.html" class="hover:text-brand-orange transition">Backlink Ledger</a>
        <a href="doc1_route_domains_directory.csv" download class="hover:text-brand-orange transition">Download CSV ({total_count})</a>
        <a href="master_1000_publishing_registry.json" download class="hover:text-brand-orange transition">Download JSON</a>
        <a href="image-gallery.html" class="hover:text-brand-orange transition">Trade Gallery</a>
      </nav>

      <div class="flex items-center space-x-3">
        <span class="inline-flex items-center space-x-1 px-2.5 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-mono">
          <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping"></span>
          <span>Rule 45 Air-Gap PASS</span>
        </span>
        <a href="tel:07860244274" class="hidden sm:inline-flex items-center text-xs font-mono font-bold px-3 py-1.5 rounded-lg bg-neutral-900 border border-neutral-700 text-neutral-200 hover:border-brand-orange hover:text-brand-orange transition">
          07860 244 274
        </a>
      </div>
    </div>
  </header>

  <!-- Hero Section -->
  <main class="flex-grow">
    <section class="relative pt-12 pb-8 overflow-hidden">
      <!-- Glow ambient -->
      <div class="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[300px] bg-brand-orange/10 blur-[120px] rounded-full pointer-events-none"></div>

      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 text-center">
        <div class="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-white/5 border border-white/10 text-[11px] font-mono text-neutral-300 mb-4">
          <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span>Google Stacking & Parasite SEO Architecture • 2026 Master Edition</span>
        </div>
        <h1 class="text-3xl sm:text-5xl font-black text-white tracking-tight uppercase max-w-4xl mx-auto leading-tight">
          Master 1,000 Free Public <span class="text-transparent bg-clip-text bg-gradient-to-r from-brand-orange via-orange-400 to-amber-300">Publishing Destinations</span>
        </h1>
        <p class="mt-4 text-sm sm:text-base text-neutral-400 max-w-3xl mx-auto leading-relaxed">
          The ultimate master directory of {total_count} verified free hosted and self-hosted platforms across 10 functional categories with documented APIs, MCP servers, and automation routes. Built for <strong class="text-neutral-200">Gary Pearce / ADI Communications</strong> under strict <strong class="text-brand-orange">Rule 45 Google Shield</strong> air-gapping.
        </p>

        <!-- Stats Bar -->
        <div class="mt-8 grid grid-cols-2 sm:grid-cols-4 gap-3 max-w-4xl mx-auto text-left">
          <div class="glass-card p-3 rounded-xl">
            <div class="text-[11px] font-mono text-neutral-400 uppercase">Total Platforms</div>
            <div class="text-2xl font-black text-white mt-0.5">{total_count}</div>
            <div class="text-[10px] text-neutral-500">10 Functional Categories</div>
          </div>
          <div class="glass-card p-3 rounded-xl">
            <div class="text-[11px] font-mono text-neutral-400 uppercase">Hosted Free Tiers</div>
            <div class="text-2xl font-black text-emerald-400 mt-0.5">{hosted_count}</div>
            <div class="text-[10px] text-neutral-500">Zero-cost deployment</div>
          </div>
          <div class="glass-card p-3 rounded-xl">
            <div class="text-[11px] font-mono text-neutral-400 uppercase">Docker / Self-Host</div>
            <div class="text-2xl font-black text-blue-400 mt-0.5">{selfhost_count}</div>
            <div class="text-[10px] text-neutral-500">FOSS Self-hosted infra</div>
          </div>
          <div class="glass-card p-3 rounded-xl">
            <div class="text-[11px] font-mono text-neutral-400 uppercase">Rule 45 Google Shield</div>
            <div class="text-2xl font-black text-brand-orange mt-0.5">100%</div>
            <div class="text-[10px] text-neutral-500">0 Raw Root Links</div>
          </div>
        </div>

        <!-- Search and Filter Bar -->
        <div class="mt-8 max-w-5xl mx-auto space-y-4">
          <div class="flex flex-col sm:flex-row gap-3">
            <div class="relative flex-grow">
              <svg class="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-neutral-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
              <input type="text" id="searchInput" placeholder="Search platforms, APIs, automation routes, or MCP tools..." class="w-full pl-10 pr-4 py-2.5 rounded-xl bg-white/[0.04] border border-white/10 text-white placeholder-neutral-500 text-sm focus:outline-none focus:border-brand-orange transition">
            </div>
            <select id="hostingFilter" class="px-3.5 py-2.5 rounded-xl bg-[#0f0f16] border border-white/10 text-neutral-300 text-sm focus:outline-none focus:border-brand-orange">
              <option value="ALL">All Hosting Types</option>
              <option value="Free Hosted">Free Hosted ({hosted_count})</option>
              <option value="Self-Host">Self-Host / Docker ({selfhost_count})</option>
            </select>
          </div>

          <!-- Category Filter Pills -->
          <div class="flex flex-wrap gap-1.5 justify-center" id="categoryPills">
            <button class="cat-pill active px-3 py-1 rounded-full text-xs font-medium border bg-brand-orange border-brand-orange text-white" data-cat="ALL">All Categories ({total_count})</button>
'''
    for cat in categories:
        count = sum(1 for p in platforms if p["category"] == cat)
        html += f'''            <button class="cat-pill px-3 py-1 rounded-full text-xs font-medium border bg-white/5 border-white/10 text-neutral-300 hover:border-white/20 transition" data-cat="{cat}">{cat} ({count})</button>\n'''

    html += '''          </div>
        </div>
      </div>
    </section>

    <!-- Table Section -->
    <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-16">
      <div class="glass-card rounded-2xl overflow-hidden border border-white/10">
        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs text-neutral-300 divide-y divide-white/5" id="platformsTable">
            <thead class="bg-black/40 text-neutral-400 font-mono uppercase text-[10px] tracking-wider">
              <tr>
                <th class="px-4 py-3.5 text-center">ID</th>
                <th class="px-4 py-3.5">Platform & Category</th>
                <th class="px-4 py-3.5">Type</th>
                <th class="px-4 py-3.5">API & MCP Status</th>
                <th class="px-4 py-3.5">Signup & Auth</th>
                <th class="px-4 py-3.5">Free Limits & Role</th>
                <th class="px-4 py-3.5 text-right">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-white/5" id="tableBody">
'''

    for p in platforms:
        type_badge = "bg-emerald-500/10 text-emerald-400 border-emerald-500/20" if "Free Hosted" in p["hosting_type"] else "bg-blue-500/10 text-blue-400 border-blue-500/20"
        status_badge = "bg-emerald-500/10 text-emerald-400 border-emerald-500/20" if p["join_status"] == "JOINED" else "bg-neutral-800 text-neutral-400 border-neutral-700"
        mcp_color = "text-amber-300" if "MCP" in p.get("mcp_support", "") and "None" not in p.get("mcp_support", "") else "text-neutral-500"

        html += f'''              <tr class="platform-row hover:bg-white/[0.02] transition" 
                  data-name="{p['platform_name'].lower()}" 
                  data-cat="{p['category']}" 
                  data-hosting="{p['hosting_type']}"
                  data-search="{p['platform_name'].lower()} {p['category'].lower()} {p.get('signup_oauth_method','').lower()} {p.get('mcp_support','').lower()} {p.get('stacking_role','').lower()}">
                <td class="px-4 py-4 text-center font-mono text-neutral-500">{p['platform_id']}</td>
                <td class="px-4 py-4">
                  <div class="font-bold text-white text-sm flex items-center space-x-2">
                    <a href="{p['homepage_url']}" target="_blank" rel="noopener noreferrer" class="hover:text-brand-orange transition flex items-center space-x-1">
                      <span>{p['platform_name']}</span>
                      <svg class="w-3 h-3 opacity-60" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg>
                    </a>
                    <span class="inline-flex px-1.5 py-0.2 rounded text-[9px] font-mono border {status_badge}">{p['join_status']}</span>
                  </div>
                  <div class="text-[11px] text-neutral-400 mt-0.5">{p['category']}</div>
                </td>
                <td class="px-4 py-4 whitespace-nowrap">
                  <span class="inline-flex px-2 py-0.5 rounded text-[10px] font-mono border {type_badge}">{p['hosting_type']}</span>
                </td>
                <td class="px-4 py-4">
                  <div class="text-xs">
                    <a href="{p['api_doc_url']}" target="_blank" rel="noopener noreferrer" class="text-brand-orange hover:underline font-mono inline-flex items-center space-x-1">
                      <span>API Reference</span>
                      <svg class="w-2.5 h-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
                    </a>
                  </div>
                  <div class="text-[11px] {mcp_color} font-mono mt-0.5">{p.get('mcp_support','None')}</div>
                </td>
                <td class="px-4 py-4">
                  <div class="text-neutral-200 text-xs font-mono">{p['signup_oauth_method']}</div>
                  <div class="text-[11px] text-neutral-400 mt-0.5">Handle: <span class="text-neutral-300 font-mono">{p.get('account_handle', 'unregistered')}</span></div>
                </td>
                <td class="px-4 py-4">
                  <div class="text-neutral-300 text-xs">{p['free_limits']}</div>
                  <div class="text-[11px] text-neutral-400 mt-0.5 italic">{p.get('stacking_role', '')}</div>
                </td>
                <td class="px-4 py-4 text-right whitespace-nowrap">
                  <a href="{p['homepage_url']}" target="_blank" rel="noopener noreferrer" class="inline-flex items-center space-x-1 px-2.5 py-1 rounded bg-white/5 hover:bg-white/10 text-neutral-300 hover:text-white border border-white/10 text-[11px] font-mono transition">
                    <span>Visit</span>
                  </a>
                </td>
              </tr>
'''

    html += f'''            </tbody>
          </table>
        </div>
        <div class="p-4 bg-black/40 border-t border-white/5 flex items-center justify-between text-xs text-neutral-400">
          <div id="resultsCount">Showing {total_count} of {total_count} platforms</div>
          <div class="font-mono text-[11px] text-neutral-500">Gary Pearce • ADI Communications • Rule 45 Google Shield Compliant</div>
        </div>
      </div>
    </section>

    <!-- Operational Playbook Section -->
    <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-16">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="glass-card p-6 rounded-2xl border border-white/10">
          <div class="w-8 h-8 rounded-lg bg-orange-500/10 border border-orange-500/30 flex items-center justify-center text-brand-orange font-bold text-sm mb-4">01</div>
          <h3 class="text-base font-bold text-white">Rule 45 Google Shield Air-Gap</h3>
          <p class="mt-2 text-xs text-neutral-400 leading-relaxed">
            All endpoints link exclusively into Tier-2 Google Shield assets:
            <br>• <strong>Blogger DA 99:</strong> <code>tvandhomesecurity.blogspot.com</code>
            <br>• <strong>Drive DA 100:</strong> <code>1jkTPHdni9Bki3kwNbna5d5oK2ejPJf88</code>
            <br>• <strong>YouTube DA 100:</strong> <code>@CCTV.services</code>
            <br>• <strong>Buffer Guides:</strong> <code>/news/</code> subfolder posts only.
            <br><span class="text-red-400 font-bold">ZERO raw root links</span> to <code>adicommunications.co.uk</code>.
          </p>
        </div>
        <div class="glass-card p-6 rounded-2xl border border-white/10">
          <div class="w-8 h-8 rounded-lg bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400 font-bold text-sm mb-4">02</div>
          <h3 class="text-base font-bold text-white">Priority Automation Core</h3>
          <p class="mt-2 text-xs text-neutral-400 leading-relaxed">
            The core authority platforms automated first with n8n and Python:
            <br>• <strong>Blogger + Google Drive</strong> (Google Tier 1)
            <br>• <strong>GitHub Pages + GitLab Pages</strong> (Git/CI Microsites)
            <br>• <strong>Internet Archive</strong> (Permanent Whitepapers & Media)
            <br>• <strong>YouTube</strong> (1080p Video Masterclasses)
            <br>• <strong>Pinterest + Flickr</strong> (Infographic & Visuals)
            <br>• <strong>Hugging Face + Zenodo</strong> (Datasets & DOIs)
          </p>
        </div>
        <div class="glass-card p-6 rounded-2xl border border-white/10">
          <div class="w-8 h-8 rounded-lg bg-purple-500/10 border border-purple-500/30 flex items-center justify-center text-purple-400 font-bold text-sm mb-4">03</div>
          <h3 class="text-base font-bold text-white">100-Platform Category Scale</h3>
          <p class="mt-2 text-xs text-neutral-400 leading-relaxed">
            • <strong>10 Specialized Categories:</strong> Cloud, Images, Videos, PDFs, Datasets, Code, Audio, Blogs, Social, and Docker FOSS.
            <br>• <strong>Universal OAuth:</strong> 1-click Google and GitHub sign-in.
            <br>• <strong>Docker n8n:</strong> Executes multi-stack syndication in parallel.
            <br>• <strong>Social Ban:</strong> Zero Facebook or LinkedIn automation.
          </p>
        </div>
      </div>
    </section>
  </main>

  <!-- Footer -->
  <footer class="border-t border-white/5 py-8 bg-black/60">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between text-xs text-neutral-500 gap-4">
      <div>
        <span class="text-neutral-300 font-semibold">ADI Communications</span> • Gary Pearce (25+ Years Experience • £10M Public Liability) • Direct: <a href="tel:07860244274" class="text-brand-orange hover:underline font-mono">07860 244 274</a>
      </div>
      <div class="font-mono text-[11px]">
        Protected by Rule 45 Google Shield • 100% Validated Directory ({total_count} Platforms)
      </div>
    </div>
  </footer>

  <!-- Instant Filter & Search Script -->
  <script>
    const searchInput = document.getElementById('searchInput');
    const hostingFilter = document.getElementById('hostingFilter');
    const categoryPills = document.querySelectorAll('.cat-pill');
    const rows = document.querySelectorAll('.platform-row');
    const resultsCount = document.getElementById('resultsCount');

    let currentCategory = 'ALL';

    function filterTable() {{
      const query = searchInput.value.toLowerCase().trim();
      const hosting = hostingFilter.value;
      let visible = 0;

      rows.forEach(row => {{
        const searchData = row.getAttribute('data-search') || '';
        const cat = row.getAttribute('data-cat') || '';
        const host = row.getAttribute('data-hosting') || '';

        const matchesQuery = query === '' || searchData.includes(query);
        const matchesCat = currentCategory === 'ALL' || cat === currentCategory;
        const matchesHosting = hosting === 'ALL' || 
          (hosting === 'Free Hosted' && host.includes('Free Hosted')) ||
          (hosting === 'Self-Host' && (host.includes('Self-Host') || host.includes('Docker')));

        if (matchesQuery && matchesCat && matchesHosting) {{
          row.style.display = '';
          visible++;
        }} else {{
          row.style.display = 'none';
        }}
      }});

      resultsCount.textContent = `Showing ${{visible}} of {total_count} platforms`;
    }}

    searchInput.addEventListener('input', filterTable);
    hostingFilter.addEventListener('change', filterTable);

    categoryPills.forEach(pill => {{
      pill.addEventListener('click', () => {{
        categoryPills.forEach(p => p.classList.remove('active', 'bg-brand-orange', 'border-brand-orange', 'text-white'));
        categoryPills.forEach(p => p.classList.add('bg-white/5', 'border-white/10', 'text-neutral-300'));

        pill.classList.add('active', 'bg-brand-orange', 'border-brand-orange', 'text-white');
        pill.classList.remove('bg-white/5', 'border-white/10', 'text-neutral-300');

        currentCategory = pill.getAttribute('data-cat');
        filterTable();
      }});
    }});
  </script>
</body>
</html>'''

    with open("publishing-directory.html", "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Generated publishing-directory.html successfully with {total_count} platforms.")

if __name__ == "__main__":
    generate_html()
