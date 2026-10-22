import json
import csv

def generate_tracker_html():
    # Load Doc 1
    with open("doc1_route_domains_directory.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        doc1 = list(reader)

    # Load Doc 2
    with open("doc2_established_profiles_list.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        doc2 = list(reader)

    # Load Doc 3
    with open("doc3_published_asset_links.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        doc3 = list(reader)

    html = f'''<!DOCTYPE html>
<html lang="en-GB" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Property, Profile & Asset Link Tracker | ADI Communications</title>
  <meta name="robots" content="index, follow">
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
  <style>
    body {{ background: #060609; color: #e2e8f0; font-family: 'Plus Jakarta Sans', sans-serif; }}
    .brand-orange {{ color: #FF5500; }}
    .glass-card {{ background: rgba(15, 15, 22, 0.75); backdrop-filter: blur(16px); border: 1px solid rgba(255, 255, 255, 0.08); }}
    .tab-btn.active {{ background: #FF5500; color: white; border-color: #FF5500; }}
  </style>
</head>
<body class="min-h-screen flex flex-col p-4 sm:p-8 selection:bg-[#FF5500] selection:text-white">

  <div class="max-w-7xl mx-auto w-full flex-grow">
    <!-- Header -->
    <header class="mb-8">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div class="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-orange-500/10 border border-orange-500/30 text-xs font-mono text-[#FF5500] mb-3">
            <span class="w-2 h-2 rounded-full bg-[#FF5500] animate-pulse"></span>
            <span>Dedicated Property & Asset Tracking Engine • 3-Level Relational Hierarchy</span>
          </div>
          <h1 class="text-3xl sm:text-5xl font-black text-white uppercase tracking-tight">Property, Profile & Asset Tracker</h1>
          <p class="mt-2 text-sm text-neutral-400 max-w-3xl">
            Live operations portal mapping <strong class="text-neutral-200">{len(doc1)} Route Domains</strong>, <strong class="text-emerald-400">Established Profiles</strong>, and <strong class="text-blue-400">Published Asset Links</strong> under strict <strong class="text-brand-orange">Rule 45 Google Shield Air-Gap</strong>.
          </p>
        </div>
        <div class="flex flex-col sm:flex-row gap-2">
          <a href="doc1_route_domains_directory.csv" download class="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-white/5 hover:bg-white/10 border border-white/10 text-xs font-mono font-semibold transition">
            <span>Doc 1: Domains ({len(doc1)})</span>
          </a>
          <a href="doc2_established_profiles_list.csv" download class="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-emerald-500/10 hover:bg-emerald-500/20 border border-emerald-500/30 text-emerald-400 text-xs font-mono font-semibold transition">
            <span>Doc 2: Profiles ({len(doc2)})</span>
          </a>
          <a href="doc3_published_asset_links.csv" download class="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-[#FF5500] hover:bg-orange-600 text-white text-xs font-mono font-semibold shadow-lg shadow-orange-500/20 transition">
            <span>Doc 3: Links ({len(doc3)})</span>
          </a>
        </div>
      </div>

      <!-- Quick Metrics -->
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-6">
        <div class="glass-card p-4 rounded-xl">
          <div class="text-[11px] font-mono text-neutral-400 uppercase">Doc 1: Target Route Domains</div>
          <div class="text-2xl font-black text-white mt-1">{len(doc1)}</div>
          <div class="text-[10px] text-neutral-500">10 Functional Stacks</div>
        </div>
        <div class="glass-card p-4 rounded-xl">
          <div class="text-[11px] font-mono text-neutral-400 uppercase">Doc 2: Established Profiles</div>
          <div class="text-2xl font-black text-emerald-400 mt-1">{len(doc2)}</div>
          <div class="text-[10px] text-neutral-500">Joined & Verified Accounts</div>
        </div>
        <div class="glass-card p-4 rounded-xl">
          <div class="text-[11px] font-mono text-neutral-400 uppercase">Doc 3: Published Asset Links</div>
          <div class="text-2xl font-black text-blue-400 mt-1">{len(doc3)}</div>
          <div class="text-[10px] text-neutral-500">Photos, PDFs, Data & Tools</div>
        </div>
        <div class="glass-card p-4 rounded-xl">
          <div class="text-[11px] font-mono text-neutral-400 uppercase">Assigned AI Agent</div>
          <div class="text-xl font-bold text-[#FF5500] mt-1 font-mono">stack-property</div>
          <div class="text-[10px] text-neutral-500">State & Memory Manager</div>
        </div>
      </div>

      <!-- Navigation Tabs -->
      <div class="flex items-center space-x-2 mt-6 border-b border-white/10 pb-3">
        <button onclick="switchTab('profiles')" id="tabBtnProfiles" class="tab-btn active px-4 py-2 rounded-lg text-xs font-bold border border-white/10 transition">Level 2: Established Profiles ({len(doc2)})</button>
        <button onclick="switchTab('links')" id="tabBtnLinks" class="tab-btn px-4 py-2 rounded-lg text-xs font-bold border border-white/10 bg-white/5 text-neutral-300 hover:text-white transition">Level 3: Published Asset Links ({len(doc3)})</button>
        <button onclick="switchTab('domains')" id="tabBtnDomains" class="tab-btn px-4 py-2 rounded-lg text-xs font-bold border border-white/10 bg-white/5 text-neutral-300 hover:text-white transition">Level 1: Route Domains Directory ({len(doc1)})</button>
      </div>
    </header>

    <!-- TAB 1: ESTABLISHED PROFILES (LEVEL 2) -->
    <div id="tabProfiles" class="tab-content">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
'''

    for p in doc2:
        child_links_count = sum(1 for a in doc3 if a["parent_profile_id"] == p["profile_id"])
        html += f'''        <div class="glass-card p-5 rounded-2xl border border-white/10 hover:border-white/20 transition">
          <div class="flex items-start justify-between">
            <div>
              <span class="inline-flex px-2 py-0.5 rounded text-[10px] font-mono bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">{p['profile_id']}</span>
              <h3 class="text-lg font-bold text-white mt-1">{p['platform_name']}</h3>
              <div class="text-xs text-[#FF5500] font-mono">@{p['profile_handle']}</div>
            </div>
            <span class="px-2 py-0.5 rounded-full text-[10px] font-mono bg-blue-500/10 text-blue-400 border border-blue-500/20">{child_links_count} Assets Linked</span>
          </div>
          <p class="text-xs text-neutral-300 mt-3 leading-relaxed">{p['bio_copy']}</p>
          <div class="mt-4 pt-3 border-t border-white/5 flex items-center justify-between text-xs font-mono">
            <a href="{p['profile_live_url']}" target="_blank" rel="noopener" class="text-blue-400 hover:underline inline-flex items-center space-x-1">
              <span>View Live Profile</span>
              <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg>
            </a>
            <span class="text-neutral-500 text-[11px]">Auth: {p['auth_credentials_ref']}</span>
          </div>
        </div>
'''

    html += '''      </div>
    </div>

    <!-- TAB 2: PUBLISHED ASSET LINKS (LEVEL 3) -->
    <div id="tabLinks" class="tab-content hidden">
      <div class="glass-card rounded-2xl overflow-hidden border border-white/10">
        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs">
            <thead class="bg-black/60 text-neutral-400 font-mono uppercase text-[11px] border-b border-white/10">
              <tr>
                <th class="px-4 py-3 text-center w-12">#</th>
                <th class="px-4 py-3">Asset Title & Type</th>
                <th class="px-4 py-3">Parent Profile</th>
                <th class="px-4 py-3">Public Asset URL</th>
                <th class="px-4 py-3">Shield Target</th>
                <th class="px-4 py-3 text-center">Status</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-white/5">
'''

    for a in doc3:
        html += f'''              <tr class="hover:bg-white/[0.02] transition">
                <td class="px-4 py-3 font-mono text-neutral-500 text-center">{a['asset_id']}</td>
                <td class="px-4 py-3">
                  <div class="font-bold text-white text-sm">{a['asset_title']}</div>
                  <div class="text-[11px] text-neutral-400">{a['asset_type']}</div>
                </td>
                <td class="px-4 py-3 whitespace-nowrap">
                  <span class="inline-flex px-2 py-0.5 rounded text-[10px] font-mono bg-white/5 border border-white/10 text-neutral-300">{a['platform_name']}</span>
                </td>
                <td class="px-4 py-3 font-mono text-xs">
                  <a href="{a['asset_public_url']}" target="_blank" rel="noopener" class="text-blue-400 hover:underline break-all inline-flex items-center space-x-1">
                    <span>{a['asset_public_url']}</span>
                    <svg class="w-2.5 h-2.5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg>
                  </a>
                </td>
                <td class="px-4 py-3 font-mono text-xs text-neutral-400">
                  <a href="{a['shield_target_url']}" target="_blank" rel="noopener" class="hover:text-white hover:underline break-all">
                    {a['shield_target_url']}
                  </a>
                </td>
                <td class="px-4 py-3 text-center whitespace-nowrap">
                  <span class="inline-flex px-1.5 py-0.5 rounded text-[10px] font-mono bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">{a['verification_status']}</span>
                </td>
              </tr>
'''

    html += '''            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- TAB 3: ROUTE DOMAINS DIRECTORY (LEVEL 1) -->
    <div id="tabDomains" class="tab-content hidden">
      <div class="glass-card rounded-2xl overflow-hidden border border-white/10">
        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs">
            <thead class="bg-black/60 text-neutral-400 font-mono uppercase text-[11px] border-b border-white/10">
              <tr>
                <th class="px-4 py-3 text-center w-12">#</th>
                <th class="px-4 py-3">Platform</th>
                <th class="px-4 py-3">Category</th>
                <th class="px-4 py-3">Join Status</th>
                <th class="px-4 py-3">Auth / Signup</th>
                <th class="px-4 py-3">Free Limits</th>
                <th class="px-4 py-3 text-right">Links</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-white/5">
'''

    for d in doc1:
        status_color = "bg-emerald-500/10 text-emerald-400 border-emerald-500/20" if d['join_status'] == "JOINED" else "bg-amber-500/10 text-amber-400 border-amber-500/20"
        html += f'''              <tr class="hover:bg-white/[0.02] transition">
                <td class="px-4 py-3 font-mono text-neutral-500 text-center">{d['platform_id']}</td>
                <td class="px-4 py-3 font-bold text-white">
                  <a href="{d['homepage_url']}" target="_blank" rel="noopener" class="hover:text-[#FF5500] inline-flex items-center space-x-1">
                    <span>{d['platform_name']}</span>
                    <svg class="w-2.5 h-2.5 opacity-60" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg>
                  </a>
                </td>
                <td class="px-4 py-3 text-neutral-400 text-[11px]">{d['category']}</td>
                <td class="px-4 py-3 whitespace-nowrap">
                  <span class="inline-flex px-2 py-0.5 rounded text-[10px] font-mono border {status_color}">{d['join_status']}</span>
                </td>
                <td class="px-4 py-3 text-neutral-300 font-mono text-[11px]">{d['signup_oauth_method']}</td>
                <td class="px-4 py-3 text-neutral-400 text-xs">{d['free_limits']}</td>
                <td class="px-4 py-3 text-right whitespace-nowrap">
                  <a href="{d['api_doc_url']}" target="_blank" rel="noopener" class="px-2 py-1 rounded bg-white/5 hover:bg-white/10 border border-white/10 text-[11px] font-mono text-neutral-300 hover:text-white transition">API Docs</a>
                </td>
              </tr>
'''

    html += '''            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <footer class="mt-12 pt-6 border-t border-white/5 text-xs text-neutral-500 flex flex-col sm:flex-row items-center justify-between gap-4">
      <div>
        <span class="text-neutral-300 font-semibold">ADI Communications</span> • Gary Pearce (07860 244 274) • Managed by <code class="text-brand-orange">stack-property-agent</code>
      </div>
      <div class="font-mono text-[11px]">
        Rule 45 Google Shield Air-Gap: 100% Enforced • All Profiles Protected
      </div>
    </footer>
  </div>

  <script>
    function switchTab(tab) {
      document.querySelectorAll('.tab-btn').forEach(b => {
        b.classList.remove('active', 'bg-[#FF5500]', 'text-white');
        b.classList.add('bg-white/5', 'text-neutral-300');
      });
      document.querySelectorAll('.tab-content').forEach(c => c.classList.add('hidden'));

      if (tab === 'profiles') {
        document.getElementById('tabProfiles').classList.remove('hidden');
        document.getElementById('tabBtnProfiles').classList.add('active', 'bg-[#FF5500]', 'text-white');
        document.getElementById('tabBtnProfiles').classList.remove('bg-white/5', 'text-neutral-300');
      } else if (tab === 'links') {
        document.getElementById('tabLinks').classList.remove('hidden');
        document.getElementById('tabBtnLinks').classList.add('active', 'bg-[#FF5500]', 'text-white');
        document.getElementById('tabBtnLinks').classList.remove('bg-white/5', 'text-neutral-300');
      } else if (tab === 'domains') {
        document.getElementById('tabDomains').classList.remove('hidden');
        document.getElementById('tabBtnDomains').classList.add('active', 'bg-[#FF5500]', 'text-white');
        document.getElementById('tabBtnDomains').classList.remove('bg-white/5', 'text-neutral-300');
      }
    }
  </script>
</body>
</html>
'''

    with open("property-asset-tracker.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("Generated property-asset-tracker.html successfully.")

if __name__ == "__main__":
    generate_tracker_html()
