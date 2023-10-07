"""
Services - Music Player Provider
"""

import threading
from typing import Optional, Callable
from vlc import Instance, MediaListPlayer, MediaList, State, MediaPlayer, Media
from rkstreamer.interfaces.player import MusicPlayer, MusicPlayerControls


class PyVLCPlayerInstance(MusicPlayer):
    """VLC Player implementation"""

    def __init__(self) -> None:
        self.songs_list = []
        self.instance: Instance = Instance()
        self.player: MediaListPlayer = self.instance.media_list_player_new()
        self.media_list: MediaList = None
        self._init_media_list()

    def _init_media_list(self):
        """Creates a new media list adds to MLplayer"""
        self.media_list = self.instance.media_list_new()
        self.player.set_media_list(self.media_list)

    def _set_new_media(self):
        """Sets the songs_list as new media list"""
        self.media_list = self.instance.media_list_new(self.songs_list)
        self.player.set_media_list(self.media_list)

    def add_media(self, media_url: str):
        """Appends the new media to media_list"""
        if media_url not in self.songs_list:
            self.songs_list.append(media_url)
            self._set_new_media()

    def add_medias(self, media_urls: list):
        """Appends the new media from LIST to media_list."""
        self.songs_list = media_urls #this is required for play_media.
        self.media_list = self.instance.media_list_new(self.songs_list)
        self.player.set_media_list(self.media_list)

    def remove_media(self, media_url: str):
        """Removes media from media list and sets the updated list"""
        if media_url in self.songs_list:
            self.songs_list.remove(media_url)
            self._set_new_media()

    def play_media(self, media_url: str):
        """Plays the media from the song list.
        It checks if the media_url is already part of song_list.
        If yes, then play that media by getting the index.
        If not, then append it to the media_list, set it and then play the added song."""
        if media_url in self.songs_list:
            song_index = self.songs_list.index(media_url)
            return self.player.play_item_at_index(song_index)
        else:
            self.add_media(media_url)
            self._set_new_media()
            return self.player.play_item_at_index(self.songs_list.index(media_url))

    @property
    def get_media_player(self):
        """Gets the instance of Mplayer used"""
        return self.player.get_media_player()


class PyVLCPlayer(MusicPlayerControls):
    """Handler for Player Controls"""

    def __init__(
            self,
            mlplayer_factory: Optional[PyVLCPlayerInstance] = None) -> None:

        self.mlplayer_factory = mlplayer_factory if mlplayer_factory else PyVLCPlayerInstance()
        self.mlplayer_controls = MediaListPlayerControls(self.mlplayer_factory.player)
        self.mplayer_controls = MediaPlayerControls(self.mlplayer_factory.get_media_player)
        # Media List player will invoke MediaPlayerControls and pass it other controls.
        self.volume_controls = VolumeControls(self.mplayer_controls)
        self.state_controls = StateControls(self.mplayer_controls)
        self.misc_controls = MiscControls(self.mplayer_controls)
        self.playback_controls = PlaybackControls(self.mplayer_controls)
        self.monitor_state = MonitorState(self.mplayer_controls)

    def player_controls(self, user_input: str):
        """Handler method for Player Controls"""

        if user_input.lower().startswith(('+', '-', 'v')):
            self.volume_controls.manage(user_input)

        elif user_input.lower().startswith(('n','pr')):
            if user_input == 'n':
                self.mlplayer_controls.next_song()
            elif user_input == 'pr':
                self.mlplayer_controls.previous_song()

        elif user_input.lower().startswith(('p', 'q', 'e', 's')):
            self.state_controls.manage(user_input)

        elif user_input.lower().startswith(('lo', 'co', 't')):
            self.misc_controls.manage(user_input)

        elif user_input.lower().startswith(('<', '>')):
            self.playback_controls.manage(user_input)


