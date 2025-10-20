from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .pydantic_models import QueryRequest, QueryResponse
from .ai_service import get_sql_from_text
from .db_executor import execute_query

app = FastAPI(
    title="QueryCraft API",
    description="API for translating natural language to SQL and executing queries.",
    version="1.0.0"
)

# Allow all origins for development (Streamlit app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the QueryCraft API. Go to /docs for details."}


@app.post("/api/v1/query", response_model=QueryResponse)
async def handle_query(request: QueryRequest):
    """
    Receives a natural language query, converts it to SQL,
    executes it, and returns the result.
    """
    try:
        # 1. Get SQL from AI
        sql_query = get_sql_from_text(request.text)
        
    except RuntimeError as e:
        # Error if the AI model isn't loaded
        return QueryResponse(sql_query="", error=f"AI Model Error: {e}")
    except Exception as e:
        # Other unexpected AI errors
        return QueryResponse(sql_query="", error=f"AI Error: {e}")

    try:
        # 2. Execute SQL query
        data = execute_query(sql_query)
        # 3. Return successful response
        return QueryResponse(sql_query=sql_query, data=data)
        
    except ValueError as e:
        # Handle SQL errors (e.g., "Only SELECT allowed" or bad syntax)
        return QueryResponse(sql_query=sql_query, error=str(e))
    except Exception as e:
        # Other unexpected DB errors
        return QueryResponse(sql_query=sql_query, error=f"Database Error: {e}")
