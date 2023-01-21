import taegel.models as models
import taegel.views as views
import taegel.controllers as ctr

import rich
import rich.traceback

from typing import List
from argparse import Namespace
from taegel.models.types import AlbumInfo

rich.traceback.install()


def run() -> None:
    """ Main function to run the taegel cli tool.
    """
    args: Namespace = models.arguments.get_args()

    views.log.print('checking up arguments', title=True)
    user_url = ctr.data.filter_arguments(args.url)

    views.log.print('generating objects', title=True)
    album_list: List[AlbumInfo] = ctr.data.gen_album_list(user_url.videos,
                                                          user_url.playlists,
                                                          args.target)

    views.log.print('creating directories', title=True)
    for album in album_list:
        ctr.filesystem.check_target_dir(album.target)

    views.log.print('starting the download process', title=True)
    for album in album_list:
        ctr.parallel.download_handler(album, args.parallel)
