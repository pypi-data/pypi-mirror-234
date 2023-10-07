"""Tests: Search playlist provider"""

from rkstreamer.services.network import PyRequests
from rkstreamer.services.playlist import JioSaavnPlaylistProvider


proxy = {'https': 'http://127.0.0.1:8888'}
test = JioSaavnPlaylistProvider(client=PyRequests(verify=False, proxy=proxy))
search = test.search_playlists('akon')
print(search)
