import rich


def print(msg: str, use_console=False):
    rich.print(msg)


def warting(msg: str, use_console=False):
    rich.print(f'[yellow]WARNING:[/] {msg}')
