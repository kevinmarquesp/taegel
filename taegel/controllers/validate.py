import taegel.models as models
import taegel.views as views
import taegel.controllers as ctr

import rich.console  # debug

from taegel.models.objects import DownloadData
from typing import List, Tuple
from rich.console import Console
from re import Match

console: Console = rich.console.Console()


def urllist_split(url_list: List[str]) -> Tuple[List[str], List[str]]:
    """Return two separated lists, one of only with video URL's and the other
    with the playlist URL's. It also filter the repeated URL's and the
    invalid ones from booth lists.

    :param List[str] url_list: List with a bunch of links given by the user.
    """
    playlists: List[str] = []
    videos: List[str] = []

    for url in url_list:
        is_yturl: None | Match = models.objects.regex_url.search(url)
        is_playlist: None | Match = models.objects.regex_playlist.search(url)

        if is_yturl is None:
            views.out.warting(f'{url} is not a youtube url')
            continue

        if is_playlist is not None:
            views.out.print(f'Playlist detected: {url}')

            if url not in playlists:
                playlists.append(url)

        else:
            if url not in videos:
                videos.append(url)

    return playlists, videos


def get_data(url_list: List[str], target: str) -> List[DownloadData]:
    """Return a list with a ``DownloadData`` object for each playlist. The
    ``target`` field for each of them will be the ``target`` parameter plus the
    playlist name, or the ``target`` itself for the videos only URL's (they
    will be trated as a single playlist).

    :param List[str] url_list: List with a bunch of links given by the user.
    :param str target: User's target directory to download the files
    """
    playlists: List[str] = []
    videos: List[str] = []
    playlists, videos = urllist_split(url_list)

    result: List[DownloadData] = [] if len(videos) < 1 else [
        models.objects.DownloadData(target=target, sources=videos)
    ]

    for url in playlists:
        data: DownloadData = ctr.youtube.playlist_videos(url, target)
        result.append(data)

    return result
