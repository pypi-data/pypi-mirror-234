"""
DI module for domain models
"""

from ._interface import ABC, abstractmethod


class IModel(ABC):
    """Interface for model"""

    @abstractmethod
    def search(self, search_string: str, **kwargs):
        """Search item"""

    @abstractmethod
    def select(self, selection: int, **kwargs):
        """Select item"""


class IQueue(ABC):
    """Interface for queue"""

    @abstractmethod
    def add(self, entity):
        """Add entity to queue"""

    @abstractmethod
    def remove(self, index: int):
        """Remove entity from queue and updates the index"""

    @abstractmethod
    def fetch(self, index: int):
        """fetch entity from queue index"""

    @property
    @abstractmethod
    def get_queue(self):
        """Returns the queue"""

    @property
    @abstractmethod
    def get_indexed_queue(self):
        """Returns the indexed queue"""


class ISongModel(IModel):
    """Interface for Song model"""

    @abstractmethod
    def get_song_url(self, data):
        """Get Song stream url"""

    @abstractmethod
    def get_related_songs(self, data):
        """Load related songs"""


class ISongQueue(IQueue):
    """Inferace for Song queue"""

    @abstractmethod
    def add_related_songs(self, songs):
        """Add related songs to queue"""

    @abstractmethod
    def update_qstatus(self, status, stream_url):
        """Update the main queue status"""

    @abstractmethod
    def pop_rsong(self):
        """Get related song from Rqueue list"""

    @abstractmethod
    def get_rsong_index(self, index: int):
        """Get related song by index"""

    @abstractmethod
    def remove_rsong_index(self, index: int):
        """Remove related song by index"""

    @abstractmethod
    def update_rqueue(self, rsongs):
        """Updates the related song queue"""

    @property
    @abstractmethod
    def get_rsongs(self):
        """Get rsongs list"""


class IAlbumModel(IModel):
    """Inferface for Album model"""

    @abstractmethod
    def select_song_from_album(self, selection: int):
        """Select song from album"""


class IPlaylistModel(IModel):
    """Interface for Playlist model"""
