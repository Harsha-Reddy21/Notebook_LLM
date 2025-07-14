from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.session import Base


class Query(Base):
    __tablename__ = "queries"

    id = Column(Integer, primary_key=True, index=True)
    query_text = Column(Text)
    response = Column(Text, nullable=True)
    meta_data = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_favorite = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="queries")
    document = relationship("Document", back_populates="queries")
    citations = relationship("Citation", back_populates="query", cascade="all, delete-orphan")


class Citation(Base):
    __tablename__ = "citations"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    meta_data = Column(JSON, nullable=True)
    query_id = Column(Integer, ForeignKey("queries.id"))
    document_section_id = Column(Integer, ForeignKey("document_sections.id"))
    
    # Relationships
    query = relationship("Query", back_populates="citations")
    document_section = relationship("DocumentSection") 