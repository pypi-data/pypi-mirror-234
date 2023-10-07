"""
RK Streamer

A command-line music player that allows you to play/stream songs, albums, playlists.

Author: Ray A.
Email: ray@raysecure.ml

(c) 2023 Ray A. All rights reserved.

License:
This project is licensed under the terms of the MIT License.
See the LICENSE file for more information.
"""

from rkstreamer.state import State, StateMachine
from rkstreamer.services.player import PyVLCPlayer
from rkstreamer.services.network import PyRequests
from rkstreamer.models import (
    JioSaavnSongModel,
    JioSaavnAlbumModel,
    JioSaavnPlaylistModel
)
from rkstreamer.views import (
    JioSaavnSongView,
    JioSaavnAlbumView,
    JioSaavnPlaylistView
)
from rkstreamer.controllers import (
    JioSaavnSongController,
    JioSaavnAlbumController,
    JioSaavnPlaylistController
)

# proxy = {'https': 'http://127.0.0.1:8888'}
pyrequests = PyRequests(proxy=None)

song_controller = JioSaavnSongController(
    model=JioSaavnSongModel(pyrequests),
    view=JioSaavnSongView(player=PyVLCPlayer())
)

album_controller = JioSaavnAlbumController(
    model=JioSaavnAlbumModel(pyrequests),
    view=JioSaavnAlbumView(player=PyVLCPlayer())
)

plist_controller = JioSaavnPlaylistController(
    model=JioSaavnPlaylistModel(pyrequests),
    view=JioSaavnPlaylistView(player=PyVLCPlayer())
)

song = State(
    "song",
    "Enter the song name: ",
    song_controller
)

album = State(
    "album",
    "Enter the album name: ",
    album_controller
)

playlist = State(
    "plist",
    "Enter the playlist name: ",
    plist_controller
)


def main():
    """Main entrypoint for rkstreamer"""
    print(r"""

    *** RK Streamer ***

    @Powered by Jio Saavn

    """)

    streamer = StateMachine()
    streamer.add_state({'song': song, 'album': album, 'plist': playlist})
    streamer.set_start_state('song')
    streamer.trigger()

if __name__ == '__main__':
    main()
