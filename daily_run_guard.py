import os
import subprocess
import datetime
import socket

LOCK_FILE = "last_run.lock"
SCRIPT_TO_RUN = "run_scrapy_job.py"

def has_internet(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception:
        return False

def already_ran_today():
    if not os.path.exists(LOCK_FILE):
        return False
    with open(LOCK_FILE, "r") as f:
        last_run_date = f.read().strip()
        return last_run_date == datetime.date.today().isoformat()

def update_lock():
    with open(LOCK_FILE, "w") as f:
        f.write(datetime.date.today().isoformat())

if __name__ == "__main__":
    if already_ran_today():
        print("⏱️ Already ran today, skipping.")
    elif not has_internet():
        print("📡 No internet. Will try again on next boot.")
    else:
        print("🚀 Running mortgage rate scraper...")
        subprocess.run(["python", SCRIPT_TO_RUN])
        update_lock()
        print("✅ Job finished and locked for today.")
