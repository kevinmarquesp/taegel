import taegel.views as views

import rich.console
import os
import shutil
import uuid

from rich.console import Console

console: Console = rich.console.Console()



def create_tmp_directory() -> str:
    CURRENT_DIRECTORY: str = os.getcwd()
    DIRECTORY_ID: str = str(uuid.uuid4())
    TMP_DIR: str = f'{CURRENT_DIRECTORY}/tmp_{DIRECTORY_ID}'

    os.mkdir(TMP_DIR)
    return TMP_DIR


def remove_tmp_directory(tmp_directory: str) -> None:
    try:
        views.log.warning(f'removing the {tmp_directory} directory')
        shutil.rmtree(tmp_directory)

    except Exception as err:
        console.log(err, style='red')
