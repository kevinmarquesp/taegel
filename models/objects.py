import dataclasses
import os
import re

from typing import List
from re import Pattern


regex_url: Pattern = re.compile(r'^(?:https?://)?(?:www\.)?(?:youtube\.com/(watch\?v=|playlist\?list=)|youtu\.be/)([^&]{11})')
regex_playlist: Pattern = re.compile(r'playlist\?list=')


@dataclasses.dataclass(frozen=True)
class Data:
    target: str = dataclasses.field(default_factory=os.getcwd)
    sources: List[str] = dataclasses.field(default_factory=List)
