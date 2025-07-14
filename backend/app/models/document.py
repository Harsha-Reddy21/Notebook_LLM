from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.session import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
    file_path = Column(String)
    file_type = Column(String)
    file_size = Column(Integer)
    meta_data = Column(JSON, nullable=True)  # Renamed from metadata to meta_data
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    owner = relationship("User", back_populates="documents")
    sections = relationship("DocumentSection", back_populates="document", cascade="all, delete-orphan")
    queries = relationship("Query", back_populates="document")


class DocumentSection(Base):
    __tablename__ = "document_sections"

    id = Column(Integer, primary_key=True, index=True)
    section_type = Column(String)  # text, image, table, chart, code
    content = Column(Text, nullable=True)
    page_num = Column(Integer, nullable=True)
    position = Column(Integer)
    meta_data = Column(JSON, nullable=True)  # Renamed from metadata to meta_data
    vector_id = Column(String, nullable=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    
    # Relationships
    document = relationship("Document", back_populates="sections")
    images = relationship("DocumentImage", back_populates="section", cascade="all, delete-orphan")


class DocumentImage(Base):
    __tablename__ = "document_images"

    id = Column(Integer, primary_key=True, index=True)
    image_path = Column(String)
    image_type = Column(String)
    caption = Column(Text, nullable=True)
    meta_data = Column(JSON, nullable=True)  # Renamed from metadata to meta_data
    section_id = Column(Integer, ForeignKey("document_sections.id"))
    
    # Relationships
    section = relationship("DocumentSection", back_populates="images") 