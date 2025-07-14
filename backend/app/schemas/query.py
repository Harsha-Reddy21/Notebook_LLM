from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel


class CitationBase(BaseModel):
    content: str
    meta_data: Optional[Dict[str, Any]] = None


class CitationCreate(CitationBase):
    document_section_id: int


class Citation(CitationBase):
    id: int
    query_id: int
    document_section_id: int

    class Config:
        orm_mode = True
        from_attributes = True


class QueryBase(BaseModel):
    query_text: str
    meta_data: Optional[Dict[str, Any]] = None


class QueryCreate(QueryBase):
    document_id: Optional[int] = None


class QueryUpdate(BaseModel):
    is_favorite: Optional[bool] = None
    meta_data: Optional[Dict[str, Any]] = None


class Query(QueryBase):
    id: int
    response: Optional[str] = None
    created_at: datetime
    is_favorite: bool
    user_id: int
    document_id: Optional[int] = None
    citations: List[Citation] = []

    class Config:
        orm_mode = True
        from_attributes = True


class QueryResponse(BaseModel):
    query: Query
    citations: List[Citation] = []


class QueryList(BaseModel):
    queries: List[Query]
    total: int 