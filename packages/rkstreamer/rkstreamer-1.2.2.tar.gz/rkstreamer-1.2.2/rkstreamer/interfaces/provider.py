"""
DI Module for stream providers API
"""

from ._interface import ABC,abstractmethod

class ISongProvider(ABC):
    """Interface for song provider"""

    @abstractmethod
    def search_songs(self, search_string: str, **kwargs):
        """Search songs"""

    @abstractmethod
    def select_song(self, arg: str, **kwargs):
        """Select song"""


class IAlbumProvider(ABC):
    """Interface for album provider"""

    @abstractmethod
    def search_albums(self, search_string: str, **kwargs):
        """Search albums"""

    @abstractmethod
    def select_album(self, arg: str, **kwargs):
        """Select album"""


class IPlaylistProvider(ABC):
    """Interface for playlist provider"""

    @abstractmethod
    def search_playlists(self, search_string: str, **kwargs):
        """Search playlists"""

    @abstractmethod
    def select_playlist(self, arg: int, **kwargs):
        """Select playlist"""
