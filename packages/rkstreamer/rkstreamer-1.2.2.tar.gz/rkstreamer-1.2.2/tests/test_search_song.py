"""Tests: Search songs"""

from rkstreamer.services.network import PyRequests
from rkstreamer.services.song import JioSaavnSongProvider


test = JioSaavnSongProvider(client=PyRequests(verify=False))
search = test.search_songs('pokkal pokkum')
assert search[0].items()
print(search[0].items())
