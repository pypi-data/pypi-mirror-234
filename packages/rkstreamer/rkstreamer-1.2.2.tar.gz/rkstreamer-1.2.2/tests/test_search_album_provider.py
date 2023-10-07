"""Test: Search albums"""

from rkstreamer.services.network import PyRequests
from rkstreamer.services.album import JioSaavnAlbumProvider


test = JioSaavnAlbumProvider(client=PyRequests(verify=False))
search = test.search_albums('madhrasapattinam')
assert search[0].items()
print(search[0].items())