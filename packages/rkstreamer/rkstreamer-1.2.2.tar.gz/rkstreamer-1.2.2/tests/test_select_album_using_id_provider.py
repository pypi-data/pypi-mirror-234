"""Test: Get album using ID"""

from rkstreamer.services.network import PyRequests
from rkstreamer.services.album import JioSaavnAlbumProvider


test = JioSaavnAlbumProvider(client=PyRequests(verify=False))
search = test.select_album_id('qKErkhPpdTE_')
print(search)