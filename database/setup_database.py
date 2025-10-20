import sqlite3
import requests
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "chinook.db")
SQL_URL = "https://raw.githubusercontent.com/lerocha/chinook-database/master/ChinookDatabase/DataSources/Chinook_Sqlite.sql"
SQL_FILE_PATH = os.path.join(os.path.dirname(__file__), "chinook.sql")

def setup():
    """
    Downloads the Chinook SQL script and executes it to create the database.
    """
    if os.path.exists(DB_PATH):
        print(f"Database already exists at {DB_PATH}")
        return

    # 1. Download the SQL file
    print(f"Downloading SQL script from {SQL_URL}...")
    try:
        response = requests.get(SQL_URL)
        response.raise_for_status()
        with open(SQL_FILE_PATH, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"SQL script saved to {SQL_FILE_PATH}")
    except requests.RequestException as e:
        print(f"Failed to download SQL script: {e}")
        return

    # 2. Create the database and execute the SQL
    print(f"Creating database at {DB_PATH}...")
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        with open(SQL_FILE_PATH, "r", encoding="utf-8") as f:
            sql_script = f.read()
        
        cursor.executescript(sql_script)
        
        conn.commit()
        conn.close()
        print("Database created and populated successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred during database creation: {e}")
    finally:
        # 3. Clean up the SQL file
        if os.path.exists(SQL_FILE_PATH):
            os.remove(SQL_FILE_PATH)
            print(f"Cleaned up {SQL_FILE_PATH}")

if __name__ == "__main__":
    setup()
