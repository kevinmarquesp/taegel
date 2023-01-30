import taegel.controllers as ctr

import os

from taegel.models.types import AlbumInfo


def test_pool_to_generate_albums_with_a_list_of_playlist_urls() -> None:
    album_list: list[AlbumInfo] = ctr.parallel.select_playlist_videos([
        'https://www.youtube.com/playlist?list=PLF452AA85EDA3A598',  # it has invalid videos
        'https://yt.artemislena.eu/playlist?list=PLBFE349B5F9B3E8C1',  # from a invidus instance
    ], os.getcwd(), os.cpu_count())

    assert len(album_list[0].sources) == 10
    assert len(album_list[1].sources) == 13
