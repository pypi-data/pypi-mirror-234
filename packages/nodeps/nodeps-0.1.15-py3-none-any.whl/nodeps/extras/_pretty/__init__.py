"""NoDeps Extras Pretty Module."""
__all__ = (
    "CONSOLE",
    "ic",
    "icc",
)

import os

try:
    # nodeps[pretty] extras
    import rich.pretty  # type: ignore[attr-defined]
    import rich.traceback  # type: ignore[attr-defined]

    CONSOLE = rich.console.Console(force_interactive=True, color_system="256")

    rich.pretty.install(CONSOLE, expand_all=True)
    rich.traceback.install(show_locals=True)
except ModuleNotFoundError:
    CONSOLE = None


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
