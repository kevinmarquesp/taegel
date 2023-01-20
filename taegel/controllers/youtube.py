import taegel.models as models
import taegel.views as views

import pytube
import os

from typing import List
from multiprocessing.connection import Connection
from taegel.models.objects import DownloadData
from pytube import Playlist, YouTube, Stream


@views.progress.idle('Fetching...')
def playlist_videos(url: str, target: str) -> DownloadData:
    """Given a playlist link, it will create an ``DownloadData`` object with a
    list of the videos within that plylist. The ``target`` field will be
    appended with the playlist name.

    :param str url: Playlist URL.
    :param str target: Target directory.
    """
    views.out.print(f'Getting list from: {url}')

    playlist: Playlist = pytube.Playlist(url)
    target: str = f'{target}/{playlist.title}'

    sources: List[str] = []
    for url_video in playlist:
        sources.append(url_video)

    return models.objects.DownloadData(target=target, sources=sources)


# todo: add a docstring
def download(cpipe: Connection, target: str, url: str) -> None:
    """Download the YouTube video and save to the ``target`` directory. Sending
    some useful log information throught the parent pipe channel.

    Also, it just send an "task failed" log if the given link is brocken or the
    video is not valid, and terminate the function without errors.

    :param Connection cpipe: Parent pipe to send the log messages.
    :param str target: Target directory path.
    :param str url: Video URL.
    """
    try:
        youtube: YouTube = pytube.YouTube(url)
        video: Stream | None = youtube.streams.filter(only_audio=True).first()

    except Exception as err:
        cpipe.send({'info': err, 'is_ok': False,  'done': True})
        return

    target_file: str = video.download(output_path=target)

    basename, _ = os.path.splitext(target_file)
    os.rename(target_file, basename + '.mp3')
    cpipe.send({'info': youtube.title, 'is_ok': True,  'done': True})