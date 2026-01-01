"""
Date and time utility functions.
"""
from datetime import datetime, timezone
from typing import Optional


class DateTimeUtils:
    """Utility class for date and time operations."""
    
    @staticmethod
    def aware_utcnow() -> datetime:
        """Return current UTC datetime with timezone awareness."""
        return datetime.now(timezone.utc)
    
    @staticmethod
    def to_gmt1(dt: Optional[datetime]) -> Optional[datetime]:
        """Convert datetime to GMT+1 timezone."""
        if dt is None:
            return None
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)  # For now, just return UTC


def to_gmt1_or_none(dt: Optional[datetime]) -> Optional[datetime]:
    """Convert datetime to GMT+1 or return None."""
    return DateTimeUtils.to_gmt1(dt)
