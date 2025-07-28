import os
import csv
import sys
from supabase import create_client, Client

# Supabase credentials from GitHub Secrets (CI/CD)
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
SUPABASE_TABLE = os.environ.get("SUPABASE_TABLE", "mortgage_rates")
CSV_PATH = os.path.join("output", "mortgage_rates.csv")

# Validate Supabase credentials
if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ Missing Supabase credentials. Ensure secrets are passed as environment variables.")
    sys.exit(1)

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Load current Supabase records to avoid duplicates
try:
    response = supabase.table(SUPABASE_TABLE).select("loan_product", "date").execute()
    existing_records = set((item["loan_product"], item["date"]) for item in response.data)
    print(f"📊 Fetched {len(existing_records)} existing records from Supabase.")
except Exception as e:
    print(f"❌ Supabase fetch error: {e}")
    sys.exit(1)

# Prepare new rows from CSV
new_rows = []
try:
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (row["loan_product"], row["date"])
            if key not in existing_records:
                try:
                    row["interest_rate"] = float(row["interest_rate"])
                    row["apr"] = float(row["apr"])
                    row["loan_term_years"] = int(row["loan_term_years"])
                    row["forecasted_rate"] = float(row["forecasted_rate"])
                except ValueError:
                    print(f"⚠️ Skipping invalid row due to type error: {row}")
                    continue
                new_rows.append(row)
except FileNotFoundError:
    print(f"❌ CSV file not found at: {CSV_PATH}")
    sys.exit(1)

# Upload new rows to Supabase
if new_rows:
    try:
        supabase.table(SUPABASE_TABLE).insert(new_rows).execute()
        print(f"✅ Uploaded {len(new_rows)} new row(s) to Supabase.")
    except Exception as e:
        print(f"❌ Supabase upload error: {e}")
        sys.exit(1)
else:
    print("📁 No new data to upload.")
