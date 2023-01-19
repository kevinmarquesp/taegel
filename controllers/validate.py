import models
import views
import controllers

import rich.console  # debug

from models.objects import Data
from typing import List
from rich.console import Console
from re import Match

console: Console = rich.console.Console()


# todo: add a docstring
def urllist_split(url_list: List[str]) -> (List[str], List[str]):
    playlists: List[str] = []
    videos: List[str] = []

    for url in url_list:
        is_yturl: None | Match = models.objects.regex_url.search(url)
        is_playlist: None | Match = models.objects.regex_playlist.search(url)

        if is_yturl is None:
            views.out.warting(f'{url} is not a youtube url', use_console=True)
            continue

        if is_playlist is not None:
            views.out.print(f'Playlist detected: {url}', use_console=True)

            if url not in playlists:
                playlists.append(url)

        else:
            if url not in videos:
                videos.append(url)

    return playlists, videos


# todo: add a docstring
def get_data(url_list: List[str], target: str) -> List[Data]:
    playlists: List[str] = []
    videos: List[str] = []
    playlists, videos = urllist_split(url_list)

    result: List[Data] = [] if len(videos) < 1 else [
        models.objects.Data(target=target, sources=videos)
    ]

    for url in playlists:
        data: Data = controllers.youtube.playlist_videos(url, target)
        result.append(data)

    return result
