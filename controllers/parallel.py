import models
import views
import controllers

import time
import multiprocessing as mp

from multiprocessing import Process
from multiprocessing.connection import Connection


def download_pool(pipe: Connection, data: models.objects.Data, parallel: int) -> None:
    with mp.Pool(parallel) as pool:
        pool.starmap(controllers.youtube.download,
                     [(pipe, data.target, url) for url in data.sources])


def handler(data: models.objects.Data, parallel: int) -> None:
    parent_pipe: Connection
    child_pipe: Connection

    parent_pipe, child_pipe = mp.Pipe()
    data_size: int = len(data.sources)

    time.sleep(.5)
    proc_display: Process = mp.Process(target=views.progress.downloading,
                                       args=[parent_pipe, data_size])
    proc_display.start()

    time.sleep(.5)
    proc_download: Process = mp.Process(target=download_pool,
                                        args=[child_pipe, data, parallel])
    proc_download.start()

    proc_download.join()
    proc_display.join()
