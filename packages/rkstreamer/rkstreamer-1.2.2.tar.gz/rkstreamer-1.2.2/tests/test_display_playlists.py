"""Tests: Playlists"""

from rkstreamer.services.player import PyVLCPlayer
from rkstreamer.controllers.playlist import JioSaavnPlaylistController
from rkstreamer.models.playlist import JioSaavnPlaylistModel
from rkstreamer.views.playlist import JioSaavnPlaylistView
from rkstreamer.services.network import PyRequests

proxy = {'https': 'http://127.0.0.1:8888'}
pyrequests = PyRequests(proxy=None)

test = JioSaavnPlaylistController(
    model=JioSaavnPlaylistModel(pyrequests),
    view=JioSaavnPlaylistView(player=PyVLCPlayer()))

while True:
    user_input = input("Enter the playlist name: ")
    if user_input:
        test.handle_input(user_input)
