"""Tests: Get album using ID"""

from rkstreamer.services.network import PyRequests
from rkstreamer.models.album import JioSaavnAlbumModel


test = JioSaavnAlbumModel(network_provider=PyRequests(verify=False))
search = test.select_album_using_id('qKErkhPpdTE_')
print(search)