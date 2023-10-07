"""Playlist controller implemenation"""

import re
from typing import Union
from rkstreamer.interfaces.patterns import Command
from rkstreamer.interfaces.controllers import IController
from rkstreamer.controllers.enums import ControllerEnum
from rkstreamer.controllers.patterns import PlayerControlsCommand
from rkstreamer.controllers.queue import SongQueueCommand
from rkstreamer.utils.helper import parse_input, PLIST_PATTERN
from rkstreamer.types import (
    PlaylistModelType,
    PlaylistViewType,
    PlaylistControllerType,
    CommandType,
    SongType
)


class JioSaavnPlaylistController(IController):
    """Playlist Controller implemented for Jio Saavn model"""

    def __init__(self, model: PlaylistModelType, view: PlaylistViewType) -> None:
        self.model = model
        self.view = view
        self.commands = {
            ControllerEnum.QUEUE: SongQueueCommand(self),
            ControllerEnum.CONTROLS: PlayerControlsCommand(self),
            ControllerEnum.PVIEW: PlaylistViewCommand(self),
            str: PlaylistSearchCommand(self),
            int: PlaylistSelectCommand(self),
        }
        self.view.set_controller_callback(self.uow_update_song_status)

    def handle_input(self, user_input: Union[str, int]):
        if user_input.startswith('-'):
            re_match = re.match(r'(-\w{1})', user_input)
            try:
                enum_obj = ControllerEnum(re_match.group(1))
                command: CommandType = self.commands.get(enum_obj)
                command.execute(user_input)
            except (ValueError, AttributeError) as exc:
                print(f"{exc.__class__, 'Invalid input. Please try again'}")
        else:
            input_type = type(parse_input(user_input))
            command: CommandType = self.commands.get(input_type)
            command.execute(user_input)

    def uow_update_song_status(self, status: str, stream_url: str):
        """)override) Updating song status in queue to "Played"""
        return self.model.queue.update_qstatus(status, stream_url)

    def uow_add_songs_queue(self, playlist):
        """UOW: (override) Add songs to queue & don't play it"""
        self.model.queue.add_playlist(playlist)
        songs = []
        for song in playlist.songs:
            songs.append(song.stream_url)
        self.view.add_media_list(songs)

    def uow_play_songs(self, playlist):
        """UOW: (override) play the songs"""
        self.view.stop()
        self.model.queue.flush_queue()  # clears the queue before setting the new plist
        self.uow_add_songs_queue(playlist)
        self.view.play()

    def uow_play_songs_remove_loaded_before(self, song: SongType):
        """UOW: plays the song from song queue - playlist mode so don't change the played status
        of other songs.
        
        name of the function has to be kept as it is
        because it's being called by SongQueueCommand."""
        self.view.play_media(song)


class PlaylistSelectCommand(Command):
    """Playlist Select command implementation"""

    def __init__(self, controller: PlaylistControllerType):
        self.controller = controller
        self.model: PlaylistModelType = self.controller.model
        self.view: PlaylistViewType = self.controller.view

    def execute(self, user_input: int):
        playlist = self.model.select(user_input)
        self.controller.uow_play_songs(playlist)


class PlaylistSearchCommand(Command):
    """Album Search"""

    def __init__(self, controller: PlaylistControllerType):
        self.controller = controller
        self.model: PlaylistModelType = self.controller.model
        self.view: PlaylistViewType = self.controller.view

    def execute(self, user_input: str):
        match_input = re.match(PLIST_PATTERN, user_input)
        if match_input:
            plist = match_input.group('plist').strip()
            match_input.groupdict().pop('plist')
            search_results = self.model.search(plist, **match_input.groupdict())
            self.view.display(search_results)
        else:
            print("Invalid Input provided!")
        # search_results = self.model.search(user_input)
        # self.view.display(search_results)


class PlaylistViewCommand(Command):
    """Album Search"""

    def __init__(self, controller: PlaylistControllerType):
        self.controller = controller
        self.model: PlaylistModelType = self.controller.model
        self.view: PlaylistViewType = self.controller.view

    def execute(self, user_input: str):
        user_input = user_input.strip('-v')
        search_results = self.model.select(user_input, view=True)
        self.view.display_playlist_songs(search_results)
