import rich.progress

from rich.progress import Progress, TaskID
from multiprocessing.connection import Connection
from typing import Any, Callable


#: Configuration for the download process progress bar display
progress_config: list[Any] = [
    rich.progress.SpinnerColumn(),
    '{task.description}',
    rich.progress.BarColumn(),
    rich.progress.TextColumn('[progress.percentage]{task.percentage:>3.0f}%')
]

#: Configuration for the idle progress bar display
idle_config: list[Any] = [
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


def downloading_handler(ppipe: Connection, prog: Progress, task: TaskID) -> None:
    """Log handler for the :py:meth:`downloading` progress bar, this recives
    the info sended throught the *parent pipe* and update the task with that.

    :param Connection ppipe: Parent pipe to recive the log status.
    :param Progress prog: Progress bar to update and display the log messages.
    :param TaskID task: Task to be updated.
    """
    status: dict = ppipe.recv()
    log: Callable = prog.console.print

    if status['done']:
        prog.update(task, advance=1)

    if status['is_ok']:
        log(f"Downloaded [cyan]{status['info']}[/] with success! [black]{status['url']}[/]")
    else:
        log(f"{status['info']}, sorry... {status['url']}", style='red')

    if status['desc'] is not None:
        log(status['desc'])


def downloading(ppipe: Connection, total: int, done: int) -> None:
    """Display a progress bar that recives the progress information throught
    parent pipe channel.

    :param Connection ppipe: Parent pipe channel to recive information.
    :param int total: Total steps to comple the progress bar.
    """
    with rich.progress.Progress(*progress_config, transient=True) as prog:
        task: TaskID = prog.add_task('Downloading...', total=total)
        prog.update(task, advance=done)

        prog.console.print('[on green] [/] It may take a while, be patient! :coffee:')

        while not prog.finished:
            downloading_handler(ppipe, prog, task)
