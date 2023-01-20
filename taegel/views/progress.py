import rich.progress

from multiprocessing.connection import Connection
from typing import List, Any, Callable


#: Configuration for the download process progress bar display
progress_config: List[Any] = [
    rich.progress.SpinnerColumn(),
    '{task.description}',
    rich.progress.BarColumn(),
    rich.progress.TextColumn('[progress.percentage]{task.percentage:>3.0f}%')
]

#: Configuration for the idle progress bar display
idle_config: List[Any] = [
    rich.progress.SpinnerColumn(),
    '{task.description}',
    rich.progress.BarColumn()
]


# this amount of nested functions is to use arguments in the decorator call
def idle(description: str) -> Callable:
    """Decorator that keep displaying a simple idle progress bar until the
    decorated function ends.

    :param str description: Task name to display aside with the bar.
    """
    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any) -> Callable:
            with rich.progress.Progress(*idle_config, transient=True) as prog:
                prog.add_task(description, total=None)
                return func(*args)
        return wrapper
    return decorator


def downloading(ppipe: Connection, total: int) -> None:
    """Display a progress bar that recives the progress information throught
    parent pipe channel.

    :param Connection ppipe: Parent pipe channel to recive information.
    :param int total: Total steps to comple the progress bar.
    """
    bfr: str = ''  # buffer to store strings temporarialy

    with rich.progress.Progress(*progress_config, transient=True) as prog:
        task_download = prog.add_task('Downloading...', total=total)

        bfr = '[on green] [/] It may take a while, be patient! :coffee:\n'
        prog.console.print(bfr)

        while not prog.finished:
            status: dict = ppipe.recv()

            if status['done']:
                prog.update(task_download, advance=1)

            if status['is_ok']:
                bfr = f'Downloaded [cyan]{status["info"]}[/] with success!'
                prog.console.print(bfr, style='green')

            else:
                bfr = f'{status["info"]}, sorry...'
                prog.console.print(bfr, style='red')
