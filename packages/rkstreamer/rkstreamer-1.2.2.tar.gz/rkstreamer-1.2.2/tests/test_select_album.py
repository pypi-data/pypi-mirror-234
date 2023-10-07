"""Test: Select Album"""

from rkstreamer.services.network import PyRequests
from rkstreamer.models.album import JioSaavnAlbumModel


test = JioSaavnAlbumModel(network_provider=PyRequests(verify=False))
search = test.search('madhrasapattinam')
select = test.select(1)
print(select)