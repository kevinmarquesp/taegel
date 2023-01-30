import taegel.views as views

import rich.console
import os
import shutil
import uuid

from rich.console import Console

console: Console = rich.console.Console()


def create_tmp_directory() -> str:
    """This function will create a temp directory, with an random UUID in the
    name, and return the name (the full path) of that directory as a string.
    Note that this directory will be created in the folder that the user/dev
    are right now -- usually in the root of this project.
    """
    CURRENT_DIRECTORY: str = os.getcwd()
    DIRECTORY_ID: str = str(uuid.uuid4())
    TMP_DIR: str = f'{CURRENT_DIRECTORY}/tmp_{DIRECTORY_ID}'

    os.mkdir(TMP_DIR)
    return TMP_DIR


def remove_tmp_directory(tmp_directory: str) -> None:
    """Will delete an directory that has a 'tmp_' string in it, if that file
    doesn't exists, it just will show a log message and return.

    :param str tmp_directory: Path of that temp directory
    """
    if 'tmp_' not in tmp_directory:
        return

    try:
        views.log.warning(f'removing the {tmp_directory} directory')
        shutil.rmtree(tmp_directory)

    except Exception as err:
        console.log(err, style='red')
