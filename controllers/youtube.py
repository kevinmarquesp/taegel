import models
import views

import time
import pytube
import os

from typing import List
from multiprocessing.connection import Connection
from models.objects import Data
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
    views.out.print(f'Fetching data from {url} (be patiente)')

    youtube: YouTube = pytube.YouTube(url)
    video: Stream | None = youtube.streams.filter(only_audio=True).first()

    views.out.print(f'Saving [cyan]{youtube.title}[/] in  [cyan]{target}[/]')
    target_file: str = video.download(output_path=target)

    basename, _ = os.path.splitext(target_file)
    os.rename(target_file, basename + '.mp3')
    pipe.send(True)
