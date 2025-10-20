from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class QueryRequest(BaseModel):
    """Request model for a user's plain-English query."""
    text: str

class QueryResponse(BaseModel):
    """Response model containing the SQL, data, and any errors."""
    sql_query: str
    data: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None
