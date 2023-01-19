import taegel.views as views

import os


# todo: add a docstring
def check_target_dir(target: str) -> None:
    if os.path.exists(target):
        if len(os.listdir(target)) > 0:
            views.out.warting('The target directory is not empty!')
    else:
        views.out.warting(f'Creating the [cyan underline]{target}[/] album')
        os.mkdir(target)
