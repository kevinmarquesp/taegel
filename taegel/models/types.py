import dataclasses
import os

from typing import List


@dataclasses.dataclass(frozen=True)
class AlbumInfo:
    """Class to pack the crucial information to work with.
    """
    #: Target directory related with the YouTube video links.
    target: str = dataclasses.field(default_factory=os.getcwd)
    #: List of videos to be saved in the ``target`` directory.
    sources: List[str] = dataclasses.field(default_factory=List)


@dataclasses.dataclass(frozen=True)
class ArgsFiltered:
    """A more organized version of the  URL list argument given by the user,
    instead of just a confusing and long list.
    """
    #: Raw user argument, without any filter or order.
    raw: List[str] = dataclasses.field(default_factory=List)
    #: List with only with the **videos** URL's
    videos: List[str] = dataclasses.field(default_factory=List)
    #: List with only with the **playlist** URL's
    playlists: List[str] = dataclasses.field(default_factory=List)
