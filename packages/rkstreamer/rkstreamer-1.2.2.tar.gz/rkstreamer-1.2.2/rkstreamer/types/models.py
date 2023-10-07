"""
Types used by domain models
"""

from typing import NewType
from rkstreamer.models.data import (
    Song,
    SongSearch,
    SongQueue,
    Album,
    AlbumSearch,
    Playlist,
    PlaylistSearch)
from rkstreamer.interfaces import (
    ISongModel,
    ISongQueue,
    IAlbumModel,
    IPlaylistModel,
    ISongProvider,
    IAlbumProvider,
    IPlaylistProvider)

# Interfaces

SongModelType = NewType('ISongModel', ISongModel)
SongQueueModelType = NewType('ISongQueue', ISongQueue)
AlbumModelType = NewType('IAlbumModel', IAlbumModel)
PlaylistModelType = NewType('IPlaylistModel', IPlaylistModel)

# Primitives

SongRawType = NewType('SongRaw', dict[str,str])
SongListRawType = NewType('SongListRaw', list[SongRawType])
AlbumRawType = NewType('AlbumRaw', dict[str,str])
AlbumListRawType = NewType('SongListRaw', list[AlbumRawType])
PlaylistRawType = NewType("PlaylistRaw", dict[str,str])
PListRawType = NewType("PlaylistListRaw", list[PlaylistRawType])

# Data

SongType = NewType('Song', Song)
SongSearchType = NewType('SongSearch', SongSearch)
SongQueueType = NewType('SongQueue', SongQueue)
SongListType = NewType('SongList', list[SongType])
SongIndexType = NewType('SongIndex', dict[int, SongType])
SongUrl = NewType('SongUrl', str)
SongSearchIndexType = NewType('SongSearchIndex', dict[int,SongSearchType])
SongQueueIndexType = NewType('SongQueueIndex', dict[int,SongQueueType])

AlbumType = NewType('Album', Album)
AlbumSearchType = NewType('AlbumSearch', AlbumSearch)
AlbumSearchIndexType = NewType('AlbumSearchIndex', dict[int,AlbumSearchType])

PlaylistType = NewType('Playlist', Playlist)
PlaylistSearchType = NewType('PlaylistSearch', PlaylistSearch)
PlaylistSearchIndexType = NewType('AlbumSearchIndex', dict[int,PlaylistSearchType])

SongProviderType = NewType("SongProvider", ISongProvider)
AlbumProviderType = NewType("AlbumProvider", IAlbumProvider)
PlaylistProviderType = NewType("PlaylistProvider", IPlaylistProvider)
