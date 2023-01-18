import os

from argparse import Namespace, ArgumentParser


description: str = 'a simple to use cli youtube downloader with some advanced features'
url_help: str = 'youtube video, or playlist, url to extract the audio'
target_help: str = 'directory path to save the audios'
parallel_help: str = 'how manny process this app can run at the same time'


# todo: add a docstring
def get_args() -> Namespace:
    parser: ArgumentParser = ArgumentParser(description=description)

    parser.add_argument('url', type=str, nargs='+', help=url_help)
    parser.add_argument('--target', '-t', type=str, default=os.getcwd(),
                        help=target_help)
    parser.add_argument('--parallel', type=int, default=os.cpu_count(),
                        help=parallel_help)

    return parser.parse_args()
