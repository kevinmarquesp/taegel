import rich


def print(msg: str, title=False):
    """Just display some text on the screen. Just to make it easer to add some
    logic on the display before doing it, but it just do that for now...

    :param str msg: Text to display:
    """
    if title:
        rich.print(f'\n[green]➤[/] {msg}')
    else:
        rich.print(f'{msg}')


def warning(msg: str):
    """Print an message in the srcreen, but with an simple "warning" sign
    before the text.

    :param str msg: Text to display:
    """
    rich.print(f'[yellow]warning:[/] {msg}')
