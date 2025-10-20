import sqlite3
import os
from typing import List, Dict, Any

# Build the path to the database
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "database", "chinook.db")

def get_db_schema():
    """
    Connects to the DB and returns the schema as a string.
    This is used to inform the AI model.
    """
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Database not found at {DB_PATH}. Did you run `python database/setup_database.py`?")
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table';")
    schema = "\n".join([f"Table '{name}':\n{sql}\n" for name, sql in cursor.fetchall()])
    
    conn.close()
    return schema

def execute_query(sql_query: str) -> List[Dict[str, Any]]:
    """
    Safely executes a read-only SQL query against the database.
    Prevents any non-SELECT statements.
    """
    # SECURITY: A critical, simple check to prevent modifications
    if not sql_query.strip().upper().startswith("SELECT"):
        raise ValueError("Only SELECT queries are allowed.")
        
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Database not found at {DB_PATH}.")

    conn = sqlite3.connect(DB_PATH)
    # Set row_factory to get results as dictionaries
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        cursor.execute(sql_query)
        # Fetch all results and convert them from sqlite3.Row to standard dicts
        results = [dict(row) for row in cursor.fetchall()]
        return results
    except sqlite3.Error as e:
        raise ValueError(f"SQL execution error: {e}")
    finally:
        conn.close()
