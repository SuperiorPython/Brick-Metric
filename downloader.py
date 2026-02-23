import requests
import gzip
import shutil
import os

# The direct links to Rebrickable's daily exports
FILES = {
    "sets": "https://cdn.rebrickable.com/media/downloads/sets.csv.gz",
    "themes": "https://cdn.rebrickable.com/media/downloads/themes.csv.gz",
    "colors": "https://cdn.rebrickable.com/media/downloads/colors.csv.gz"
}


def download_brick_data():
    if not os.path.exists('data'):
        os.makedirs('data')

    for name, url in FILES.items():
        print(f"Fetching latest {name} data...")
        response = requests.get(url, stream=True)

        # Save the compressed file
        gz_path = f"data/{name}.csv.gz"
        with open(gz_path, 'wb') as f:
            f.write(response.content)

        # Unzip it into a clean CSV
        with gzip.open(gz_path, 'rb') as f_in:
            with open(f"data/{name}.csv", 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        print(f"Successfully saved data/{name}.csv")


if __name__ == "__main__":
    download_brick_data()