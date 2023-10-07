"""Models - Exception module"""

class InvalidInput(Exception):
    """Invalid/unexpected input provided"""

class QueueException(Exception):
    """Base exception for Queue models"""

class AddMediaError(QueueException):
    """Add media to queue failed"""

class RemoveMediaError(QueueException):
    """Remove media from queue failed"""

class GetMediaError(QueueException):
    """Get media from queue failed"""

class MediaNotFound(QueueException):
    """Media not found in queue"""
