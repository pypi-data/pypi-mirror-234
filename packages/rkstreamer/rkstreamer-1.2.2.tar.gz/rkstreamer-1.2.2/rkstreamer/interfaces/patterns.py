"""
Design Patterns for Interfaces
"""

from ._interface import ABC, abstractmethod


class Command(ABC):
    """Command pattern interface"""

    @abstractmethod
    def execute(self, user_input):
        """Execute method that does the action"""
