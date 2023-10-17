"""NoDeps Extras Pretty Module.

    Performs the following always when imported:
        - Aliases :func:`rich.inspect` as :func:`rich_inspect` for :class:`rich._inspect.Inspect`
        - Replaces :builtin:`print` with :rich:`rich.print`.
        - Imports: :func:`rich.print_json`
        - Patches :class:`rich.console.Console` to detect PyCharm console and other consoles.
        - Installs: :class:`rich.pretty.Pretty`.
        - Installs :class:`rich.traceback.Traceback`.
        - Installs :class:`rich.inspect.Inspect`.

    the following if running in a console:
        - Imports :class:`ghapi.all.GhApi` and initializes it with `GITHUB_TOKEN` environment variable.
        - Preprend current working dir and cwd/src if exists to :obj:`sys.path`

Examples:
    >>> import time
    >>> from rich.console import Console
    >>> from rich.json import JSON
    >>>
    >>> c = Console()
    >>> with c.status("Working...", spinner="material"):  # doctest: +SKIP
    ...    time.sleep(2)
    >>>
    >>> c.log(JSON('["foo", "bar"]'))  # doctest: +SKIP
    >>>
    >>> print_json('["foo", "bar"]')  # doctest: +SKIP
    >>>
    >>> c.log("Hello, World!")  # doctest: +SKIP
    >>> c.print([1, 2, 3])  # doctest: +SKIP
    >>> c.print("[blue underline]Looks like a link")  # doctest: +SKIP
    >>> c.print(locals())  # doctest: +SKIP
    >>> c.print("FOO", style="white on blue")  # doctest: +SKIP
    >>>
    >>> blue_console = Console(style="white on blue")  # doctest: +SKIP
    >>> blue_console.print("I'm blue. Da ba dee da ba di.")  # doctest: +SKIP
    >>>
    >>> c.input("What is [i]your[/i] [bold red]name[/]? :smiley: ")  # doctest: +SKIP


References:
    `IPython Configuration File <https://ipython.readthedocs.io/en/stable/config/intro.html>`_
    ~/.ipython/profile_default/startup/00-console.py
    ~/.ipython/profile_default/ipython_config.py

    ``c.InteractiveShellApp.extensions.extend(['autoreload', 'rich'])``
    or include
    ``%load_ext rich``

    Test with: `print("[italic red]Hello[/italic red] World!", locals())`

    `Rich Inspect <https://rich.readthedocs.io/en/stable/traceback.html?highlight=sitecustomize>`_

    ``rich.traceback.install(suppress=[click])``

    To see the spinners: `python -m rich.spinner`
    To print json from the comamand line: `python -m rich.json cats.json`

    `Rich Console <https://rich.readthedocs.io/en/stable/console.html>`_

    Input: `console.input("What is [i]your[/i] [bold red]name[/]? :smiley: ")`
"""
__all__ = (
    "FORCE_COLOR",
    "IPYTHON",
    "IS_REPL",
    "IS_TTY",
    "OpenIO",
    "ins",
    "is_terminal",
    "CONSOLE",
    "print_json",
    "ic",
    "icc",
)

import os
import pathlib
import sys
from io import BufferedRandom, BufferedReader, BufferedWriter, FileIO, TextIOWrapper
from typing import IO, Any, BinaryIO

try:
    # nodeps[pretty] extras
    import rich.console  # type: ignore[attr-defined]
    import rich.pretty  # type: ignore[attr-defined]
    import rich.traceback  # type: ignore[attr-defined]
    from rich import print_json  # type: ignore[attr-defined]
    from rich.console import Console  # type: ignore[name-defined]
except ModuleNotFoundError:
    Console = object
    print_json = object()

CONSOLE = None

FORCE_COLOR = False
"""Set by :func:`.is_terminal` to force color for rich."""

try:
    IPYTHON = get_ipython()  # type: ignore[name-defined]
    """Instance :class:`IPython.core.interactiveshell.InteractiveShell` None no InteractiveShell instance registered."""
except NameError:
    nested_ipython = 0
    IPYTHON = None

IS_REPL = bool(IPYTHON) or hasattr(sys, 'ps1') or 'pythonconsole' in sys.stdout.__class__.__module__
"""True if running on REPL, otherwise False."""
IS_TTY = False
"""Is a tty?, not jupyter, not FORCE_COLOR set and not idlelib."""

OpenIO = BinaryIO | BufferedRandom | BufferedReader | BufferedWriter | FileIO | IO | TextIOWrapper


