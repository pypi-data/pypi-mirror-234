"""
DI modules for Player
"""

from ._interface import ABC, abstractmethod

class MusicPlayer(ABC):
    """Interface for music player"""

    @abstractmethod
    def add_media(self, media_url: str):
        """Add media to queue"""

    @abstractmethod
    def remove_media(self, media_url: str):
        """Add media to queue"""

    @abstractmethod
    def play_media(self, media_url: str):
        """Play media"""

class MusicPlayerControls(ABC):
    """Interface for music player cntrols"""

    @abstractmethod
    def player_controls(self, user_input: str):
        """Player controls"""
