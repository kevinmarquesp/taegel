import taegel.models as models
import taegel.controllers as controllers

import rich
import rich.traceback
import rich.console

from typing import List
from argparse import Namespace
from taegel.models.objects import Data

rich.traceback.install()


# todo: add a docstring
def run() -> None:
    args: Namespace = models.arguments.get_args()

    data_arr: List[Data] = controllers.validate.get_data(args.url, args.target)
    print()  # empty print for astetic propurses

    for data in data_arr:
        controllers.filesystem.check_target_dir(data.target)

    for data in data_arr:
        controllers.parallel.handler(data, args.parallel)
