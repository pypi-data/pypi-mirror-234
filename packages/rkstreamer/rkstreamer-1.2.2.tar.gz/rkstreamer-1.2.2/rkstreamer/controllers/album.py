"""Album controller - module"""

import re
from typing import Union
from rkstreamer.interfaces.patterns import Command
from rkstreamer.controllers.enums import ControllerEnum
from rkstreamer.controllers.queue import AlbumQueueCommand, ReSongQueueCommand
from rkstreamer.controllers.patterns import (
    ControllerUtils,
    PlayerControlsCommand,
    GotoAlbumCommand
)
from rkstreamer.utils.helper import parse_input
from rkstreamer.utils.helper import ALBUM_PATTERN
from rkstreamer.types import (
    AlbumModelType,
    AlbumViewType,
    AlbumControllerType,
    CommandType
)


class JioSaavnAlbumController(ControllerUtils):
    """Album Controller implemented for Jio Saavn model"""

    def __init__(self, model: AlbumModelType, view: AlbumViewType) -> None:
        self.model = model
        self.goto_album = model
        self.view = view
        self.commands = {
            ControllerEnum.QUEUE: AlbumQueueCommand(self),
            ControllerEnum.CONTROLS: PlayerControlsCommand(self),
            ControllerEnum.RQUEUE: ReSongQueueCommand(self),
            ControllerEnum.GTALBUM: GotoAlbumCommand(self),
            'as': AlbumSongSelectCommand(self),
            str: AlbumSearchCommand(self),
            int: AlbumSelectCommand(self),
        }
        self.goto_album_songs = {}
        super().__init__(model, view)

    def handle_input(self, user_input: Union[str, int]):
        """Handles the user input"""
        if user_input.startswith('-'):
            re_match = re.match(r'(-\w{1})', user_input)
            try:
                enum_obj = ControllerEnum(re_match.group(1))
                command: CommandType = self.commands.get(enum_obj)
                command.execute(user_input)
            except (ValueError, AttributeError):
                print("Invalid input. Please try again")
        else:
            album_selection = re.match(r'[aA](\d+)', user_input)
            if album_selection:
                song_selection = album_selection.group(1)
                command: CommandType = self.commands.get('as')
                command.execute(song_selection)
            else:
                input_type = type(parse_input(user_input))
                command: CommandType = self.commands.get(input_type)
                command.execute(user_input)


class AlbumSearchCommand(Command):
    """Album Search"""

    def __init__(self, controller: AlbumControllerType):
        self.controller = controller
        self.model: AlbumModelType = self.controller.model
        self.view: AlbumViewType = self.controller.view

    def execute(self, user_input: str):
        match_input = re.match(ALBUM_PATTERN, user_input)
        if match_input:
            album = match_input.group('album').strip()
            match_input.groupdict().pop('album')
            search_results = self.model.search(album, **match_input.groupdict())
            self.view.display(search_results)
        else:
            print("Invalid Input provided!")


class AlbumSelectCommand(Command):
    """Song Select command implementation"""

    def __init__(self, controller: AlbumControllerType):
        self.controller = controller
        self.model: AlbumModelType = self.controller.model
        self.view: AlbumViewType = self.controller.view

    def execute(self, user_input: int):
        album = self.model.select(int(user_input))
        self.view.display_album_songs(album)


class AlbumSongSelectCommand(Command):
    """Song Select command implementation"""

    def __init__(self, controller: AlbumControllerType):
        self.controller = controller
        self.model: AlbumModelType = self.controller.model
        self.view: AlbumViewType = self.controller.view

    def execute(self, user_input: int):
        album_song = self.model.select_song_from_album(int(user_input))
        self.controller.uow_play_songs_remove_loaded(album_song)
