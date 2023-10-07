"""Models - Album"""

from typing import Optional
from rkstreamer.interfaces.models import IAlbumModel
from rkstreamer.models.song import JioSaavnSongQueue
from rkstreamer.models.data import Album, AlbumSearch, Song
from rkstreamer.services.album import JioSaavnAlbumProvider
from rkstreamer.services.song import JioSaavnSongProvider
from rkstreamer.types import (
    AlbumType,
    AlbumSearchType,
    AlbumListRawType,
    AlbumSearchIndexType,
    NetworkProviderType,
    SongQueueModelType,
    SongType,
    SongListRawType,
    SongListType,
    SongIndexType
)
from rkstreamer.models.exceptions import (
    InvalidInput
)


class JioSaavnAlbumModel(IAlbumModel):
    """Album model implemented for Jio Saavn service"""

    def __init__(self, network_provider: NetworkProviderType) -> None:
        self.network_provider = network_provider
        self.stream_provider = JioSaavnAlbumProvider(
            client=self.network_provider)
        self.song_provider = JioSaavnSongProvider(client=self.network_provider)
        self.queue: SongQueueModelType = JioSaavnSongQueue()
        self.indexed_search_albums = {}
        self.indexed_album_songs = {}
        self._recomm_song_index = 1

    def _create_song(self, **kwargs) -> SongType:
        return Song(**kwargs)

    def _create_search_album(self, **kwargs) -> AlbumSearchType:
        return AlbumSearch(**kwargs)

    def _create_album(self, **kwargs) -> AlbumType:
        return Album(**kwargs)

    def _create_search_album_index(self, albums: AlbumListRawType) -> AlbumSearchIndexType:
        self.indexed_search_albums = {count: self._create_search_album(**album)
                                      for count, album in enumerate(albums, 1)}
        return self.indexed_search_albums

    def _create_album_song_index(self, albums: AlbumListRawType) -> SongIndexType:
        self.indexed_album_songs = {count: self._create_song(**album)
                                    for count, album in enumerate(albums, 1)}
        return self.indexed_album_songs

    def _create_recomm_song(self, songs: SongListRawType) -> SongIndexType:
        recomm_songs = {}
        _songs: SongListType = [self._create_song(**song) for song in songs]
        for song in _songs:
            if song not in self.queue.rsongs_copy_:
                recomm_songs.update({self._recomm_song_index: song})
                self._recomm_song_index += 1
        return recomm_songs

    def search(self, search_string: str, **kwargs) -> AlbumSearchIndexType:
        search_result = self.stream_provider.search_albums(
            search_string, **kwargs)
        return self._create_search_album_index(search_result)

    def select(self, selection: int, **kwargs) -> AlbumType:
        selected_album = self.indexed_search_albums.get(int(selection))
        if selected_album:
            album_songs_raw = self.stream_provider.select_album(
                selected_album.id, **kwargs)
            selected_album.__dict__.update(
                {'songs': self._create_album_song_index(album_songs_raw)})
            return self._create_album(**selected_album.__dict__)
        raise InvalidInput("Invalid album selection input provided.")

    def select_album_using_id(self, album_id: str) -> AlbumType:
        """Select album using ID"""
        album_songs_raw = self.stream_provider.select_album_id(album_id)
        album_songs_raw.update(
            {'songs': self._create_album_song_index(album_songs_raw['songs'])})
        return self._create_album(**album_songs_raw)

    def select_song_from_album(self, selection: int) -> Optional[SongType]:
        """Selecting song from the album"""
        selected_song = self.indexed_album_songs.get(selection)
        if selected_song:
            song_url = self.song_provider.select_song(selected_song.token)
            if song_url:
                selected_song.__dict__.update({'stream_url': song_url})
                selected_song.__dict__.update({'status': 'Loaded'})
                return selected_song
        raise InvalidInput("Invalid album song selection input provided.")

    def get_related_songs(self, data: str) -> SongIndexType:
        """Gets recommended songs using song_id and updates the RQueue"""
        recomm_songs_raw: SongListRawType = self.song_provider.get_recomm_songs(
            data)
        if recomm_songs_raw:
            return self._create_recomm_song(recomm_songs_raw)

    def get_song_url(self, data: str) -> str:
        """Get the song's stream url using Enc Url Token - used for rsongs download"""
        stream_url = self.song_provider.select_song(data)
        return stream_url
