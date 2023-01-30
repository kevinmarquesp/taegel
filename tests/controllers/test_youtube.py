import taegel.controllers as ctr

import os
import rich.console

from taegel.models.types import AlbumInfo
from rich.console import Console

console: Console = rich.console.Console()


def test_playlist_fetching_to_generate_an_album() -> None:
    album: AlbumInfo = ctr.youtube.playlist_to_album('https://yt.artemislena.eu/playlist?list=PLBFE349B5F9B3E8C1',
                                                     os.getcwd())
    assert len(album.sources) == 13
