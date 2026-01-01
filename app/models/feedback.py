"""
Feedback model for storing user feedback.
"""
from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from sqlalchemy.orm import Mapped as M
from sqlalchemy.dialects.postgresql import UUID
import uuid

from ..extensions import db
from ..utils.date_time import DateTimeUtils

if TYPE_CHECKING:
    from .user import AppUser


class Feedback(db.Model):
    """Model to store user feedback."""
    __tablename__ = "feedback"
    
    id: M[uuid.UUID] = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id: M[Optional[uuid.UUID]] = db.Column(UUID(as_uuid=True), db.ForeignKey('app_user.id', ondelete='SET NULL'), nullable=True, index=True)
    name: M[str] = db.Column(db.String(200), nullable=False)
    email: M[str] = db.Column(db.String(255), nullable=False)
    subject: M[Optional[str]] = db.Column(db.String(200), nullable=True)
    message: M[str] = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=DateTimeUtils.aware_utcnow, nullable=False)
    
    # Relationship
    app_user = db.relationship('AppUser', backref='feedbacks', lazy=True)
    
    def __repr__(self):
        return f'<Feedback ID: {self.id}, from: {self.email}>'
    
    def to_dict(self):
        """Convert feedback to dictionary."""
        return {
            'id': str(self.id),
            'user_id': str(self.user_id) if self.user_id else None,
            'name': self.name,
            'email': self.email,
            'subject': self.subject,
            'message': self.message,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def save(self):
        """Save the feedback."""
        db.session.add(self)
        db.session.commit()
        return self
    
    def delete(self):
        """Delete the feedback."""
        db.session.delete(self)
        db.session.commit()
