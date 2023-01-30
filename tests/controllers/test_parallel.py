import taegel.models as models
import taegel.views as views

import taegel.controllers as ctr

import tests
import os

from taegel.models.types import AlbumInfo


def test_pool_to_generate_albums_with_a_list_of_playlist_urls() -> None:
    album_list: list[AlbumInfo] = ctr.parallel.select_playlist_videos([
        'https://www.youtube.com/playlist?list=PLF452AA85EDA3A598',  # it has invalid videos
        'https://yt.artemislena.eu/playlist?list=PLBFE349B5F9B3E8C1',  # from a invidus instance
    ], os.getcwd(), os.cpu_count())

    assert len(album_list[0].sources) == 10
    assert len(album_list[1].sources) == 13


def test_interface_download_handler_progress_communication() -> None:
    if os.getenv('SKIP_INTERFACE') in ['true', '1']:
        views.log.warning('skiping interface test')
        return

    tmp_target: str = tests.create_tmp_directory()

    album: AlbumInfo = models.types.AlbumInfo(target=tmp_target, sources=[
        'https://www.youtube.com/watch?v=Ne0_v4Yadmm',  # invalid link
        'https://www.youtube.com/watch?v=Ne0_v4YadmM',  # valid link
    ])

    ctr.parallel.download_handler(album, 2, len(album.sources))

    if os.getenv('DELETE_TMP') not in ['false', '0']:
        tests.remove_tmp_directory(tmp_target)
