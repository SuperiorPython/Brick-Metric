import pandas as pd
import sqlite3


def create_database():
    # 1. Connect to (or create) the database file
    conn = sqlite3.connect('brick_archive.db')

    # 2. Load the CSVs into DataFrames
    print("Reading CSVs...")
    df_sets = pd.read_csv('data/sets.csv')
    df_themes = pd.read_csv('data/themes.csv')

    # 3. Push the data into SQL tables
    print("Populating database...")
    df_sets.to_sql('sets', conn, if_exists='replace', index=False)
    df_themes.to_sql('themes', conn, if_exists='replace', index=False)

    # 4. Create an Index (This makes your search bar lightning fast!)
    conn.execute("CREATE INDEX idx_set_num ON sets(set_num)")
    conn.execute("CREATE INDEX idx_set_name ON sets(name)")

    conn.close()
    print("Done! Your LEGO database 'brick_archive.db' is ready.")


if __name__ == "__main__":
    create_database()