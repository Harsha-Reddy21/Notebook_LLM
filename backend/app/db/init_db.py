import os
from sqlalchemy.orm import Session

from app.core.auth import get_password_hash
from app.core.config import settings
from app.db.session import Base, engine
from app.models.user import User
from app.models.document import Document, DocumentSection, DocumentImage
from app.models.query import Query, Citation


def init_db(db: Session) -> None:
    """
    Initialize the database with tables and initial data.
    """
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Check if we should create a superuser
    user = db.query(User).filter(User.email == "admin@example.com").first()
    if not user:
        user = User(
            email="admin@example.com",
            full_name="Admin User",
            hashed_password=get_password_hash("admin"),
            is_superuser=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    # Create document storage directory
    os.makedirs(settings.DOCUMENT_STORAGE_PATH, exist_ok=True)
    
    # Create vector database directory
    os.makedirs(settings.VECTOR_DB_PATH, exist_ok=True)


if __name__ == "__main__":
    from app.db.session import SessionLocal
    
    db = SessionLocal()
    init_db(db) 