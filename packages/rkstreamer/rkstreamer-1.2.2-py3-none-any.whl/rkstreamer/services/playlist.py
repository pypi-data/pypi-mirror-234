"""
Playlist provider - API
"""

from __future__ import annotations
from typing import TYPE_CHECKING
from html import unescape
from urllib.parse import urlencode
from urllib3 import disable_warnings
from rkstreamer.interfaces.provider import IPlaylistProvider
from rkstreamer.utils.helper import LANGUAGES

if TYPE_CHECKING:
    from rkstreamer.types import (
        SongUrl,
        PListRawType,
        NetworkProviderType,
        NetworkProviderResponseType
    )

disable_warnings()  # Function to suppress the SSL Verification error.


class JioSaavnPlaylistProvider(IPlaylistProvider):
    """Jio Saavn - Playlist provider API"""

    API_BASE = "https://www.jiosaavn.com/api.php"

    PARAMS_DEFAULT = {'api_version': 4, '_format': 'json', '_marker': 0,
                      'ctx': 'web6dot0'}
    PARAMS_FTEXT = {'api_version': 4, '_format': 'text', '_marker': 0,
                    'ctx': 'web6dot0'}  # Format set to text for plist songs download.

    plist_search = {'__call': 'search.getPlaylistResults', 'p': 1, 'q': ''}

    plist_download = {'__call': 'webapi.get', 'token': '', 'type': 'playlist',
                      'includeMetaTags': 0, 'p': 1, 'n': 50}

    def __init__(self, client: NetworkProviderType) -> None:
        self.client = client

    def search_playlists(self, search_string: str, **kwargs) -> PListRawType:
        """Playlist search"""
        self.plist_search['q'] = search_string
        language = [kwargs.get('lang'),] \
            if kwargs.get('lang') \
            else LANGUAGES
        plist_request = self.client.get(
            url=f"{self.API_BASE}?{urlencode(self.plist_search|self.PARAMS_DEFAULT, safe='+')}")
        return self._parse_playlist(plist_request, lang=language)

    def _parse_playlist(self, response: NetworkProviderResponseType, **kwargs) -> PListRawType:
        """Parse playlist response"""
        return [{'name': plist['title'],
                'token': plist['perma_url'].split('/')[-1],
                'language': plist['more_info']['language'],
                 'song_count': plist['more_info']['song_count']}
                for plist in response.json()['results']
                if plist['more_info']['language'] in kwargs.get('lang')]

    def select_playlist(self, arg: str, **kwargs) -> PListRawType:
        self.plist_download['token'] = arg
        plist_select = self.client.get(
            url=self.API_BASE, params=self.plist_download | self.PARAMS_FTEXT)
        return self._parse_playlist_songs(plist_select, **kwargs)

    def _parse_playlist_songs(self, response: NetworkProviderResponseType, **kwargs) -> PListRawType:
        """Parse songs from playlist selection"""
        if kwargs.get('view'):
            return [{'name': unescape(song['song_for_player'])}
                    for song in response.json()['fullsongs']]

        return [{'name': unescape(song['song_for_player']),
                'stream_url': self._change_plist_song_url(song['download_url'])}
                for song in response.json()['fullsongs']]

    def _change_plist_song_url(self, song_url: str) -> SongUrl:
        """Change plist song urls with latest JS CDN host"""
        if 'SAR' in song_url:  # for handling URLs - https://h.saavncdn.com/*/SAR-*.mp3
            return song_url
        rm_pattern = song_url.removeprefix(
            'http://h.saavncdn.com').removeprefix('https://h.saavncdn.com').removesuffix('.mp3')
        new_pattern = "https://aac.saavncdn.com"+rm_pattern+"_96.mp4"
        return new_pattern
