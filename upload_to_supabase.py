import os
import csv
import sys
from datetime import datetime
from pathlib import Path
from supabase import create_client, Client
from dotenv import load_dotenv

# Load .env file from the project root directory
dotenv_path = Path.cwd() / ".env"
if not dotenv_path.exists():
    print(f"❌ .env file not found at {dotenv_path}")
    sys.exit(1)

load_dotenv(dotenv_path)

# Get Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_TABLE = os.getenv("SUPABASE_TABLE", "mortgage_rates")
CSV_PATH = os.path.join("output", "mortgage_rates.csv")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ Missing Supabase credentials.")
    sys.exit(1)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Load current Supabase records (only product + date keys to avoid duplicates)
try:
    response = supabase.table(SUPABASE_TABLE).select("loan_product", "date").execute()
    existing_records = set((item["loan_product"], item["date"]) for item in response.data)
except Exception as e:
    print(f"❌ Supabase fetch error: {e}")
    sys.exit(1)

# Prepare new rows from CSV
new_rows = []
with open(CSV_PATH, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        key = (row["loan_product"], row["date"])
        if key not in existing_records:
            # Ensure numeric fields are correct
            try:
                row["interest_rate"] = float(row["interest_rate"])
                row["apr"] = float(row["apr"])
                row["loan_term_years"] = int(row["loan_term_years"])
                row["forecasted_rate"] = float(row["forecasted_rate"])
            except ValueError as e:
                print(f"⚠️ Skipping invalid row: {row}")
                continue
            new_rows.append(row)

# Upload new rows
if new_rows:
    try:
        supabase.table(SUPABASE_TABLE).insert(new_rows).execute()
        print(f"✅ Uploaded {len(new_rows)} new row(s) to Supabase.")
    except Exception as e:
        print(f"❌ Supabase upload error: {e}")
        sys.exit(1)
else:
    print("📁 No new data to upload.")

