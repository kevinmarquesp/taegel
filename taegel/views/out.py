import rich


def print(msg: str):
    """Just display some text on the screen. Just to make it easer to add some
    logic on the display before doing it, but it just do that for now...

    :param str msg: Text to display:
    """
    rich.print(msg)


def warting(msg: str):
    """Print an message in the srcreen, but with an simple "warning" sign
    before the text.

    :param str msg: Text to display:
    """
    rich.print(f'[yellow]WARNING:[/] {msg}')
