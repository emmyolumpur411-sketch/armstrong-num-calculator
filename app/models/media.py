"""
Media model for storing file references.
"""
from __future__ import annotations
from sqlalchemy.orm import Mapped as M
from sqlalchemy.dialects.postgresql import UUID
import uuid

from ..extensions import db


class Media(db.Model):
    """Model to store media file references."""
    __tablename__ = "media"
    
    id: M[uuid.UUID] = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    filename: M[str] = db.Column(db.String(255), nullable=False)
    file_path: M[str] = db.Column(db.String(500), nullable=False)
    file_type: M[str] = db.Column(db.String(50), nullable=True)
    
    def __repr__(self):
        return f'<Media ID: {self.id}, filename: {self.filename}>'
    
    def get_path(self):
        """Get the file path."""
        return self.file_path
    
    def to_dict(self):
        """Convert media to dictionary."""
        return {
            'id': str(self.id),
            'filename': self.filename,
            'file_path': self.file_path,
            'file_type': self.file_type
        }
