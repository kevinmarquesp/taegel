import rich.progress

from multiprocessing.connection import Connection
from typing import List, Any, Callable


progress_config: List[Any] = [
    rich.progress.SpinnerColumn(),
    '{task.description}',
    rich.progress.BarColumn(),
    rich.progress.TextColumn('[progress.percentage]{task.percentage:>3.0f}%')
]

idle_config: List[Any] = [
    rich.progress.SpinnerColumn(),
    '{task.description}',
    rich.progress.BarColumn()
]


# todo: add a docstring
def idle(description: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any) -> Callable:
            with rich.progress.Progress(*idle_config,
                                        transient=True) as progress:
                progress.add_task(description, total=None)
                return func(*args)
        return wrapper
    return decorator


# todo: add a docstring
def downloading(pipe: Connection, total: int) -> None:
    bfr: str = ''  # buffer to store strings temporarialy

    with rich.progress.Progress(*progress_config, transient=True) as progress:
        task_download = progress.add_task('Downloading...', total=total)

        bfr = '[on green] [/] It may take a while, be patiente! :coffee:\n'
        progress.console.print(bfr)

        while not progress.finished:
            status: dict = pipe.recv()

            if status['done']:
                progress.update(task_download, advance=1)

            if status['is_ok']:
                bfr = f'Downloaded [cyan]{status["info"]}[/] with success!'
                progress.console.print(bfr, style='green')

            else:
                bfr = f'{status["info"]}, sorry...'
                progress.console.print(bfr, style='red')