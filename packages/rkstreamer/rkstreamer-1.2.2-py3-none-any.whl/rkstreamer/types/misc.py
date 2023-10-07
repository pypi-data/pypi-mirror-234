"""Types"""

from typing import NewType
from rkstreamer.interfaces import (
    Command,
    INetworkProvider,
    INetworkProviderResponse,
    MusicPlayer,
    MusicPlayerControls)

NetworkProviderType = NewType('INetworkProvider', INetworkProvider)
NetworkProviderResponseType = NewType('INetworkProviderResponse', INetworkProviderResponse)
CommandType = NewType('Command', Command)
MusicPlayerType = NewType('MusicPlayer', MusicPlayer)
MusicPlayerControlsType = NewType('MusicPlayerControls', MusicPlayerControls)