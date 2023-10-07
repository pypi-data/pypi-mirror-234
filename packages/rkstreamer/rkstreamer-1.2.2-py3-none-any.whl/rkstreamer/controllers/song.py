"""Controller Implementation module"""

import re
from typing import Union
from rkstreamer.interfaces.patterns import Command
from rkstreamer.controllers.enums import ControllerEnum
from rkstreamer.controllers.queue import SongQueueCommand, ReSongQueueCommand
from rkstreamer.controllers.patterns import (
    ControllerUtils,
    PlayerControlsCommand,
    GotoAlbumCommand
)
from rkstreamer.models.album import JioSaavnAlbumModel
from rkstreamer.utils.helper import parse_input
from rkstreamer.utils.helper import SONG_PATTERN
from rkstreamer.types import (
    SongModelType,
    SongViewType,
    SongControllerType,
    CommandType
)


class JioSaavnSongController(ControllerUtils):
    """Song Controller implemented for Jio Saavn model"""

    def __init__(self, model: SongModelType, view: SongViewType) -> None:
        self.model = model
        self.view = view
        self.goto_album = JioSaavnAlbumModel(
            network_provider=model.network_provider)
        self.commands = {
            ControllerEnum.QUEUE: SongQueueCommand(self),
            ControllerEnum.CONTROLS: PlayerControlsCommand(self),
            ControllerEnum.RQUEUE: ReSongQueueCommand(self),
            ControllerEnum.GTALBUM: GotoAlbumCommand(self),
            str: SongSearchCommand(self),
            int: SongSelectCommand(self),
        }
        self.goto_album_songs = {}
        super().__init__(model, view)

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


class SongSearchCommand(Command):
    """Song Search command implementation"""

    def __init__(self, controller: SongControllerType):
        self.controller = controller
        self.model: SongModelType = self.controller.model
        self.view: SongViewType = self.controller.view

    def execute(self, user_input: str):
        match_input = re.match(SONG_PATTERN, user_input)
        if match_input:
            song = match_input.group('song').strip()
            match_input.groupdict().pop('song')
            search_results = self.model.search(song, **match_input.groupdict())
            self.view.display(search_results)
        else:
            print("Invalid Input provided!")


class SongSelectCommand(Command):
    """Song Select command implementation"""

    def __init__(self, controller: SongControllerType):
        self.controller = controller
        self.model: SongModelType = self.controller.model
        self.view: SongViewType = self.controller.view

    def execute(self, user_input: int):
        song = self.model.select(user_input)
        self.controller.uow_play_songs_remove_loaded(song)
