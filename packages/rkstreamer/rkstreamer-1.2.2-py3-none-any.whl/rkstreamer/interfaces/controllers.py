"""
DI module for Controllers
"""

from typing import Union
from ._interface import ABC, abstractmethod


class IController(ABC):
    """Interface for Song controller"""

    @abstractmethod
    def handle_input(self, user_input: Union[str, int]) -> None:
        """Process user input"""


class ISongController(IController):
    """Interface for Song controller"""

    @abstractmethod
    def monitor_queue_pull_rsong(self):
        """Pull rsong by monitoring queue status"""

    @abstractmethod
    def uow_update_song_status(self, status: str, stream_url: str):
        """UOW: updates song status in queue"""

    @abstractmethod
    def uow_add_rsongs_rqueue(self, data: str):
        """UOW: Add rsongs to rqueue"""

    @abstractmethod
    def uow_add_songs_queue(self, song):
        """Add songs to queue"""

    @abstractmethod
    def uow_play_songs_remove_loaded(self, song):
        """Sets all loaded songs to 'Played' when playing songs
        from search or rsongs queue"""


class IAlbumController(ISongController):
    """Interface for Album controller"""


class IPlaylistController(IController):
    """Interface for Playlist controller"""

    @abstractmethod
    def uow_add_songs_queue(self, song):
        """Add songs to queue"""

    @abstractmethod
    def uow_play_songs(self, song):
        """sets media list and play"""
