import taegel.models as models
import taegel.views as views

import pytube
import os

from typing import List
from multiprocessing.connection import Connection
from taegel.models.objects import Data
from pytube import Playlist, YouTube, Stream


# todo: add a docstring
@views.progress.idle('Fetching...')
def playlist_videos(url: str, target: str) -> Data:
    views.out.print(f'Getting list from: {url}')

    playlist: Playlist = pytube.Playlist(url)
    target: str = f'{target}/{playlist.title}'

    sources: List[str] = []
    for url_video in playlist:
        sources.append(url_video)

    return models.objects.Data(target=target, sources=sources)


# todo: add a docstring
def download(pipe: Connection, target: str, url: str) -> None:
    try:
        youtube: YouTube = pytube.YouTube(url)
        video: Stream | None = youtube.streams.filter(only_audio=True).first()

    except Exception as err:
        pipe.send({'info': err, 'is_ok': False,  'done': True})
        return

    target_file: str = video.download(output_path=target)

    basename, _ = os.path.splitext(target_file)
    os.rename(target_file, basename + '.mp3')
    pipe.send({'info': youtube.title, 'is_ok': True,  'done': True})