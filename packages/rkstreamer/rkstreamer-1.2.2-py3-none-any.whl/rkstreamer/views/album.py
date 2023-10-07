"""
Album view implementation module
"""

from rkstreamer.types import MusicPlayerControlsType
from rkstreamer.views.song import JioSaavnSongView


class JioSaavnAlbumView(JioSaavnSongView):
    """Jio Saavn Album view"""

    def __init__(self, player: MusicPlayerControlsType) -> None:
        self.player = player
        super().__init__(player)

    def display(self, entity) -> None:
        print('\n\033[33m\033[01m***Albums Search***\033[0m\n')
        for count, album in entity.items():
            print(f"{count}- {album.name} ({album.language})")
            print(f"Music - {album.artists}")
            print(f"Song Count - {album.song_count}")
            print()

    def display_album_songs(self, entity) -> None:
        """Display album songs"""
        print('\n\033[33m\033[01m***Albums Songs***\033[0m\n')
        for count, song in entity.songs.items():
            print(f"A{count}- {song.name}")
            print(f"Artists - {song.artists}")
            print()
