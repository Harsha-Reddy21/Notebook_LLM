import os
import shutil
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    UnstructuredHTMLLoader,
    CSVLoader,
    UnstructuredExcelLoader,
    UnstructuredPowerPointLoader,
    UnstructuredImageLoader,
    NotebookLoader,
)
from langchain_community.document_loaders.base import BaseLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

from app.core.config import settings


def get_loader_for_file(file_path: str) -> BaseLoader:
    """
    Get the appropriate document loader based on file extension
    """
    file_extension = Path(file_path).suffix.lower()
    
    if file_extension == ".pdf":
        return PyPDFLoader(file_path)
    elif file_extension == ".docx":
        return Docx2txtLoader(file_path)
    elif file_extension in [".html", ".htm"]:
        return UnstructuredHTMLLoader(file_path)
    elif file_extension == ".csv":
        return CSVLoader(file_path)
    elif file_extension in [".xlsx", ".xls"]:
        return UnstructuredExcelLoader(file_path)
    elif file_extension in [".ppt", ".pptx"]:
        return UnstructuredPowerPointLoader(file_path)
    elif file_extension in [".jpg", ".jpeg", ".png", ".gif"]:
        return UnstructuredImageLoader(file_path, mode="elements")
    elif file_extension == ".ipynb":
        return NotebookLoader(file_path)
    else:
        raise ValueError(f"Unsupported file extension: {file_extension}")


def save_uploaded_file(file_data: bytes, filename: str) -> str:
    """
    Save an uploaded file to the document storage directory
    """
    os.makedirs(settings.DOCUMENT_STORAGE_PATH, exist_ok=True)
    
    file_path = os.path.join(settings.DOCUMENT_STORAGE_PATH, filename)
    
    with open(file_path, "wb") as f:
        f.write(file_data)
    
    return file_path


def process_document(file_path: str) -> Tuple[List[Document], Dict[str, Any]]:
    """
    Process a document using LangChain and extract its content and metadata
    """
    loader = get_loader_for_file(file_path)
    documents = loader.load()
    
    # Extract metadata
    meta_data = {
        "page_count": len(documents),
        "file_type": Path(file_path).suffix.lower(),
        "file_name": Path(file_path).name,
    }
    
    return documents, meta_data


def split_documents(documents: List[Document]) -> List[Document]:
    """
    Split documents into smaller chunks for better processing
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    
    return text_splitter.split_documents(documents)


def create_embeddings_for_documents(documents: List[Document], document_id: str) -> str:
    """
    Create embeddings for documents and store them in the vector database
    """
    os.makedirs(settings.VECTOR_DB_PATH, exist_ok=True)
    
    # Use HuggingFace embeddings for technical content
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Create vector store
    vector_store_path = os.path.join(settings.VECTOR_DB_PATH, f"doc_{document_id}")
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=vector_store_path,
    )
    
    # Persist the vector store
    vectorstore.persist()
    
    return vector_store_path


def extract_document_structure(documents: List[Document]) -> List[Dict[str, Any]]:
    """
    Extract document structure including sections, images, tables, etc.
    """
    sections = []
    position = 0
    
    for doc in documents:
        section_type = "text"
        if "image" in doc.metadata.get("source", "").lower():
            section_type = "image"
        elif "table" in doc.metadata.get("category", "").lower():
            section_type = "table"
        elif "code" in doc.metadata.get("category", "").lower():
            section_type = "code"
        
        section = {
            "section_type": section_type,
            "content": doc.page_content,
            "page_num": doc.metadata.get("page", None),
            "position": position,
            "meta_data": doc.metadata,  # Changed from metadata to meta_data
        }
        
        sections.append(section)
        position += 1
    
    return sections 