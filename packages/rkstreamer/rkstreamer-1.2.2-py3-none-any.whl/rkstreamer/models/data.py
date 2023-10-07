"""Data Models"""

from ._model import dataclass, field

@dataclass(unsafe_hash=True)
class SongBase():
    """Base for song model"""
    name: str = field(hash=True, compare=True)
    id: str = field(hash=False, compare=False, default=None, repr=False)
    artists: str = field(hash=False, compare=False, default=None)
    music: str = field(hash=False, compare=False, default=None)
    album_name: str = field(hash=False, compare=False, default=None)
    album_id: str = field(hash=False, compare=False, default=None, repr=False)
    duration: int = field(hash=False, compare=False, default=None, repr=False)


@dataclass(unsafe_hash=True)
class SongSearch(SongBase):
    """Song Search model'"""
    status: str = field(hash=False, compare=False, default='Fetched', repr=False)
    token: str = field(hash=False, compare=False, default=None, repr=False)
    language: str = field(hash=False, compare=False, default=None, repr=False)


@dataclass(unsafe_hash=True)
class Song(SongSearch):
    """Song model"""
    stream_url: str = field(hash=False, compare=False, default=None)


@dataclass
class SongQueue():
    """Song Queue model"""
    songs: list = field(default_factory=list)


@dataclass
class AlbumBase():
    """Album base model"""
    name: str = field(hash=True, compare=True)
    id: str = field(hash=False, compare=False, default=None, repr=False)
    artists: str = field(hash=False, compare=False, default=None)
    music: str = field(hash=False, compare=False, default=None)

@dataclass
class AlbumSearch(AlbumBase):
    """Album search model"""
    song_count: int = field(hash=False, default=None)
    language: str = field(hash=False, compare=False, default=None, repr=False)

@dataclass
class Album(AlbumSearch):
    """Album model"""
    songs: list = field(default_factory=list)


@dataclass
class PlaylistBase():
    """Playlist base model"""
    name: str = field(hash=True, compare=True)

@dataclass
class PlaylistSearch(PlaylistBase):
    """Playlist search model"""
    token: str = field(default=None, repr=False)
    song_count: int = field(default=None)
    language: str = field(hash=False, compare=False, default=None, repr=False)


@dataclass
class Playlist(PlaylistSearch):
    """Playlist model"""
    songs: dict = field(default_factory=dict)
