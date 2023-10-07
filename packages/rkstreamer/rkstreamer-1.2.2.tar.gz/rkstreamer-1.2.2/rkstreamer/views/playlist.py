"""
Playlist view implementation module
"""

from rkstreamer.types import MusicPlayerControlsType
from rkstreamer.views.song import JioSaavnSongView


class JioSaavnPlaylistView(JioSaavnSongView):
    """Jio Saavn Playlist view"""

    def __init__(self, player: MusicPlayerControlsType) -> None:
        self.player = player
        super().__init__(player)

    def display(self, entity) -> None:
        print('\n\033[33m\033[01m***Playlist Search***\033[0m\n')
        for count, playlist in entity.items():
            print(f"{count}- {playlist.name} ({playlist.language})")
            print(f"Song Count - {playlist.song_count}")
            print()

    def display_playlist_songs(self, entity) -> None:
        """Display playlist songs"""
        print('\n\033[33m\033[01m***Playlist Songs***\033[0m\n')
        for count, song in enumerate(entity.songs):
            print(f"#{count}- {song.name}")
        print()

    def add_media_list(self, songs_list: list):
        """Add songs list to player mlist"""
        return self.player.mlplayer_factory.add_medias(songs_list)
