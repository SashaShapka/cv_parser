from pydantic import BaseModel
from typing import Optional


class QueryResponse(BaseModel):
    id: str
    name: str
    skills: str
    experience: Optional[str] = None
    source: str


class QueryRequest(BaseModel):
    query: str


class GenerateCvRequest(BaseModel):
    candidate_id: str