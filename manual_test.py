import requests
import gzip
import shutil
import os

# Create the folder if it doesn't exist
os.makedirs('data', exist_ok=True)

url = "https://cdn.rebrickable.com/media/downloads/themes.csv.gz"
print("Downloading...")
r = requests.get(url)
with open("data/themes.csv.gz", "wb") as f:
    f.write(r.content)

print("Unboxing...")
with gzip.open("data/themes.csv.gz", "rb") as f_in:
    with open("data/themes.csv", "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)

print("Check your /data folder for themes.csv!")