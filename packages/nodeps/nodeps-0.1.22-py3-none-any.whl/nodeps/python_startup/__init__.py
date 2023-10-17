#!/usr/bin/env python3.11
"""PYTHONSTARTUP (DOes not work with PyCharm."""
import os
import sys

try:
    import IPython
except ModuleNotFoundError:
    IPython = object

os.environ['PYTHONSTARTUP'] = ''  # Prevent running this again


def main():
    """Main function."""
    if sys.argv[0] and "IPython" not in name:  # sys.argv == [] if `python3`
        print(__file__)
        sys.exit()


try:
    name = sys._getframe(1).f_globals["__name__"]
except ValueError:
    name = ""

if not sys.argv[0] and IPython != object():
    IPython.start_ipython()
    raise SystemExit

if __name__ == "__main__":
    main()
