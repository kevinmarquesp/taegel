import taegel.models as models
import taegel.views as views
import taegel.controllers as ctr

import os
import tests

from taegel.models.types import AlbumInfo


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
