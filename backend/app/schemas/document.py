from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel


class DocumentImageBase(BaseModel):
    image_type: str
    caption: Optional[str] = None
    meta_data: Optional[Dict[str, Any]] = None


class DocumentImageCreate(DocumentImageBase):
    image_path: str


class DocumentImage(DocumentImageBase):
    id: int
    image_path: str
    section_id: int

    class Config:
        orm_mode = True
        from_attributes = True


class DocumentSectionBase(BaseModel):
    section_type: str
    content: Optional[str] = None
    page_num: Optional[int] = None
    position: int
    meta_data: Optional[Dict[str, Any]] = None


class DocumentSectionCreate(DocumentSectionBase):
    pass


class DocumentSection(DocumentSectionBase):
    id: int
    document_id: int
    vector_id: Optional[str] = None
    images: List[DocumentImage] = []

    class Config:
        orm_mode = True
        from_attributes = True


class DocumentBase(BaseModel):
    title: str
    description: Optional[str] = None
    file_type: str
    meta_data: Optional[Dict[str, Any]] = None


class DocumentCreate(DocumentBase):
    file_path: str
    file_size: int


class Document(DocumentBase):
    id: int
    file_path: str
    file_size: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    owner_id: int
    sections: List[DocumentSection] = []

    class Config:
        orm_mode = True
        from_attributes = True


class DocumentList(BaseModel):
    documents: List[Document]
    total: int 