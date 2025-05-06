from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class DocumentMetadata(BaseModel):
    """Flexible metadata model that can accommodate any document type"""
    source: str
    content_type: str
    text: str
    document_id: str
    title: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    created_at: Optional[str] = None
    last_modified: Optional[str] = None
    custom_fields: Optional[Dict[str, Any]] = None

    class Config:
        json_schema_extra = {
            "example": {
                "source": "uploaded_file.pdf",
                "content_type": "application/pdf",
                "text": "This is the extracted text content...",
                "document_id": "doc_123",
                "title": "Project Proposal",
                "description": "Initial project proposal document",
                "tags": ["project", "proposal"],
                "created_at": "2023-10-15T14:30:00Z",
                "custom_fields": {"author": "John Doe", "pages": 10}
            }
        }

class DocumentEmbedding(BaseModel):
    id: int
    values: List[float]
    metadata: DocumentMetadata

class Vector(BaseModel):
    id: str
    values: List[float]
    metadata: DocumentMetadata
    score: float