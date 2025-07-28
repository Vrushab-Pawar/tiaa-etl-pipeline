import subprocess
import os
import sys

project_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(project_dir)

# Cleanup old files
for f in ["./output/mortgage_rates.json", "./output/mortgage_rates.jsonl"]:
    try:
        os.remove(f)
    except FileNotFoundError:
        pass

# Step 1: Run Scrapy Spider
print("🚀 Running Scrapy spider...")

subprocess.run(
    [sys.executable, "-m", "scrapy", "crawl", "bankrate_spider", "-s", "LOG_LEVEL=WARNING"],
    check=True
)
print("✅ Scraping complete.")


# Step 3: Append JSON to CSV
print("📤 Appending to CSV...")
subprocess.run([sys.executable, "./append_json_csv.py"], check=True)
print("📤 Appending Complete...")

# print("☁️ Uploading CSV to Supabase (if needed)...")
# subprocess.run([sys.executable, "./upload_to_supabase.py"], check=True)