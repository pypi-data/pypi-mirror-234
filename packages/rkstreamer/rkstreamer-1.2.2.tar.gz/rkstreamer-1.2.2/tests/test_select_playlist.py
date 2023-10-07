"""Tests: Select playlist"""

from rkstreamer.services.network import PyRequests
from rkstreamer.models.playlist import JioSaavnPlaylistModel


proxy = {'https': 'http://127.0.0.1:8888'}
test = JioSaavnPlaylistModel(network_provider=PyRequests(verify=False, proxy=proxy))
test.search('akon')
search = test.select(1)
print(search)