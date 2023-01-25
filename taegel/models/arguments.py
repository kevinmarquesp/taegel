import os

from argparse import Namespace, ArgumentParser


# todo: add a docstring
def get_args(args: list[str]) -> Namespace:
    """Function with all the argument configuration using the ``argparser``
    library that return the arguments given by the user in a ease to use
    ``Namespace`` object.
    """
    parser: ArgumentParser = ArgumentParser(description='a simple to use cli youtube downloader with some advanced features')

    parser.add_argument('url', type=str, nargs='+',
                        help='youtube video, or playlist, url to extract the audio')

    parser.add_argument('--target', '-t', type=str, default=os.getcwd(),
                        help='directory path to save the audios')

    parser.add_argument('--parallel', type=int, default=os.cpu_count(),
                        help='how manny process this app can run at the same time')

    return parser.parse_args(args)
