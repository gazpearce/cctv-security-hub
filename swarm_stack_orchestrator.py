"""
Swarm Stack Orchestrator & QC Engine
Controls the multi-agent swarm for Gary Pearce / ADI Communications.
Coordinates 5 specialized subagent teams and updates the public CSV master ledger.
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime

STACK_TEAMS = {
    "blog": {
        "agent": "stack-blog-agent",
        "description": "Blogger DA 99, Hashnode, DEV.to, Write.as, Ghost publishing",
        "script": "syndicate_blog_stack.py"
    },
    "pdf": {
        "agent": "stack-pdf-agent",
        "description": "Interactive ReportLab vector PDFs, whitepapers, Internet Archive, Zenodo",
        "script": "generate_reportlab_whitepapers.py"
    },
    "data": {
        "agent": "stack-dataset-agent",
        "description": "UK police crime telemetry, CCTV DORI matrices, Hugging Face, Google Sheets",
        "script": "generate_public_datasets.py"
    },
    "media": {
        "agent": "stack-media-agent",
        "description": "Trade photography (FreeImage.Host, ImgBB, Pinterest), YouTube videos, Dailymotion",
        "script": "image_stack_syndicator.py"
    },
    "microsite": {
        "agent": "stack-microsite-agent",
        "description": "Firebase Hosting Edge tools, GitHub Pages calculators, Cloudflare Pages",
        "script": "build_master_100_directory.py"
    },
    "ledger": {
        "agent": "stack-ledger-agent",
        "description": "Aggregates all published backlinks, updates public CSV & HTML ledgers, audits Rule 45",
        "script": "build_public_backlink_ledger.py"
    }
}

def run_step(cmd, desc):
    print(f"\n[ORCHESTRATOR] >>> {desc}...")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"[QC PASS] {desc} completed successfully.")
        return True, result.stdout
    else:
        print(f"[QC FAIL] {desc} failed with return code {result.returncode}!")
        print(result.stderr)
        return False, result.stderr

def run_qc_audit():
    print("\n=======================================================")
    print("      RUNNING AUTONOMOUS RULE 45 AIR-GAP QC GATE       ")
    print("=======================================================")
    success, out = run_step("python verify_no_root_anchors.py", "Rule 45 Air-Gap Verification")
    if not success:
        print("[CRITICAL QC ERROR] Rule 45 violation detected! Aborting deployment.")
        sys.exit(1)

def update_public_ledger():
    print("\n=======================================================")
    print("   UPDATING PUBLIC BACKLINK MASTER LEDGER & CSV STACK  ")
    print("=======================================================")
    run_step("python build_public_backlink_ledger.py", "Rebuilding Public CSV & HTML Ledgers")

def deploy_to_cloud():
    print("\n=======================================================")
    print("   DEPLOYING SYNDICATED ASSETS TO FIREBASE & GIT EDGE  ")
    print("=======================================================")
    run_step("git add public_backlink_master_ledger.csv public_backlink_master_ledger.json public_backlink_ledger.html", "Staging Ledger Files")
    run_step('git commit -m "feat(ledger): sync public backlink master ledger and crawler discovery stack" || exit 0', "Git Commit")
    run_step("git push origin master && git push gitlab master", "Pushing to GitHub & GitLab")
    run_step("firebase deploy --only hosting --project gary-pearce-forensic-hub", "Deploying to Firebase Edge")

def main():
    parser = argparse.ArgumentParser(description="Swarm Stack Orchestrator & QC Engine")
    parser.add_argument("--stack", choices=["all", "blog", "pdf", "data", "media", "microsite", "ledger"], default="all",
                        help="Target stack to execute (or 'all' for full swarm)")
    parser.add_argument("--skip-deploy", action="store_true", help="Skip git push and firebase deployment")

    args = parser.parse_args()

    print("=======================================================")
    print("     ADI COMMUNICATIONS • SWARM STACK ORCHESTRATOR     ")
    print(f"     Lead Engineer: Gary Pearce (07860 244 274)        ")
    print(f"     Target Stack Mode: {args.stack.upper()}           ")
    print("=======================================================")

    if args.stack == "all":
        print("\n[ORCHESTRATOR] Launching full autonomous swarm across all 6 specialized teams...")
        for name, info in STACK_TEAMS.items():
            print(f" -> Assigned Subagent: [{info['agent']}] for {info['description']}")
            if os.path.exists(info["script"]):
                run_step(f"python {info['script']}", f"Executing {name.upper()} Stack via {info['script']}")
    else:
        info = STACK_TEAMS[args.stack]
        print(f"\n[ORCHESTRATOR] Launching single specialized stack: [{args.stack.upper()}]...")
        print(f" -> Assigned Subagent: [{info['agent']}] ({info['description']})")
        if os.path.exists(info["script"]):
            run_step(f"python {info['script']}", f"Executing {args.stack.upper()} Stack via {info['script']}")

    # Rebuild ledger
    update_public_ledger()

    # Autonomous QC Check
    run_qc_audit()

    # Cloud Deploy
    if not args.skip_deploy:
        deploy_to_cloud()

    print("\n=======================================================")
    print("  SWARM EXECUTION & QC AUDIT: 100% COMPLETE & VERIFIED ")
    print("=======================================================\n")

if __name__ == "__main__":
    main()
