import taegel.models as models
import taegel.controllers as ctr

import rich
import rich.traceback
import rich.console

from typing import List
from argparse import Namespace
from taegel.models.objects import DownloadData

rich.traceback.install()


def run() -> None:
    """ Main function to run the taegel cli tool. It needs to.
    """
    args: Namespace = models.arguments.get_args()

    data_arr: List[DownloadData] = ctr.validate.get_data(args.url, args.target)
    print()  # empty print for astetic propurses

    for data in data_arr:
        ctr.filesystem.check_target_dir(data.target)

    for data in data_arr:
        ctr.parallel.handler(data, args.parallel)
