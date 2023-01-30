import taegel.views as views
import taegel.controllers as ctr

import multiprocessing as mp

from taegel.models.types import AlbumInfo
from multiprocessing import Process
from multiprocessing.connection import Connection


@views.progress.idle('Fetching...')
def select_playlist_videos(playlists: list[str], root_target: str,
                           procs: int) -> list[AlbumInfo]:
    """Function that generate a list of ``AlbumInfo`` objects based on a
    list of Youtube playlist links. It will use multiple process and reutrn
    the generated list once every list was done.

    :param list[str] playlists: List of Youtube playlist links.
    :param str root_target: The playlist name will be appended with that path.
    :param int procs: How many processes will run at the same time to do that.
    """
    with mp.Pool(processes=procs) as pool:
        return pool.starmap(ctr.youtube.playlist_to_album, [(url, root_target)
                            for url in playlists])


def download_pool(cpipe: Connection, album: AlbumInfo, procs: int) -> None:
    """Create a pool of processes and call the
    :py:meth:`taegel.controllers.youtube.download` function using the URL list
    provide by the ``down_data`` parammeter. That function will be executed
    with every URL using multiple process at the same time.

    :param multiprocessing.connection.Connection cpipe: Parent pipe connection
      to pass to the download function, in order to make it send info through
      that pipe.
    :param DownloadData down_data: Downlaod data with a list of URL's to
      download.
    :param int parallel_procs: Max procs that will be running in parallel.
    """
    with mp.Pool(processes=procs) as pool:
        pool.starmap(ctr.youtube.download, [(cpipe, album.target, url)
                     for url in album.sources])


def download_handler(album: AlbumInfo, procs: int, tasks: int,
                     done=0) -> None:
    """Main download handler that runs the multiprocessing stuff and the nice
    looking progress bar (:py:meth:`taegel.views.progress.downloading`) at the
    same time in different process.

    They share information -- such as some logging messages -- through a pipe
    channel connected in these two proccesses.

    :param DownloadData down_data: Information needed to execute the
      downloading process.
    :param int procs: How many processes will be running to download the URL
      list in the :py:meth:`taegel.models.objects.DownloadData` object.
    :param int tasks: How many tasks need to run.
    :param int done: How many of them is already done.
    """
    parent_pipe: Connection
    child_pipe: Connection

    parent_pipe, child_pipe = mp.Pipe()
    data_size: int = tasks

    proc_display: Process = mp.Process(target=views.progress.downloading,
                                       args=[parent_pipe, data_size, done])

    proc_download: Process = mp.Process(target=download_pool, args=[child_pipe,
                                        album, procs])

    proc_display.start()
    proc_download.start()
    proc_display.join()
    proc_download.join()
