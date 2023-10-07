### RK Music Streamer

A command-line music streamer that allows you to stream songs, albums, playlists. <br>
**@Powered by [Jio Saavn](https://www.jiosaavn.com) Web APIs**

---
#### Prerequisites
- Python 3.9.x or above.
- VLC player must be installed. <br> _This application uses the VLC player for streaming and python-vlc bindings for interaction with libvlc library._ <br>
(Install from [VLC](https://www.videolan.org/vlc/))

#### Dependencies
- [requests](https://pypi.org/project/requests/)
- [python-vlc](https://pypi.org/project/python-vlc/)
---
#### Installation
```
> python3 -m pip install rkstreamer
$ pip/pip3 install rkstreamer
```
---
#### Launch
```
Application can be launched by entering the following in the command prompt/terminal:

> python3 -m rkstreamer
or
> rkstreamer

```
---
#### Features
- Has 3 main modes - Song, Album, Playlist.
- Main modes can be activated/toggled using the '--' switches:
    - **--song** - Song Mode.
    - **--album** - Album Mode.
    - **--plist** - Playlist Mode.
- Default mode is 'Song Search' Mode.
- Has 2 Queue modes and 1 Misc mode which can be activated using '-' switches:
    - **-q** - displays Songs Queue.
    - **-r** - displays Recommended Songs Queue.
    - **-g** - displays Go-to-Album Songs.
- Supports search parameters for Songs, Albums Mode.
    - **Format:** 'search string' -n:number -l:language -b:bitrate

- Has 3 Action Modes:
    - **a(index)** - Add Media.
    - **p(index)** - Play Media.
    - **r(index)** - Remove Media.
    **Index** - Index shown in the queue/search output.
- Above action modes can be combined with Queue and Misc modes for managing the media - _See **Controls** section for more details._

---
#### Controls

**-c** - Player control mode.<br>
Actions should be suffixed with the '-c' switch:

- **Player controls**:
    - **-cp** - play/pause.
    - **-cs** - stop.
    - **-cn** - next song.
    - **-cpr** - previous song.
    - **-clo** - list output devices.
    - **-cco(index)** - change output to device (index - shown by list output devices command).

- **Volume controls**:
    - **-cv** - displays Current volume.
    - **-cv(number)** - sets the volume.
    - **-c+(number)** - Volume Increase.
    - **-c-(number)** - Volume Decrease. <br>
    **Number** - value to set.

- **Playback controls**:
    - **-c>(seconds)** - seek forward.
    - **-c<(seconds)** - seek backward.
    - **-ct** - show remaining time.

**-q** - Song Queue mode. <br>
Actions should be suffixed with the '-q' switch:
- **-qa(index)** - Adds the song to queue.
- **-qr(index)** - Removes the song from queue.
- **-qp(index)** - Plays the song from queue.

**-r** - Recommended Songs Queue mode. <br>
Actions should be suffixed with the '-r' switch:
- **-ra(index)** - Adds the song to queue.
- **-rr(index)** - Removes the song from queue.
- **-rp(index)** - Plays the song from queue.

**-g** - Go-to-Album Songs list. <br>
Actions should be suffixed with the '-g' switch:
- **-ga(index)** - Adds the album song to song queue.
- **-gp(index)** - Plays the album song.


---
#### Examples

```
Song Mode:
(--song)

> Enter the song name: song1 -n:5 -l:tamil -b:320
(-n, -l, -b are optional)

Legends:
(
    Search string - song1,
    Number of results to display - 5,
    Language - tamil,
    Bitrate - 320kpbs
)

1 - Play the 1st song from search output.


Album Mode:
(--album)

> Enter the album name: album1 -n:5 -l:tamil

(-n, -l are optional)

Legends:
(
    Search string - album1,
    Number of results to display - 5,
    Language - tamil
)

- Album can be selected using the index number.
- Song in the albums can be played using a(index).

1 - Select the 1st album from search list.
a1 - Play the album's 1st song.


Playlist Mode:
(--plist)

> Enter the playlist name: playlist1 -l:tamil -n:5
(-n, -l are optional)

Legends:
(
    Search string - playlist1,
    Number of results to display - 5,
    Language - tamil
)

1 - Play the 1st playlist displayed in search output.
-v(index) - View the playlist songs

***When a song is playing***

> Enter the song name: -q
(Displays the song queue)

> -r
(Displays the recommended song queue)

> -g
(Displays the playing song's album songs)

> -qr1 - removes the first index song from queue
> -qp1 - plays the first index song from queue
> -qa1 - adds the first index song from search list

Similar behaviors for -r (recommended songs), -g (go-to-album).


Volume Controls:
  -cv - Shows current volume
  -c+10 - Increase volume by 10
  -c-10 - Decrease volume by 10
  -cv100 - Set volume to 100

Playback controls:
  -c>10 - Forward by 10 seconds
  -c<10 - Backward by 10 seconds
  -ct - Show remaining time

```

