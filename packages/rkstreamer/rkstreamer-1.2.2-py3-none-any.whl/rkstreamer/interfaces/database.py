"""DI module for Database API
"""

from ._interface import ABC, abstractmethod


class IDatabaseProvider(ABC):
    """Interface for Database Providers"""

    @abstractmethod
    def connect(self):
        """Connect to DB"""

    @abstractmethod
    def check(self, name: str):
        """Checking DB content"""

    @abstractmethod
    def read(self, name: str):
        """Reading DB content"""

    @abstractmethod
    def write(self, name: str):
        """Writing DB content"""

    @abstractmethod
    def close(self):
        """Close DB connection"""
