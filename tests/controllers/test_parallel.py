import taegel.models as models
import taegel.views as views
import taegel.controllers as ctr

import os
import tests

from taegel.models.types import AlbumInfo


def test_interface_download_handler_progress_communication():
    if os.getenv('SKIP_INTERFACE') not in ['false', 'False', 'FALSE', '0']:
        views.log.warning('skiping interface test')
        return

    tmp_target: str = tests.create_tmp_directory()

    album: AlbumInfo = models.types.AlbumInfo(target=tmp_target, sources=[
        'https://www.youtube.com/watch?v=Ne0_v4Yadmm',  # invalid link
        'https://www.youtube.com/watch?v=Ne0_v4YadmM',  # valid link
        'https://inv.bp.projectsegfau.lt/watch?v=DWYMyp638PQ&list=PLOttxkyjhZeIwNpyDKV0HIRltQaHrzMm3&index=1',  # invidius link
    ])

    ctr.parallel.download_handler(album, 2, len(album.sources))

    tests.remove_tmp_directory(tmp_target)
