import time
import subprocess

while True:
    print("🔁 Checking for new trades...")
    subprocess.run(["python", "scrape_trady_flow.py"])
    time.sleep(60)
