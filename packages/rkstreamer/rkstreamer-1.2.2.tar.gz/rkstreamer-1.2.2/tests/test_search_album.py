"""Test: Select album"""

from rkstreamer.services.network import PyRequests
from rkstreamer.models.album import JioSaavnAlbumModel


test = JioSaavnAlbumModel(network_provider=PyRequests(verify=False))
search = test.search('madhrasapattinam')
print(search)