"""
Design patterns implementation
"""

from __future__ import annotations
import threading
from typing import Union, TYPE_CHECKING
from rkstreamer.interfaces.controllers import ISongController
from rkstreamer.interfaces.patterns import Command
from rkstreamer.controllers.enums import GotoAlbumEnum
if TYPE_CHECKING:
    from rkstreamer.types import (
        SongControllerType,
        SongType,
        SongModelType,
        SongViewType,
        AlbumModelType,
        AlbumViewType,
        CommandType
    )


class ControllerUtils(ISongController):
    """Generic controller utils for handling songs"""

    def __init__(
            self,
            model: Union[SongModelType, AlbumModelType],
            view: Union[SongViewType, AlbumViewType]) -> None:

        self.model = model
        self.view = view

        self.view.set_controller_callback(self.uow_update_song_status)

        _ = threading.Timer(30, self.monitor_queue_pull_rsong)
        _.setDaemon(True)
        _.start()

    def uow_update_song_status(self, status: str, stream_url: str):
        """Updating song status in queue to "Played"
        if the song has been selected to play from search or from queue
        This function fetchs the rsongs for the playing song and updates rsong list."""
        song = self.model.queue.update_qstatus(status, stream_url)
        if song and len(self.model.queue.get_rsongs) <= 50:
            self.uow_add_rsongs_rqueue(song.id)

    def monitor_queue_pull_rsong(self):
        """Pull rsong by monitoring the queue songs status"""
        if self.model.queue.check_status(self.model.queue.get_queue):
            get_rsong = self.model.queue.pop_rsong()
            if get_rsong:
                get_rsong.stream_url = self.model.get_song_url(get_rsong.token)
                self.uow_add_songs_queue(get_rsong)
        threading.Timer(45, self.monitor_queue_pull_rsong).start()

    def uow_add_songs_queue(self, song: SongType):
        """UOW: Add songs to queue & media list. Doesn't play it"""
        self.model.queue.add(song)
        self.view.add_media(song)

    def uow_add_rsongs_rqueue(self, data: str):
        """UOW: Add Recommended songs to RQueue
        :data - song_id"""
        recomm_songs = self.model.get_related_songs(data)
        if recomm_songs:
            self.model.queue.update_rqueue(recomm_songs)

    def uow_play_songs_remove_loaded(self, song: SongType):
        """UOW: changes the queue status to played &
        play the media - suitable for rsongs play"""
        self.model.queue.change_loaded_status()
        self.model.queue.add(song)
        self.view.play_media(song)

    def uow_play_songs_remove_loaded_before(self, song: SongType):
        """UOW: changes the status of queue song to played (only those are before this song)"""
        self.model.queue.change_loaded_status_before(song)
        self.view.play_media(song)


class GotoAlbumCommand(Command):
    """Goto Album Command"""

    def __init__(self, controller: SongControllerType):
        self.controller = controller
        self._model = controller.model
        self.model: AlbumModelType = self.controller.goto_album
        self.view: SongViewType = self.controller.view
        self.commands = {
            GotoAlbumEnum.ADD: GotoAlbumAddCommand(self.controller),
            GotoAlbumEnum.PLAY: GotoAlbumPlayCommand(self.controller),
        }
        self.current_album_id = ''

    def execute(self, user_input):
        if user_input == '-g':
            album_id = self._model.queue.current_playing_song.album_id
            if self.current_album_id != album_id:
                # self.controller.goto_album_songs.clear() # flush dict before saving new songs.
                self.controller.goto_album_songs = self.model.select_album_using_id(album_id)
                self.current_album_id = album_id
                self.view.display_gotoalbum_songs(self.controller.goto_album_songs)
            else:
                self.view.display_gotoalbum_songs(self.controller.goto_album_songs)
        elif len(user_input) > 2:
            user_input = user_input.replace('-g', '')
            try:
                enum_obj = GotoAlbumEnum(user_input[0])
                command: CommandType = self.commands.get(enum_obj)
                command.execute(user_input.replace(
                    user_input[0], '').split(','))
            except (ValueError, AttributeError) as exc:
                print(f"{exc.__class__, 'Invalid input. Please try again'}")


class GotoAlbumAddCommand(Command):
    """Goto Album - Add Command"""

    def __init__(self, controller: SongControllerType):
        self.controller = controller
        self.model: SongModelType = self.controller.model
        self.view: SongViewType = self.controller.view

    def execute(self, user_input: list):
        for number in user_input:
            album_song = self.controller.goto_album_songs.songs.get(
                int(number))
            if album_song:
                album_song.stream_url = self.model.get_song_url(album_song.token)
                album_song.status = 'Loaded'
                self.controller.uow_add_songs_queue(album_song)


class GotoAlbumPlayCommand(Command):
    """Goto Album - Play Command"""

    def __init__(self, controller: SongControllerType):
        self.controller = controller
        self.model: SongModelType = self.controller.model
        self.view: SongViewType = self.controller.view

    def execute(self, user_input: list):
        for number in user_input:
            album_song = self.controller.goto_album_songs.songs.get(
                int(number))
            if album_song:
                album_song.stream_url = self.model.get_song_url(album_song.token)
                album_song.status = 'Loaded'
                self.controller.uow_play_songs_remove_loaded(album_song)


class PlayerControlsCommand(Command):
    """Player Controls"""

    def __init__(self, controller: SongControllerType):
        self.controller = controller
        self.model: SongModelType = self.controller.model
        self.view: SongViewType = self.controller.view

    def execute(self, user_input: str):
        if user_input.lower().startswith('-c'):
            self.view.player_input(user_input.replace('-c', ''))
