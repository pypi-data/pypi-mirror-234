"""Tests: Display songs"""

from rkstreamer.services.player import PyVLCPlayer
from rkstreamer.controllers.song import JioSaavnSongController
from rkstreamer.models.song import JioSaavnSongModel
from rkstreamer.views.song import JioSaavnSongView
from rkstreamer.services.network import PyRequests

proxy = {'https': 'http://127.0.0.1:8888'}
pyrequests = PyRequests(proxy=None)

test = JioSaavnSongController(
    model=JioSaavnSongModel(pyrequests),
    view=JioSaavnSongView(player=PyVLCPlayer()))

while True:
    user_input = input("Enter the song name: ")
    if user_input:
        test.handle_input(user_input)
