import taegel.views as views

import os


# todo: add a docstring
def check_target_dir(target: str) -> None:
    """Check if the target directory exists and create it if not. Also, it will
    complain if the target directory is not empty.

    :param str target: Path to the directory to check/create
    """
    if os.path.exists(target):
        if len(os.listdir(target)) > 0:
            views.out.warting('The target directory is not empty!')
    else:
        views.out.warting(f'Creating the [cyan underline]{target}[/] album')
        os.mkdir(target)
