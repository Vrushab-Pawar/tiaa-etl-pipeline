import os, csv, json, sys
from datetime import datetime

jsonl_path = os.path.join("output", "mortgage_rates.jsonl")
csv_path = os.path.join("output", "mortgage_rates.csv")
today = datetime.today().strftime("%Y-%m-%d")

# ✅ Check JSONL exists and is non-empty
if not os.path.exists(jsonl_path) or os.path.getsize(jsonl_path) == 0:
    print("❌ No JSONL file or it's empty.")
    sys.exit(0)

# ✅ Load JSONL lines
raw_data = []
with open(jsonl_path, "r", encoding="utf-8") as f:
    for line in f:
        try:
            item = json.loads(line.strip())
            item["forecasted_rate"] = round(item["interest_rate"] + 0.15, 2)
            item["data_collection_agent"] = "AutomatedScraper"
            item["date"] = today
            raw_data.append(item)
        except json.JSONDecodeError:
            print(f"⚠️ Skipping malformed line: {line.strip()}")

if not raw_data:
    print("⚠️ No valid data in JSONL.")
    sys.exit(0)

# ✅ Load existing CSV rows
existing = set()
if os.path.exists(csv_path):
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            existing.add((row["loan_product"], row["date"]))

# ✅ Filter out duplicates
new_rows = [
    item for item in raw_data
    if (item["loan_product"], item["date"]) not in existing
]

# ✅ Append to CSV
if new_rows:
    with open(csv_path, "a", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=new_rows[0].keys())
        if os.stat(csv_path).st_size == 0:
            writer.writeheader()
        writer.writerows(new_rows)
    print(f"✅ Appended {len(new_rows)} new row(s) to CSV.")
else:
    print("📁 No new data to append.")

# ✅ Clear JSONL safely
with open(jsonl_path, "w", encoding="utf-8") as f:
    pass  # Empty the file
print("🧹 JSONL cleared.")
