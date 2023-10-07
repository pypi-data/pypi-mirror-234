"""
Song view Implementation module
"""

from typing import Callable
from rkstreamer.interfaces.views import ISongView
from rkstreamer.types import (
    SongSearchIndexType,
    SongType,
    SongQueueIndexType,
    MusicPlayerControlsType,
    )


class JioSaavnSongView(ISongView):
    """Jio Saavn Songs View"""

    def __init__(self, player: MusicPlayerControlsType) -> None:
        self.player = player
        self.media_player = self.player.mlplayer_factory

    def display(self, entity: SongSearchIndexType) -> None:
        print('\n\033[33m\033[01m***Songs Search***\033[0m\n')
        for count, song in entity.items():
            print(f"{count}- {song.name} ({song.language})")
            print(f"Album - {song.album_name}")
            print(f"Artists - {song.artists}")
            print()

    def display_selected(self, entity: SongType) -> None:
        print(entity)

    def display_queue(self, queue: SongQueueIndexType) -> None:
        print('\n\033[33m\033[01m***Songs Queue***\033[0m\n')
        for count, song in queue.items():
            print(f"#{count} - {song.name} - {song.status}")
        print()

    def display_rsongs_queue(self, queue: list[SongType]) -> None:
        """Displays the recommended songs queue"""
        print('\n\033[33m\033[01m***Recommended Songs***\033[0m\n')
        for count, song in queue.items():
            print(f"#{count} - {song.name} - {song.artists}")
        print()

    def display_gotoalbum_songs(self, entity) -> None:
        """Display album songs"""
        print('\n\033[33m\033[01m***Albums Songs***\033[0m\n')
        print(f'\033[04m\033[01m\033[32mALBUM: {entity.name}\033[0m\n')
        for count, song in entity.songs.items():
            print(f"{count}- {song.name}")
        print()

    def play_media(self, media: SongType) -> None:
        # print(f"\n\033[31m> Playing '{media.name}' <\033[0m\n ")
        return self.media_player.play_media(media.stream_url)

    def remove_media(self, media: SongType) -> None:
        """Removes media from media list"""
        return self.media_player.remove_media(media.stream_url)

    def add_media(self, media: SongType) -> None:
        """Adding media to media list"""
        return self.media_player.add_media(media.stream_url)

    def player_input(self, user_input: str) -> None:
        """Player input"""
        self.player.player_controls(user_input)

    def set_controller_callback(self, callback_fn: Callable) -> None:
        """Updates the callback attribute to mlplayer's monitor state"""
        self.player.monitor_state.callback = callback_fn

    def play(self):
        """Play the media list"""
        return self.player.mlplayer_controls.play()

    def stop(self):
        """stop the media list"""
        return self.player.mlplayer_controls.stop()
