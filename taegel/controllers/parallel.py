import taegel.views as views
import taegel.controllers as ctr

import multiprocessing as mp

from taegel.models.objects import DownloadData
from multiprocessing import Process
from multiprocessing.connection import Connection


def download_pool(cpipe: Connection, down_data: DownloadData,
                  parallel_procs: int) -> None:
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
    with mp.Pool(parallel_procs) as pool:
        pool.starmap(ctr.youtube.download, [(cpipe, down_data.target, url)
                     for url in down_data.sources])


def handler(down_data: DownloadData, parallel_procs: int) -> None:
    """Main download handler that runs the multiprocessing stuff and the nice
    looking progress bar (:py:meth:`taegel.views.progress.downloading`) at the
    same time in different process.

    They shar information -- such as some logging messages -- through a pipe
    channel connected in these two proccesses.

    :param DownloadData down_data: Information needed to execute the
      downloading process.
    :param int parallel_procs: How manny processes will be running at the same
      time to download the URL list in the
      :py:meth:`taegel.models.objects.DownloadData` object.
    """
    parent_pipe: Connection
    child_pipe: Connection

    parent_pipe, child_pipe = mp.Pipe()
    data_size: int = len(down_data.sources)

    proc_display: Process = mp.Process(target=views.progress.downloading,
                                       args=[parent_pipe, data_size])

    proc_download: Process = mp.Process(target=download_pool, args=[child_pipe,
                                        down_data, parallel_procs])

    proc_display.start()
    proc_download.start()

    proc_download.join()
    proc_display.join()
