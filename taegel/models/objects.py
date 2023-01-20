import dataclasses
import os
import re

from typing import List
from re import Pattern


#: Regex object to validate if an URL is an valid YouTube video or playlist.
regex_url: Pattern = re.compile(r'^(?:https?://)?(?:www\.)?(?:youtube\.com/(watch\?v=|playlist\?list=)|youtu\.be/)([^&]{11})')

#: Regex object to verify if the (validated) URL is, in fact, a playlist.
regex_playlist: Pattern = re.compile(r'playlist\?list=')


@dataclasses.dataclass(frozen=True)
class DownloadData:
    """Class to pack the crucial information to work with.
    """
    #: Target directory related with the YouTube video links.
    target: str = dataclasses.field(default_factory=os.getcwd)

    #: List of videos to be saved in the ``target`` directory.
    sources: List[str] = dataclasses.field(default_factory=List)
