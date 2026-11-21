"""
Automated Daily Crawler & SEO Pipeline Runner for AllSarkariJobs.
Designed for both local execution and GitHub Actions automation.
"""
import sys
import subprocess
from datetime import datetime

FORBIDDEN_COMPETITORS = [
    "rojgarresult.com",
    "sarkariresults.org.in",
    "scribd.com",
    "freejobalert.com"
]

def run_step(step_name: str, module_name: str):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting: {step_name}...")
    res = subprocess.run([sys.executable, "-m", module_name], capture_output=True, text=True)
    if res.stdout:
        print(res.stdout.strip())
    if res.returncode != 0:
        print(f"ERROR in {step_name}:", res.stderr)
        sys.exit(res.returncode)
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Completed: {step_name}\n")

def audit_competitor_links():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Auditing competitor links...")
    from pathlib import Path
    base = Path(__file__).resolve().parent.parent
    check_files = [base / "portal_data.js", base / "sitemap.xml", base / "detail.html"]
    violations = 0
    for cf in check_files:
        if cf.exists():
            text = cf.read_text(encoding="utf-8", errors="ignore").lower()
            for comp in FORBIDDEN_COMPETITORS:
                if comp in text:
                    print(f"VIOLATION: Found forbidden competitor link '{comp}' in {cf.name}!")
                    violations += 1
    if violations > 0:
        print(f"FAILURE: Total {violations} competitor link violations detected.")
        sys.exit(1)
    print("SUCCESS: 0 competitor links detected across all checked files.\n")

def main():
    print(f"=== ALLSARKARIJOBS DAILY UPDATE PIPELINE ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ===")
    
    # Step 1: Scrape authoritative portals and sync portal_data.js
    run_step("Live Recruitment Crawl & Portal Data Sync", "backend.scrape_sarkariresult")
    
    # Step 2: Regenerate 20 programmatic SEO landing pages in jobs/*/ with static FAQPage schema
    run_step("Programmatic SEO Pages Generation", "backend.generate_programmatic_seo")
    
    # Step 3: Regenerate authoritative sitemap.xml with updated timestamps
    run_step("Sitemap & Robots.txt Generation", "backend.generate_sitemap")
    
    # Step 4: Strict competitor link blacklist audit
    audit_competitor_links()
    
    print(f"=== PIPELINE COMPLETED SUCCESSFULLY AT {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")

if __name__ == "__main__":
    main()