class MediaPlayerControls():
    """Player Controls"""

    def __init__(self, media_player_instance: MediaPlayer) -> None:
        self.media = media_player_instance
        self.devices = []
        self.volume = 100
        self.state = None
        self.get_devices()

    @property
    def get_song_url_from_player(self):
        """Get Media URL from MediaPlayer instance"""
        media_playing: Media = self.media.get_media()
        return media_playing.get_mrl()

    def get_devices(self) -> list:
        """Gets the available audio output devices"""
        mods = self.media.audio_output_device_enum()
        count = 0
        if mods:
            mod = mods
            while mod:
                mod = mod.contents
                self.devices.append(
                    {'id': count, 'device': mod.device,
                        'description': (mod.description).decode()}
                )
                count += 1
                mod = mod.next

    def display_devices(self) -> None:
        """Pretty print list of output devices."""
        for device in self.devices:
            print(f"ID: {device['id']}")
            print(f"Device: {device['description']}")
        print()

    def select_device(self, selection_: int) -> None:
        """Selects the output device."""
        for device in self.devices:
            if device['id'] == selection_:
                print(f'Switching output to "{device["description"]}"')
                self.media.audio_output_device_set(None, device['device'])
                break
        print()

    def get_volume(self) -> int:
        """Get current volume value"""
        setattr(self, "volume", self.media.audio_get_volume())
        return self.volume

    def set_volume(self, volume: int) -> int:
        """Set volume between 0 - 100"""
        if volume < 0:
            print("Cannot set volume below 0")
        elif volume <= 100:
            self.media.audio_set_volume(volume)
            self.volume = volume
        else:
            print("Cannot set volume above 100")

    def increase_volume(self, volume: int) -> None:
        """Increase volume"""
        self.get_volume()
        if self.volume < 100:
            if (self.volume+volume) <= 100:
                self.media.audio_set_volume(
                    self.volume+volume
                )
                print(f"Volume: {self.media.audio_get_volume()}")
            else:
                self.media.audio_set_volume(100)
                self.volume = 100

    def decrease_volume(self, volume: int) -> None:
        """Decrease volume"""
        self.get_volume()
        if self.volume > 0:
            if (self.volume-volume) >= 0:
                self.media.audio_set_volume(
                    self.volume-volume
                )
                print(f"Volume: {self.media.audio_get_volume()}")
            else:
                self.media.audio_set_volume(0)
                self.volume = 0

    def get_length(self):
        """Get full track length: milliseconds"""
        return self.media.get_length()

    def get_time(self) -> int:
        """Get current media time: milliseconds"""
        return self.media.get_time()

    def remaining_time(self) -> int:
        """Get the remaining track time : seconds"""
        return (self.get_length()-self.get_time())/1000

    def seek_forward(self, time: int) -> None:
        """Seek forward"""
        self.media.set_time(
            self.get_time()+(time*1000)
        )

    def seek_backward(self, time: int) -> None:
        """Seek forward"""
        self.media.set_time(
            self.get_time()-(time*1000)
        )

    def get_state(self):
        """Get media state"""
        return self.media.get_state()

    def play(self):
        """Play"""
        self.media.play()

    def pause(self):
        """Pause"""
        self.media.pause()

    def stop(self):
        """Stop"""
        self.media.stop()


class MediaListPlayerControls():
    """Media List Player Controls"""

    def __init__(self, media_list_player: MediaListPlayer) -> None:
        self.media_list_player = media_list_player
        self.media_player = MediaPlayerControls(
            self.media_list_player.get_media_player())

    def play_index(self, index: int):
        """Plays item at certain index"""
        result = self.media_list_player.play_item_at_index(index)
        if result == 0:
            return self.media_player.get_song_url_from_player
        print("!*! Invalid Index/Song not found !*!")
        return None

    def next_song(self):
        """Plays next song in the list"""
        _next = self.media_list_player.next()
        if _next == 0:
            return self.media_player.get_song_url_from_player
        print("!*! Reached End of Media List !*!")
        return None

    def previous_song(self):
        """Plays previous song in the list"""
        _previous = self.media_list_player.previous()
        if _previous == 0:
            return self.media_player.get_song_url_from_player
        print("!*! Reached Start of Media List !*!")
        return None

    def play_start(self):
        """Play the first song in media list - start from beginning"""
        return self.media_list_player.play_item_at_index(0)

    def play(self):
        """Starts playing the media list"""
        return self.media_list_player.play()

    def stop(self):
        """Stops the playing media list"""
        return self.media_list_player.stop()

    def pause(self):
        """Pauses the playing media list"""
        return self.media_list_player.pause()


