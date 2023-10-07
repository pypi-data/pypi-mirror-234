"""Type used by Controllers"""

from typing import NewType
from rkstreamer.interfaces import (
    ISongController,
    IAlbumController,
    IPlaylistController
)

SongControllerType = NewType('ISongController', ISongController)
AlbumControllerType = NewType('IAlbumController', IAlbumController)
PlaylistControllerType = NewType('IPlaylistController', IPlaylistController)
