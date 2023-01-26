import taegel.views as views

import os
from datetime import datetime


def check_target_dir(target: str, display=True) -> None:
    """Check if the target directory exists and create it if not. Also, it will
    complain if the target directory is not empty.

    :param str target: Path to the directory to check/create
    :param bool display: Display log messages when interating with the system
    """
    if not os.path.exists(target):
        if display:
            views.log.print(f'creating an album directory [black]{target}[/]')
        os.mkdir(target)

    elif len(os.listdir(target)) > 0 and display:
        views.log.warning(f'the target is not empty! [black]{target}[/]')


def rename_song(target_file: str) -> None | str:
    """Rename a mp4 song to an mp3 one, and return an info message if that file
    already exists.

    :param str terget_file: Full path with the song name.
    """
    basename, _ = os.path.splitext(target_file)
    mp3_file = basename + '.mp3'

    if os.path.exists(mp3_file):
        return f'The [cyan]{mp3_file}[] already exists'

    os.rename(target_file, mp3_file)


# todo: make it cross plataform
def create_cache_dir() -> str:
    """Create the taegel cache dir and return the name of that directory.
    Of course it isn't cross plataform, which meas it work only on unix
    machines.
    """
    cache: str = os.getenv('HOME') + '/.cache'
    check_target_dir(cache, display=False)

    cache = f'{cache}/taegel'
    check_target_dir(cache, display=False)

    today: str = datetime.now().strftime('%d-%m-%Y_%H-%M-%S')
    cache = f'{cache}/{today}'
    check_target_dir(cache, display=False)

    return cache
