"""Queue command module"""

from __future__ import annotations
from typing import TYPE_CHECKING
from rkstreamer.interfaces.patterns import Command
from rkstreamer.controllers.enums import QueueEnum
if TYPE_CHECKING:
    from rkstreamer.types import (
        SongControllerType,
        SongModelType,
        SongViewType,
        AlbumControllerType,
        AlbumModelType,
        AlbumViewType,
        CommandType
    )

class SongQueueCommand(Command):
    """Song Queue command implementation"""

    def __init__(self, controller: SongControllerType):
        self.controller = controller
        self.model: SongModelType = self.controller.model
        self.view: SongViewType = self.controller.view
        self.commands = {
            QueueEnum.ADD: SongQueueAddCommand(self.controller),
            QueueEnum.REMOVE: SongQueueRemoveCommand(self.controller),
            QueueEnum.PLAY: SongQueuePlayCommand(self.controller),
        }

    def execute(self, user_input: str):
        if user_input == '-q':
            queue = self.model.queue.get_indexed_queue
            self.view.display_queue(queue)
        elif len(user_input) > 2:
            user_input = user_input.replace('-q', '')
            try:
                enum_obj = QueueEnum(user_input[0])
                command: CommandType = self.commands.get(enum_obj)
                command.execute(user_input.replace(
                    user_input[0], '').split(','))
            except (ValueError, AttributeError) as exc:
                print(f"{exc.__class__, 'Invalid input. Please try again'}")


class SongQueueAddCommand(Command):
    """Song Queue - Add command"""

    def __init__(self, controller: SongControllerType):
        self.controller = controller
        self.model: SongModelType = self.controller.model

    def execute(self, user_input: list):
        for number in user_input:
            song = self.model.select(int(number))
            self.controller.uow_add_songs_queue(song)


class SongQueueRemoveCommand(Command):
    """Song Queue - Remove command"""

    def __init__(self, controller: SongControllerType):
        self.controller = controller
        self.model: SongModelType = self.controller.model
        self.view: SongViewType = self.controller.view

    def execute(self, user_input: list):
        songs = self.model.queue.remove(user_input)
        for song in songs:
            self.view.remove_media(song)


class SongQueuePlayCommand(Command):
    """Song Queue - Play command"""

    def __init__(self, controller: SongControllerType):
        self.controller = controller
        self.model: SongModelType = self.controller.model
        self.view: SongViewType = self.controller.view

    def execute(self, user_input: list):
        song = self.model.queue.fetch(user_input[0])
        self.controller.uow_play_songs_remove_loaded_before(song)


class AlbumQueueCommand(Command):
    """Album queue command"""

    def __init__(self, controller: AlbumControllerType):
        self.controller = controller
        self.model: AlbumModelType = self.controller.model
        self.view: AlbumViewType = self.controller.view
        self.commands = {
            QueueEnum.ADD: AlbumQueueAddCommand(self.controller),
            QueueEnum.REMOVE: SongQueueRemoveCommand(self.controller),
            QueueEnum.PLAY: SongQueuePlayCommand(self.controller)
        }

    def execute(self, user_input: str):
        if user_input == '-q':
            queue = self.model.queue.get_indexed_queue
            self.view.display_queue(queue)
        elif len(user_input) > 2:
            user_input = user_input.replace('-q', '')
            try:
                enum_obj = QueueEnum(user_input[0])
                command: CommandType = self.commands.get(enum_obj)
                command.execute(user_input.replace(
                    user_input[0], '').split(','))
            except (ValueError, AttributeError) as exc:
                print(f"{exc.__class__, 'Invalid input. Please try again'}")


class AlbumQueueAddCommand(Command):
    """Album Queue - Add command"""

    def __init__(self, controller: SongControllerType):
        self.controller = controller
        self.model: AlbumModelType = self.controller.model

    def execute(self, user_input: list):
        for number in user_input:
            song = self.model.select_song_from_album(int(number))
            self.controller.uow_add_songs_queue(song)


class ReSongQueueCommand(Command):
    """Recommended songs - Queue Command"""

    def __init__(self, controller: SongControllerType):
        self.controller = controller
        self.model: SongModelType = self.controller.model
        self.view: SongViewType = self.controller.view
        self.commands = {
            QueueEnum.ADD: ReSongQueueAddCommand(self.controller),
            QueueEnum.REMOVE: ReSongQueueRemoveCommand(self.controller),
            QueueEnum.PLAY: ReSongQueuePlayCommand(self.controller)
        }

    def execute(self, user_input: str):
        if user_input == '-r':
            queue = self.model.queue.get_rsongs
            self.view.display_rsongs_queue(queue)
        elif len(user_input) > 2:
            user_input = user_input.replace('-r', '')
            try:
                enum_obj = QueueEnum(user_input[0])
                command: CommandType = self.commands.get(enum_obj)
                command.execute(user_input.replace(
                    user_input[0], '').split(','))
            except (ValueError, AttributeError) as exc:
                print(f"{exc.__class__, 'Invalid input. Please try again'}")


class ReSongQueueAddCommand(Command):
    """RS Queue - Add Command"""

    def __init__(self, controller: SongControllerType):
        self.controller = controller
        self.model: SongModelType = self.controller.model
        self.view: SongViewType = self.controller.view

    def execute(self, user_input: list):
        for number in user_input:
            rsong = self.model.queue.get_rsong_index(int(number))
            rsong.stream_url = self.model.get_song_url(rsong.token)
            rsong.status = 'Loaded'
            self.controller.uow_add_songs_queue(rsong)


class ReSongQueueRemoveCommand(Command):
    """RS Queue - Remove Command"""

    def __init__(self, controller: SongControllerType):
        self.controller = controller
        self.model: SongModelType = self.controller.model
        self.view: SongViewType = self.controller.view

    def execute(self, user_input: list):
        for index in user_input:
            self.model.queue.remove_rsong_index(int(index))


class ReSongQueuePlayCommand(Command):
    """RS Queue - Play command"""

    def __init__(self, controller: SongControllerType):
        self.controller = controller
        self.model: SongModelType = self.controller.model
        self.view: SongViewType = self.controller.view

    def execute(self, user_input: list):
        song = self.model.queue.get_rsong_index(int(user_input[0]))
        if song:
            song.stream_url = self.model.get_song_url(song.token)
            song.status = 'Loaded'
            self.controller.uow_play_songs_remove_loaded(song)
