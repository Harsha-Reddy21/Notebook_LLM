from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.auth import get_current_active_user
from app.db.session import get_db
from app.models.query import Query, Citation
from app.models.user import User
from app.schemas.query import QueryCreate, Query as QuerySchema, QueryList, QueryResponse, QueryUpdate
from app.services.query_processor import process_query

router = APIRouter()


@router.post("/", response_model=QueryResponse)
def create_query(
    *,
    db: Session = Depends(get_db),
    query_in: QueryCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create a new query and get response.
    """
    # Create query record
    db_query = Query(
        query_text=query_in.query_text,
        meta_data=query_in.meta_data,  # Changed from metadata to meta_data
        user_id=current_user.id,
        document_id=query_in.document_id,
    )
    db.add(db_query)
    db.commit()
    db.refresh(db_query)
    
    # Process the query
    try:
        result = process_query(
            query_text=query_in.query_text,
            document_id=str(query_in.document_id) if query_in.document_id else None
        )
        
        # Update the query with the response
        db_query.response = result["response"]
        db.add(db_query)
        db.commit()
        db.refresh(db_query)
        
        # Create citations
        citations = []
        for citation_data in result["citations"]:
            db_citation = Citation(
                content=citation_data["content"],
                meta_data=citation_data["meta_data"],  # Changed from metadata to meta_data
                query_id=db_query.id,
                document_section_id=citation_data["document_section_id"],
            )
            db.add(db_citation)
            citations.append(db_citation)
        
        db.commit()
        
        return {"query": db_query, "citations": citations}
    
    except Exception as e:
        # Update the query with the error
        db_query.response = f"Error processing query: {str(e)}"
        db.add(db_query)
        db.commit()
        
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}",
        )


@router.get("/", response_model=QueryList)
def list_queries(
    skip: int = 0,
    limit: int = 100,
    document_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve query history.
    """
    query = db.query(Query).filter(Query.user_id == current_user.id)
    
    if document_id:
        query = query.filter(Query.document_id == document_id)
    
    total = query.count()
    queries = query.order_by(Query.created_at.desc()).offset(skip).limit(limit).all()
    
    return {"queries": queries, "total": total}


@router.get("/{query_id}", response_model=QueryResponse)
def get_query(
    query_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get a specific query by ID.
    """
    query = db.query(Query).filter(Query.id == query_id, Query.user_id == current_user.id).first()
    if not query:
        raise HTTPException(status_code=404, detail="Query not found")
    
    citations = db.query(Citation).filter(Citation.query_id == query_id).all()
    
    return {"query": query, "citations": citations}


@router.put("/{query_id}", response_model=QuerySchema)
def update_query(
    *,
    db: Session = Depends(get_db),
    query_id: int,
    query_in: QueryUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update a query (e.g., mark as favorite).
    """
    query = db.query(Query).filter(Query.id == query_id, Query.user_id == current_user.id).first()
    if not query:
        raise HTTPException(status_code=404, detail="Query not found")
    
    update_data = query_in.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(query, field, value)
    
    db.add(query)
    db.commit()
    db.refresh(query)
    
    return query


@router.delete("/{query_id}", status_code=204)
def delete_query(
    query_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> None:
    """
    Delete a query.
    """
    query = db.query(Query).filter(Query.id == query_id, Query.user_id == current_user.id).first()
    if not query:
        raise HTTPException(status_code=404, detail="Query not found")
    
    db.delete(query)
    db.commit() 