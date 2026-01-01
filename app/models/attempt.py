"""
Attempt model for storing user Armstrong number calculation attempts.
"""
from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped as M
from sqlalchemy.dialects.postgresql import UUID
import uuid

from ..extensions import db
from ..utils.date_time import DateTimeUtils

if TYPE_CHECKING:
    from .user import AppUser


class Attempt(db.Model):
    """Model to store user attempts at checking Armstrong numbers."""
    __tablename__ = "attempt"
    
    id: M[uuid.UUID] = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id: M[uuid.UUID] = db.Column(UUID(as_uuid=True), db.ForeignKey('app_user.id', ondelete='CASCADE'), nullable=False, index=True)
    input_value: M[str] = db.Column(db.String(50), nullable=False)  # Store as string to handle ranges like "100-999"
    input_type: M[str] = db.Column(db.String(20), nullable=False)  # 'single' or 'range'
    result: M[str] = db.Column(db.Text, nullable=True)  # JSON string or result text
    is_armstrong: M[bool] = db.Column(db.Boolean, nullable=True)  # For single number checks
    count: M[int] = db.Column(db.Integer, nullable=True)  # For range searches
    created_at = db.Column(db.DateTime(timezone=True), default=DateTimeUtils.aware_utcnow, nullable=False)
    
    # Relationship
    app_user = db.relationship('AppUser', backref='attempts', lazy=True)
    
    def __repr__(self):
        return f'<Attempt ID: {self.id}, user: {self.user_id}, input: {self.input_value}>'
    
    def to_dict(self):
        """Convert attempt to dictionary."""
        return {
            'id': str(self.id),
            'user_id': str(self.user_id),
            'input_value': self.input_value,
            'input_type': self.input_type,
            'result': self.result,
            'is_armstrong': self.is_armstrong,
            'count': self.count,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def save(self):
        """Save the attempt."""
        db.session.add(self)
        db.session.commit()
        return self
    
    def delete(self):
        """Delete the attempt."""
        db.session.delete(self)
        db.session.commit()
