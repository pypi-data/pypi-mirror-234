"""Tests: Search playlist"""

from rkstreamer.services.network import PyRequests
from rkstreamer.models.playlist import JioSaavnPlaylistModel


proxy = {'https': 'http://127.0.0.1:8888'}
test = JioSaavnPlaylistModel(network_provider=PyRequests(verify=False, proxy=proxy))
search = test.search('akon')
print(search)