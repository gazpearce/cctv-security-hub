import json

def generate_html():
    with open("master_100_publishing_registry.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    platforms = data["platforms"]

    # Categories list
    categories = sorted(list(set(p["category"] for p in platforms)))

    html = f'''<!DOCTYPE html>
<html lang="en-GB" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Master 100 Free Publishing & Automation Directory | ADI Communications</title>
  <meta name="description" content="Forensic directory of 100 free public publishing destinations, APIs, MCP servers, and automation routes for Google Stacking and Tier-2 authority syndication.">
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
    body {{
      background-color: #060609;
      color: #e2e8f0;
    }}
    .glass-card {{
      background: rgba(15, 15, 22, 0.75);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid rgba(255, 255, 255, 0.07);
    }}
    .glass-nav {{
      background: rgba(8, 8, 12, 0.85);
      backdrop-filter: blur(20px);
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }}
    /* Custom scrollbar */
    ::-webkit-scrollbar {{
      width: 8px;
      height: 8px;
    }}
    ::-webkit-scrollbar-track {{
      background: #08080c;
    }}
    ::-webkit-scrollbar-thumb {{
      background: #27273a;
      border-radius: 4px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
      background: #FF5500;
    }}
  </style>
</head>
<body class="font-sans antialiased min-h-screen flex flex-col selection:bg-brand-orange selection:text-white">

  <!-- Top Glass Navigation -->
  <header class="sticky top-0 z-50 glass-nav">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <a href="/" class="flex items-center space-x-2.5">
          <span class="w-8 h-8 rounded-lg bg-gradient-to-br from-brand-orange to-red-600 flex items-center justify-center font-black text-white text-sm shadow-lg shadow-orange-500/20">ADI</span>
          <span class="font-extrabold text-white tracking-tight text-base sm:text-lg">Publishing Directory</span>
        </a>
        <span class="hidden md:inline-flex text-[11px] font-mono uppercase tracking-wider px-2 py-0.5 rounded-full bg-brand-orange/10 border border-brand-orange/30 text-brand-orange">100 Endpoints</span>
      </div>
      <div class="flex items-center space-x-3">
        <a href="master_100_publishing_directory.csv" download class="inline-flex items-center space-x-2 text-xs font-mono font-semibold px-3 py-1.5 rounded-lg bg-white/5 hover:bg-white/10 border border-white/10 text-neutral-300 hover:text-white transition">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/></svg>
          <span>Export CSV</span>
        </a>
        <a href="master_100_publishing_registry.json" target="_blank" class="inline-flex items-center space-x-2 text-xs font-mono font-semibold px-3 py-1.5 rounded-lg bg-brand-orange text-white hover:bg-orange-600 shadow-md shadow-orange-500/20 transition">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"/></svg>
          <span>Raw JSON</span>
        </a>
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
          <span>Google Stacking & Parasite SEO Architecture • 2026 Edition</span>
        </div>
        <h1 class="text-3xl sm:text-5xl font-black text-white tracking-tight uppercase max-w-4xl mx-auto leading-tight">
          Master 100 Free Public <span class="text-transparent bg-clip-text bg-gradient-to-r from-brand-orange via-orange-400 to-amber-300">Publishing Destinations</span>
        </h1>
        <p class="mt-4 text-sm sm:text-base text-neutral-400 max-w-3xl mx-auto leading-relaxed">
          Forensic directory of 100 free hosted and self-hosted platforms with documented APIs, MCP servers, and automation routes. Built for <strong class="text-neutral-200">Gary Pearce / ADI Communications</strong> to power multi-tier content syndication under strict <strong class="text-brand-orange">Rule 45 Google Shield</strong> air-gapping.
        </p>

        <!-- Stats Bar -->
        <div class="mt-8 grid grid-cols-2 sm:grid-cols-4 gap-3 max-w-4xl mx-auto text-left">
          <div class="glass-card p-3 rounded-xl">
            <div class="text-[11px] font-mono text-neutral-400 uppercase">Total Platforms</div>
            <div class="text-2xl font-black text-white mt-0.5">100</div>
            <div class="text-[10px] text-neutral-500">10 Functional Categories</div>
          </div>
          <div class="glass-card p-3 rounded-xl">
            <div class="text-[11px] font-mono text-neutral-400 uppercase">Hosted Free Tiers</div>
            <div class="text-2xl font-black text-emerald-400 mt-0.5">85</div>
            <div class="text-[10px] text-neutral-500">Zero-cost deployment</div>
          </div>
          <div class="glass-card p-3 rounded-xl">
            <div class="text-[11px] font-mono text-neutral-400 uppercase">Docker / Self-Host</div>
            <div class="text-2xl font-black text-blue-400 mt-0.5">15</div>
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
              <option value="Free Hosted">Free Hosted (85)</option>
              <option value="Self-Host">Self-Host / Docker / Static (15)</option>
            </select>
          </div>

          <!-- Category Filter Pills -->
          <div class="flex flex-wrap gap-1.5 justify-center" id="categoryPills">
            <button class="cat-pill active px-3 py-1 rounded-full text-xs font-medium border bg-brand-orange border-brand-orange text-white" data-cat="ALL">All Categories (100)</button>
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
            <thead class="bg-black/40 text-neutral-400 font-mono uppercase text-[11px]">
              <tr>
                <th class="px-4 py-3.5 w-12 text-center">#</th>
                <th class="px-4 py-3.5">Platform & Category</th>
                <th class="px-4 py-3.5">Type</th>
                <th class="px-4 py-3.5">API & MCP Status</th>
                <th class="px-4 py-3.5">Automation & Auth</th>
                <th class="px-4 py-3.5">Free Limits & Links</th>
                <th class="px-4 py-3.5 text-right">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-white/5" id="tableBody">
'''

    for p in platforms:
        type_badge = "bg-emerald-500/10 text-emerald-400 border-emerald-500/20" if "Free Hosted" in p["hosting_type"] else "bg-blue-500/10 text-blue-400 border-blue-500/20"
        link_badge = "bg-purple-500/10 text-purple-300 border-purple-500/20" if "Dofollow" in p["clickable_link_support"] else "bg-neutral-800 text-neutral-400 border-neutral-700"
        mcp_color = "text-amber-300" if "MCP" in p["mcp_status"] and "None" not in p["mcp_status"] else "text-neutral-500"

        html += f'''              <tr class="platform-row hover:bg-white/[0.02] transition" 
                  data-name="{p['platform'].lower()}" 
                  data-cat="{p['category']}" 
                  data-hosting="{p['hosting_type']}"
                  data-search="{p['platform'].lower()} {p['category'].lower()} {p['automation_route'].lower()} {p['mcp_status'].lower()}">
                <td class="px-4 py-4 text-center font-mono text-neutral-500">{p['id']}</td>
                <td class="px-4 py-4">
                  <div class="font-bold text-white text-sm flex items-center space-x-2">
                    <a href="{p['homepage_url']}" target="_blank" rel="noopener noreferrer" class="hover:text-brand-orange transition flex items-center space-x-1">
                      <span>{p['platform']}</span>
                      <svg class="w-3 h-3 opacity-60" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg>
                    </a>
                  </div>
                  <div class="text-[11px] text-neutral-400 mt-0.5">{p['category']}</div>
                </td>
                <td class="px-4 py-4 whitespace-nowrap">
                  <span class="inline-flex px-2 py-0.5 rounded text-[10px] font-mono border {type_badge}">{p['hosting_type']}</span>
                </td>
                <td class="px-4 py-4">
                  <div class="text-xs">
                    <a href="{p['api_doc_url']}" target="_blank" rel="noopener noreferrer" class="text-brand-orange hover:underline font-mono inline-flex items-center space-x-1">
                      <span>API Docs</span>
                      <svg class="w-2.5 h-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
                    </a>
                  </div>
                  <div class="text-[11px] {mcp_color} font-mono mt-0.5">{p['mcp_status']}</div>
                </td>
                <td class="px-4 py-4">
                  <div class="text-neutral-200 text-xs font-mono">{p['automation_route']}</div>
                  <div class="text-[11px] text-neutral-400 mt-0.5">Auth: <span class="text-neutral-300 font-mono">{p['auth_type']}</span></div>
                </td>
                <td class="px-4 py-4">
                  <div class="text-neutral-300 text-xs">{p['free_tier_limits']}</div>
                  <div class="mt-1 flex items-center space-x-1.5">
                    <span class="inline-flex px-1.5 py-0.5 rounded text-[9px] font-mono border {link_badge}">{p['clickable_link_support']}</span>
                    <span class="text-[10px] text-neutral-400">Public: {p['public_page_support']}</span>
                  </div>
                </td>
                <td class="px-4 py-4 text-right whitespace-nowrap">
                  <a href="{p['api_doc_url']}" target="_blank" rel="noopener noreferrer" class="inline-flex items-center space-x-1 px-2.5 py-1 rounded bg-white/5 hover:bg-white/10 text-neutral-300 hover:text-white border border-white/10 text-[11px] font-mono transition">
                    <span>Docs</span>
                  </a>
                </td>
              </tr>
'''

    html += '''            </tbody>
          </table>
        </div>
        <div class="p-4 bg-black/40 border-t border-white/5 flex items-center justify-between text-xs text-neutral-400">
          <div id="resultsCount">Showing 100 of 100 platforms</div>
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
            All 100 endpoints must link exclusively into Tier-2 Google Shield assets:
            <br>• <strong>Blogger DA 99:</strong> <code>tvandhomesecurity.blogspot.com</code>
            <br>• <strong>Drive DA 100:</strong> <code>1jkTPHdni9Bki3kwNbna5d5oK2ejPJf88</code>
            <br>• <strong>YouTube DA 100:</strong> <code>@CCTV.services</code>
            <br>• <strong>Buffer Guides:</strong> <code>/news/</code> subfolder posts only.
            <br><span class="text-red-400 font-bold">ZERO raw root links</span> to <code>adicommunications.co.uk</code>.
          </p>
        </div>
        <div class="glass-card p-6 rounded-2xl border border-white/10">
          <div class="w-8 h-8 rounded-lg bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400 font-bold text-sm mb-4">02</div>
          <h3 class="text-base font-bold text-white">First Tier Automation Group</h3>
          <p class="mt-2 text-xs text-neutral-400 leading-relaxed">
            The 8 highest authority platforms to automate first with n8n and Python:
            <br>• <strong>Blogger + Google Drive</strong> (Google Tier 1)
            <br>• <strong>GitHub Pages + GitLab Pages</strong> (Git/CI Microsites)
            <br>• <strong>Internet Archive</strong> (Permanent Whitepapers & Media)
            <br>• <strong>YouTube</strong> (1080p Video Masterclasses)
            <br>• <strong>Pinterest</strong> (Infographic & Dofollow Visuals)
            <br>• <strong>Hugging Face + Zenodo</strong> (Datasets & DOIs)
          </p>
        </div>
        <div class="glass-card p-6 rounded-2xl border border-white/10">
          <div class="w-8 h-8 rounded-lg bg-purple-500/10 border border-purple-500/30 flex items-center justify-center text-purple-400 font-bold text-sm mb-4">03</div>
          <h3 class="text-base font-bold text-white">LetMePost & MCP Orchestration</h3>
          <p class="mt-2 text-xs text-neutral-400 leading-relaxed">
            • <strong>LetMePost.dev:</strong> Open-source social publishing API with native Model Context Protocol support (50 free posts/mo).
            <br>• <strong>API Atlas:</strong> Searchable catalogue for live MCP servers.
            <br>• <strong>Docker n8n:</strong> Executes workflows in parallel via <code>n8n_master_multistack_workflow.json</code>.
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
        Protected by Rule 45 Google Shield • 100% Validated Directory
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

    function filterTable() {
      const query = searchInput.value.toLowerCase().trim();
      const hosting = hostingFilter.value;
      let visible = 0;

      rows.forEach(row => {
        const searchData = row.getAttribute('data-search');
        const cat = row.getAttribute('data-cat');
        const host = row.getAttribute('data-hosting');

        const matchesQuery = query === '' || searchData.includes(query);
        const matchesCat = currentCategory === 'ALL' || cat === currentCategory;
        const matchesHosting = hosting === 'ALL' || 
          (hosting === 'Free Hosted' && host.includes('Free Hosted')) ||
          (hosting === 'Self-Host' && (host.includes('Self-Host') || host.includes('Static')));

        if (matchesQuery && matchesCat && matchesHosting) {
          row.style.display = '';
          visible++;
        } else {
          row.style.display = 'none';
        }
      });

      resultsCount.textContent = `Showing ${visible} of 100 platforms`;
    }

    searchInput.addEventListener('input', filterTable);
    hostingFilter.addEventListener('change', filterTable);

    categoryPills.forEach(pill => {
      pill.addEventListener('click', () => {
        categoryPills.forEach(p => {
          p.classList.remove('bg-brand-orange', 'border-brand-orange', 'text-white');
          p.classList.add('bg-white/5', 'border-white/10', 'text-neutral-300');
        });
        pill.classList.remove('bg-white/5', 'border-white/10', 'text-neutral-300');
        pill.classList.add('bg-brand-orange', 'border-brand-orange', 'text-white');

        currentCategory = pill.getAttribute('data-cat');
        filterTable();
      });
    });
  </script>
</body>
</html>
'''

    with open("publishing-directory.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("Generated publishing-directory.html successfully.")

if __name__ == "__main__":
    generate_html()