def ins(obj: Any, *, _console: Console | None = None, title: str | None = None, _help: bool = False,
        methods: bool = True, docs: bool = False, private: bool = True,
        dunder: bool = False, sort: bool = True, _all: bool = False, value: bool = True, ):
    """Wrapper :func:`rich.inspect` for :class:`rich._inspect.Inspect`.

    Changing defaults to: ``docs=False, methods=True, private=True``.

    Inspect any Python object.

    Examples:
        >>> from nodeps.extras._pretty import ins
        >>>
        >>> # to see summarized info.
        >>> ins(ins)  # doctest: +SKIP
        >>> # to not see methods.
        >>> ins(ins, methods=False)  # doctest: +SKIP
        >>> # to see full (non-abbreviated) help.
        >>> ins(ins, help=True)  # doctest: +SKIP
        >>> # to not see private attributes (single underscore).
        >>> ins(ins, private=False)  # doctest: +SKIP
        >>> # to see attributes beginning with double underscore.
        >>> ins(ins, dunder=True)  # doctest: +SKIP
        >>> # to see all attributes.
        >>> ins(ins, _all=True)  # doctest: +SKIP
        '

    Args:
        obj (Any): An object to inspect.
        _console (Console, optional): Rich Console.
        title (str, optional): Title to display over inspect result, or None use type. Defaults to None.
        _help (bool, optional): Show full help text rather than just first paragraph. Defaults to False.
        methods (bool, optional): Enable inspection of callables. Defaults to False.
        docs (bool, optional): Also render doc strings. Defaults to True.
        private (bool, optional): Show private attributes (beginning with underscore). Defaults to False.
        dunder (bool, optional): Show attributes starting with double underscore. Defaults to False.
        sort (bool, optional): Sort attributes alphabetically. Defaults to True.
        _all (bool, optional): Show all attributes. Defaults to False.
        value (bool, optional): Pretty print value. Defaults to True.
    """
    rich.inspect(obj=obj, console=_console, title=title, help=_help, methods=methods, docs=docs, private=private,
                 dunder=dunder, sort=sort, all=_all, value=value)


def is_terminal(file: Console | OpenIO | None = None) -> bool:
    """Patch of :data:``rich.Console.is_terminal`` for PyCharm.

    Check if the console is writing to a terminal.

    Environment:
        FORCE_COLOR: set to True for rich if is a terminal

    Arguments:
        file: file descriptor or instance of :class:`rich.console.Console`

    Returns:
        bool: True if the console writing to a device capable of
        understanding terminal codes, otherwise False.
    """
    if IS_TTY is False:
        if file is None and 'rich.console' in sys.modules:
            file = c if (c := globals().get('CONSOLE')) is not None and isinstance(c, rich.console.Console) \
                else rich.console.Console(color_system="256")
            global CONSOLE  # noqa: PLW0603
            CONSOLE = file

        if hasattr(sys.stdin, "__module__") and sys.stdin.__module__.startswith(
            "idlelib"
        ):
            # Return False for Idle which claims to be a tty but can't handle ansi codes
            return False

        if hasattr(file, "is_jupyter") and file.is_jupyter:
            # return False for Jupyter, which may have FORCE_COLOR set
            return False

        force_color = os.environ.get("FORCE_COLOR")
        if force_color is not None:
            global FORCE_COLOR  # noqa: PLW0603
            FORCE_COLOR = True
            if hasattr(file, "_force_terminal"):
                file._force_terminal = True
            return True

        try:
            return IS_REPL or (hasattr(file, "isatty") and file.isatty()) or \
                (hasattr(file, "file") and hasattr(file.file, "isatty") and file.file.isatty())
        except ValueError:
            return False
    return IS_TTY


try:
    from icecream import IceCreamDebugger  # type: ignore[name-defined]

    ic = IceCreamDebugger(prefix="")
    icc = IceCreamDebugger(prefix="", includeContext=True)
    ic.enabled = icc.enabled = bool(os.environ.get("IC"))
except ModuleNotFoundError:

    def ic(*a):
        """Include Context."""
        return None if not a else a[0] if len(a) == 1 else a

    def icc(*a):
        """Include Context."""
        return None if not a else a[0] if len(a) == 1 else a


IS_TTY = is_terminal()

if IS_TTY:
    os.environ["COLORIZE"] = "1"
    os.environ["FORCE_COLOR"] = "1"
    if CONSOLE is not None:
        CONSOLE._force_terminal = True

if IS_REPL:
    _cwd = pathlib.Path.cwd().absolute()
    if str(_cwd) not in sys.path:
        sys.path.insert(0, str(_cwd))
    if (_src := _cwd / "src").exists() and str(_src) not in sys.path:
        sys.path.insert(0, str(_src))


if "rich.pretty" in sys.modules:
    # noinspection PyUnboundLocalVariable
    rich.pretty.install(CONSOLE, expand_all=True)  # type: ignore[attr-defined]
    rich.traceback.install(show_locals=True, suppress={"click", "_pytest", "rich", })  # type: ignore[attr-defined]