class StateControls():
    """Handler for State Controls"""

    def __init__(self, mplayer: MediaPlayerControls) -> None:
        self.mplayer_controls = mplayer
        self.input = None

    def manage(self, user_input: str):
        """Manages the player state"""

        self.input = user_input

        if self.input.lower() == 'p':

            if self.mplayer_controls.get_state() == State(4) or self.mplayer_controls.get_state() == State(5):  # 4 - Paused
                print("Resuming")
                self.mplayer_controls.play()

            elif self.mplayer_controls.get_state() == State(3):  # 3 - Playing (See State Enum definit.)
                print("Paused")
                self.mplayer_controls.pause()

        elif self.input.lower() == 's':
            print("Stopped")
            self.mplayer_controls.stop()

        elif (self.input.lower() == 'q' or self.input.lower() == 'e'):
            raise SystemExit("Bye! Bye!")


class VolumeControls():
    """Handler for Volume Controls"""

    def __init__(self, controls: MediaPlayerControls) -> None:
        self.controls = controls
        self.input = None

    def manage(self, user_input: str):
        """Manages volume increase/decrease"""

        self.input = user_input

        if self.input.startswith('+') and self.input.strip('+').isnumeric():
            vol = self.input.strip('+')
            if vol:
                self.controls.increase_volume(int(vol))
                # print(f"Volume: {self.controls.get_volume()}")

        elif self.input.startswith('-') and self.input.strip('-').isnumeric():
            vol = self.input.strip('-')
            if vol:
                self.controls.decrease_volume(int(vol))
                # print(f"Volume: {self.controls.get_volume()}")

        elif self.input.lower().startswith('v'):
            if self.input.lower().strip('v') and self.input.lower().strip('v').isnumeric():
                vol = self.input.lower().strip('v')
                if vol:
                    self.controls.set_volume(int(vol))
                    # print(f"Volume: {self.controls.get_volume()}")
            else:
                print(f"Volume: {self.controls.get_volume()}")


class MiscControls():
    """Handler for Misc Controls"""

    def __init__(self, controls: MediaPlayerControls) -> None:
        self.controls = controls
        self.input = None

    def manage(self, user_input: str):
        """Manages the Misc Options"""

        self.input = user_input

        if self.input.lower().startswith('lo'):
            # Pretty prints the available output devices.
            self.controls.display_devices()

        elif self.input.lower().startswith('co') and self.input.lower().strip('co').isnumeric():
            dev = self.input.lower().strip('co')
            if dev:
                self.controls.select_device(int(dev))

        elif self.input.lower().startswith('t'):
            print(f"Time Remaining {self.controls.remaining_time()} seconds")


class PlaybackControls():
    """Handler for Playback Controls"""

    def __init__(self, controls: MediaPlayerControls) -> None:
        self.controls = controls
        self.input = None

    def manage(self, user_input: str):
        """Manages the Playback Options"""

        self.input = user_input

        if self.input.startswith('>') and self.input.strip('>').isnumeric():
            seek = self.input.strip('>')
            if seek:
                self.controls.seek_forward(int(seek))
                print(
                    f"Forward: {seek}, RT - {self.controls.remaining_time()} seconds")

        elif self.input.startswith('<') and self.input.strip('<').isnumeric():
            seek = self.input.strip('<')
            if seek:
                self.controls.seek_backward(int(seek))
                print(
                    f"Backward: {seek}, RT - {self.controls.remaining_time()} seconds")


class MonitorState():
    """Handler for State Controls"""

    callback: Callable

    def __init__(self, controls: MediaPlayerControls) -> None:
        self.controls = controls
        _ = threading.Timer(5, self.manage)
        _.setDaemon(True)
        _.start()

    def manage(self):
        """Thread loop to monitor player status and update main song queue"""
        if self.controls.get_state() == State(3):
            self.callback('\033[31mPlayed\033[0m', self.controls.get_song_url_from_player)
        threading.Timer(15, self.manage).start()
        # if self.controls.get_state() == State(4):
        # elif self.controls.get_state() == State(6):
        # elif self.controls.get_state() == State(5):
