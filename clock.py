import schedule
import time
import subprocess

def update_data():
    print("Updating LEGO Archive...")
    subprocess.run(["python", "scripts/downloader.py"])
    subprocess.run(["python", "scripts/importer.py"])

# Run every day at 3 AM
schedule.every().day.at("03:00").do(update_data)

while True:
    schedule.run_pending()
    time.sleep(60)