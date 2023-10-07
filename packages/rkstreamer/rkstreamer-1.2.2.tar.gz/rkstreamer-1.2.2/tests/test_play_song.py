"""Test - Play song"""

from rkstreamer.controllers.song import JioSaavnSongController
from rkstreamer.models.song import JioSaavnSongModel
from rkstreamer.views.song import JioSaavnSongView
from rkstreamer.services.network import PyRequests

pyrequests = PyRequests()
test = JioSaavnSongController(model=JioSaavnSongModel(pyrequests), view=JioSaavnSongView())

while True:
    user_input = input("Enter the song name: ")
    test.handle_input(user_input)