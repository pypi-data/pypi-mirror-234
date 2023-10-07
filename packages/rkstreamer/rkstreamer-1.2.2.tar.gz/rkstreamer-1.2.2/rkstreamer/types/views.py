"""Types used by Views"""

from typing import NewType
from rkstreamer.interfaces import (
    ISongView,
    IAlbumView,
    IPlaylistView
)

SongViewType = NewType('ISongView', ISongView)
AlbumViewType = NewType('IAlbumView', IAlbumView)
PlaylistViewType = NewType('IPlaylistView', IPlaylistView)
