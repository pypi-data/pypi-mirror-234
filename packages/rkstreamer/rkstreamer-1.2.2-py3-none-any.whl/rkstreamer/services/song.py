"""
Songs Provider API
"""

import random
from html import unescape
from urllib.parse import quote_plus, urlencode
from urllib3 import disable_warnings
from rkstreamer.interfaces.provider import ISongProvider
from rkstreamer.utils.helper import LANGUAGES
from rkstreamer.types import (
    SongListRawType,
    NetworkProviderType,
    NetworkProviderResponseType
)
disable_warnings()  # Function to suppress the SSL Verification error.


class JioSaavnSongProvider(ISongProvider):
    """Jio Saavn - Song provider API"""

    API_BASE = "https://www.jiosaavn.com/api.php"

    PARAMS_DEFAULT = {'api_version': 4, '_format': 'json', '_marker': 0,
                      'ctx': 'web6dot0'}

    # n - num of results, q- search string
    song_search = {'__call': 'search.getResults', 'p': 1, 'q': '', 'n': ''}

    song_download = {'__call': 'song.generateAuthToken',
                     'url': '', 'bitrate': ''}  # url - enc media url, bitrate - 160 or 320

    entity_station = {'__call': 'webradio.createEntityStation', 'entity_id': '',
                      'entity_type': 'queue', 'freemium': '', 'shared': ''}

    # k - count of rsongs.
    recomm_songs = {'__call': 'webradio.getSong', 'stationid': '', 'k': ''}

    def __init__(self, client: NetworkProviderType) -> None:
        self.client = client

    def search_songs(self, search_string: str, **kwargs) -> SongListRawType:
        """Search songs using the search string"""
        self.song_search['q'] = quote_plus(search_string)
        self.song_search['n'] = kwargs.get('num') or 3
        self.song_download['bitrate'] = kwargs.get('bitrate') or 320
        language = [kwargs.get('lang'),] \
            if kwargs.get('lang') \
            else LANGUAGES
        response = self.client.get(
            url=f"{self.API_BASE}?{urlencode(self.song_search|self.PARAMS_DEFAULT, safe='+')}")
        return self._parse_songs(response, lang=language)

    def _parse_songs(self, response: NetworkProviderResponseType, **kwargs) -> SongListRawType:
        """Parsing songs info from search songs call"""
        return [{'name': unescape(song['title']),
                'id': song['id'],
                 'album_name': unescape(song['more_info']['album']),
                 'music': song['more_info']['music'][:50] if song['more_info']['music'] else '',
                 'artists': unescape(song['subtitle'].replace(f" - {song['more_info']['album']}", '')),
                 'language': song['language'],
                 'duration': song['more_info']['duration'],
                 'token': song['more_info']['encrypted_media_url'],
                 'album_id': song['more_info']['album_url'].split('/')[-1]}
                for song in response.json()['results'] if song['language'] in kwargs.get('lang')]

    def select_song(self, arg: str, **kwargs) -> str:
        self.song_download['url'] = arg  # Encrypted URL
        response = self.client.get(
            url=self.API_BASE, params=self.song_download | self.PARAMS_DEFAULT)
        return self._parse_song_url(response)

    def _parse_song_url(self, response: NetworkProviderResponseType) -> str:
        """Get the song download URL"""
        auth_url = response.json()['auth_url']
        stream_url = self.client.get(url=auth_url, allow_redirects=False)
        return stream_url.headers['Location']

    def _get_station_id(self, song_id: str) -> str:
        self.entity_station['entity_id'] = f'["{song_id}"]'
        sid_response = self.client.get(
            url=self.API_BASE, params=self.entity_station | self.PARAMS_DEFAULT)
        sid = sid_response.json()['stationid']
        return sid

    def _parse_recomm_songs(self, response: NetworkProviderResponseType) -> SongListRawType:
        try:
            return [{'name': unescape(song['song']['title']),
                    'id': song['song']['id'],
                     'album_name': unescape(song['song']['more_info']['album']),
                     'music': song['song']['more_info']['music'][:50] if song ['song']['more_info']['music'] else '',
                     'artists': unescape(song['song']['subtitle'].replace(f" - {song['song']['more_info']['album']}", '')),
                     'duration': song['song']['more_info']['duration'],
                     'token': song['song']['more_info']['encrypted_media_url'],
                     'album_id': song['song']['more_info']['album_url'].split('/')[-1]}
                    for key, song in response.json().items() if key != 'stationid']
        except (KeyError, IndexError, TypeError):
            print("Get Rsongs failed")

    def get_recomm_songs(self, song_id: str, **kwargs) -> SongListRawType:
        """Get recommended songs from song_id"""
        station_id = self._get_station_id(song_id)
        self.recomm_songs['stationid'] = station_id
        self.recomm_songs['k'] = kwargs.get('rsongs') or random.randint(10, 15)
        recomm_songs = self.client.get(
            url=self.API_BASE, params=self.recomm_songs | self.PARAMS_DEFAULT)
        return self._parse_recomm_songs(recomm_songs)
