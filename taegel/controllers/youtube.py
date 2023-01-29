import taegel.models as models
import taegel.views as views
import taegel.controllers as ctr

import pytube

from multiprocessing.connection import Connection
from taegel.models.types import AlbumInfo
from pytube import Playlist, YouTube, Stream
from typing import Optional


@views.progress.idle('Fetching...')
def playlist_to_album(url: str, target: str) -> AlbumInfo:
    """Given a playlist link, it will create an ``AlbumInfo`` object with a
    list of the videos within that plylist. The ``target`` field will be
    appended with the playlist name.

    :param str url: Playlist URL.
    :param str target: Target directory.
    """
    views.log.print(f'getting videos list from [black]{url}[/]')

    playlist: Playlist = pytube.Playlist(url)
    target = f'{target}/{playlist.title}'

    sources: list[str] = []
    for url_video in playlist:
        sources.append(url_video)

    return models.types.AlbumInfo(target=target, sources=sources)


def youtube_api(url: str) -> tuple[Optional[YouTube], Optional[Stream],
                                   Optional[str]]:
    """Connect to the Youtube API to get the URL information (such as title,
    channel name, etc) and the video to download.

    :param str url: Video URL to handle.
    """
    try:
        youtube: YouTube = pytube.YouTube(url)
        video: None | Stream = youtube.streams.filter(only_audio=True).first()

    except Exception as err:
        return None, None, str(err)

    return youtube, video, None


def download(cpipe: Connection, target: str, url: str) -> None:
    """Download the YouTube video and save to the ``target`` directory. Sending
    some useful log information throught the parent pipe channel.

    Also, it just send an "task failed" log if the given link is brocken or the
    video is not valid, and terminate the function without errors.

    :param Connection cpipe: Parent pipe to send the log messages.
    :param str target: Target directory path.
    :param str url: Video URL.
    """
    youtube: Optional[YouTube] = None
    video: Optional[Stream] = None
    err: Optional[str] = None

    youtube, video, err = youtube_api(url)

    # simple type error handler
    if err is not None or not (youtube and video):
        cpipe.send({
            'url': url,
            'status_ok': False,
            'task_done': True,
            'title': None,
            'channel': None,
            'task_description': 'Maybe this URL is invalid or the video is not available'
        })
        return

    target_file: Optional[str] = video.download(output_path=target)
    filesystem_log: Optional[str] = ctr.filesystem.rename_song(target_file)

    cpipe.send({
        'url': url,
        'status_ok': True,
        'task_done': True,
        'title': video.title,
        'channel': youtube.author,
        'task_description': filesystem_log
    })
