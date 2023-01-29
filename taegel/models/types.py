from typing import TypedDict
import dataclasses
import os

from typing import Optional


@dataclasses.dataclass(frozen=True)
class AlbumInfo:
    """Class to pack the crucial information to work with.
    """
    #: Target directory related with the YouTube video links.
    target: str = dataclasses.field(default_factory=os.getcwd)
    #: List of videos to be saved in the ``target`` directory.
    sources: list[str] = dataclasses.field(default_factory=list)

    @property
    def as_dict(self) -> dict[str, str | list[str]]:
        """Property to get a dict version of an instance of that class to save
        in the cache database.
        """
        return {
            'target': self.target,
            'sources': self.sources
        }


@dataclasses.dataclass(frozen=True)
class ArgsFiltered:
    """A more organized version of the  URL list argument given by the user,
    instead of just a confusing and long list.
    """
    #: List with only with the **videos** URL's
    videos: list[str] = dataclasses.field(default_factory=list)
    #: List with only with the **playlist** URL's
    playlists: list[str] = dataclasses.field(default_factory=list)


class DownloadLog(TypedDict):
    """Dictionary shape that the :py:meth:`controllers.youtube.download()` will
    send throught the pipe to the other processes or functions. Use that class,
    and that kind of dict, just in that method to share important information
    to the other parts of the code, set the unused properties as `None` or
    `False`.
    """
    #: Youtube URL string to that specifc video
    url: str
    #: Success status of the download
    status_ok: bool
    #: If that task will update the progress bar
    task_done: bool
    #: Video title string
    title: Optional[str]
    #: Channel name
    channel: Optional[str]
    #: Log description, to display on the progress bar
    task_description: Optional[str]
