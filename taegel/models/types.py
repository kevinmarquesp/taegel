import dataclasses
import os


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
