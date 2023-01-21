import taegel.models as models
import taegel.views as views
import taegel.controllers as ctr

from taegel.models.types import AlbumInfo, ArgsFiltered
from typing import List
from re import Match


def _id_to_url(id: str) -> str:
    return f'https://www.youtube.com/{id}'


def filter_arguments(url_list: List[str]) -> ArgsFiltered:
    """Given an list of links, or random strings, it will return an object
    that separates the videos from the playlist in a way to select just the
    valid links or the ones that was not appended to the video or playlists
    lists.

    Also, when any string has a valid playlist or video ID, it will get that
    ID to generate a valid link to work with. Witch means that Invidius, for
    example, URL's will work just fine with that function.

    :param List[str] url_list: Unordered list provided by the user.
    """
    videos: List[str] = []
    videos_id: List[str] = []
    playlists: List[str] = []
    playlists_id: List[str] = []

    for url in url_list:
        is_valid: None | Match = models.regex.valid.search(url)
        is_playlist: None | Match = models.regex.playlist.search(url)
        is_video: None | Match = models.regex.video.search(url)

        has_vid: None | Match = models.regex.video_id.search(url)
        url_vid: None | str = has_vid.group() if has_vid is not None else None

        has_pid: None | Match = models.regex.playlist_id.search(url)
        url_pid: None | str = has_pid.group() if has_pid is not None else None

        if (url_pid in playlists_id or url_vid in videos_id
                or url in videos + playlists):
            views.log.warning(f'you already gave that url [black]{url}[/]')

        elif not is_valid and has_vid:
            views.log.warning(f'wait, it has an video id! [black]{url}[/]')
            videos_id.append(url_vid)

        elif not is_valid and has_pid:
            views.log.warning(f'wait, it has an playlist id! [black]{url}[/]')
            playlists_id.append(url_pid)

        elif is_video:
            views.log.print(f'video detected [black]{url}[/]')
            videos.append(url)

        elif is_playlist:
            views.log.print(f'palylist detected [black]{url}[/]')
            playlists.append(url)

    videos.extend(list(map(_id_to_url, videos_id)))
    playlists.extend(list(map(_id_to_url, playlists_id)))

    return models.types.ArgsFiltered(raw=url_list, videos=videos,
                                      playlists=playlists)


def get_videos(url_list: List[str]) -> List[str]:
    """Filters the list looking just for valid video only links (not playlists)
    and returns a list with unique video URL's.

    :param List[str] url_list: List of mixed links provided by the user.
    """
    result_videos: List[str] = []

    for url in url_list:
        is_valid: None | Match = models.types.regex_url.search(url)
        is_playlist: None | Match = models.types.regex_playlist.search(url)

        if is_valid and not is_playlist and url not in result_videos:
            result_videos.append(url)

    return result_videos


def get_playlist(url_list: List[str]) -> List[str]:
    """Filters the list looking just for valid playlist only links (not videos)
    and returns a list with unique playlist URL's.

    :param List[str] url_list: List of mixed links provided by the user.
    """
    result_playlist: List[str] = []

    for url in url_list:
        is_valid: None | Match = models.types.regex_url.search(url)
        is_playlist: None | Match = models.types.regex_playlist.search(url)

        if is_valid and is_playlist and url not in result_playlist:
            result_playlist.append(url)

    return result_playlist


def gen_album_list(videos: List[str], playlists: List[str],
                   root_target: str) -> List[AlbumInfo]:
    """Return a list with a ``AlbumInfo`` object for each playlist. The
    ``target`` field for each of them will be the ``target`` parameter plus the
    playlist name, or the ``target`` itself for the videos only URL's (they
    will be trated as a single playlist).

    :param List[str] url_list: List with a bunch of links given by the user.
    :param str target: User's target directory to download the files
    """
    # the result will be empty if any indiviual videos was provided
    album_list: List[AlbumInfo] = [] if len(videos) < 1 else [
        models.types.AlbumInfo(target=root_target, sources=videos)
    ]

    # todo: use more than one process to fetch the playlist content
    for url in playlists:
        album: AlbumInfo = ctr.youtube.playlist_to_album(url, root_target)
        album_list.append(album)

    return album_list
