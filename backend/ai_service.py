from ctransformers import AutoModelForCausalLM
import os
from .db_executor import get_db_schema

# Path to the downloaded model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "sqlcoder-7b.Q4_K_M.gguf") # <-- CORRECT FILENAME

# --- Database Schema ---
# We get the schema once when the server loads
try:
    DB_SCHEMA = get_db_schema()
except FileNotFoundError:
    print("WARNING: Database not found. Schema will be empty.")
    DB_SCHEMA = "Error: Could not load schema."

# --- AI Model Initialization ---
try:
    # Initialize the model from the local file
    llm = AutoModelForCausalLM.from_pretrained(
        MODEL_PATH,
        model_type='llama',
        context_length=2048  # <-- ADD THIS LINE
    )
    print("AI Text-to-SQL model loaded successfully.")
except Exception as e:
    print(f"Failed to load AI model: {e}")
    print("AI service will not be available.")
    llm = None

def get_sql_from_text(user_query: str) -> str:
    """
    Uses the loaded Gen AI model to convert a user's text query into SQL.
    """
    if llm is None:
        raise RuntimeError("AI model is not loaded. Cannot process query.")

    # --- This is the Prompt Engineering ---
    # We provide the schema and the user question.
    prompt = f"""
### Task
Generate a single, executable SQL query that answers the following question.
Only output the SQL query and nothing else.

### Database Schema
The query will be run on a database with the following schema:
{DB_SCHEMA}

### Question
{user_query}

### SQL Query
"""
    
    print("Generating SQL for prompt...")
    # Generate the SQL query
    sql_query = llm(prompt, max_new_tokens=256, stop=["\n\n", ";"])
    
    # Clean up the output
    if ";" not in sql_query:
        sql_query += ";"
        
    sql_query = sql_query.strip()
    
    print(f"Generated SQL: {sql_query}")
    return sql_query
