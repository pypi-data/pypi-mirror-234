"""Tests: Get related songs"""

from rkstreamer.services.network import PyRequests
from rkstreamer.models import JioSaavnSongModel

pyrequests = PyRequests()

song_model = JioSaavnSongModel(pyrequests)

recomm_songs = song_model.get_related_songs('elrx2wXJ')

print(recomm_songs)