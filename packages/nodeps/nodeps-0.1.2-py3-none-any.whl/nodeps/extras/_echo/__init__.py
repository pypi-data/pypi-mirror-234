"""NoDeps Extras Echo Module."""
__all__ = (
    "black",
    "red",
    "green",
    "yellow",
    "blue",
    "magenta",
    "cyan",
    "white",
    "bblack",
    "bred",
    "bgreen",
    "byellow",
    "bblue",
    "bmagenta",
    "bcyan",
    "bwhite",
    "reset",

    "COLORIZE",
    "EnumLower",
    "Color",
    "SYMBOL",
    "Symbol"
)

from .color import COLORIZE, SYMBOL, Color, EnumLower, Symbol, click, msg_click_typer


def black(msg="", bold=False, underline=False, blink=False, err=False):
    """black."""
    msg_click_typer()
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True,
                fg='black', err=err)


def red(msg="", bold=False, underline=False, blink=False, err=True):
    """red."""
    msg_click_typer()
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True,
                fg='red', err=err)


def green(msg="", bold=False, underline=False, blink=False, err=False):
    """green."""
    msg_click_typer()
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True,
                fg='green', err=err)


def yellow(msg="", bold=False, underline=False, blink=False, err=False):
    """yellow."""
    msg_click_typer()
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True,
                fg='yellow', err=err)


def blue(msg="", bold=False, underline=False, blink=False, err=False):
    """blue."""
    msg_click_typer()
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True,
                fg='blue', err=err)


def magenta(msg="", bold=False, underline=False, blink=False, err=False):
    """magenta."""
    msg_click_typer()
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True,
                fg='magenta', err=err)


def cyan(msg="", bold=False, underline=False, blink=False, err=False):
    """cyan."""
    msg_click_typer()
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True,
                fg='cyan', err=err)


def white(msg="", bold=False, underline=False, blink=False, err=False):
    """white."""
    msg_click_typer()
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True,
                fg='white', err=err)


def bblack(msg="", bold=False, underline=False, blink=False, err=False):
    """bblack."""
    msg_click_typer()
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True,
                fg='bright_black', err=err)


def bred(msg="", bold=False, underline=False, blink=False, err=False):
    """bred."""
    msg_click_typer()
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True,
                fg='bright_red', err=err)


def bgreen(msg="", bold=False, underline=False, blink=False, err=False):
    """bgreen."""
    msg_click_typer()
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True,
                fg='bright_green', err=err)


def byellow(msg="", bold=False, underline=False, blink=False, err=False):
    """byellow."""
    msg_click_typer()
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True,
                fg='bright_yellow', err=err)


def bblue(msg="", bold=False, underline=False, blink=False, err=False):
    """bblue."""
    msg_click_typer()
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True,
                fg='bright_blue', err=err)


def bmagenta(msg="", bold=False, underline=False, blink=False, err=False):
    """bmagenta."""
    msg_click_typer()
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True,
                fg='bright_magenta', err=err)


def bcyan(msg="", bold=False, underline=False, blink=False, err=False):
    """bcyan."""
    msg_click_typer()
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True,
                fg='bright_cyan', err=err)


def bwhite(msg="", bold=False, underline=False, blink=False, err=False):
    """bwhite."""
    msg_click_typer()
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True,
                fg='bright_white', err=err)


def reset(msg="", bold=False, underline=False, blink=False, err=False):
    """reset."""
    msg_click_typer()
    click.secho(msg, bold=bold, underline=underline, blink=blink, color=True,
                fg='reset', err=err)
