"""Test: Select song from album"""

from rkstreamer.services.network import PyRequests
from rkstreamer.models.album import JioSaavnAlbumModel


test = JioSaavnAlbumModel(network_provider=PyRequests(verify=False))
search = test.search('madhrasapattinam')
print(search)
select = test.select(1)
print(select)
song = test.select_song_from_album(1)
print(song)
