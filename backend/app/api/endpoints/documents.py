import os
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.auth import get_current_active_user
from app.db.session import get_db
from app.models.document import Document, DocumentSection, DocumentImage
from app.models.user import User
from app.schemas.document import Document as DocumentSchema, DocumentCreate, DocumentList
from app.services.document_processor import (
    save_uploaded_file,
    process_document,
    split_documents,
    create_embeddings_for_documents,
    extract_document_structure,
)

router = APIRouter()


@router.post("/upload", response_model=DocumentSchema)
async def upload_document(
    *,
    db: Session = Depends(get_db),
    title: str = Form(...),
    description: Optional[str] = Form(None),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Upload a new document.
    """
    # Save the uploaded file
    file_content = await file.read()
    file_path = save_uploaded_file(file_content, file.filename)
    
    # Process the document
    try:
        documents, meta_data = process_document(file_path)  # Changed from metadata to meta_data
        
        # Create document record
        db_document = Document(
            title=title,
            description=description,
            file_path=file_path,
            file_type=meta_data["file_type"],  # Changed from metadata to meta_data
            file_size=os.path.getsize(file_path),
            meta_data=meta_data,  # Changed from metadata to meta_data
            owner_id=current_user.id,
        )
        db.add(db_document)
        db.commit()
        db.refresh(db_document)
        
        # Split documents for better processing
        split_docs = split_documents(documents)
        
        # Create embeddings
        vector_store_path = create_embeddings_for_documents(split_docs, str(db_document.id))
        
        # Extract document structure
        sections = extract_document_structure(split_docs)
        
        # Create document sections
        for section_data in sections:
            db_section = DocumentSection(
                section_type=section_data["section_type"],
                content=section_data["content"],
                page_num=section_data["page_num"],
                position=section_data["position"],
                meta_data=section_data["meta_data"],  # Changed from metadata to meta_data
                document_id=db_document.id,
            )
            db.add(db_section)
            db.commit()
            db.refresh(db_section)
            
            # If this is an image section, create image record
            if section_data["section_type"] == "image" and "source" in section_data["meta_data"]:  # Changed from metadata to meta_data
                db_image = DocumentImage(
                    image_path=section_data["meta_data"]["source"],  # Changed from metadata to meta_data
                    image_type=section_data["meta_data"].get("image_type", "unknown"),  # Changed from metadata to meta_data
                    section_id=db_section.id,
                )
                db.add(db_image)
        
        db.commit()
        
        return db_document
    
    except Exception as e:
        # Clean up the file if processing fails
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing document: {str(e)}",
        )


@router.get("/", response_model=DocumentList)
def list_documents(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve user's documents.
    """
    documents = db.query(Document).filter(Document.owner_id == current_user.id).offset(skip).limit(limit).all()
    total = db.query(Document).filter(Document.owner_id == current_user.id).count()
    
    return {"documents": documents, "total": total}


@router.get("/{document_id}", response_model=DocumentSchema)
def get_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get a specific document by ID.
    """
    document = db.query(Document).filter(Document.id == document_id, Document.owner_id == current_user.id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> None:
    """
    Delete a document.
    """
    document = db.query(Document).filter(Document.id == document_id, Document.owner_id == current_user.id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Delete the file
    if os.path.exists(document.file_path):
        os.remove(document.file_path)
    
    # Delete vector store if it exists
    vector_store_path = os.path.join(os.getenv("VECTOR_DB_PATH", "./vector_db"), f"doc_{document_id}")
    if os.path.exists(vector_store_path):
        import shutil
        shutil.rmtree(vector_store_path)
    
    # Delete from database
    db.delete(document)
    db.commit() 