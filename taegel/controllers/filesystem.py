import taegel.views as views

import os


def check_target_dir(target: str) -> None:
    """Check if the target directory exists and create it if not. Also, it will
    complain if the target directory is not empty.

    :param str target: Path to the directory to check/create
    """
    if not os.path.exists(target):
        views.log.print(f'creating an album directory [black]{target}[/]')
        os.mkdir(target)

    elif len(os.listdir(target)) > 0:
        views.log.warning(f'the target directory is not empty! [black]{target}[/]')
