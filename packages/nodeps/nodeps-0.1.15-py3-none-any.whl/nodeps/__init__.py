"""NoDeps Helpers and Utils Module."""
from __future__ import annotations

__all__ = (
    "AUTHOR",
    "GIT",
    "GIT_DEFAULT_SCHEME",
    "GITHUB_DOMAIN",
    "GITHUB_TOKEN",
    "GITHUB_URL",
    "LINUX",
    "MACOS",
    "NODEPS_EXECUTABLE",
    "NODEPS_PIP_POST_INSTALL_FILENAME",
    "NODEPS_PROJECT_NAME",
    "PYTHON_VERSIONS",
    "PYTHON_DEFAULT_VERSION",
    "USER",
    "EMAIL",
    "PW_ROOT",
    "PW_USER",
    "AnyIO",
    "ChainLiteral",
    "ExcType",
    "GitSchemeLiteral",
    "ModuleSpec",
    "PathIsLiteral",
    "StrOrBytesPath",
    "ThreadLock",
    "RunningLoop",
    "AnyPath",
    "LockClass",
    "Bump",
    "CalledProcessError",
    "Chain",
    "CmdError",
    "ColorLogger",
    "CommandNotFoundError",
    "EnumLower",
    "Env",
    "EnvBuilder",
    "FileConfig",
    "FrameSimple",
    "GitSHA",
    "GroupUser",
    "InvalidArgumentError",
    "LetterCounter",
    "NamedtupleMeta",
    "OwnerRepo",
    "Passwd",
    "PathStat",
    "Path",
    "PipMetaPathFinder",
    "ProjectRepos",
    "Project",
    "PTHBuildPy",
    "PTHDevelop",
    "PTHEasyInstall",
    "PTHInstallLib",
    "TempDir",
    "aioclone",
    "aioclosed",
    "aiocmd",
    "aiocommand",
    "aiodmg",
    "aiogz",
    "aioloop",
    "aioloopid",
    "aiorunning",
    "allin",
    "ami",
    "anyin",
    "chdir",
    "clone",
    "cmd",
    "cmdrun",
    "cmdsudo",
    "command",
    "completions",
    "current_task_name",
    "dict_sort",
    "dmg",
    "effect",
    "elementadd",
    "exec_module_from_file",
    "filterm",
    "findfile",
    "findup",
    "firstfound",
    "flatten",
    "framesimple",
    "from_latin9",
    "fromiter",
    "getpths",
    "getsitedir",
    "group_user",
    "gz",
    "in_tox",
    "noexc",
    "parent",
    "parse_str",
    "pipmetapathfinder",
    "returncode",
    "siteimported",
    "sourcepath",
    "split_pairs",
    "stdout",
    "stdquiet",
    "suppress",
    "syssudo",
    "tardir",
    "tilde",
    "timestamp_now",
    "toiter",
    "urljson",
    "which",
    "EXECUTABLE",
    "EXECUTABLE_SITE",
)

import abc
import asyncio
import collections
import contextlib
import copy
import dataclasses
import datetime
import enum
import filecmp
import fnmatch
import getpass
import grp
import hashlib
import importlib.abc
import importlib.metadata
import importlib.util
import inspect
import io
import ipaddress
import itertools
import json
import logging
import os
import pathlib
import pwd
import re
import shutil
import signal
import stat
import string
import subprocess
import sys
import sysconfig
import tarfile
import tempfile
import threading
import time
import tokenize
import types
import urllib.request
import venv
import warnings
import zipfile
from collections.abc import Callable, Hashable, Iterable, Iterator, MutableMapping, Sequence
from ipaddress import IPv4Address, IPv6Address
from typing import (
    IO,
    TYPE_CHECKING,
    Any,
    AnyStr,
    ClassVar,
    Generic,
    Literal,
    ParamSpec,
    TextIO,
    TypeAlias,
    TypeVar,
    cast,
)
from urllib.parse import ParseResult

try:
    # nodeps[pth] extras
    from setuptools.command.build_py import build_py  # type: ignore[attr-defined]
    from setuptools.command.develop import develop  # type: ignore[attr-defined]
    from setuptools.command.easy_install import easy_install  # type: ignore[attr-defined]
    from setuptools.command.install_lib import install_lib  # type: ignore[attr-defined]
except ModuleNotFoundError:
    build_py = object
    develop = object
    easy_install = object
    install_lib = object

try:
    if "_in_process.py" not in sys.argv[0]:
        # Avoids failing when asking for build requirements and distutils.core is not available since pip patch it
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=UserWarning, message="Setuptools is replacing distutils.")

            # Must be imported after setuptools
            # noinspection PyCompatibility
            import pip._internal.cli.base_command
            import pip._internal.metadata
            import pip._internal.models.direct_url
            import pip._internal.models.scheme
            import pip._internal.operations.install.wheel
            import pip._internal.req.req_install
            import pip._internal.req.req_uninstall
except ModuleNotFoundError:
    pip = object

from . import extras
from .extras import *

if TYPE_CHECKING:
    # noinspection PyCompatibility
    from pip._internal.cli.base_command import Command

__all__ += extras.__all__


_NODEPS_PIP_POST_INSTALL = {}
"""Holds the context with wheels installed and paths to package installed to be used in post install"""
AUTHOR = "José Antonio Puértolas Montañés"
GIT = os.environ.get("GIT", "j5pu")
"""GitHub user name"""
GIT_DEFAULT_SCHEME = "https"
GITHUB_DOMAIN = "github.com"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", os.environ.get("GH_TOKEN", os.environ.get("TOKEN")))
"""GitHub Token"""
GITHUB_URL = {
    "api": f"https://api.{GITHUB_DOMAIN}/",
    "git+file": "git+file://",
    "git+https": f"git+https://{GITHUB_DOMAIN}/",
    "git+ssh": f"git+ssh://git@{GITHUB_DOMAIN}/",
    "https": f"https://{GITHUB_DOMAIN}/",
    "ssh": f"git@{GITHUB_DOMAIN}:",
}
"""
GitHub: api, git+file, git+https, git+ssh, https, ssh and git URLs
(join directly the user or path without '/' or ':')
"""
LINUX = sys.platform == "linux"
"""Is Linux? sys.platform == 'linux'"""
MACOS = sys.platform == "darwin"
"""Is macOS? sys.platform == 'darwin'"""
NODEPS_EXECUTABLE = "p"
"""NoDeps Executable Name"""
NODEPS_PIP_POST_INSTALL_FILENAME = "_post_install.py"
"""Filename that will be searched after pip installs a package."""
NODEPS_PROJECT_NAME = "nodeps"
"""NoDeps Project Name"""
PYTHON_VERSIONS = (
    os.environ.get("PYTHON_DEFAULT_VERSION", "3.11"),
    "3.12",
)
"""Python versions for venv, etc."""
PYTHON_DEFAULT_VERSION = PYTHON_VERSIONS[0]
"""Python default version for venv, etc."""
USER = os.getenv("USER")
""""Environment Variable $USER"""

EMAIL = f"63794670+{GIT}@users.noreply.github.com"
PW_ROOT = pwd.getpwnam("root")
PW_USER = pwd.getpwnam(USER) if USER else PW_ROOT

AnyIO = IO[AnyStr]
ChainLiteral: TypeAlias = Literal["all", "first", "unique"]
ExcType: TypeAlias = type[Exception] | tuple[type[Exception], ...]
GitSchemeLiteral = Literal["git+file", "git+https", "git+ssh", "https", "ssh"]
ModuleSpec = importlib._bootstrap.ModuleSpec
PathIsLiteral: TypeAlias = Literal["exists", "is_dir", "is_file"]
PathType: TypeAlias = "Path"
StrOrBytesPath = str | bytes | os.PathLike[str] | os.PathLike[bytes]
ThreadLock = threading.Lock
RunningLoop = asyncio.events._RunningLoop

AnyPath: TypeAlias = os.PathLike | AnyStr | IO[AnyStr]
LockClass = type(ThreadLock())

_KT = TypeVar("_KT")
_T = TypeVar("_T")
_VT = TypeVar("_VT")
P = ParamSpec("P")
T = TypeVar("T")


class _NoDepsBaseError(Exception):
    """Base Exception from which all other custom Exceptions defined in semantic_release inherit."""


class Bump(str, enum.Enum):
    """Bump class."""

    MAJOR = enum.auto()
    MINOR = enum.auto()
    PATCH = enum.auto()


class CalledProcessError(subprocess.SubprocessError):
    """Patched :class:`subprocess.CalledProcessError`.

    Raised when run() and the process returns a non-zero exit status.

    Attributes:
        cmd: The command that was run.
        returncode: The exit code of the process.
        output: The output of the process.
        stderr: The error output of the process.
        completed: :class:`subprocess.CompletedProcess` object.
    """

    returncode: int
    cmd: StrOrBytesPath | Sequence[StrOrBytesPath]
    output: AnyStr | None
    stderr: AnyStr | None
    completed: subprocess.CompletedProcess | None

    # noinspection PyShadowingNames
    def __init__(
        self,
        returncode: int | None = None,
        cmd: StrOrBytesPath | Sequence[StrOrBytesPath] | None = None,
        output: AnyStr | None = None,
        stderr: AnyStr | None = None,
        completed: subprocess.CompletedProcess | None = None,
    ) -> None:
        r"""Patched :class:`subprocess.CalledProcessError`.

        Args:
            cmd: The command that was run.
            returncode: The exit code of the process.
            output: The output of the process.
            stderr: The error output of the process.
            completed: :class:`subprocess.CompletedProcess` object.

        Examples:
            >>> import subprocess
            >>> 3/0  # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            ZeroDivisionError: division by zero
            >>> subprocess.run(["ls", "foo"], capture_output=True, check=True)  # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            project.CalledProcessError:
              Return Code:
                1
            <BLANKLINE>
              Command:
                ['ls', 'foo']
            <BLANKLINE>
              Stderr:
                b'ls: foo: No such file or directory\n'
            <BLANKLINE>
              Stdout:
                b''
            <BLANKLINE>
        """
        self.returncode = returncode
        self.cmd = cmd
        self.output = output
        self.stderr = stderr
        self.completed = completed
        if self.returncode is None:
            self.returncode = self.completed.returncode
            self.cmd = self.completed.args
            self.output = self.completed.stdout
            self.stderr = self.completed.stderr

    def _message(self):
        if self.returncode and self.returncode < 0:
            try:
                return f"Died with {signal.Signals(-self.returncode)!r}."
            except ValueError:
                return f"Died with with unknown signal {-self.returncode}."
        else:
            return f"{self.returncode:d}"

    def __str__(self):
        """Returns str."""
        return f"""
  Return Code:
    {self._message()}

  Command:
    {self.cmd}

  Stderr:
    {self.stderr}

  Stdout:
    {self.output}
"""

    @property
    def stdout(self) -> str:
        """Alias for output attribute, to match stderr."""
        return self.output

    @stdout.setter
    def stdout(self, value):
        # There's no obvious reason to set this, but allow it anyway so
        # .stdout is a transparent alias for .output
        self.output = value


class Chain(collections.ChainMap):
    # noinspection PyUnresolvedReferences
    """Variant of chain that allows direct updates to inner scopes and returns more than one value, not the first one.

    Examples:
        >>> from nodeps import Chain
        >>>
        >>> class Test3:
        ...     a = 2
        >>>
        >>> class Test4:
        ...     a = 2
        >>>
        >>> Test1 = collections.namedtuple('Test1', 'a b')
        >>> Test2 = collections.namedtuple('Test2', 'a d')
        >>> test1 = Test1(1, 2)
        >>> test2 = Test2(3, 5)
        >>> test3 = Test3()
        >>> test4 = Test4()
        >>>
        >>> maps = [dict(a=1, b=2), dict(a=2, c=3), dict(a=3, d=4), dict(a=dict(z=1)), dict(a=dict(z=1)), \
        dict(a=dict(z=2))]
        >>> chain = Chain(*maps)
        >>> assert chain['a'] == [1, 2, 3, {'z': 1}, {'z': 2}]
        >>> chain = Chain(*maps, rv="first")
        >>> assert chain['a'] == 1
        >>> chain = Chain(*maps, rv="all")
        >>> assert chain['a'] == [1, 2, 3, {'z': 1}, {'z': 1}, {'z': 2}]
        >>>
        >>> maps = [dict(a=1, b=2), dict(a=2, c=3), dict(a=3, d=4), dict(a=dict(z=1)), dict(a=dict(z=1)),\
        dict(a=dict(z=2)), test1, test2]
        >>> chain = Chain(*maps)
        >>> assert chain['a'] == [1, 2, 3, {'z': 1}, {'z': 2}]
        >>> chain = Chain(*maps, rv="first")
        >>> assert chain['a'] == 1
        >>> chain = Chain(*maps, rv="all")
        >>> assert chain['a'] == [1, 2, 3, {'z': 1}, {'z': 1}, {'z': 2}, 1, 3]
        >>>
        >>> maps = [dict(a=1, b=2), dict(a=2, c=3), dict(a=3, d=4), dict(a=dict(z=1)), dict(a=dict(z=1)), \
        dict(a=dict(z=2)), test1, test2]
        >>> chain = Chain(*maps)
        >>> del chain['a']
        >>> assert chain == Chain({'b': 2}, {'c': 3}, {'d': 4}, test1, test2)
        >>> assert chain['a'] == [1, 3]
        >>>
        >>> maps = [dict(a=1, b=2), dict(a=2, c=3), dict(a=3, d=4), dict(a=dict(z=1)), dict(a=dict(z=1)), \
        dict(a=dict(z=2)), test1, test2]
        >>> chain = Chain(*maps)
        >>> assert chain.delete('a') == Chain({'b': 2}, {'c': 3}, {'d': 4}, test1, test2)
        >>> assert chain.delete('a')['a'] == [1, 3]
        >>>
        >>> maps = [dict(a=1, b=2), dict(a=2, c=3), dict(a=3, d=4), dict(a=dict(z=1)), dict(a=dict(z=1)), \
        dict(a=dict(z=2)), test1, test2]
        >>> chain = Chain(*maps, rv="first")
        >>> del chain['a']
        >>> del maps[0]['a'] # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        KeyError:
        >>>
        >>> assert chain['a'] == 2
        >>>
        >>> maps = [dict(a=1, b=2), dict(a=2, c=3), dict(a=3, d=4), dict(a=dict(z=1)), dict(a=dict(z=1)), \
        dict(a=dict(z=2)), test1, test2]
        >>> chain = Chain(*maps, rv="first")
        >>> new = chain.delete('a')
        >>> del maps[0]['a'] # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        KeyError:
        >>> assert new.delete('a')
        >>> del maps[1]['a'] # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        KeyError:
        >>>
        >>> assert new['a'] == 3
        >>>
        >>> maps = [dict(a=1, b=2), dict(a=2, c=3), dict(a=3, d=4), dict(a=dict(z=1)), dict(a=dict(z=1)), \
        dict(a=dict(z=2)), test1, test3]
        >>> chain = Chain(*maps)
        >>> del chain['a']
        >>> assert chain[4] == []
        >>> assert not hasattr(test3, 'a')
        >>> assert chain.set('a', 9)
        >>> assert chain['a'] == [9, 1]
        >>>
        >>> maps = [dict(a=1, b=2), dict(a=2, c=3), dict(a=3, d=4), dict(a=dict(z=1)), dict(a=dict(z=1)), \
        dict(a=dict(z=2)), test1, test4]
        >>> chain = Chain(*maps)
        >>> chain.set('j', 9)  # doctest: +ELLIPSIS
        Chain({'a': 1, 'b': 2, 'j': 9}, {'a': 2, 'c': 3}, {'a': 3, 'd': 4}, {'a': {'z': 1}}, {'a': {'z': 1}}, \
{'a': {'z': 2}}, Test1(a=1, b=2), <....Test4 object at 0x...>)
        >>> assert [maps[0]['j']] == chain['j'] == [9]
        >>> chain.set('a', 10)  # doctest: +ELLIPSIS
        Chain({'a': 10, 'b': 2, 'j': 9}, {'a': 10, 'c': 3}, {'a': 10, 'd': 4}, {'a': 10}, {'a': 10}, {'a': 10}, \
Test1(a=1, b=2), <....Test4 object at 0x...>)
        >>> # noinspection PyUnresolvedReferences
        >>> assert [maps[0]['a'], 1] == chain['a'] == [maps[7].a, 1] == [10, 1]  # 1 from namedtuple
        >>>
        >>> maps = [dict(a=1, b=2), dict(a=2, c=3), dict(a=3, d=4), dict(a=dict(z=1)), dict(a=dict(z=1)), \
        dict(a=dict(z=2)), test1, test4]
        >>> chain = Chain(*maps, rv="first")
        >>> chain.set('a', 9)  # doctest: +ELLIPSIS
        Chain({'a': 9, 'b': 2}, {'a': 2, 'c': 3}, {'a': 3, 'd': 4}, {'a': {'z': 1}}, {'a': {'z': 1}}, \
{'a': {'z': 2}}, Test1(a=1, b=2), <....Test4 object at 0x...>)
        >>> assert maps[0]['a'] == chain['a'] == 9
        >>> assert maps[1]['a'] == 2
    """

    rv: ChainLiteral = "unique"
    default: Any = None
    maps: list[Iterable | NamedtupleMeta | MutableMapping] = []  # noqa: RUF012

    def __init__(self, *maps, rv: ChainLiteral = "unique", default: Any = None) -> None:
        """Init."""
        super().__init__(*maps)
        self.rv = rv
        self.default = default

    def __getitem__(self, key: Hashable) -> Any:  # noqa: PLR0912
        """Get item."""
        rv = []
        for mapping in self.maps:
            if hasattr(mapping, "_field_defaults"):
                mapping = mapping._asdict()  # noqa: PLW2901
            elif hasattr(mapping, "asdict"):
                to_dict = mapping.__class__.asdict
                if isinstance(to_dict, property):
                    mapping = mapping.asdict  # noqa: PLW2901
                elif callable(to_dict):
                    mapping = mapping.asdict()  # noqa: PLW2901
            if hasattr(mapping, "__getitem__"):
                try:
                    value = mapping[key]
                    if self.rv == "first":
                        return value
                    if (self.rv == "unique" and value not in rv) or self.rv == "all":
                        rv.append(value)
                except KeyError:
                    pass
            elif (
                hasattr(mapping, "__getattribute__")
                and isinstance(key, str)
                and not isinstance(mapping, (tuple | bool | int | str | bytes))
            ):
                try:
                    value = getattr(mapping, key)
                    if self.rv == "first":
                        return value
                    if (self.rv == "unique" and value not in rv) or self.rv == "all":
                        rv.append(value)
                except AttributeError:
                    pass
        return self.default if self.rv == "first" else rv

    def __delitem__(self, key: Hashable) -> Chain:
        """Delete item."""
        index = 0
        deleted = []
        found = False
        for mapping in self.maps:
            if mapping:
                if not isinstance(mapping, (tuple | bool | int | str | bytes)):
                    if hasattr(mapping, "__delitem__"):
                        if key in mapping:
                            del mapping[key]
                            if self.rv == "first":
                                found = True
                    elif hasattr(mapping, "__delattr__") and hasattr(mapping, key) and isinstance(key, str):
                        delattr(mapping.__class__, key) if key in dir(mapping.__class__) else delattr(mapping, key)
                        if self.rv == "first":
                            found = True
                if not mapping:
                    deleted.append(index)
                if found:
                    break
            index += 1
        for index in reversed(deleted):
            del self.maps[index]
        return self

    def delete(self, key: Hashable) -> Chain:
        """Delete item."""
        del self[key]
        return self

    def __setitem__(self, key: Hashable, value: Any) -> Chain:  # noq: C901
        """Set item."""
        found = False
        for mapping in self.maps:
            if mapping:
                if not isinstance(mapping, (tuple | bool | int | str | bytes)):
                    if hasattr(mapping, "__setitem__"):
                        if key in mapping:
                            mapping[key] = value
                            if self.rv == "first":
                                found = True
                    elif hasattr(mapping, "__setattr__") and hasattr(mapping, key) and isinstance(key, str):
                        setattr(mapping, key, value)
                        if self.rv == "first":
                            found = True
                if found:
                    break
        if not found and not isinstance(self.maps[0], (tuple | bool | int | str | bytes)):
            if hasattr(self.maps[0], "__setitem__"):
                self.maps[0][key] = value
            elif hasattr(self.maps[0], "__setattr__") and isinstance(key, str):
                setattr(self.maps[0], key, value)
        return self

    def set(self, key: Hashable, value: Any) -> Chain:  # noqa: A003
        """Set item."""
        return self.__setitem__(key, value)


class CmdError(subprocess.CalledProcessError):
    """Raised when run() and the process returns a non-zero exit status.

    Attribute:
      process: The CompletedProcess object returned by run().
    """

    def __init__(self, process: subprocess.CompletedProcess | None = None) -> None:
        """Init."""
        super().__init__(process.returncode, process.args, output=process.stdout, stderr=process.stderr)

    def __str__(self) -> str:
        """Str."""
        value = super().__str__()
        if self.stderr is not None:
            value += "\n" + self.stderr
        if self.stdout is not None:
            value += "\n" + self.stdout
        return value


class ColorLogger(logging.Formatter):
    """Color logger class."""

    black = "\x1b[30m"
    blue = "\x1b[34m"
    cyan = "\x1b[36m"
    green = "\x1b[32m"
    grey = "\x1b[38;21m"
    magenta = "\x1b[35m"
    red = "\x1b[31;21m"
    red_bold = "\x1b[31;1m"
    reset = "\x1b[0m"
    white = "\x1b[37m"
    yellow = "\x1b[33;21m"
    fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    vertical = f"{red}|{reset} "
    FORMATS: ClassVar[dict[int, str]] = {
        logging.DEBUG: grey + fmt + reset,
        logging.INFO: f"{cyan}%(levelname)8s{reset} {vertical}"
        f"{cyan}%(name)s{reset} {vertical}"
        f"{cyan}%(filename)s{reset}:{cyan}%(lineno)d{reset} {vertical}"
        f"{green}%(extra)s{reset} {vertical}"
        f"{cyan}%(message)s{reset}",
        logging.WARNING: f"{yellow}%(levelname)8s{reset} {vertical}"
        f"{yellow}%(name)s{reset} {vertical}"
        f"{yellow}%(filename)s{reset}:{yellow}%(lineno)d{reset} {vertical}"
        f"{green}%(repo)s{reset} {vertical}"
        f"{yellow}%(message)s{reset}",
        logging.ERROR: red + fmt + reset,
        logging.CRITICAL: red_bold + fmt + reset,
    }

    def format(self, record):  # noqa: A003
        """Format log."""
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        if "extra" not in record.__dict__:
            record.__dict__["extra"] = ""
        return formatter.format(record)

    @classmethod
    def logger(cls, name: str = __name__) -> logging.Logger:
        """Get logger.

        Examples:
            >>> from nodeps import ColorLogger
            >>> from nodeps import NODEPS_PROJECT_NAME
            >>>
            >>> lo = ColorLogger.logger(NODEPS_PROJECT_NAME)
            >>> lo.info("hola", extra=dict(extra="bapy"))
            >>> lo.info("hola")

        Args:
            name: logger name

        Returns:
            logging.Logger
        """
        l = logging.getLogger(name)
        l.propagate = False
        l.setLevel(logging.DEBUG)
        if l.handlers:
            l.handlers[0].setLevel(logging.DEBUG)
            l.handlers[0].setFormatter(cls())
        else:
            handler = logging.StreamHandler()
            handler.setLevel(logging.DEBUG)
            handler.setFormatter(cls())
            l.addHandler(handler)
        return l


class CommandNotFoundError(_NoDepsBaseError):
    """Raised when command is not found."""


class EnumLower(enum.Enum):
    """EnumLower class."""

    def _generate_next_value_(self: str, start, count: int, last_values) -> str:
        return str(self).lower()


# noinspection LongLine,SpellCheckingInspection
@dataclasses.dataclass
class Env:
    """GitHub Actions Variables Class.

    See Also: `Environment variables
    <https://docs.github.com/en/enterprise-cloud@latest/actions/learn-github-actions/environment-variables>`_

    If you need to use a workflow run's URL from within a job, you can combine these environment variables:
        ``$GITHUB_SERVER_URL/$GITHUB_REPOSITORY/actions/runs/$GITHUB_RUN_ID``

    If you generate a value in one step of a job, you can use the value in subsequent ``steps`` of
        the same job by assigning the value to an existing or new environment variable and then writing
        this to the ``GITHUB_ENV`` environment file, see `Commands
        <https://docs.github.com/en/enterprise-cloud@latest/actions/reference/workflow-commands-for-github-actions
        /#setting-an-environment-variable>`_.

    If you want to pass a value from a step in one job in a ``workflow`` to a step in another job in the workflow,
        you can define the value as a job output, see `Syntax
        <https://docs.github.com/en/enterprise-cloud@latest/actions/learn-github-actions/workflow-syntax-for-github
        -actions#jobsjob_idoutputs>`_.
    """

    CI: bool | str | None = dataclasses.field(default=None, init=False)
    """Always set to ``true`` in a GitHub Actions environment."""

    GITHUB_ACTION: str | None = dataclasses.field(default=None, init=False)
    # noinspection LongLine
    """
    The name of the action currently running, or the `id
    <https://docs.github.com/en/enterprise-cloud@latest/actions/using-workflows/workflow-syntax-for-github-actions#jobs\
        job_idstepsid>`_ of a step.

    For example, for an action, ``__repo-owner_name-of-action-repo``.

    GitHub removes special characters, and uses the name ``__run`` when the current step runs a script without an id.

    If you use the same script or action more than once in the same job,
    the name will include a suffix that consists of the sequence number preceded by an underscore.

    For example, the first script you run will have the name ``__run``, and the second script will be named ``__run_2``.

    Similarly, the second invocation of ``actions/checkout`` will be ``actionscheckout2``.
    """

    GITHUB_ACTION_PATH: Path | str | None = dataclasses.field(default=None, init=False)
    """
    The path where an action is located. This property is only supported in composite actions.

    You can use this path to access files located in the same repository as the action.

    For example, ``/home/runner/work/_actions/repo-owner/name-of-action-repo/v1``.
    """

    GITHUB_ACTION_REPOSITORY: str | None = dataclasses.field(default=None, init=False)
    """
    For a step executing an action, this is the owner and repository name of the action.

    For example, ``actions/checkout``.
    """

    GITHUB_ACTIONS: bool | str | None = dataclasses.field(default=None, init=False)
    """
    Always set to ``true`` when GitHub Actions is running the workflow.

    You can use this variable to differentiate when tests are being run locally or by GitHub Actions.
    """

    GITHUB_ACTOR: str | None = dataclasses.field(default=None, init=False)
    """
    The name of the person or app that initiated the workflow.

    For example, ``octocat``.
    """

    GITHUB_API_URL: ParseResult | str | None = dataclasses.field(default=None, init=False)
    """
    API URL.

    For example: ``https://api.github.com``.
    """

    GITHUB_BASE_REF: str | None = dataclasses.field(default=None, init=False)
    """
    The name of the base ref or target branch of the pull request in a workflow run.

    This is only set when the event that triggers a workflow run is either ``pull_request`` or ``pull_request_target``.

    For example, ``main``.
    """

    GITHUB_ENV: Path | str | None = dataclasses.field(default=None, init=False)
    """
    The path on the runner to the file that sets environment variables from workflow commands.

    This file is unique to the current step and changes for each step in a job.

    For example, ``/home/runner/work/_temp/_runner_file_commands/set_env_87406d6e-4979-4d42-98e1-3dab1f48b13a``.

    For more information, see `Workflow commands for GitHub Actions.
    <https://docs.github.com/en/enterprise-cloud@latest/actions/using-workflows/workflow-commands-for-github-actions
    #setting-an-environment-variable>`_
    """

    GITHUB_EVENT_NAME: str | None = dataclasses.field(default=None, init=False)
    """
    The name of the event that triggered the workflow.

    For example, ``workflow_dispatch``.
    """

    GITHUB_EVENT_PATH: Path | str | None = dataclasses.field(default=None, init=False)
    """
    The path to the file on the runner that contains the full event webhook payload.

    For example, ``/github/workflow/event.json``.
    """

    GITHUB_GRAPHQL_URL: ParseResult | str | None = dataclasses.field(default=None, init=False)
    """
    Returns the GraphQL API URL.

    For example: ``https://api.github.com/graphql``.
    """

    GITHUB_HEAD_REF: str | None = dataclasses.field(default=None, init=False)
    """
    The head ref or source branch of the pull request in a workflow run.

    This property is only set when the event that triggers a workflow run is either
    ``pull_request`` or ``pull_request_target``.

    For example, ``feature-branch-1``.
    """

    GITHUB_JOB: str | None = dataclasses.field(default=None, init=False)
    """
    The `job_id
    <https://docs.github.com/en/enterprise-cloud@latest/actions/reference/workflow-syntax-for-github-actions
    #jobsjob_id>`_
    of the current job.

    For example, ``greeting_job``.
    """

    GITHUB_PATH: Path | str | None = dataclasses.field(default=None, init=False)
    """
    The path on the runner to the file that sets system PATH variables from workflow commands.
    This file is unique to the current step and changes for each step in a job.

    For example, ``/home/runner/work/_temp/_runner_file_commands/add_path_899b9445-ad4a-400c-aa89-249f18632cf5``.

    For more information, see `Workflow commands for GitHub Actions.
    <https://docs.github.com/en/enterprise-cloud@latest/actions/using-workflows/workflow-commands-for-github-actions
    #adding-a-system-path>`_
    """

    GITHUB_REF: str | None = dataclasses.field(default=None, init=False)
    """
    The branch or tag ref that triggered the workflow run.

    For branches this is the format ``refs/heads/<branch_name>``,
    for tags it is ``refs/tags/<tag_name>``,
    and for pull requests it is ``refs/pull/<pr_number>/merge``.

    This variable is only set if a branch or tag is available for the event type.

    For example, ``refs/heads/feature-branch-1``.
    """

    GITHUB_REF_NAME: str | None = dataclasses.field(default=None, init=False)
    """
    The branch or tag name that triggered the workflow run.

    For example, ``feature-branch-1``.
    """

    GITHUB_REF_PROTECTED: bool | str | None = dataclasses.field(default=None, init=False)
    """
    ``true`` if branch protections are configured for the ref that triggered the workflow run.
    """

    GITHUB_REF_TYPE: str | None = dataclasses.field(default=None, init=False)
    """
    The type of ref that triggered the workflow run.

    Valid values are ``branch`` or ``tag``.

    For example, ``branch``.
    """

    GITHUB_REPOSITORY: str | None = dataclasses.field(default=None, init=False)
    """
    The owner and repository name.

    For example, ``octocat/Hello-World``.
    """

    GITHUB_REPOSITORY_OWNER: str | None = dataclasses.field(default=None, init=False)
    """
    The repository owner's name.

    For example, ``octocat``.
    """

    GITHUB_RETENTION_DAYS: str | None = dataclasses.field(default=None, init=False)
    """
    The number of days that workflow run logs and artifacts are kept.

    For example, ``90``.
    """

    GITHUB_RUN_ATTEMPT: str | None = dataclasses.field(default=None, init=False)
    """
    A unique number for each attempt of a particular workflow run in a repository.

    This number begins at ``1`` for the workflow run's first attempt, and increments with each re-run.

    For example, ``3``.
    """

    GITHUB_RUN_ID: str | None = dataclasses.field(default=None, init=False)
    """
    A unique number for each workflow run within a repository.

    This number does not change if you re-run the workflow run.

    For example, ``1658821493``.
    """

    GITHUB_RUN_NUMBER: str | None = dataclasses.field(default=None, init=False)
    """
    A unique number for each run of a particular workflow in a repository.

    This number begins at ``1`` for the workflow's first run, and increments with each new run.
    This number does not change if you re-run the workflow run.

    For example, ``3``.
    """

    GITHUB_SERVER_URL: ParseResult | str | None = dataclasses.field(default=None, init=False)
    """
    The URL of the GitHub Enterprise Cloud server.

    For example: ``https://github.com``.
    """

    GITHUB_SHA: str | None = dataclasses.field(default=None, init=False)
    """
    The commit SHA that triggered the workflow.

    The value of this commit SHA depends on the event that triggered the workflow.
    For more information, see `Events that trigger workflows.
    <https://docs.github.com/en/enterprise-cloud@latest/actions/using-workflows/events-that-trigger-workflows>`_

    For example, ``ffac537e6cbbf934b08745a378932722df287a53``.
    """

    GITHUB_WORKFLOW: Path | str | None = dataclasses.field(default=None, init=False)
    """
    The name of the workflow.

    For example, ``My test workflow``.

    If the workflow file doesn't specify a name,
    the value of this variable is the full path of the workflow file in the repository.
    """

    GITHUB_WORKSPACE: Path | str | None = dataclasses.field(default=None, init=False)
    """
    The default working directory on the runner for steps, and the default location of your repository
    when using the `checkout <https://github.com/actions/checkout>`_ action.

    For example, ``/home/runner/work/my-repo-name/my-repo-name``.
    """

    RUNNER_ARCH: str | None = dataclasses.field(default=None, init=False)
    """
    The architecture of the runner executing the job.

    Possible values are ``X86``, ``X64``, ``ARM``, or ``ARM64``.

    For example, ``X86``.
    """

    RUNNER_NAME: str | None = dataclasses.field(default=None, init=False)
    """
    The name of the runner executing the job.

    For example, ``Hosted Agent``.
    """

    RUNNER_OS: str | None = dataclasses.field(default=None, init=False)
    """
    The operating system of the runner executing the job.

    Possible values are ``Linux``, ``Windows``, or ``macOS``.

    For example, ``Linux``.
    """

    RUNNER_TEMP: Path | str | None = dataclasses.field(default=None, init=False)
    """
    The path to a temporary directory on the runner.

    This directory is emptied at the beginning and end of each job.

    Note that files will not be removed if the runner's user account does not have permission to delete them.

    For example, ``_temp``.
    """

    RUNNER_TOOL_CACHE: str | None = dataclasses.field(default=None, init=False)
    # noinspection LongLine
    """
    The path to the directory containing preinstalled tools for GitHub-hosted runners.

    For more information, see `About GitHub-hosted runners.
    <https://docs.github.com/en/enterprise-cloud@latest/actions/reference/specifications-for-github-hosted-runners
    /#supported-software>`_

    `Ubuntu latest <https://github.com/actions/virtual-environments/blob/main/images/linux/Ubuntu2004-Readme.md>`_
    `macOS latest <https://github.com/actions/virtual-environments/blob/main/images/macos/macos-11-Readme.md>`_

    For example, ``C:/hostedtoolcache/windows``.
    """

    COMMAND_MODE: str | None = dataclasses.field(default=None, init=False)
    HOME: str | None = dataclasses.field(default=None, init=False)
    IPYTHONENABLE: str | None = dataclasses.field(default=None, init=False)
    LC_TYPE: str | None = dataclasses.field(default=None, init=False)
    LOGNAME: str | None = dataclasses.field(default=None, init=False)
    OLDPWD: str | None = dataclasses.field(default=None, init=False)
    PATH: str | None = dataclasses.field(default=None, init=False)
    PS1: str | None = dataclasses.field(default=None, init=False)
    PWD: str | None = dataclasses.field(default=None, init=False)
    PYCHARM_DISPLAY_PORT: str | None = dataclasses.field(default=None, init=False)
    PYCHARM_HOSTED: str | None = dataclasses.field(default=None, init=False)
    PYCHARM_MATPLOTLIB_INDEX: str | None = dataclasses.field(default=None, init=False)
    PYCHARM_MATPLOTLIB_INTERACTIVE: str | None = dataclasses.field(default=None, init=False)
    PYCHARM_PROPERTIES: str | None = dataclasses.field(default=None, init=False)
    PYCHARM_VM_OPTIONS: str | None = dataclasses.field(default=None, init=False)
    PYDEVD_LOAD_VALUES_ASYNC: str | None = dataclasses.field(default=None, init=False)
    PYTHONIOENCODING: str | None = dataclasses.field(default=None, init=False)
    PYTHONPATH: str | None = dataclasses.field(default=None, init=False)
    PYTHONUNBUFFERED: str | None = dataclasses.field(default=None, init=False)
    SHELL: str | None = dataclasses.field(default=None, init=False)
    SSH_AUTH_SOCK: str | None = dataclasses.field(default=None, init=False)
    SUDO_USER: str | None = dataclasses.field(default=None, init=False)
    TMPDIR: str | None = dataclasses.field(default=None, init=False)
    XPC_FLAGS: str | None = dataclasses.field(default=None, init=False)
    XPC_SERVICE_NAME: str | None = dataclasses.field(default=None, init=False)
    __CFBundleIdentifier: str | None = dataclasses.field(default=None, init=False)
    __CF_USER_TEXT_ENCODING: str | None = dataclasses.field(default=None, init=False)

    _parse_as_int: ClassVar[tuple[str, ...]] = (
        "GITHUB_RUN_ATTEMPT",
        "GITHUB_RUN_ID",
        "GITHUB_RUN_NUMBER",
    )
    _parse_as_int_suffix: ClassVar[tuple[str, ...]] = (
        "_GID",
        "_JOBS",
        "_PORT",
        "_UID",
    )
    parsed: dataclasses.InitVar[bool] = True

    def __post_init__(self, parsed: bool) -> None:
        """Instance of Env class.

        Args:
            parsed: Parse the environment variables using :func:`nodeps.parse_str`,
                except :func:`Env.as_int` (default: True)
        """
        # TODO: python-decouple
        self.__dict__.update({k: self.as_int(k, v) for k, v in os.environ.items()} if parsed else os.environ)

    def __contains__(self, item):
        """Check if item is in self.__dict__."""
        return item in self.__dict__

    def __getattr__(self, name: str) -> str | None:
        """Get attribute from self.__dict__ if exists, otherwise return None."""
        if name in self:
            return self.__dict__[name]
        return None

    def __getattribute__(self, name: str) -> str | None:
        """Get attribute from self.__dict__ if exists, otherwise return None."""
        if hasattr(self, name):
            return super().__getattribute__(name)
        return None

    def __getitem__(self, item: str) -> str | None:
        """Get item from self.__dict__ if exists, otherwise return None."""
        return self.__getattr__(item)

    @classmethod
    def as_int(cls, key: str, value: str = "") -> bool | Path | ParseResult | IPv4Address | IPv6Address | int | str:
        """Parse as int if environment variable should be forced to be parsed as int checking if:.

            - has value,
            - key in :data:`Env._parse_as_int` or
            - key ends with one of the items in :data:`Env._parse_as_int_suffix`.

        Args:
            key: Environment variable name.
            value: Environment variable value (default: "").

        Returns:
            int, if key should be parsed as int and has value, otherwise according to :func:`parse_str`.
        """
        convert = False
        if value:
            if key in cls._parse_as_int:
                convert = True
            else:
                for item in cls._parse_as_int_suffix:
                    if key.endswith(item):
                        convert = True
        return int(value) if convert and value.isnumeric() else parse_str(value)

    @staticmethod
    def parse_as_bool(
        variable: str = "USER",
    ) -> bool | Path | ParseResult | IPv4Address | IPv6Address | int | str | None:
        """Parses variable from environment 1 and 0 as bool instead of int.

        Parses:
            - bool: 1, 0, True, False, yes, no, on, off (case insensitive)
            - int: integer only numeric characters but 1 and 0 or SUDO_UID or SUDO_GID
            - ipaddress: ipv4/ipv6 address
            - url: if "//" or "@" is found it will be parsed as url
            - path: start with / or ~ or .
            - others as string

        Arguments:
            variable: variable name to parse from environment (default: USER)

        Examples:
            >>> from nodeps import Path
            >>> from nodeps import Env
            >>>
            >>> assert isinstance(Env.parse_as_bool(), str)
            >>>
            >>> os.environ['FOO'] = '1'
            >>> assert Env.parse_as_bool("FOO") is True
            >>>
            >>> os.environ['FOO'] = '0'
            >>> assert Env.parse_as_bool("FOO") is False
            >>>
            >>> os.environ['FOO'] = 'TrUe'
            >>> assert Env.parse_as_bool("FOO") is True
            >>>
            >>> os.environ['FOO'] = 'OFF'
            >>> assert Env.parse_as_bool("FOO") is False
            >>>
            >>> os.environ['FOO'] = '~/foo'
            >>> assert Env.parse_as_bool("FOO") == Path('~/foo')
            >>>
            >>> os.environ['FOO'] = '/foo'
            >>> assert Env.parse_as_bool("FOO") == Path('/foo')
            >>>
            >>> os.environ['FOO'] = './foo'
            >>> assert Env.parse_as_bool("FOO") == Path('./foo')
            >>>
            >>> os.environ['FOO'] = './foo'
            >>> assert Env.parse_as_bool("FOO") == Path('./foo')
            >>>
            >>> v = "https://github.com"
            >>> os.environ['FOO'] = v
            >>> assert Env.parse_as_bool("FOO").geturl() == v
            >>>
            >>> v = "git@github.com"
            >>> os.environ['FOO'] = v
            >>> assert Env.parse_as_bool("FOO").geturl() == v
            >>>
            >>> v = "0.0.0.0"
            >>> os.environ['FOO'] = v
            >>> assert Env.parse_as_bool("FOO").exploded == v
            >>>
            >>> os.environ['FOO'] = "::1"
            >>> assert Env.parse_as_bool("FOO").exploded.endswith(":0001")
            >>>
            >>> v = "2"
            >>> os.environ['FOO'] = v
            >>> assert Env.parse_as_bool("FOO") == int(v)
            >>>
            >>> v = "2.0"
            >>> os.environ['FOO'] = v
            >>> assert Env.parse_as_bool("FOO") == v
            >>>
            >>> del os.environ['FOO']
            >>> assert Env.parse_as_bool("FOO") is None

        Returns:
            None
        """
        if value := os.environ.get(variable):
            if variable in ("SUDO_UID", "SUDO_GID"):
                return int(value)
            if variable == "PATH":
                return value
            return parse_str(value)
        return value

    @classmethod
    def parse_as_int(
        cls,
        name: str = "USER",
    ) -> bool | Path | ParseResult | IPv4Address | IPv6Address | int | str | None:
        """Parses variable from environment using :func:`mreleaser.parse_str`,.

        except ``SUDO_UID`` or ``SUDO_GID`` which are parsed as int instead of bool.

        Arguments:
            name: variable name to parse from environment (default: USER)

        Examples:
            >>> from nodeps import Path
            >>> from nodeps import Env
            >>> assert isinstance(Env.parse_as_int(), str)
            >>>
            >>> os.environ['FOO'] = '1'
            >>> assert Env.parse_as_int("FOO") is True
            >>>
            >>> os.environ['FOO'] = '0'
            >>> assert Env.parse_as_int("FOO") is False
            >>>
            >>> os.environ['FOO'] = 'TrUe'
            >>> assert Env.parse_as_int("FOO") is True
            >>>
            >>> os.environ['FOO'] = 'OFF'
            >>> assert Env.parse_as_int("FOO") is False
            >>>
            >>> os.environ['FOO'] = '~/foo'
            >>> assert Env.parse_as_int("FOO") == Path('~/foo')
            >>>
            >>> os.environ['FOO'] = '/foo'
            >>> assert Env.parse_as_int("FOO") == Path('/foo')
            >>>
            >>> os.environ['FOO'] = './foo'
            >>> assert Env.parse_as_int("FOO") == Path('./foo')
            >>>
            >>> os.environ['FOO'] = './foo'
            >>> assert Env.parse_as_int("FOO") == Path('./foo')
            >>>
            >>> v = "https://github.com"
            >>> os.environ['FOO'] = v
            >>> assert Env.parse_as_int("FOO").geturl() == v
            >>>
            >>> v = "git@github.com"
            >>> os.environ['FOO'] = v
            >>> assert Env.parse_as_int("FOO").geturl() == v
            >>>
            >>> v = "0.0.0.0"
            >>> os.environ['FOO'] = v
            >>> assert Env.parse_as_int("FOO").exploded == v
            >>>
            >>> os.environ['FOO'] = "::1"
            >>> assert Env.parse_as_int("FOO").exploded.endswith(":0001")
            >>>
            >>> v = "2"
            >>> os.environ['FOO'] = v
            >>> assert Env.parse_as_int("FOO") == int(v)
            >>>
            >>> v = "2.0"
            >>> os.environ['FOO'] = v
            >>> assert Env.parse_as_int("FOO") == v
            >>>
            >>> del os.environ['FOO']
            >>> assert Env.parse_as_int("FOO") is None
            >>>
            >>> if not os.environ.get("CI"):
            ...     assert isinstance(Env.parse_as_int("PATH"), str)

        Returns:
            Value parsed
        """
        if value := os.environ.get(name):
            return cls.as_int(name, value)
        return value


@dataclasses.dataclass
class EnvBuilder(venv.EnvBuilder):
    """Wrapper for :class:`venv.EnvBuilder`.

    Changed defaults for: `prompt`` `symlinks` and `with_pip`, adds `env_dir` to `__init__` arguments.

    Post install in :py:meth:`.post_setup`.

    This class exists to allow virtual environment creation to be
    customized. The constructor parameters determine the builder's
    behaviour when called upon to create a virtual environment.

    By default, the builder makes the system (global) site-packages dir *un*available to the created environment.

    If invoked using the Python -m option, the default is to use copying
    on Windows platforms but symlinks elsewhere. If instantiated some
    other way, the default is to *not* use symlinks (changed with the wrapper to use symlinks always).

    Attributes:
        system_site_packages: bool
            If True, the system (global) site-packages dir is available to created environments.
        clear: bool
            If True, delete the contents of the environment directory if it already exists, before environment creation.
        symlinks: bool
            If True, attempt to symlink rather than copy files into virtual environment.
        upgrade: bool
            If True, upgrade an existing virtual environment.
        with_pip: bool
            If True, ensure pip is installed in the virtual environment.
        prompt: str
            Alternative terminal prefix for the environment.
        upgrade_deps: bool
            Update the base venv modules to the latest on PyPI (python 3.9+).
        context: Simplenamespace
            The information for the environment creation request being processed.
        env_dir: bool
            The target directory to create an environment in.
    """

    system_site_packages: bool = False
    clear: bool = False
    symlinks: bool = True
    upgrade: bool = True
    """Upgrades scripts and run :class:`venv.EnvBuilder.post_setup`."""
    with_pip: bool = True
    prompt: str | None = "."
    """To use basename use '.'."""
    upgrade_deps: bool = True
    """upgrades :data:`venv.CORE_VENV_DEPS`."""
    env_dir: Path | str | None = "venv"
    context: types.SimpleNamespace | None = dataclasses.field(default=None, init=False)

    def __post_init__(self):
        """Initialize the environment builder and also creates the environment is does not exist."""
        super().__init__(
            system_site_packages=self.system_site_packages,
            clear=self.clear,
            symlinks=self.symlinks,
            upgrade=self.upgrade,
            with_pip=self.with_pip,
            prompt=self.prompt,
            **({"upgrade_deps": self.upgrade_deps} if sys.version_info >= (3, 9) else {}),
        )
        if self.env_dir:
            self.env_dir = Path(self.env_dir).absolute()
            if self.env_dir.exists():
                self.ensure_directories()
            else:
                self.create(self.env_dir)

    def create(self, env_dir: Path | str | None = None) -> None:
        """Create a virtual environment in a directory.

        Args:
            env_dir: The target directory to create an environment in.
        """
        self.env_dir = env_dir or self.env_dir
        super().create(self.env_dir)

    def ensure_directories(self, env_dir: Path | str | None = None) -> types.SimpleNamespace:
        """Create the directories for the environment.

        Args:
            env_dir: The target directory to create an environment in.

        Returns:
            A context object which holds paths in the environment, for use by subsequent logic.
        """
        self.context = super().ensure_directories(env_dir or self.env_dir)
        return self.context

    def post_setup(self, context: types.SimpleNamespace | None = None) -> None:
        """Hook for post-setup modification of the venv.

        Subclasses may install additional packages or scripts here, add activation shell scripts, etc.

        Args:
            context: The information for the environment creation request being processed.
        """


@dataclasses.dataclass
class FileConfig:
    """FileConfig class."""

    file: Path | None = None
    config: dict = dataclasses.field(default_factory=dict)


@dataclasses.dataclass
class FrameSimple:
    """Simple frame class."""

    back: types.FrameType
    code: types.CodeType
    frame: types.FrameType
    function: str
    globals: dict[str, Any]  # noqa: A003, A003
    lineno: int
    locals: dict[str, Any]  # noqa: A003
    name: str
    package: str
    path: Path
    vars: dict[str, Any]  # noqa: A003


@dataclasses.dataclass
class GroupUser:
    """GroupUser class."""

    group: int | str
    user: int | str


class GitSHA(str, enum.Enum):
    """Git SHA options."""

    BASE = enum.auto()
    LOCAL = enum.auto()
    REMOTE = enum.auto()


class InvalidArgumentError(_NoDepsBaseError):
    """Raised when function is called with invalid argument."""


class LetterCounter:
    """Letter Counter generator function. This way, each time you call next() on the generator.

    It will yield the next counter value. We will also remove the maximum counter check

    Examples:
        >>> from nodeps import LetterCounter
        >>>
        >>> c = LetterCounter("Z")
        >>> assert c.increment() == 'AA'
    """

    def __init__(self, start: str = "A") -> None:
        """Init."""
        self.current_value = [string.ascii_uppercase.index(v) for v in start[::-1]]

    def increment(self) -> str:
        """Increments 1.

        Exaamples:
            >>> from nodeps import LetterCounter
            >>>
            >>> c = LetterCounter('BWDLQZZ')
            >>> assert c.increment() == 'BWDLRAA'
            >>> assert c.increment() == 'BWDLRAB'

        Returns:
            str
        """
        for i in range(len(self.current_value)):
            # If digit is less than Z, increment and finish
            if self.current_value[i] < 25:  # noqa: PLR2004
                self.current_value[i] += 1
                break
            # Otherwise, set digit to A (0) and continue to next digit
            self.current_value[i] = 0
            # If we've just set the most significant digit to A,
            # we need to add another 'A' at the most significant end
            if i == len(self.current_value) - 1:
                self.current_value.append(0)
                break
        # Form the string and return
        return "".join(reversed([string.ascii_uppercase[i] for i in self.current_value]))


class NamedtupleMeta(metaclass=abc.ABCMeta):
    """Namedtuple Metaclass.

    Examples:
        >>> import collections
        >>> from nodeps import NamedtupleMeta
        >>>
        >>> named = collections.namedtuple('named', 'a', defaults=('a', ))
        >>>
        >>> assert isinstance(named(), NamedtupleMeta) == True
        >>> assert isinstance(named(), tuple) == True
        >>>
        >>> assert issubclass(named, NamedtupleMeta) == True
        >>> assert issubclass(named, tuple) == True
    """

    _fields: tuple[str, ...] = ()
    _field_defaults: dict[str, Any] = {}  # noqa: RUF012

    @abc.abstractmethod
    def _asdict(self) -> dict[str, Any]:
        return {}

    # noinspection PyPep8Naming
    @classmethod
    def __subclasshook__(cls, C: type) -> bool:  # noqa: N803
        """Subclass hook."""
        if cls is NamedtupleMeta:
            return (hasattr(C, "_asdict") and callable(C._asdict)) and all(
                [issubclass(C, tuple), hasattr(C, "_fields"), hasattr(C, "_field_defaults")]
            )
        return NotImplemented


@dataclasses.dataclass
class OwnerRepo:
    """Owner Repo and Url Parser Class.

    if scheme is "git+file" will only use repo argument as the path and must be absolute path

    furl:
        - url.query: after "?", i.e. ?ref=master&foo=bar
        - url.args: query args dict, i.e. {'ref': 'master', 'foo': 'bar'}
        - url.fragment: after "#", i.e. #two/directories?one=argument
        - url.fragment.path.segments: i.e. ['two', 'directories']
        - url.fragment.args: i.e. {'one': 'argument'}


    Examples:
        >>> import os
        >>> import pytest
        >>> import nodeps
        >>> from nodeps import OwnerRepo
        >>>
        >>> r = OwnerRepo()
        >>> r.url # doctest: +ELLIPSIS
        'https://github.com/.../nodeps'
        >>> assert r.url == OwnerRepo(nodeps.__file__).url
        >>> OwnerRepo(repo="test").url # doctest: +ELLIPSIS
        'https://github.com/.../test'
        >>> OwnerRepo("cpython", "cpython").url
        'https://github.com/cpython/cpython'
        >>> OwnerRepo(repo="/tmp/cpython", scheme="git+file").url
        'git+file:///tmp/cpython.git'
        >>> OwnerRepo("cpython", "cpython", scheme="git+https").url
        'git+https://github.com/cpython/cpython'
        >>> OwnerRepo("cpython", "cpython", scheme="git+ssh").url
        'git+ssh://git@github.com/cpython/cpython'
        >>> OwnerRepo("cpython", "cpython", scheme="ssh").url
        'git@github.com:cpython/cpython'
        >>> OwnerRepo("cpython", "cpython", scheme="https").url
        'https://github.com/cpython/cpython'

    Args:
        owner: repo owner
        repo: repo name or repo path for git+file scheme
        scheme: Git URL scheme
        data: url or path to get remote url

    Raises:
        InvalidArgumentError: if invalid argument to get URL
    """

    owner: str = dataclasses.field(default=GIT)
    repo: str = dataclasses.field(default=None)
    scheme: str = dataclasses.field(default=GIT_DEFAULT_SCHEME)
    data: ParseResult | Path | str = dataclasses.field(default=None)
    parsed: ParseResult = dataclasses.field(default=None, init=False)
    path: Path = dataclasses.field(default=None, init=False)
    """Url path"""

    def __post_init__(self):
        """Post Init."""
        u = None
        if self.repo:
            if self.scheme == "git+file":
                if not self.repo.startswith("/"):
                    msg = f"Repo must be an absolute file for '{self.scheme}': {self.repo}"
                    raise ValueError(msg)
                self.owner = ""
            u = GITHUB_URL[self.scheme] + self.owner_repo
        elif isinstance(self.data, Path) or self.data is None:
            u = self.remote()
        elif isinstance(self.data, (str | ParseResult)):
            u = self.data

        if u is None:
            msg = f"Invalid repository path or remote url in repository: {self.data}"
            raise InvalidArgumentError(msg)

        self.parsed = urllib.parse.urlparse(u) if isinstance(u, str) else u
        self.path = Path(self.parsed.path.removeprefix("/"))
        if self.parsed.scheme == "git+file" and self.path.suffix == "":
            u = self.parsed.geturl() + ".git"
        elif self.parsed.scheme != "git+file" and self.path.suffix == ".git":
            u = self.parsed.geturl().removesuffix(".git")

        if isinstance(u, str):
            self.parsed = urllib.parse.urlparse(u)
        if self.repo is None:
            self.scheme = self.parsed.scheme
            self.owner = self.path.parts[0]
            self.repo = self.path.parts[1]

    @property
    def owner_repo(self) -> str:
        """Get owner/repo."""
        return f"{self.owner + '/' if self.owner else ''}{self.repo}"

    def remote(self) -> str | None:
        """Get remote url."""
        path = self.data.to_parent() if isinstance(self.data, Path) else Path.cwd() if self.data is None else None
        if path:
            self.data = path
            return stdout(f"git -C {path} config --get remote.origin.url")
        return None

    @property
    def url(self) -> str:
        """Url."""
        rv = self.parsed.geturl()
        if self.scheme == "git+file":
            rv = rv.replace(":/", ":///")
        return rv


@dataclasses.dataclass
class Passwd:
    """Passwd class from either `uid` or `user`.

    Args:
    -----
        uid: int
            User ID
        user: str
            Username

    Attributes:
    -----------
        gid: int
            Group ID
        gecos: str
            Full name
        group: str
            Group name
        groups: tuple(str)
            Groups list
        home: Path
            User's home
        shell: Path
            User shell
        uid: int
            User ID (default: :func:`os.getuid` current user id)
        user: str
            Username
    """

    data: dataclasses.InitVar[AnyPath | str | int] = None
    gid: int = dataclasses.field(default=None, init=False)
    gecos: str = dataclasses.field(default=None, init=False)
    group: str = dataclasses.field(default=None, init=False)
    groups: dict[str, int] = dataclasses.field(default=None, init=False)
    home: Path = dataclasses.field(default=None, init=False)
    shell: Path = dataclasses.field(default=None, init=False)
    uid: int = dataclasses.field(default=None, init=False)
    user: str = dataclasses.field(default=None, init=False)

    def __post_init__(self, data: int | str):
        """Instance of :class:`nodeps:Passwd`  from either `uid` or `user` (default: :func:`os.getuid`).

        Uses completed/real id's (os.getgid, os.getuid) instead effective id's (os.geteuid, os.getegid) as default.
            - UID and GID: when login from $LOGNAME, $USER or os.getuid()
            - RUID and RGID: completed real user id and group id inherit from UID and GID
                (when completed start EUID and EGID and set to the same values as RUID and RGID)
            - EUID and EGID: if executable has 'setuid' or 'setgid' (i.e: ping, sudo), EUID and EGID are changed
                to the owner (setuid) or group (setgid) of the binary.
            - SUID and SGID: if executable has 'setuid' or 'setgid' (i.e: ping, sudo), SUID and SGID are saved with
                RUID and RGID to do unprivileged tasks by a privileged completed (had 'setuid' or 'setgid').
                Can not be accessed in macOS with `os.getresuid()` and `os.getresgid()`

        Examples:
            >>> import pathlib
            >>> from nodeps import MACOS
            >>> from nodeps import Passwd
            >>> from nodeps import Path
            >>>
            >>> default = Passwd()
            >>> user = os.environ["USER"]
            >>> login = Passwd.from_login()
            >>>
            >>> assert default == Passwd(Path()) == Passwd(pathlib.Path())  == Passwd(user) == Passwd(os.getuid()) == \
                    login != Passwd().from_root()
            >>> assert default.gid == os.getgid()
            >>> assert default.home == Path(os.environ["HOME"])
            >>> if shell := os.environ.get("SHELL"):
            ...     assert default.shell == Path(shell)
            >>> assert default.uid == os.getuid()
            >>> assert default.user == user
            >>> if MACOS:
            ...    assert "staff" in default.groups
            ...    assert "admin" in default.groups

        Errors:
            os.setuid(0)
            os.seteuid(0)
            os.setreuid(0, 0)

        os.getuid()
        os.geteuid(
        os.setuid(uid) can only be used if running as root in macOS.
        os.seteuid(euid) -> 0
        os.setreuid(ruid, euid) -> sets EUID and RUID (probar con 501, 0)
        os.setpgid(os.getpid(), 0) -> sets PGID and RGID (probar con 501, 0)

        Returns:
            Instance of :class:`nodeps:Passwd`
        """
        if (isinstance(data, str) and not data.isnumeric()) or isinstance(data, pathlib.PurePosixPath):
            passwd = pwd.getpwnam(cast(str, getattr(data, "owner", lambda: None)() or data))
        else:
            passwd = pwd.getpwuid(int(data) if data or data == 0 else os.getuid())

        self.gid = passwd.pw_gid
        self.gecos = passwd.pw_gecos
        self.home = Path(passwd.pw_dir)
        self.shell = Path(passwd.pw_shell)
        self.uid = passwd.pw_uid
        self.user = passwd.pw_name

        group = grp.getgrgid(self.gid)
        self.group = group.gr_name
        self.groups = {grp.getgrgid(gid).gr_name: gid for gid in os.getgrouplist(self.user, self.gid)}

    @property
    def is_su(self) -> bool:
        """Returns True if login as root, uid=0 and not `SUDO_USER`."""
        return self.uid == 0 and not bool(os.environ.get("SUDO_USER"))

    @property
    def is_sudo(self) -> bool:
        """Returns True if SUDO_USER is set."""
        return bool(os.environ.get("SUDO_USER"))

    @property
    def is_user(self) -> bool:
        """Returns True if user and not `SUDO_USER`."""
        return self.uid != 0 and not bool(os.environ.get("SUDO_USER"))

    @classmethod
    def from_login(cls) -> Passwd:
        """Returns instance of :class:`nodeps:Passwd` from '/dev/console' on macOS and `os.getlogin()` on Linux."""
        try:
            user = Path("/dev/console").owner() if MACOS else os.getlogin()
        except OSError:
            user = Path("/proc/self/loginuid").owner()
        return cls(user)

    @classmethod
    def from_sudo(cls) -> Passwd:
        """Returns instance of :class:`nodeps:Passwd` from `SUDO_USER` if set or current user."""
        uid = os.environ.get("SUDO_UID", os.getuid())
        return cls(uid)

    @classmethod
    def from_root(cls) -> Passwd:
        """Returns instance of :class:`nodeps:Passwd` for root."""
        return cls(0)


@dataclasses.dataclass
class PathStat:
    """Helper class for :func:`nodeps.Path.stats`.

    Args:
        gid: file GID
        group: file group name
        mode: file mode string formatted as '-rwxrwxrwx'
        own: user and group string formatted as 'user:group'
        passwd: instance of :class:`nodeps:Passwd` for file owner
        result: result of os.stat
        root: is owned by root
        sgid: group executable and sticky bit (GID bit), members execute as the executable group (i.e.: crontab)
        sticky: sticky bit (directories), new files created in this directory will be owned by the directory's owner
        suid: user executable and sticky bit (UID bit), user execute and as the executable owner (i.e.: sudo)
        uid: file UID
        user: file user name
    """

    gid: int
    group: str
    mode: str
    own: str
    passwd: Passwd
    result: os.stat_result
    root: bool
    sgid: bool
    sticky: bool
    suid: bool
    uid: int
    user: str


class Path(pathlib.Path, pathlib.PurePosixPath, Generic[_T]):
    """Path helper class."""

    def __call__(
        self,
        name: AnyPath = "",
        file: PathIsLiteral = "is_dir",
        passwd: Passwd | None = None,
        mode: int | str | None = None,
        effective_ids: bool = False,
        follow_symlinks: bool = False,
    ) -> Path:
        """Make dir or touch file and create subdirectories as needed.

        Examples:
            >>> from nodeps import Path
            >>>
            >>> with Path.tempdir() as t:
            ...     p = t('1/2/3/4')
            ...     assert p.is_dir() is True
            ...     p = t('1/2/3/4/5/6/7.py', file="is_file")
            ...     assert p.is_file() is True
            ...     t('1/2/3/4/5/6/7.py/8/9.py', file="is_file") # doctest: +IGNORE_EXCEPTION_DETAIL, +ELLIPSIS
            Traceback (most recent call last):
            NotADirectoryError: File: ...

        Args:
            name: path to add.
            file: file or directory.
            passwd: user.
            mode: mode.
            effective_ids: If True, access will use the effective uid/gid instead of
            follow_symlinks: resolve self if self is symlink (default: True).

        Returns:
            Path.
        """
        # noinspection PyArgumentList
        return (self.mkdir if file in ["is_dir", "exists"] else self.touch)(
            name=name,
            passwd=passwd,
            mode=mode,
            effective_ids=effective_ids,
            follow_symlinks=follow_symlinks,
        )

    def __contains__(self, value: Iterable) -> bool:
        """Checks all items in value exist in self.resolve().

        To check only parts use self.has.

        Examples:
            >>> from nodeps import Path
            >>>
            >>> assert '/usr' in Path('/usr/local')
            >>> assert 'usr local' in Path('/usr/local')
            >>> assert 'home' not in Path('/usr/local')
            >>> assert '' not in Path('/usr/local')
            >>> assert '/' in Path()
            >>> assert os.environ["USER"] in Path.home()

        Args:
            value: space separated list of items to check, or iterable of items.

        Returns:
            bool
        """
        value = self.__class__(value) if isinstance(value, str) and "/" in value else toiter(value)
        return all(item in self.resolve().parts for item in value)

    def __eq__(self, other: Path) -> bool:
        """Equal based on parts.

        Examples:
            >>> from nodeps import Path
            >>>
            >>> assert Path('/usr/local') == Path('/usr/local')
        """
        if not isinstance(other, self.__class__):
            return NotImplemented
        return tuple(self.parts) == tuple(other.parts)

    def __hash__(self) -> int:
        """Hash based on parts."""
        return self._hash if hasattr(self, "_hash") else hash(tuple(self.parts))

    def __iter__(self) -> Iterator[_T]:
        """Iterate over path parts.

        Examples:
            >>> from nodeps import Path
            >>>
            >>> assert list(Path('/usr/local')) == ['/', 'usr', 'local',]

        Returns:
            Iterable of path parts.
        """
        return iter(self.parts)

    def __lt__(self, other: Path) -> bool:
        """Less than based on parts."""
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.parts < other.parts

    def __le__(self, other: Path) -> bool:
        """Less than or equal based on parts."""
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.parts <= other.parts

    def __gt__(self, other: Path) -> bool:
        """Greater than based on parts."""
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.parts > other.parts

    def __ge__(self, other: Path) -> bool:
        """Greater than or equal based on parts."""
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.parts >= other.parts

    def access(
        self,
        os_mode: int = os.W_OK,
        *,
        dir_fd: int | None = None,
        effective_ids: bool = False,
        follow_symlinks: bool = False,
    ) -> bool | None:
        # noinspection LongLine
        """Checks if file or directory exists and has access (returns None if file/directory does not exist.

        Use the real uid/gid to test for access to a path `Real Effective IDs.`_.

        -   real: user owns the completed.
        -   effective: user invoking.

        Examples:
            >>> import os
            >>> from nodeps import Path
            >>> from nodeps import MACOS
            >>>
            >>> assert Path().access() is True
            >>> assert Path('/usr/bin').access() is False
            >>> assert Path('/tmp').access(follow_symlinks=True) is True
            >>> assert Path('/tmp').access(effective_ids=True, follow_symlinks=True) is True
            >>> if MACOS:
            ...     assert Path('/etc/bashrc').access(effective_ids=True) is False
            >>> if MACOS and not os.environ.get("CI"):
            ...     assert Path('/etc/sudoers').access(effective_ids=True, os_mode=os.R_OK) is False


        Args:
            os_mode: Operating-system mode bitfield. Can be F_OK to test existence,
                or the inclusive-OR of R_OK, W_OK, and X_OK (default: `os.W_OK`).
            dir_fd: If not None, it should be a file descriptor open to a directory,
                and path should be relative; path will then be relative to that
                directory.
            effective_ids: If True, access will use the effective uid/gid instead of
                the real uid/gid (default: True).
            follow_symlinks: If False, and the last element of the path is a symbolic link,
                access will examine the symbolic link itself instead of the file
                the link points to (default: False).

        Note:
            Most operations will use the effective uid/gid (what the operating system
            looks at to make a decision whether you are allowed to do something), therefore this
            routine can be used in a suid/sgid environment to test if the invoking user
            has the specified access to the path.

            When a setuid program (`-rwsr-xr-x`) executes, the completed changes its Effective User ID (EUID)
            from the default RUID to the owner of this special binary executable file:

                -   euid: owner of executable (`os.geteuid()`).
                -   uid: user starting the completed (`os.getuid()`).

        Returns:
            True if access.

        See Also:
        `Real Effective IDs.
        <https://stackoverflow.com/questions/32455684/difference-between-real-user-id-effective-user-id-and-saved
        -user-id>`_
        """
        if not self.exists():
            return None
        return os.access(
            self,
            mode=os_mode,
            dir_fd=dir_fd,
            effective_ids=effective_ids,
            follow_symlinks=follow_symlinks,
        )

    def add(self, *args: str, exception: bool = False) -> Path:
        """Add args to self.

        Examples:
            >>> from nodeps import Path
            >>> import nodeps
            >>>
            >>> p = Path().add('a/a')
            >>> assert Path() / 'a/a' == p
            >>> p = Path().add(*['a', 'a'])
            >>> assert Path() / 'a/a' == p
            >>> p = Path(nodeps.__file__)
            >>> p.add('a', exception=True)  # doctest: +IGNORE_EXCEPTION_DETAIL, +ELLIPSIS
            Traceback (most recent call last):
            FileNotFoundError...

        Args:
            *args: parts to be added.
            exception: raise exception if self is not dir and parts can not be added (default: False).

        Raises:
            FileNotFoundError: if self is not dir and parts can not be added.

        Returns:
            Compose path.
        """
        if exception and self.is_file() and args:
            msg = f"parts: {args}, can not be added since path is file or not directory: {self}"
            raise FileNotFoundError(msg)
        args = toiter(args)
        path = self
        for arg in args:
            path = path / arg
        return path

    def append_text(self, text: str, encoding: str | None = None, errors: str | None = None) -> str:
        """Open the file in text mode, append to it, and close the file (creates file if not file).

        Examples:
            >>> from nodeps import Path
            >>>
            >>> with Path.tempfile() as tmp:
            ...    _ = tmp.write_text('Hello')
            ...    assert 'Hello World!' in tmp.append_text(' World!')

        Args:
            text: text to add.
            encoding: encoding (default: None).
            errors: raise error if there is no file (default: None).

        Returns:
            File text with text appended.
        """
        if not isinstance(text, str):
            msg = f"data must be str, not {text.__class__.__name__}"
            raise TypeError(msg)
        with self.open(mode="a", encoding=encoding, errors=errors) as f:
            f.write(text)
        return self.read_text()

    @contextlib.contextmanager
    def cd(self) -> Path:
        """Change dir context manager to self if dir or parent if file and exists.

        Examples:
            >>> from nodeps import Path
            >>>
            >>> new = Path('/usr/local')
            >>> p = Path.cwd()
            >>> with new.cd() as prev:
            ...     assert new == Path.cwd()
            ...     assert prev == p
            >>> assert p == Path.cwd()

        Returns:
            Old Pwd Path.
        """
        oldpwd = self.cwd()
        try:
            self.chdir()
            yield oldpwd
        finally:
            oldpwd.chdir()

    def chdir(self) -> Path:
        """Change to self if dir or file parent if file and file exists.

        Examples:
            >>> from nodeps import Path
            >>>
            >>> new = Path(__file__).chdir()
            >>> assert new == Path(__file__).parent
            >>> assert Path.cwd() == new
            >>>
            >>> new = Path(__file__).parent
            >>> assert Path.cwd() == new
            >>>
            >>> Path("/tmp/foo").chdir()  # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            FileNotFoundError: ... No such file or directory: '/tmp/foo'

        Raises:
            FileNotFoundError: No such file or directory if path does not exist.

        Returns:
            Path with changed directory.
        """
        path = self.to_parent()
        os.chdir(path)
        return path

    def checksum(
        self,
        algorithm: Literal["md5", "sha1", "sha224", "sha256", "sha384", "sha512"] = "sha256",
        block_size: int = 65536,
    ) -> str:
        """Calculate the checksum of a file.

        Examples:
            >>> from nodeps import Path
            >>>
            >>> with Path.tempfile() as tmp:
            ...    _ = tmp.write_text('Hello')
            ...    assert tmp.checksum() == '185f8db32271fe25f561a6fc938b2e264306ec304eda518007d1764826381969'

        Args:
            algorithm: hash algorithm (default: 'sha256').
            block_size: block size (default: 65536).

        Returns:
            Checksum of file.
        """
        sha = hashlib.new(algorithm)
        with self.open("rb") as f:
            for block in iter(lambda: f.read(block_size), b""):
                sha.update(block)
        return sha.hexdigest()

    def chmod(
        self,
        mode: int | str | None = None,
        effective_ids: bool = False,
        exception: bool = True,
        follow_symlinks: bool = False,
        recursive: bool = False,
    ) -> Path:
        """Change mode of self.

        Examples:
            >>> from nodeps import Path
            >>>
            >>> with Path.tempfile() as tmp:
            ...     changed = tmp.chmod(777)
            ...     assert changed.stat().st_mode & 0o777 == 0o777
            ...     assert changed.stats().mode == "-rwxrwxrwx"
            ...     assert changed.chmod("o-x").stats().mode == '-rwxrwxrw-'
            >>>
            >>> Path("/tmp/foo").chmod()  # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            FileNotFoundError: ... No such file or directory: '/tmp/foo'

        Raises:
            FileNotFoundError: No such file or directory if path does not exist and exception is True.

        Args:
            mode: mode to change to (default: None).
            effective_ids: If True, access will use the effective uid/gid instead of
                the real uid/gid (default: False).
            follow_symlinks: resolve self if self is symlink (default: True).
            exception: raise exception if self does not exist (default: True).
            recursive: change owner of self and all subdirectories (default: False).

        Returns:
            Path with changed mode.
        """
        if exception and not self.exists():
            msg = f"path does not exist: {self}"
            raise FileNotFoundError(msg)

        subprocess.run(
            [
                *self.sudo(
                    force=True,
                    effective_ids=effective_ids,
                    follow_symlinks=follow_symlinks,
                ),
                f"{self.chmod.__name__}",
                *(["-R"] if recursive and self.is_dir() else []),
                str(mode or (755 if self.is_dir() else 644)),
                self.resolve() if follow_symlinks else self,
            ],
            capture_output=True,
        )

        return self

    def chown(
        self,
        passwd=None,
        effective_ids: bool = False,
        exception: bool = True,
        follow_symlinks: bool = False,
        recursive: bool = False,
    ) -> Path:
        """Change owner of path.

        Examples:
            >>> from nodeps import Path
            >>> from nodeps import Passwd
            >>> from nodeps import MACOS
            >>>
            >>> with Path.tempfile() as tmp:
            ...     changed = tmp.chown(passwd=Passwd.from_root())
            ...     st = changed.stat()
            ...     assert st.st_gid == 0
            ...     assert st.st_uid == 0
            ...     stats = changed.stats()
            ...     assert stats.gid == 0
            ...     assert stats.uid == 0
            ...     assert stats.user == "root"
            ...     if MACOS:
            ...         assert stats.group == "wheel"
            ...         g = "admin"
            ...     else:
            ...         assert stats.group == "root"
            ...         g = "adm"
            ...     changed = tmp.chown(f"{os.getuid()}:{g}")
            ...     stats = changed.stats()
            ...     assert stats.group == g
            ...     assert stats.uid == os.getuid()
            >>>
            >>> Path("/tmp/foo").chown()  # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            FileNotFoundError: ... No such file or directory: '/tmp/foo'

        Raises:
            FileNotFoundError: No such file or directory if path does not exist and exception is True.
            ValueError: passwd must be string with user:group.

        Args:
            passwd: user/group passwd to use, or string with user:group (default: None).
            effective_ids: If True, access will use the effective uid/gid instead of
                the real uid/gid (default: False).
            exception: raise exception if self does not exist (default: True).
            follow_symlinks: resolve self if self is symlink (default: True).
            recursive: change owner of self and all subdirectories (default: False).

        Returns:
            Path with changed owner.
        """
        if exception and not self.exists():
            msg = f"path does not exist: {self}"
            raise FileNotFoundError(msg)

        if isinstance(passwd, str) and ":" not in passwd:
            msg = f"passwd must be string with user:group, or 'Passwd' instance, got {passwd}"
            raise ValueError(msg)

        passwd = passwd or Passwd.from_login()

        subprocess.run(
            [
                *self.sudo(
                    force=True,
                    effective_ids=effective_ids,
                    follow_symlinks=follow_symlinks,
                ),
                f"{self.chown.__name__}",
                *(["-R"] if recursive and self.is_dir() else []),
                f"{passwd.user}:{passwd.group}" if isinstance(passwd, Passwd) else passwd,
                self.resolve() if follow_symlinks else self,
            ],
            check=True,
            capture_output=True,
        )

        return self

    def cmp(self, other: AnyPath) -> bool:
        """Determine, whether two files provided to it are the same or not.

        By the same means that their contents are the same or not (excluding any metadata).
        Uses Cryptographic Hashes (using SHA256 - Secure hash algorithm 256) as a hash function.

        Examples:
            >>> from nodeps import Path
            >>> import nodeps
            >>> import asyncio
            >>>
            >>> assert Path(nodeps.__file__).cmp(nodeps.__file__) is True
            >>> assert Path(nodeps.__file__).cmp(asyncio.__file__) is False

        Args:
            other: other file to compare to

        Returns:
            True if equal.
        """
        return self.checksum() == self.__class__(other).checksum()

    def cp(
        self,
        dest: AnyPath,
        contents: bool = False,
        effective_ids: bool = False,
        follow_symlinks: bool = False,
        preserve: bool = False,
    ) -> Path:
        """Wrapper for shell `cp` command to copy file recursivily and adding sudo if necessary.

        Examples:
            # FIXME: Ubuntu
            >>> from nodeps import Path
            >>> from nodeps import Passwd
            >>>
            >>> with Path.tempfile() as tmp:
            ...     changed = tmp.chown(passwd=Passwd.from_root())
            ...     copied = Path(__file__).cp(changed)
            ...     st = copied.stat()
            ...     assert st.st_gid == 0
            ...     assert st.st_uid == 0
            ...     stats = copied.stats()
            ...     assert stats.mode == "-rw-------"
            ...     _ = tmp.chown()
            ...     assert copied.cmp(__file__)

            >>> with Path.tempdir() as tmp:
            ...     _ = tmp.chmod("go+rx")
            ...     _ = tmp.chown(passwd=Passwd.from_root())
            ...     src = Path(__file__).parent
            ...     dirname = src.name
            ...     filename = Path(__file__).name
            ...
            ...     _ = src.cp(tmp)
            ...     destination = tmp / dirname
            ...     stats = destination.stats()
            ...     assert stats.mode == "drwxr-xr-x"
            ...     file = destination / filename
            ...     st = file.stat()
            ...     assert st.st_gid == 0
            ...     assert st.st_uid == 0
            ...     assert file.owner() == "root"
            ...     tmp = tmp.chown(recursive=True)
            ...     assert file.owner != "root"
            ...     assert file.cmp(__file__)
            ...
            ...     _ = src.cp(tmp, contents=True)
            ...     file = tmp / filename
            ...     assert (tmp / filename).cmp(__file__)
            >>>
            >>> Path("/tmp/foo").cp("/tmp/boo")  # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            FileNotFoundError: ... No such file or directory: '/tmp/foo'

        Args:
            dest: destination.
            contents: copy contents of self to dest, `cp src/ dest` instead of `cp src dest` (default: False)`.
            effective_ids: If True, access will use the effective uid/gid instead of
                the real uid/gid (default: False).
            follow_symlinks: '-P' the 'cp' default, no symlinks are followed,
                all symbolic links are followed when True '-L' (actual files are copyed but if there are existing links
                will be left them untouched) (default: False)
                `-H` cp option is not implemented (default: False).
            preserve: preserve file attributes (default: False).

        Raises:
            FileNotFoundError: No such file or directory if path does not exist.

        Returns:
            Dest.
        """
        dest = self.__class__(dest)

        if not self.exists():
            msg = f"path does not exist: {self}"
            raise FileNotFoundError(msg)

        subprocess.run(
            [
                *dest.sudo(effective_ids=effective_ids, follow_symlinks=follow_symlinks),
                f"{self.cp.__name__}",
                *(["-R"] if self.is_dir() else []),
                *(["-L"] if follow_symlinks else []),
                *(["-p"] if preserve else []),
                f"{self!s}{'/' if contents else ''}",
                dest,
            ],
            check=True,
            capture_output=True,
        )

        return dest

    def exists(self) -> bool:
        """Check if file exists or is a broken link (super returns False if it is a broken link, we return True).

        Examples:
            >>> from nodeps import Path
            >>>
            >>> Path(__file__).exists()
            True
            >>> with Path.tempcd() as tmp:
            ...    source = tmp.touch("source")
            ...    destination = source.ln("destination")
            ...    assert destination.is_symlink()
            ...    source.unlink()
            ...    assert destination.exists()
            ...    assert not pathlib.Path(destination).exists()

        Returns:
            True if file exists or is broken link.
        """
        if super().exists():
            return True
        return self.is_symlink()

    @classmethod
    def expandvars(cls, path: str | None = None) -> Path:
        """Return a Path instance from expanded environment variables in path.

        Expand shell variables of form $var and ${var}.
        Unknown variables are left unchanged.

        Examples:
            >>> from nodeps import Path
            >>>
            >>> Path.expandvars('~/repo')  # doctest: +ELLIPSIS
            Path('~/repo')
            >>> Path.expandvars('${HOME}/repo')  # doctest: +ELLIPSIS
            Path('.../repo')

        Returns:
            Expanded Path.
        """
        return cls(os.path.expandvars(path) if path is not None else "")

    def file_in_parents(self, exception: bool = True, follow_symlinks: bool = False) -> Path | None:
        """Find up until file with name is found.

        Examples:
            >>> from nodeps import Path
            >>>
            >>> with Path.tempfile() as tmpfile:
            ...     new = tmpfile / "sub" / "file.py"
            ...     assert new.file_in_parents(exception=False) == tmpfile.absolute()
            >>>
            >>> with Path.tempdir() as tmpdir:
            ...    new = tmpdir / "sub" / "file.py"
            ...    assert new.file_in_parents() is None

        Args:
            exception: raise exception if a file is found in parents (default: False).
            follow_symlinks: resolve self if self is symlink (default: True).

        Raises:
            NotADirectoryError: ... No such file or directory: '/tmp/foo'

        Returns:
            File found in parents (str) or None
        """
        path = self.resolve() if follow_symlinks else self
        start = path
        while True:
            if path.is_file():
                if exception:
                    msg = f"File: {path} found in path: {start}"
                    raise NotADirectoryError(msg)
                return path
            if path.is_dir() or (
                path := path.parent.resolve() if follow_symlinks else path.parent.absolute()
            ) == self.__class__("/"):
                return None

    def find_up(
        self, function: PathIsLiteral = "is_file", name: str = "__init__.py", uppermost: bool = False
    ) -> Path | None:
        """Find file or dir up.

        Examples:
            >>> import email.mime.application
            >>> import email
            >>> import email.mime
            >>> from nodeps import Path
            >>>
            >>> assert 'email/mime/__init__.py' in Path(email.mime.__file__).find_up()
            >>> assert 'email/__init__.py' in Path(email.__file__).find_up(uppermost=True)


        Args:
            function: :class:`PIs` (default: PIs.IS_FILE)
            name: name (default: data.INIT_PY).
            uppermost: find uppermost (default: False).

        Returns:
            FindUp:
        """
        start = self.to_parent().absolute()
        latest = None
        found = None
        while True:
            find = start / name
            if getattr(find, function)():
                found = find
                if not uppermost:
                    return find
                latest = find
            start = start.parent
            if start == Path("/"):
                return latest if getattr(latest, function)() else found

    def has(self, value: Iterable) -> bool:
        """Checks all items in value exist in `self.parts` (not absolute and not relative).

        Only checks parts and not resolved as checked by __contains__ or absolute.

        Examples:
            >>> from nodeps import Path
            >>>
            >>> assert Path('/usr/local').has('/usr') is True
            >>> assert Path('/usr/local').has('usr local') is True
            >>> assert Path('/usr/local').has('home') is False
            >>> assert Path('/usr/local').has('') is False

        Args:
            value: space separated list of items to check, or iterable of items.

        Returns:
            bool
        """
        value = self.__class__(value) if isinstance(value, str) and "/" in value else toiter(value)
        return all(item in self.parts for item in value)

    def ln(self, dest: AnyPath, force: bool = True) -> Path:
        """Wrapper for super `symlink_to` to return the new path and changing the argument.

        If symbolic link already exists and have the same source, it will not be overwritten.

        Similar:

            - dest.symlink_to(src)
            - src.ln(dest) -> dest
            - os.symlink(src, dest)

        Examples:
            >>> from nodeps import Path
            >>>
            >>> with Path.tempcd() as tmp:
            ...     source = tmp.touch("source")
            ...     _ = source.ln("destination")
            ...     destination = source.ln("destination")
            ...     assert destination.is_symlink()
            ...     assert destination.resolve() == source.resolve()
            ...     assert destination.readlink().resolve() == source.resolve()
            ...
            ...     touch = tmp.touch("touch")
            ...     _ = tmp.ln("touch", force=False)  # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            FileExistsError:

        Raises:
            FileExistsError: if dest already exists or is a symbolic link with different source and force is False.

        Args:
           dest: link destination (ln -s self dest)
           force: force creation of link, if file or link exists and is different (default: True)
        """
        # TODO: relative symlinks https://gist.dreamtobe.cn/willprice/311faace6fb4f514376fa405d2220615
        dest = self.__class__(dest)
        if dest.is_symlink() and dest.readlink().resolve() == self.resolve():
            return dest
        if force and dest.exists():
            dest.rm()
        os.symlink(self, dest)
        return dest

    def mkdir(
        self,
        name: AnyPath = "",
        passwd: Passwd | None = None,
        mode: int | str | None = None,
        effective_ids: bool = False,
        follow_symlinks: bool = False,
    ) -> Path:
        """Add directory, make directory, change mode and return new Path.

        Examples:
            >>> import getpass
            >>> from nodeps import Path
            >>> from nodeps import Passwd
            >>>
            >>> with Path.tempcd() as tmp:
            ...     directory = tmp('1/2/3/4')
            ...     assert directory.is_dir() is True
            ...     assert directory.owner() == getpass.getuser()
            ...
            ...     _ = directory.chown(passwd=Passwd.from_root())
            ...     assert directory.owner() == "root"
            ...     five = directory.mkdir("5")
            ...     assert five.text.endswith('/1/2/3/4/5') is True
            ...     assert five.owner() == "root"
            ...
            ...     six = directory("6")
            ...     assert six.owner() == "root"
            ...
            ...     seven = directory("7", passwd=Passwd())
            ...     assert seven.owner() == getpass.getuser()
            ...
            ...     _ = directory.chown(passwd=Passwd())

        Args:
            name: name.
            passwd: group/user for chown, if None ownership will not be changed (default: None).
            mode: mode.
            effective_ids: If True, access will use the effective uid/gid instead of
                the real uid/gid (default: True).
            follow_symlinks: resolve self if self is symlink (default: True).

        Raises:
            NotADirectoryError: Directory can not be made because it's a file.

        Returns:
            Path:
        """
        path = (self / str(name)).resolve() if follow_symlinks else (self / str(name))
        if not path.is_dir() and path.file_in_parents(follow_symlinks=follow_symlinks) is None:
            subprocess.run(
                [
                    *path.sudo(effective_ids=effective_ids, follow_symlinks=follow_symlinks),
                    f"{self.mkdir.__name__}",
                    "-p",
                    *(["-m", str(mode)] if mode else []),
                    path,
                ],
                capture_output=True,
            )

            if passwd is not None:
                path.chown(
                    passwd=passwd,
                    effective_ids=effective_ids,
                    follow_symlinks=follow_symlinks,
                )
        return path

    def mv(self, dest: AnyPath) -> Path:
        """Move.

        Examples:
            >>> from nodeps import Path
            >>>
            >>> with Path.tempdir() as tmp:
            ...     name = 'dir'
            ...     pth = tmp(name)
            ...     assert pth.is_dir()
            ...     _ = pth.mv(tmp('dir2'))
            ...     assert not pth.is_dir()
            ...     assert tmp('dir2').is_dir()
            ...     name = 'file'
            ...     pth = tmp(name, "is_file")
            ...     assert pth.is_file()
            ...     _ = pth.mv(tmp('file2'))
            ...     assert not pth.is_file()

        Args:
            dest: destination.

        Returns:
            None.
        """
        subprocess.run(
            [*self.__class__(dest).sudo(), f"{self.mv.__name__}", self, dest],
            check=True,
            capture_output=True,
        )
        return dest

    def open(  # noqa: A003
        self,
        mode: str = "r",
        buffering: int = -1,
        encoding: str | None = None,
        errors: str | None = None,
        newline: str | None = None,
        token: bool = False,
    ) -> AnyIO | None:
        """Open the file pointed by this path and return a file object, as the built-in open function does."""
        if token:
            return tokenize.open(self.text) if self.is_file() else None
        return super().open(
            mode=mode,
            buffering=buffering,
            encoding=encoding,
            errors=errors,
            newline=newline,
        )

    def privileges(self, effective_ids: bool = False):
        """Return privileges of file.

        Args:
            effective_ids: If True, access will use the effective uid/gid instead of
                the real uid/gid (default: True).

        Returns:
            Privileges:
        """

    def realpath(self, exception: bool = False) -> Path:
        """Return the canonical path of the specified filename, eliminating any symbolic links encountered in the path.

        Examples:
            >>> from nodeps import Path
            >>>
            >>> assert Path('/usr/local').realpath() == Path('/usr/local')

        Args:
            exception: raise exception if path does not exist (default: False).

        Returns:
            Path with real path.
        """
        return self.__class__(os.path.realpath(self, strict=not exception))

    def relative(self, path: AnyPath) -> Path | None:
        """Return relative to path if is relative to path else None.

        Examples:
            >>> from nodeps import Path
            >>>
            >>> assert Path('/usr/local').relative('/usr') == Path('local')
            >>> assert Path('/usr/local').relative('/usr/local') == Path('.')
            >>> assert Path('/usr/local').relative('/usr/local/bin') is None

        Args:
            path: path.

        Returns:
            Relative path or None.
        """
        p = Path(path).absolute()
        return self.relative_to(p) if self.absolute().is_relative_to(p) else None

    def rm(
        self, *args: str, effective_ids: bool = False, follow_symlinks: bool = False, missing_ok: bool = True
    ) -> None:
        """Delete a folder/file (even if the folder is not empty).

        Examples:
            >>> from nodeps import Path
            >>>
            >>> with Path.tempdir() as tmp:
            ...     name = 'dir'
            ...     pth = tmp(name)
            ...     assert pth.is_dir()
            ...     pth.rm()
            ...     assert not pth.is_dir()
            ...     name = 'file'
            ...     pth = tmp(name, "is_file")
            ...     assert pth.is_file()
            ...     pth.rm()
            ...     assert not pth.is_file()
            ...     assert Path('/tmp/a/a/a/a')().is_dir()

        Raises:
            FileNotFoundError: ... No such file or directory: '/tmp/foo'

        Args:
            *args: parts to add to self.
            effective_ids: If True, access will use the effective uid/gid instead of
                the real uid/gid (default: False).
            follow_symlinks: True for resolved (default: False).
            missing_ok: missing_ok
        """
        if not missing_ok and not self.exists():
            msg = f"{self} does not exist"
            raise FileNotFoundError(msg)

        if (path := self.add(*args)).exists():
            subprocess.run(
                [
                    *path.sudo(
                        force=True,
                        effective_ids=effective_ids,
                        follow_symlinks=follow_symlinks,
                    ),
                    f"{self.rm.__name__}",
                    *(["-rf"] if self.is_dir() else []),
                    path.resolve() if follow_symlinks else path,
                ],
                capture_output=True,
            )

    def rm_empty(self, preserve: bool = True) -> None:
        """Remove empty directories recursive.

        Examples:
            >>> from nodeps import Path
            >>>
            >>> with Path.tempdir() as tmp:
            ...     first = tmp("1")
            ...
            ...     _ = tmp('1/2/3/4')
            ...     first.rm_empty()
            ...     assert first.exists() is True
            ...     assert Path("1").exists() is False
            ...
            ...     _ = tmp('1/2/3/4')
            ...     first.rm_empty(preserve=False)
            ...     assert first.exists() is False
            ...
            ...     _ = tmp('1/2/3/4/5/6/7.py', file="is_file")
            ...     first.rm_empty()
            ...     assert first.exists() is True

        Args:
            preserve: preserve top directory (default: True).

        """
        for directory, _, _ in os.walk(self, topdown=False):
            d = self.__class__(directory).absolute()
            if len(list(d.iterdir())) == 0 and (not preserve or (d != self.absolute() and preserve)):
                self.__class__(d).rmdir()

    def setid(
        self,
        name: bool | str | None = None,
        uid: bool = True,
        effective_ids: bool = False,
        follow_symlinks: bool = False,
    ) -> Path:
        """Sets the set-user-ID-on-execution or set-group-ID-on-execution bits.

        Works if interpreter binary is setuid `u+s,+x` (-rwsr-xr-x), and:

           - executable script and setuid interpreter on shebang (#!/usr/bin/env setuid_interpreter).
           - setuid_interpreter -m module (venv would be created as root

        Works if interpreter binary is setuid `g+s,+x` (-rwxr-sr-x), and:

        Examples:
            >>> from nodeps import Path
            >>>
            >>> with Path.tempdir() as p:
            ...     a = p.touch('a')
            ...     _ = a.setid()
            ...     assert a.stats().suid is True
            ...     _ = a.setid(uid=False)
            ...     assert a.stats().sgid is True
            ...
            ...     a.rm()
            ...
            ...     _ = a.touch()
            ...     b = a.setid('b')
            ...     assert b.stats().suid is True
            ...     assert a.cmp(b) is True
            ...
            ...     _ = b.setid('b', uid=False)
            ...     assert b.stats().sgid is True
            ...
            ...     _ = a.write_text('a')
            ...     assert a.cmp(b) is False
            ...     b = a.setid('b')
            ...     assert b.stats().suid is True
            ...     assert a.cmp(b) is True

        Args:
            name: name to rename if provided.
            uid: True to set UID bit, False to set GID bit (default: True).
            effective_ids: If True, access will use the effective uid/gid instead of
                the real uid/gid (default: False).
            follow_symlinks: True for resolved, False for absolute and None for relative
                or doesn't exist (default: True).

        Returns:
            Updated Path.
        """
        change = False
        chmod = f'{"u" if uid else "g"}+s,+x'
        mod = (stat.S_ISUID if uid else stat.S_ISGID) | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
        target = self.with_name(name) if name else self
        if name and (not target.exists() or not self.cmp(target)):
            self.cp(target, effective_ids=effective_ids, follow_symlinks=follow_symlinks)
            change = True
        elif target.stats().result.st_mode & mod != mod:
            change = True
        if target.owner() != "root":
            change = True
        if change:
            # First: chown, second: chmod
            target.chown(passwd=Passwd.from_root(), follow_symlinks=follow_symlinks)
            target.chmod(
                mode=chmod,
                effective_ids=effective_ids,
                follow_symlinks=follow_symlinks,
                recursive=True,
            )
        return target

    def setid_cp(
        self,
        name: bool | str | None = None,
        uid: bool = True,
        effective_ids: bool = False,
        follow_symlinks: bool = False,
    ) -> Path:
        """Sets the set-user-ID-on-execution or set-group-ID-on-execution bits.

        Examples:
            >>> from nodeps import Path
            >>>
            >>> with Path.tempdir() as p:
            ...     a = p.touch('a')
            ...     _ = a.setid()
            ...     assert a.stats().suid is True
            ...     _ = a.setid(uid=False)
            ...     assert a.stats().sgid is True
            ...
            ...     a.rm()
            ...
            ...     _ = a.touch()
            ...     b = a.setid('b')
            ...     assert b.stats().suid is True
            ...     assert a.cmp(b) is True
            ...
            ...     _ = b.setid('b', uid=False)
            ...     assert b.stats().sgid is True
            ...
            ...     _ = a.write_text('a')
            ...     assert a.cmp(b) is False
            ...     b = a.setid('b')
            ...     assert b.stats().suid is True
            ...     assert a.cmp(b) is True

        Args:
            name: name to rename if provided.
            uid: True to set UID bit, False to set GID bit (default: True).
            effective_ids: If True, access will use the effective uid/gid instead of
                the real uid/gid (default: False).
            follow_symlinks: True for resolved, False for absolute and None for relative
                or doesn't exist (default: True).

        Returns:
            Updated Path.
        """
        change = False
        chmod = f'{"u" if uid else "g"}+s,+x'
        mod = (stat.S_ISUID if uid else stat.S_ISGID) | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
        target = self.with_name(name) if name else self
        if name and (not target.exists() or not self.cmp(target)):
            self.cp(target, effective_ids=effective_ids, follow_symlinks=follow_symlinks)
            change = True
        elif target.stats().result.st_mode & mod != mod:
            change = True
        if target.owner() != "root":
            change = True
        if change:
            # First: chown, second: chmod
            target.chown(passwd=Passwd.from_root(), follow_symlinks=follow_symlinks)
            target.chmod(
                mode=chmod,
                effective_ids=effective_ids,
                follow_symlinks=follow_symlinks,
                recursive=True,
            )
        return target

    @classmethod
    def setid_executable_cp(cls, name: str | None = None, uid: bool = True) -> Path:
        r"""Sets the set-user-ID-on-execution or set-group-ID-on-execution bits for sys.executable.

        Examples:
            >>> import shutil
            >>> import subprocess
            >>> from nodeps import Path
            >>> def test():
            ...     f = Path.setid_executable_cp('setid_python_test')
            ...     assert subprocess.check_output([f, '-c', 'import os;print(os.geteuid())'], text=True) == '0\n'
            ...     assert subprocess.check_output([f, '-c', 'import os;print(os.getuid())'], text=True) != '0\n'
            ...     f.rm()
            ...     assert f.exists() is False
            >>> test() # doctest: +SKIP

        Args:
            name: name to rename if provided or False to add 'r' to original name (default: False).
            uid: True to set UID bit, False to set GID bit (default: True).

        Returns:
            Updated Path.
        """
        # FIXME: https://developer.apple.com/documentation/security/hardened_runtime
        #  https://gist.github.com/macshome/15f995a4e849acd75caf14f2e50e7e98

        path = cls(sys.executable)
        return path.setid_cp(name=name if name else f"r{path.name}", uid=uid)

    def stats(self, follow_symlinks: bool = False) -> PathStat:
        """Return result of the stat() system call on this path, like os.stat() with extra parsing for bits and root.

        Examples:
            >>> from nodeps import Path
            >>>
            >>> rv = Path().stats()
            >>> assert all([rv.root, rv.sgid, rv.sticky, rv.suid]) is False
            >>>
            >>> with Path.tempfile() as file:
            ...     _ = file.chmod('u+s,+x')
            ...     assert file.stats().suid is True
            ...     _ = file.chmod('g+s,+x')
            ...     assert file.stats().sgid is True

        Args:
            follow_symlinks: If False, and the last element of the path is a symbolic link,
                stat will examine the symbolic link itself instead of the file
                the link points to (default: False).

        Returns:
            PathStat namedtuple :class:`nodeps.PathStat`:
            gid: file GID
            group: file group name
            mode: file mode string formatted as '-rwxrwxrwx'
            own: user and group string formatted as 'user:group'
            passwd: instance of :class:`nodeps:Passwd` for file owner
            result: result of `os.stat`
            root: is owned by root
            sgid: group executable and sticky bit (GID bit), members execute as the executable group (i.e.: crontab)
            sticky: sticky bit (directories), new files created in this directory will be owned by the directory's owner
            suid: user executable and sticky bit (UID bit), user execute and as the executable owner (i.e.: sudo)
            uid: file UID
            user: file owner name
        """
        mapping = {
            "sgid": stat.S_ISGID | stat.S_IXGRP,
            "suid": stat.S_ISUID | stat.S_IXUSR,
            "sticky": stat.S_ISVTX,
        }
        result = super().stat(follow_symlinks=follow_symlinks)
        passwd = Passwd(result.st_uid)
        # noinspection PyArgumentList
        return PathStat(
            gid=result.st_gid,
            group=grp.getgrgid(result.st_gid).gr_name,
            mode=stat.filemode(result.st_mode),
            own=f"{passwd.user}:{passwd.group}",
            passwd=passwd,
            result=result,
            root=result.st_uid == 0,
            uid=result.st_uid,
            user=passwd.user,
            **{i: result.st_mode & mapping[i] == mapping[i] for i in mapping},
        )

    def sudo(
        self,
        force: bool = False,
        to_list: bool = True,
        os_mode: int = os.W_OK,
        effective_ids: bool = False,
        follow_symlinks: bool = False,
    ) -> list[str] | str | None:
        """Returns sudo command if path or ancestors exist and is not own by user and sudo command not installed.

        Examples:
            >>> from nodeps import which
            >>> from nodeps import Path
            >>>
            >>> su = which()
            >>> assert Path('/tmp').sudo(to_list=False, follow_symlinks=True) == ''
            >>> assert "sudo" in Path('/usr/bin').sudo(to_list=False)
            >>> assert Path('/usr/bin/no_dir/no_file.text').sudo(to_list=False) == su
            >>> assert Path('no_dir/no_file.text').sudo(to_list=False) == ''
            >>> assert Path('/tmp').sudo(follow_symlinks=True) == []
            >>> assert Path('/usr/bin').sudo() == [su]

        Args:
            force: if sudo installed and user is ot root, return always sudo path
            to_list: return starred/list for command with no shell (default: True).
            os_mode: Operating-system mode bitfield. Can be F_OK to test existence,
                or the inclusive-OR of R_OK, W_OK, and X_OK (default: `os.W_OK`).
            effective_ids: If True, access will use the effective uid/gid instead of
                the real uid/gid (default: True).
            follow_symlinks: If False, and the last element of the path is a symbolic link,
                access will examine the symbolic link itself instead of the file
                the link points to (default: False).

        Returns:
            `sudo` or "", str or list.
        """
        if (rv := which()) and (os.geteuid if effective_ids else os.getuid)() != 0:
            path = self
            while path:
                if path.access(
                    os_mode=os_mode,
                    effective_ids=effective_ids,
                    follow_symlinks=follow_symlinks,
                ):
                    if not force:
                        rv = ""
                    break
                if path.exists() or str(path := (path.parent.resolve() if follow_symlinks else path.parent)) == "/":
                    break
        return ([rv] if rv else []) if to_list else rv

    @property
    def text(self) -> str:
        """Path as text.

        Examples:
            >>> from nodeps import Path
            >>>
            >>> assert Path('/usr/local').text == '/usr/local'

        Returns:
            Path string.
        """
        return str(self)

    @classmethod
    @contextlib.contextmanager
    def tempcd(
        cls, suffix: AnyStr | None = None, prefix: AnyStr | None = None, directory: AnyPath | None = None
    ) -> Path:
        """Create temporaly directory, change to it and return it.

        This has the same behavior as mkdtemp but can be used as a context manager.

        Upon exiting the context, the directory and everything contained
        in it are removed.

        Examples:
            >>> from nodeps import Path
            >>>
            >>> work = Path.cwd()
            >>> with Path.tempcd() as tmp:
            ...     assert tmp.exists() and tmp.is_dir()
            ...     assert Path.cwd() == tmp.resolve()
            >>> assert work == Path.cwd()
            >>> assert tmp.exists() is False

        Args:
            suffix: If 'suffix' is not None, the directory name will end with that suffix,
                otherwise there will be no suffix. For example, .../T/tmpy5tf_0suffix
            prefix: If 'prefix' is not None, the directory name will begin with that prefix,
                otherwise a default prefix is used.. For example, .../T/prefixtmpy5tf_0
            directory: If 'directory' is not None, the directory will be created in that directory (must exist,
                otherwise a default directory is used. For example, DIRECTORY/tmpy5tf_0

        Returns:
            Directory Path.
        """
        with cls.tempdir(suffix=suffix, prefix=prefix, directory=directory) as tmpdir, tmpdir.cd():
            try:
                yield tmpdir
            finally:
                pass

    @classmethod
    @contextlib.contextmanager
    def tempdir(
        cls, suffix: AnyStr | None = None, prefix: AnyStr | None = None, directory: AnyPath | None = None
    ) -> Path:
        """Create and return tmp directory.  This has the same behavior as mkdtemp but can be used as a context manager.

        Upon exiting the context, the directory and everything contained in it are removed.

        Examples:
            >>> from nodeps import Path
            >>>
            >>> work = Path.cwd()
            >>> with Path.tempdir() as tmpdir:
            ...     assert tmpdir.exists() and tmpdir.is_dir()
            ...     assert Path.cwd() != tmpdir
            ...     assert work == Path.cwd()
            >>> assert tmpdir.exists() is False

        Args:
            suffix: If 'suffix' is not None, the directory name will end with that suffix,
                otherwise there will be no suffix. For example, .../T/tmpy5tf_0suffix
            prefix: If 'prefix' is not None, the directory name will begin with that prefix,
                otherwise a default prefix is used.. For example, .../T/prefixtmpy5tf_0
            directory: If 'directory' is not None, the directory will be created in that directory (must exist,
                otherwise a default directory is used. For example, DIRECTORY/tmpy5tf_0

        Returns:
            Directory Path.
        """
        with tempfile.TemporaryDirectory(suffix=suffix, prefix=prefix, dir=directory) as tmp:
            try:
                yield cls(tmp)
            finally:
                pass

    @classmethod
    @contextlib.contextmanager
    def tempfile(
        cls,
        mode: Literal[
            "r",
            "w",
            "a",
            "x",
            "r+",
            "w+",
            "a+",
            "x+",
            "rt",
            "wt",
            "at",
            "xt",
            "r+t",
            "w+t",
            "a+t",
            "x+t",
        ] = "w",
        buffering: int = -1,
        encoding: str | None = None,
        newline: str | None = None,
        suffix: AnyStr | None = None,
        prefix: AnyStr | None = None,
        directory: AnyPath | None = None,
        delete: bool = True,
        *,
        errors: str | None = None,
    ) -> Path:
        """Create and return a temporary file.

        Examples:
            >>> from nodeps import Path
            >>>
            >>> with Path.tempfile() as tmpfile:
            ...    assert tmpfile.exists() and tmpfile.is_file()
            >>> assert tmpfile.exists() is False

        Args:
            mode: the mode argument to io.open (default "w+b").
            buffering:  the buffer size argument to io.open (default -1).
            encoding: the encoding argument to `io.open` (default None)
            newline: the newline argument to `io.open` (default None)
            delete: whether the file is deleted on close (default True).
            suffix: prefix for filename.
            prefix: prefix for filename.
            directory: directory.
            errors: the errors' argument to `io.open` (default None)

        Returns:
            An object with a file-like interface; the name of the file
            is accessible as its 'name' attribute.  The file will be automatically
            deleted when it is closed unless the 'delete' argument is set to False.
        """
        with tempfile.NamedTemporaryFile(
            mode=mode,
            buffering=buffering,
            encoding=encoding,
            newline=newline,
            suffix=suffix,
            prefix=prefix,
            dir=directory,
            delete=delete,
            errors=errors,
        ) as tmp:
            try:
                yield cls(tmp.name)
            finally:
                pass

    def to_parent(self) -> Path:
        """Return Parent if is file and exists or self.

        Examples:
            >>> from nodeps import Path
            >>>
            >>> assert Path(__file__).to_parent() == Path(__file__).parent

        Returns:
            Path of directory if is file or self.
        """
        return self.parent if self.is_file() else self

    def touch(
        self,
        name: AnyPath = "",
        passwd: Passwd | None = None,
        mode: int | str | None = None,
        effective_ids: bool = False,
        follow_symlinks: bool = False,
    ) -> Path:
        """Add file, touch and return post_init Path. Parent paths are created.

        Examples:
            >>> from nodeps import Path
            >>> from nodeps import Passwd
            >>>
            >>> import getpass
            >>> with Path.tempcd() as tmp:
            ...     file = tmp('1/2/3/4/5/6/root.py', file="is_file", passwd=Passwd.from_root())
            ...     assert file.is_file() is True
            ...     assert file.parent.owner() == getpass.getuser()
            ...     assert file.owner() == "root"
            ...
            ...     new = file.parent("user.py", file="is_file")
            ...     assert new.owner() == getpass.getuser()
            ...
            ...     touch = file.parent.touch("touch.py")
            ...     assert touch.owner() == getpass.getuser()
            ...
            ...     last = (file.parent / "last.py").touch()
            ...     assert last.owner() == getpass.getuser()
            ...     assert last.is_file() is True
            ...
            ...     file.rm()

        Args:
            name: name.
            passwd: group/user for chown, if None ownership will not be changed (default: None).
            mode: mode.
            effective_ids: If True, access will use the effective uid/gid instead of
                the real uid/gid (default: False).
            follow_symlinks: If False, I think is useless (default: False).

        Returns:
            Path.
        """
        path = self / str(name)
        path = path.resolve() if follow_symlinks else path.absolute()
        if (
            not path.is_file()
            and not path.is_dir()
            and path.parent.file_in_parents(follow_symlinks=follow_symlinks) is None
        ):
            if not (d := path.parent).exists():
                d.mkdir(
                    mode=mode,
                    effective_ids=effective_ids,
                    follow_symlinks=follow_symlinks,
                )
            subprocess.run(
                [
                    *path.sudo(effective_ids=effective_ids, follow_symlinks=follow_symlinks),
                    f"{self.touch.__name__}",
                    path,
                ],
                capture_output=True,
                check=True,
            )
            path.chmod(mode=mode, effective_ids=effective_ids, follow_symlinks=follow_symlinks)
            if passwd is not None:
                path.chown(
                    passwd=passwd,
                    effective_ids=effective_ids,
                    follow_symlinks=follow_symlinks,
                )
        return path

    def with_suffix(self, suffix: str = "") -> Path:
        """Sets default for suffix to "", since :class:`pathlib.Path` does not have default.

        Return a new path with the file suffix changed.  If the path
        has no suffix, add given suffix.  If the given suffix is an empty
        string, remove the suffix from the path.

        Examples:
            >>> from nodeps import Path
            >>>
            >>> Path("/tmp/test.txt").with_suffix()
            Path('/tmp/test')

        Args:
            suffix: suffix (default: '')

        Returns:
            Path.
        """
        return super().with_suffix(suffix=suffix)


AnyPath: TypeAlias = Path | AnyPath


class PipMetaPathFinder(importlib.abc.MetaPathFinder):
    """A importlib.abc.MetaPathFinder to auto-install missing modules using pip.

    Examples:
        >>> from nodeps import PipMetaPathFinder
        >>>
        >>> sys.meta_path.append(PipMetaPathFinder)
        >>> # noinspection PyUnresolvedReferences
        >>> import simplejson  # doctest: +SKIP
    """

    # noinspection PyMethodOverriding,PyMethodParameters
    def find_spec(
        fullname: str,
        path: Sequence[str | bytes] | None,
        target: types.ModuleType | None = None,
    ) -> importlib._bootstrap.ModuleSpec | None:
        """Try to find a module spec for the specified module."""
        packages = {
            "linkify_it": "linkify-it-py",
        }
        exclude = ["cPickle", "ctags", "PIL"]
        if path is None and fullname is not None and fullname not in exclude:

            package = packages.get(fullname) or fullname.split(".")[0].replace("_", "-")
            try:
                importlib.metadata.Distribution.from_name(package)
            except importlib.metadata.PackageNotFoundError as e:
                if subprocess.run([sys.executable, "-m", "pip", "install", "-q", package]).returncode == 0:
                    return importlib.import_module(fullname)
                msg = f"Cannot install: {package=},  {fullname=}"
                raise RuntimeError(msg) from e
        return None


class ProjectRepos(str, enum.Enum):
    """Options to show repos in Project class."""

    DICT = enum.auto()
    INSTANCES = enum.auto()
    NAMES = enum.auto()
    PATHS = enum.auto()


@dataclasses.dataclass
class Project:
    """Project Class."""

    data: Path | str | types.ModuleType = None
    """File, directory or name (str or path with one word) of project (default: current working directory)"""
    brewfile: Path | None = dataclasses.field(default=None, init=False)
    """Data directory Brewfile"""
    ci: bool = dataclasses.field(default=False, init=False)
    """running in CI or tox"""
    data_dir: Path | None = dataclasses.field(default=None, init=False)
    """Data directory"""
    directory: Path | None = dataclasses.field(default=None, init=False)
    """Parent of data if data is a file or None if it is a name (one word)"""
    docsdir: Path | None = dataclasses.field(default=None, init=False)
    """Docs directory"""
    git: str = dataclasses.field(default="git", init=False)
    """git -C directory if self.directory is not None"""
    installed: bool = dataclasses.field(default=False, init=False)
    name: str = dataclasses.field(default=None, init=False)
    """Pypi project name from setup.cfg, pyproject.toml or top name or self.data when is one word"""
    profile: Path | None = dataclasses.field(default=None, init=False)
    """Data directory profile.d"""
    pyproject_toml: FileConfig = dataclasses.field(default_factory=FileConfig, init=False)
    repo: Path = dataclasses.field(default=None, init=False)
    """top or superproject"""
    root: Path = dataclasses.field(default=None, init=False)
    """pyproject.toml or setup.cfg parent or superproject or top directory"""
    source: Path | None = dataclasses.field(default=None, init=False)
    """sources directory, parent of __init__.py or module path"""
    tomlkit: types.ModuleType | None = dataclasses.field(default=None, init=False)
    clean_match: ClassVar[list[str]] = ["*.egg-info", "build", "dist"]

    def __post_init__(self):  # noqa: PLR0912, PLR0915
        """Post init."""
        self.ci = any([in_tox(), os.environ.get("CI")])
        self.data = self.data if self.data else Path.cwd()
        data = Path(self.data.__file__ if isinstance(self.data, types.ModuleType) else self.data)
        if (
            (isinstance(self.data, str) and len(toiter(self.data, split="/")) == 1)
            or (isinstance(self.data, pathlib.PosixPath) and len(self.data.parts) == 1)
        ) and (str(self.data) != "/"):
            if r := self.repos(ret=ProjectRepos.DICT).get(self.data if isinstance(self.data, str) else self.data.name):
                self.directory = r
        elif data.is_dir():
            self.directory = data.absolute()
        elif data.is_file():
            self.directory = data.parent.absolute()
        else:
            msg = f"Invalid argument: {self.data=}"
            raise InvalidArgumentError(msg)

        if self.directory:
            self.git = f"git -C '{self.directory}'"
            if path := (
                findup(self.directory, name="pyproject.toml", uppermost=True)
                or findfile("pyproject.toml", self.directory)
            ):
                path = path[0] if isinstance(path, list) else path
                with pipmetapathfinder():
                    self.tomlkit = importlib.import_module("tomlkit")
                with Path.open(path, "rb") as f:
                    self.pyproject_toml = FileConfig(path, self.tomlkit.load(f))
                self.name = self.pyproject_toml.config.get("project", {}).get("name")
                self.root = path.parent

            self.repo = self.top() or self.superproject()
            purelib = sysconfig.get_paths()["purelib"]
            if root := self.root or self.repo:
                self.root = root.absolute()
                if (src := (root / "src")) and (str(src) not in sys.path):
                    sys.path.insert(0, str(src))
            elif self.directory.is_relative_to(purelib):
                self.name = Path(self.directory).relative_to(purelib).parts[0]
            self.name = self.name if self.name else self.root.name if self.root else None
        else:
            self.name = str(self.data)

        try:
            if self.name and ((spec := importlib.util.find_spec(self.name)) and spec.origin):
                self.source = Path(spec.origin).parent if "__init__.py" in spec.origin else Path(spec.origin)
                self.installed = True
                self.root = self.root if self.root else self.source.parent
                purelib = sysconfig.get_paths()["purelib"]
                self.installed = bool(self.source.is_relative_to(purelib) or Path(purelib).name in str(self.source))
        except (ModuleNotFoundError, ImportError):
            pass

        if self.source:
            self.data_dir = d if (d := self.source / "data").is_dir() else None
            if self.data_dir:
                self.brewfile = b if (b := self.data_dir / "Brewfile").is_file() else None
                self.profile = pr if (pr := self.data_dir / "profile.d").is_dir() else None
        if self.root:
            self.docsdir = doc if (doc := self.root / "docs").is_dir() else None
        self.log = ColorLogger.logger(__name__)

    def info(self, msg: str):
        """Logger info."""
        self.log.info(msg, extra={"extra": self.name})

    def warning(self, msg: str):
        """Logger warning."""
        self.log.warning(msg, extra={"extra": self.name})

    def bin(self, executable: str | None = None, version: str = PYTHON_DEFAULT_VERSION) -> Path:  # noqa: A003
        """Bin directory.

        Args;
            executable: command to add to path
            version: python version
        """
        return Path(self.executable(version=version)).parent / executable if executable else ""

    def brew(self, c: str | None = None) -> int:
        """Runs brew bundle."""
        if which("brew") and self.brewfile and (c is None or not which(c)):
            rv = subprocess.run(
                [
                    "brew",
                    "bundle",
                    "--no-lock",
                    "--quiet",
                    f"--file={self.brewfile}",
                ],
                shell=False,
            ).returncode
            self.info(self.brew.__name__)
            return rv
        return 0

    def browser(self, version: str = PYTHON_DEFAULT_VERSION, quiet: bool = True) -> int:
        """Build and serve the documentation with live reloading on file changes.

        Arguments:
            version: python version
            quiet: quiet mode (default: True)
        """
        if not self.docsdir:
            return 0
        build_dir = self.docsdir / "_build"
        q = "-Q" if quiet else ""
        if build_dir.exists():
            shutil.rmtree(build_dir)

        if (
            subprocess.check_call(
                f"{self.executable(version=version)} -m sphinx_autobuild {q} {self.docsdir} {build_dir}", shell=True
            )
            == 0
        ):
            self.info(self.docs.__name__)
        return 0

    def build(self, version: str = PYTHON_DEFAULT_VERSION, quiet: bool = True) -> Path | None:
        """Build a project `venv`, `completions`, `docs` and `clean`.

        Arguments:
            version: python version (default: PYTHON_DEFAULT_VERSION)
            quiet: quiet mode (default: True)
        """
        # TODO: el pth sale si execute en terminal pero no en run
        if not self.pyproject_toml.file:
            return None
        self.venv(version=version)
        self.completions()
        self.docs(quiet=quiet)
        self.clean()
        rv = subprocess.run(
            f"{self.executable(version=version)} -m build {self.root} --wheel",
            stdout=subprocess.PIPE,
            shell=True,
        )
        if rv.returncode != 0:
            sys.exit(rv.returncode)
        wheel = rv.stdout.splitlines()[-1].decode().split(" ")[2]
        if "py3-none-any.whl" not in wheel:
            raise CalledProcessError(completed=rv)
        self.info(
            f"{self.build.__name__}: {wheel}: {version}",
        )
        return self.root / "dist" / wheel

    def builds(self, quiet: bool = True) -> None:
        """Build a project `venv`, `completions`, `docs` and `clean`.

        Arguments:
            quiet: quiet mode (default: True)
        """
        if self.ci:
            self.build(quiet=quiet)
        else:
            for version in PYTHON_VERSIONS:
                self.build(version=version, quiet=quiet)

    def buildrequires(self) -> list[str]:
        """pyproject.toml build-system requires."""
        if self.pyproject_toml.file:
            return self.pyproject_toml.config.get("build-system", {}).get("requires", [])
        return []

    def clean(self) -> None:
        """Clean project."""
        if not in_tox():
            for item in self.clean_match:
                try:
                    for file in self.root.rglob(item):
                        if file.is_dir():
                            shutil.rmtree(self.root / item, ignore_errors=True)
                        else:
                            file.unlink(missing_ok=True)
                except FileNotFoundError:
                    pass

    def commit(self, msg: str | None = None) -> None:
        """commit.

        Raises:
            CalledProcessError: if  fails
            RuntimeError: if diverged or dirty
        """
        if self.dirty():
            if self.needpull():
                msg = f"Diverged: {self.name=}"
                raise RuntimeError(msg)
            if msg is None or msg == "":
                msg = "fix: "
            subprocess.check_call(f"{self.git} add -A", shell=True)
            subprocess.check_call(f"{self.git} commit -a --quiet -m '{msg}'", shell=True)
            self.info(self.commit.__name__)

    def completions(self, uninstall: bool = False):
        """Generate completions to /usr/local/etc/bash_completion.d."""
        value = []

        if self.pyproject_toml.file:
            value = self.pyproject_toml.config.get("project", {}).get("scripts", {}).keys()
        elif d := self.distribution():
            value = [item.name for item in d.entry_points]
        if value:
            for item in value:
                if file := completions(item, uninstall=uninstall):
                    self.info(f"{self.completions.__name__}: {item} -> {file}")

    def coverage(self) -> int:
        """Runs coverage."""
        if (
            self.pyproject_toml.file
            and subprocess.check_call(f"{self.executable()} -m coverage run -m pytest {self.root}", shell=True) == 0
            and subprocess.check_call(
                f"{self.executable()} -m coverage report --data-file={self.root}/reports/.coverage",
                shell=True,
            )
            == 0
        ):
            self.info(self.coverage.__name__)
        return 0

    def dependencies(self) -> list[str]:
        """Dependencies from pyproject.toml or distribution."""
        if self.pyproject_toml.config:
            return self.pyproject_toml.config.get("project", {}).get("dependencies", [])
        if d := self.distribution():
            return [item for item in d.requires if "; extra" not in item]
        msg = f"Dependencies not found for {self.name=}"
        raise RuntimeWarning(msg)

    def dirty(self) -> bool:
        """Is repository dirty  including untracked files."""
        return bool(stdout(f"{self.git} status -s"))

    def distribution(self) -> importlib.metadata.Distribution | None:
        """Distribution."""
        return suppress(importlib.metadata.Distribution.from_name, self.name)

    def diverge(self) -> bool:
        """Diverge."""
        return (self.dirty() or self.needpush()) and self.needpull()

    def docs(self, version: str = PYTHON_DEFAULT_VERSION, quiet: bool = True) -> int:
        """Build the documentation.

        Arguments:
            version: python version
            quiet: quiet mode (default: True)
        """
        if not self.docsdir:
            return 0
        build_dir = self.docsdir / "_build"
        q = "-Q" if quiet else ""
        if build_dir.exists():
            shutil.rmtree(build_dir)

        if (
            subprocess.check_call(
                f"{self.executable(version=version)} -m sphinx {q} --color {self.docsdir} {build_dir}",
                shell=True,
            )
            == 0
        ):
            self.info(f"{self.docs.__name__}: {version}")
        return 0

    def executable(self, version: str = PYTHON_DEFAULT_VERSION) -> Path:
        """Executable."""
        return v / f"bin/python{version}" if (v := self.root / "venv").is_dir() and not self.ci else sys.executable

    @staticmethod
    def _extras(d):
        e = {}
        for item in d:
            if "; extra" in item:
                key = item.split("; extra == ")[1].replace("'", "").replace('"', "").removesuffix(" ")
                if key not in e:
                    e[key] = []
                e[key].append(item.split("; extra == ")[0].replace('"', "").removesuffix(" "))
        return e

    def extras(self, as_list: bool = False) -> dict[str, list[str]] | list[str]:
        """Optional dependencies from pyproject.toml or distribution.

        Examples:
            >>> import typer
            >>> from nodeps import Project
            >>>
            >>> nodeps = Project.nodeps()
            >>> nodeps.extras()  # doctest: +ELLIPSIS
            {'ansi': ['...
            >>> nodeps.extras(as_list=True)  # doctest: +ELLIPSIS
            ['...
            >>> Project(typer.__name__).extras()  # doctest: +ELLIPSIS
            {'all':...
            >>> Project("sampleproject").extras()  # doctest: +ELLIPSIS
            {'dev':...

        Args:
            as_list: return as list

        Returns:
            dict or list
        """
        if self.pyproject_toml.config:
            e = self.pyproject_toml.config.get("project", {}).get("optional-dependencies", {})
        elif d := self.distribution():
            e = self._extras(d.requires)
        elif pypi := self.pypi():
            e = self._extras(pypi["info"]["requires_dist"])
        else:
            msg = f"Extras not found for {self.name=}"
            raise RuntimeWarning(msg)

        if as_list:
            return sorted({extra for item in e.values() for extra in item})
        return e

    def github(
        self,
    ) -> dict[str, str | list | dict[str, str | list | dict[str, str | list]]]:
        """GitHub repo api.

        Examples:
            >>> from nodeps import Project
            >>> from nodeps import NODEPS_PROJECT_NAME
            >>>
            >>> assert Project(NODEPS_PROJECT_NAME).github()["name"] == NODEPS_PROJECT_NAME

        Returns:
            dict: pypi information
        """
        return urljson(f"https://api.github.com/repos/{GIT}/{self.name}")

    def latest(self) -> str:
        """Latest tag: git {c} describe --abbrev=0 --tags."""
        latest = stdout(f"{self.git} tag | sort -V | tail -1") or ""
        if not latest:
            latest = "0.0.0"
            self.commit()
            self._tag(latest)
        return latest

    def needpull(self) -> bool:
        """Needs pull."""
        return (self.sha() != self.sha(GitSHA.REMOTE)) and (self.sha() == self.sha(GitSHA.BASE))

    def needpush(self) -> bool:
        """Needs push, commits not been pushed already."""
        return (
            (self.sha() != self.sha(GitSHA.REMOTE))
            and (self.sha() != self.sha(GitSHA.BASE))
            and (self.sha(GitSHA.REMOTE) == self.sha(GitSHA.BASE))
        )

    def _next(self, part: Bump = Bump.PATCH) -> str:
        latest = self.latest()
        v = "v" if latest.startswith("v") else ""
        version = latest.replace(v, "").split(".")
        match part:
            case Bump.MAJOR:
                index = 0
            case Bump.MINOR:
                index = 1
            case _:
                index = 2
        version[index] = str(int(version[index]) + 1)
        return f"{v}{'.'.join(version)}"

    def next(self, part: Bump = Bump.PATCH, force: bool = False) -> str:  # noqa: A003
        """Show next version based on fix: feat: or BREAKING CHANGE:.

        Args:
            part: part to increase if force
            force: force bump
        """
        latest = self.latest()
        out = stdout(f"git log --pretty=format:'%s' {latest}..@")
        if force:
            return self._next(part)
        if out:
            if "BREAKING CHANGE:" in out:
                return self._next(Bump.MAJOR)
            if "feat:" in out:
                return self._next(Bump.MINOR)
            if "fix:" in out:
                return self._next()
        return latest

    @classmethod
    def nodeps(cls) -> Project:
        """Project Instance of nodeps."""
        return cls(__file__)

    def publish(
        self,
        part: Bump = Bump.PATCH,
        force: bool = False,
        ruff: bool = True,
        tox: bool = False,
        quiet: bool = True,
    ):
        """Publish runs runs `tests`, `commit`, `tag`, `push`, `twine` and `clean`.

        Args:
            part: part to increase if force
            force: force bump
            ruff: run ruff
            tox: run tox
            quiet: quiet mode (default: True)
        """
        self.tests(ruff=ruff, tox=tox, quiet=quiet)
        self.commit()
        if (n := self.next(part=part, force=force)) != (l := self.latest()):
            self.tag(n)
            self.push()
            if rc := self.twine() != 0:
                sys.exit(rc)
            self.info(f"{self.publish.__name__}: {l} -> {n}")
        else:
            self.warning(f"{self.publish.__name__}: {n} -> nothing to do")

        self.clean()

    def pull(self) -> None:
        """pull.

        Raises:
            CalledProcessError: if pull fails
            RuntimeError: if diverged or dirty
        """
        if self.diverge():
            msg = f"Diverged: {self.diverge()} or dirty: {self.diverge()} - {self.name=}"
            raise RuntimeError(msg)
        if self.needpull():
            subprocess.check_call(f"{self.git} fetch --all  --tags --quiet", shell=True)
            subprocess.check_call(f"{self.git} pull --quiet", shell=True)
            self.info(self.pull.__name__)

    def push(self) -> None:
        """push.

        Raises:
            CalledProcessError: if push fails
            RuntimeError: if diverged
        """
        self.commit()
        if self.needpush():
            if self.needpull():
                msg = f"Diverged: {self.name=}"
                raise RuntimeError(msg)
            subprocess.check_call(f"{self.git} push --quiet", shell=True)
            self.info(self.push.__name__)

    def pypi(
        self,
    ) -> dict[str, str | list | dict[str, str | list | dict[str, str | list]]]:
        """Pypi information for a package.

        Examples:
            >>> from nodeps import Project
            >>> from nodeps import NODEPS_PROJECT_NAME
            >>>
            >>> assert Project(NODEPS_PROJECT_NAME).pypi()["info"]["name"] == NODEPS_PROJECT_NAME

        Returns:
            dict: pypi information
        """
        return urljson(f"https://pypi.org/pypi/{self.name}/json")

    def pytest(self, version: str = PYTHON_DEFAULT_VERSION) -> int:
        """Runs pytest."""
        if self.pyproject_toml.file:
            rc = subprocess.run(f"{self.executable(version=version)} -m pytest {self.root}", shell=True).returncode
            self.info(f"{self.pytest.__name__}: {version}")
            return rc
        return 0

    def pytests(self) -> int:
        """Runs pytest for all versions."""
        rc = 0
        if self.ci:
            rc = self.pytest()
        else:
            for version in PYTHON_VERSIONS:
                rc = self.pytest(version=version)
                if rc != 0:
                    sys.exit(rc)
        return rc

    @classmethod
    def repos(
        cls,
        ret: ProjectRepos = ProjectRepos.NAMES,
        py: bool = False,
        sync: bool = False,
        archive: bool = False,
    ) -> list[Path] | list[str] | dict[str, Project | str]:
        """Repo paths, names or Project instances under home and Archive.

        Args:
            ret: return names, paths, dict or instances
            py: return only python projects instances
            sync: push or pull all repos
            archive: look for repos under ~/Archive
        """
        if py or sync:
            ret = ProjectRepos.INSTANCES
        names = ret is ProjectRepos.NAMES
        add = sorted(add.iterdir()) if (add := Path.home() / "Archive").is_dir() and archive else []

        rv = [
            item.name if names else item
            for item in add + sorted(Path.home().iterdir())
            if item.is_dir() and (item / ".git").exists()
        ]
        if ret == ProjectRepos.DICT:
            return {item.name: item for item in rv}
        if ret == ProjectRepos.INSTANCES:
            rv = {item.name: cls(item) for item in rv}
            if sync:
                for item in rv.values():
                    item.sync()
            if py:
                rv = [item for item in rv.values() if item.pyproject_toml.file]
            return rv
        return rv

    def requirement(
        self, version: str = PYTHON_DEFAULT_VERSION, install: bool = False, upgrade: bool = False
    ) -> list[str] | int:
        """Dependencies and optional dependencies from pyproject.toml or distribution."""
        req = sorted({*self.dependencies() + self.extras(as_list=True)})
        req = [item for item in req if not item.startswith(f"{self.name}[")]
        if (install or upgrade) and req:
            upgrade = ["--upgrade"] if upgrade else []
            rv = subprocess.check_call([self.executable(version), "-m", "pip", "install", "-q", *upgrade, *req])
            self.info(f"{self.requirements.__name__}: {version}")
            return rv
        return req

    def requirements(self, upgrade: bool = False) -> None:
        """Install dependencies and optional dependencies from pyproject.toml or distribution for python versions."""
        if self.ci:
            self.requirement(install=True, upgrade=upgrade)
        else:
            for version in PYTHON_VERSIONS:
                self.requirement(version=version, install=True, upgrade=upgrade)

    def ruff(self, version: str = PYTHON_DEFAULT_VERSION) -> int:
        """Runs ruff."""
        if self.pyproject_toml.file:
            rv = subprocess.run(f"{self.executable(version=version)} -m ruff check {self.root}", shell=True).returncode
            self.info(f"{self.ruff.__name__}: {version}")
            return rv
        return 0

    def secrets(self) -> int:
        """Runs ruff."""
        if os.environ.get("CI"):
            return 0
        if (
            subprocess.check_call("gh secret set GH_TOKEN --body $GITHUB_TOKEN", shell=True) == 0
            and (secrets := Path.home() / "secrets/profile.d/secrets.sh").is_file()
        ):
            with tempfile.NamedTemporaryFile() as tmp:
                subprocess.check_call(
                    f"grep -v GITHUB_ {secrets} > {tmp.name} && gh secret set -f {tmp.name}",
                    shell=True,
                )
                self.info(self.secrets.__name__)
        return 0

    def sha(self, ref: GitSHA = GitSHA.LOCAL) -> str:
        """Sha for local, base or remote."""
        if ref is GitSHA.LOCAL:
            args = "rev-parse @"
        elif ref is GitSHA.BASE:
            args = "merge-base @ @{u}"
        elif ref is GitSHA.REMOTE:
            args = "rev-parse @{u}"
        else:
            msg = f"Invalid argument: {ref=}"
            raise InvalidArgumentError(msg)
        return stdout(f"{self.git} {args}")

    def sync(self):
        """Sync repository."""
        self.push()
        self.pull()

    def superproject(self) -> Path | None:
        """Git rev-parse --show-superproject-working-tree --show-toplevel."""
        if v := stdout(
            f"{self.git} rev-parse --show-superproject-working-tree --show-toplevel",
            split=True,
        ):
            return Path(v[0])
        return None

    def _tag(self, tag: str) -> None:
        subprocess.check_call(f"{self.git} tag {tag}", shell=True)
        subprocess.check_call(f"{self.git} push origin {tag} --quiet", shell=True)
        self.info(f"{self.tag.__name__}: {tag}")

    def tag(self, tag: str) -> None:
        """tag.

        Raises:
            CalledProcessError: if push fails
        """
        if self.latest() == tag:
            self.warning(f"{self.tag.__name__}: {tag} -> nothing to do")
            return
        self._tag(tag)

    # TODO: delete all tags and pypi versions

    def test(
        self, version: str = PYTHON_DEFAULT_VERSION, ruff: bool = True, tox: bool = False, quiet: bool = True
    ) -> int:
        """Test project, runs `build`, `ruff`, `pytest` and `tox`.

        Arguments:
            version: python version
            ruff: run ruff (default: True)
            tox: run tox (default: True)
            quiet: quiet mode (default: True)
        """
        self.build(version=version, quiet=quiet)
        if ruff and (rc := self.ruff(version=version) != 0):
            sys.exit(rc)

        if rc := self.pytest(version=version) != 0:
            sys.exit(rc)

        if tox and (rc := self.tox() != 0):
            sys.exit(rc)

        return rc

    def tests(self, ruff: bool = True, tox: bool = False, quiet: bool = True) -> int:
        """Test project, runs `build`, `ruff`, `pytest` and `tox` for all versions.

        Arguments:
            ruff: runs ruff
            tox: runs tox
            quiet: quiet mode (default: True)
        """
        rc = 0
        if self.ci:
            rc = self.test(ruff=ruff, tox=tox, quiet=quiet)
        else:
            for version in PYTHON_VERSIONS:
                rc = self.test(version=version, ruff=ruff, tox=tox, quiet=quiet)
                if rc != 0:
                    sys.exit(rc)
        return rc

    def top(self) -> Path | None:
        """Git rev-parse --show-toplevel."""
        if v := stdout(f"{self.git} rev-parse --show-toplevel"):
            return Path(v)
        return None

    def tox(self) -> int:
        """Runs tox."""
        if self.pyproject_toml.file:
            rv = subprocess.run(f"{self.executable()} -m tox --root {self.root}", shell=True).returncode
            self.info(self.tox.__name__)
            return rv
        return 0

    def twine(
        self,
        part: Bump = Bump.PATCH,
        force: bool = False,
    ) -> int:
        """Twine.

        Args:
            part: part to increase if force
            force: force bump
        """
        pypi = d.version if (d := self.distribution()) else None

        if (
            self.pyproject_toml.file
            and (pypi != self.next(part=part, force=force))
            and "Private :: Do Not Upload" not in self.pyproject_toml.config.get("project", {}).get("classifiers", [])
        ):
            return subprocess.run(
                f"{self.executable()} -m twine upload -u __token__  {self.build()}",
                shell=True,
            ).returncode
        return 0

    def version(self) -> str:
        """Version from pyproject.toml, tag, distribution or pypi."""
        if (v := self.pyproject_toml.config.get("project", {}).get("version")) or (self.top and (v := self.latest())):
            return v
        if d := self.distribution():
            return d.version
        if pypi := self.pypi():
            return pypi["info"]["version"]
        msg = f"Version not found for {self.name=} {self.directory=}"
        raise RuntimeWarning(msg)

    def venv(
        self,
        version: str = PYTHON_DEFAULT_VERSION,
        clear: bool = False,
        upgrade: bool = False,
    ) -> None:
        """Creates venv, runs: `write` and `requirements`."""
        version = "" if self.ci else version
        if not self.pyproject_toml.file:
            return
        if not self.root:
            msg = f"Undefined: {self.root=} for {self.name=} {self.directory=}"
            raise RuntimeError(msg)
        self.write()
        if not self.ci:
            v = self.root / "venv"
            python = f"python{version}"
            clear = "--clean" if clear else ""
            subprocess.check_call(f"{python} -m venv {v} --prompt '.' {clear} --upgrade-deps --upgrade",
                                  shell=True)
            self.info(f"{self.venv.__name__}: {version}")
        self.requirement(version=version, install=True, upgrade=upgrade)

    def venvs(
        self,
        upgrade: bool = False,
    ):
        """Installs venv for all python versions in :data:`PYTHON_VERSIONS`."""
        if self.ci:
            self.venv(upgrade=upgrade)
        else:
            for version in PYTHON_VERSIONS:
                self.venv(version=version, upgrade=upgrade)

    def write(self):
        """Updates pyproject.toml and docs conf.py."""
        if self.pyproject_toml.file:
            original_project = copy.deepcopy(self.pyproject_toml.config.get("project", {}))
            github = self.github()
            project = {
                "name": github["name"],
                "authors": [
                    {"name": AUTHOR, "email": EMAIL},
                ],
                "description": github["description"],
                "urls": {"Homepage": github["html_url"]},
                "dynamic": ["version"],
                "license": {"text": "MIT"},
                "readme": "README.md",
                "requires-python": f">={PYTHON_DEFAULT_VERSION}",
            }
            if "project" not in self.pyproject_toml.config:
                self.pyproject_toml.config["project"] = {}
            for key, value in project.items():
                if key not in self.pyproject_toml.config["project"]:
                    self.pyproject_toml.config["project"][key] = value

            self.pyproject_toml.config["project"] = dict_sort(self.pyproject_toml.config["project"])
            if original_project != self.pyproject_toml.config["project"]:
                with self.pyproject_toml.file.open("w") as f:
                    self.tomlkit.dump(self.pyproject_toml.config, f)
                    self.info(f"{self.write.__name__}: {self.pyproject_toml.file}")

            if self.docsdir:
                imp = f"import {NODEPS_PROJECT_NAME}.__main__" if self.name == NODEPS_PROJECT_NAME else ''
                conf = f"""import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
{imp}
project = "{github["name"]}"
author = "{AUTHOR}"
copyright = "{datetime.datetime.now().year}, {AUTHOR}"
extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.extlinks",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_click",
    "sphinx.ext.intersphinx",
]
autoclass_content = "both"
autodoc_default_options = {{"members": True, "member-order": "bysource",
                           "undoc-members": True, "show-inheritance": True}}
autodoc_typehints = "description"
autosectionlabel_prefix_document = True
html_theme = "furo"
html_title, html_last_updated_fmt = "{self.name} docs", "%Y-%m-%dT%H:%M:%S"
inheritance_alias = {{}}
nitpicky = True
nitpick_ignore = [('py:class', '*')]
toc_object_entries = True
toc_object_entries_show_parents = "all"
pygments_style, pygments_dark_style = "sphinx", "monokai"
extlinks = {{
    "issue": ("https://github.com/{GIT}/{self.name}/issues/%s", "#%s"),
    "pull": ("https://github.com/{GIT}/{self.name}/pull/%s", "PR #%s"),
    "user": ("https://github.com/%s", "@%s"),
}}
intersphinx_mapping = {{
    "python": ("https://docs.python.org/3", None),
    "packaging": ("https://packaging.pypa.io/en/latest", None),
}}
"""  # noqa: DTZ005
                file = self.docsdir / "conf.py"
                original = file.read_text() if file.is_file() else ""
                if original != conf:
                    file.write_text(conf)
                    self.info(f"{self.write.__name__}: {file}")

                requirements = """furo >=2023.9.10, <2024
linkify-it-py >=2.0.2, <3
myst-parser >=2.0.0, <3
sphinx >=7.2.6, <8
sphinx-autobuild >=2021.3.14, <2022
sphinx-click >=5.0.1, <6
sphinx_autodoc_typehints
sphinxcontrib-napoleon >=0.7, <1
"""
                file = self.docsdir / "requirements.txt"
                original = file.read_text() if file.is_file() else ""
                if original != requirements:
                    file.write_text(requirements)
                    self.info(f"{self.write.__name__}: {file}")

                reference = f"""# Reference

## {self.name}

```{{eval-rst}}
.. automodule:: {self.name}
   :members:
```
"""
                file = self.docsdir / "reference.md"
                original = file.read_text() if file.is_file() else ""
                if original != reference:
                    file.write_text(reference)
                    self.info(f"{self.write.__name__}: {file}")


class PTHBuildPy(build_py):
    """Build py with pth files installed."""

    def run(self):
        """Run build py."""
        super().run()
        self.outputs = []
        self.outputs = _copy_pths(self, self.build_lib)

    def get_outputs(self, include_bytecode=1):
        """Get outputs."""
        return itertools.chain(build_py.get_outputs(self, 0), self.outputs)


class PTHDevelop(develop):
    """PTH Develop Install."""

    def run(self):
        """Run develop."""
        super().run()
        _copy_pths(self, self.install_dir)


class PTHEasyInstall(easy_install):
    """PTH Easy Install."""

    def run(self, *args, **kwargs):
        """Run easy install."""
        super().run(*args, **kwargs)
        _copy_pths(self, self.install_dir)


class PTHInstallLib(install_lib):
    """PTH Install Library."""

    def run(self):
        """Run Install Library."""
        super().run()
        self.outputs = []
        self.outputs = _copy_pths(self, self.install_dir)

    def get_outputs(self):
        """Get outputs."""
        return itertools.chain(install_lib.get_outputs(self), self.outputs)


class TempDir(tempfile.TemporaryDirectory):
    """Wrapper for :class:`tempfile.TemporaryDirectory` that provides Path-like.

    Examples:
        >>> from nodeps import TempDir
        >>> from nodeps import MACOS
        >>> with TempDir() as tmp:
        ...     if MACOS:
        ...         assert tmp.parts[1] == "var"
        ...         assert tmp.resolve().parts[1] == "private"
    """

    def __enter__(self) -> Path:
        """Return the path of the temporary directory.

        Returns:
            Path of the temporary directory
        """
        return Path(self.name)


def _copy_pths(self: PTHBuildPy | PTHDevelop | PTHEasyInstall | PTHInstallLib, directory: str) -> list[str]:
    log = ColorLogger.logger()
    outputs = []
    data = self.get_outputs() if isinstance(self, (PTHBuildPy | PTHInstallLib)) else self.outputs
    for source in data:
        if source.endswith(".pth"):
            destination = Path(directory, Path(source).name)
            if not destination.is_file() or not filecmp.cmp(source, destination):
                destination = str(destination)
                msg = f"{self.__class__.__name__}: {str(Path(sys.executable).resolve())[-4:]}"
                log.info(msg, extra={"extra": f"{source} -> {destination}"},)
                self.copy_file(source, destination)
                outputs.append(destination)
    return outputs


def _pip_base_command(self: Command, args: list[str]) -> int:
    """Post install pip patch."""
    try:
        log = ColorLogger.logger()
        with self.main_context():
            rv = self._main(args)
            if rv == 0 and self.__class__.__name__ == "InstallCommand":
                for key, value in _NODEPS_PIP_POST_INSTALL.items():
                    p = Project(key)
                    p.completions()
                    p.brew()
                    for file in findfile(NODEPS_PIP_POST_INSTALL_FILENAME, value):
                        log.info(self.__class__.__name__, extra={"extra": f"post install '{key}': {file}"})
                        exec_module_from_file(file)
            return rv
    finally:
        logging.shutdown()


def _pip_install_wheel(
    name: str,
    wheel_path: str,
    scheme: pip._internal.models.scheme.Scheme,
    req_description: str,
    pycompile: bool = True,
    warn_script_location: bool = True,
    direct_url: pip._internal.models.direct_url.DirectUrl | None = None,
    requested: bool = False,
):
    """Pip install wheel patch to post install."""
    with zipfile.ZipFile(wheel_path) as z, pip._internal.operations.install.wheel.req_error_context(req_description):
        pip._internal.operations.install.wheel._install_wheel(
            name=name,
            wheel_zip=z,
            wheel_path=wheel_path,
            scheme=scheme,
            pycompile=pycompile,
            warn_script_location=warn_script_location,
            direct_url=direct_url,
            requested=requested,
        )
        global _NODEPS_PIP_POST_INSTALL  # noqa: PLW0602
        _NODEPS_PIP_POST_INSTALL[name] = Path(scheme.purelib, name)


def _pip_uninstall_req(
        self, auto_confirm: bool = False, verbose: bool = False
):
    """Pip uninstall patch to post install."""
    assert self.req  # noqa: S101
    p = Project(self.req.name)
    p.completions(uninstall=True)

    dist = pip._internal.metadata.get_default_environment().get_distribution(self.req.name)
    if not dist:
        pip._internal.req.req_install.logger.warning("Skipping %s as it is not installed.", self.name)
        return None
    pip._internal.req.req_install.logger.info("Found existing installation: %s", dist)
    uninstalled_pathset = pip._internal.req.req_uninstall.UninstallPathSet.from_dist(dist)
    uninstalled_pathset.remove(auto_confirm, verbose)
    return uninstalled_pathset


async def aioclone(
    owner: str | None = None,
    repository: str = NODEPS_PROJECT_NAME,
    scheme: GitSchemeLiteral = GIT_DEFAULT_SCHEME,
    path: Path | str | None = None,
) -> Path:
    """Async Clone Repository.

    Examples:
        >>> import asyncio
        >>> from nodeps import TempDir
        >>> from nodeps import aioclone
        >>>
        >>> with TempDir() as tmp:
        ...     directory = tmp / "1" / "2" / "3"
        ...     rv = asyncio.run(aioclone("octocat", "Hello-World", path=directory))
        ...     assert (rv / "README").exists()

    Args:
        owner: github owner, None to use GIT or USER environment variable if not defined (Default: `GIT`)
        repository: github repository (Default: `PROJECT`)
        scheme: url scheme (Default: "https")
        path: path to clone (Default: `repo`)

    Returns:
        Path of cloned repository
    """
    path = path or Path.cwd() / repository
    path = Path(path)
    if not path.exists():
        if not path.parent.exists():
            path.parent.mkdir()
        await aiocmd("git", "clone", OwnerRepo(owner, repository, scheme).url, path)
    return path


def aioclosed() -> bool:
    """Check if event loop is closed."""
    return asyncio.get_event_loop().is_closed()


async def aiocmd(*args, **kwargs) -> subprocess.CompletedProcess:
    """Async Exec Command.

    Examples:
        >>> import asyncio
        >>> from nodeps import aiocmd
        >>> from nodeps import TempDir
        >>> with TempDir() as tmp:
        ...     rv = asyncio.run(aiocmd("git", "clone", "https://github.com/octocat/Hello-World.git", cwd=tmp))
        ...     assert rv.returncode == 0
        ...     assert (tmp / "Hello-World" / "README").exists()

    Args:
        *args: command and args
        **kwargs: subprocess.run kwargs

    Raises:
        JetBrainsError

    Returns:
        None
    """
    proc = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, **kwargs
    )

    out, err = await proc.communicate()
    completed = subprocess.CompletedProcess(
        args, returncode=proc.returncode, stdout=out.decode() if out else None, stderr=err.decode() if err else None
    )
    if completed.returncode != 0:
        raise CmdError(completed)
    return completed


async def aiocommand(
    data: str | list, decode: bool = True, utf8: bool = False, lines: bool = False
) -> subprocess.CompletedProcess:
    """Asyncio run cmd.

    Args:
        data: command.
        decode: decode and strip output.
        utf8: utf8 decode.
        lines: split lines.

    Returns:
        CompletedProcess.
    """
    proc = await asyncio.create_subprocess_shell(
        data, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, loop=asyncio.get_running_loop()
    )
    out, err = await proc.communicate()
    if decode:
        out = out.decode().rstrip(".\n")
        err = err.decode().rstrip(".\n")
    elif utf8:
        out = out.decode("utf8").strip()
        err = err.decode("utf8").strip()

    out = out.splitlines() if lines else out

    return subprocess.CompletedProcess(data, proc.returncode, out, cast(Any, err))


async def aiodmg(src: Path | str, dest: Path | str) -> None:
    """Async Open dmg file and copy the app to dest.

    Examples:
        >>> from nodeps import aiodmg
        >>> async def test():    # doctest: +SKIP
        ...     await aiodmg(Path("/tmp/JetBrains.dmg"), Path("/tmp/JetBrains"))

    Args:
        src: dmg file
        dest: path to copy to

    Returns:
        CompletedProcess
    """
    with TempDir() as tmpdir:
        await aiocmd("hdiutil", "attach", "-mountpoint", tmpdir, "-nobrowse", "-quiet", src)
        for item in src.iterdir():
            if item.name.endswith(".app"):
                await aiocmd("cp", "-r", tmpdir / item.name, dest)
                await aiocmd("xattr", "-r", "-d", "com.apple.quarantine", dest)
                await aiocmd("hdiutil", "detach", tmpdir, "-force")
                break


async def aiogz(src: Path | str, dest: Path | str = ".") -> Path:
    """Async ncompress .gz src to dest (default: current directory).

    It will be uncompressed to the same directory name as src basename.
    Uncompressed directory will be under dest directory.

    Examples:
        >>> from nodeps import TempDir
        >>> from nodeps import aiogz
        >>>
        >>> cwd = Path.cwd()
        >>> with TempDir() as workdir:
        ...     os.chdir(workdir)
        ...     with TempDir() as compress:
        ...         file = compress / "test.txt"
        ...         _ = file.touch()
        ...         compressed = tardir(compress)
        ...         with TempDir() as uncompress:
        ...             uncompressed = asyncio.run(aiogz(compressed, uncompress))
        ...             assert uncompressed.is_dir()
        ...             assert Path(uncompressed).joinpath(file.name).exists()
        >>> os.chdir(cwd)

    Args:
        src: file to uncompress
        dest: destination directory to where uncompress directory will be created (default: current directory)

    Returns:
        Absolute Path of the Uncompressed Directory
    """
    return await asyncio.to_thread(gz, src, dest)


def aioloop() -> RunningLoop | None:
    """Get running loop."""
    return noexc(RuntimeError, asyncio.get_running_loop)


def aioloopid() -> int | None:
    """Get running loop id."""
    try:
        return asyncio.get_running_loop()._selector
    except RuntimeError:
        return None


def aiorunning() -> bool:
    """Check if event loop is running."""
    return asyncio.get_event_loop().is_running()


def allin(origin: Iterable, destination: Iterable) -> bool:
    """Checks all items in origin are in destination iterable.

    Examples:
        >>> from nodeps import allin
        >>> from nodeps.variables.builtin import BUILTIN_CLASS
        >>>
        >>> class Int(int):
        ...     pass
        >>> allin(tuple.__mro__, BUILTIN_CLASS)
        True
        >>> allin(Int.__mro__, BUILTIN_CLASS)
        False
        >>> allin('tuple int', 'bool dict int')
        False
        >>> allin('bool int', ['bool', 'dict', 'int'])
        True
        >>> allin(['bool', 'int'], ['bool', 'dict', 'int'])
        True

    Args:
        origin: origin iterable.
        destination: destination iterable to check if origin items are in.

    Returns:
        True if all items in origin are in destination.
    """
    origin = toiter(origin)
    destination = toiter(destination)
    return all(x in destination for x in origin)


def ami(user: str = "root") -> bool:
    """Check if Current User is User in Argument (default: root).

    Examples:
        >>> from nodeps import ami
        >>> from nodeps import USER
        >>>
        >>> ami(USER)
        True
        >>> ami()
        False

    Arguments:
        user: to check against current user (Default: root)

    Returns:
        bool True if I am user, False otherwise
    """
    return os.getuid() == pwd.getpwnam(user or getpass.getuser()).pw_uid


def anyin(origin: Iterable, destination: Iterable) -> Any | None:
    """Checks any item in origin are in destination iterable and return the first found.

    Examples:
        >>> from nodeps import anyin
        >>> from nodeps.variables.builtin import BUILTIN_CLASS
        >>>
        >>> class Int(int):
        ...     pass
        >>> anyin(tuple.__mro__, BUILTIN_CLASS)
        <class 'tuple'>
        >>> assert anyin('tuple int', BUILTIN_CLASS) is None
        >>> anyin('tuple int', 'bool dict int')
        'int'
        >>> anyin('tuple int', ['bool', 'dict', 'int'])
        'int'
        >>> anyin(['tuple', 'int'], ['bool', 'dict', 'int'])
        'int'

    Args:
        origin: origin iterable.
        destination: destination iterable to check if any of origin items are in.

    Returns:
        First found if any item in origin are in destination.
    """
    origin = toiter(origin)
    destination = toiter(destination)
    for item in toiter(origin):
        if item in destination:
            return item
    return None


@contextlib.contextmanager
def chdir(data: StrOrBytesPath | bool = True) -> Iterable[tuple[Path, Path]]:
    """Change directory and come back to previous directory.

    Examples:
        # FIXME: Ubuntu
        >>> from pathlib import Path

        >>> from nodeps import chdir
        >>> from nodeps import MACOS
        >>>
        >>> previous = Path.cwd()
        >>> new = Path('/usr/local')
        >>> with chdir(new) as (pr, ne):
        ...     assert previous == pr
        ...     assert new == ne
        ...     assert ne == Path.cwd()
        >>>
        >>> new = Path('/bin/ls')
        >>> with chdir(new) as (pr, ne):
        ...     assert previous == pr
        ...     assert new.parent == ne
        ...     assert ne == Path.cwd()
        >>>
        >>> new = Path('/bin/foo')
        >>> with chdir(new) as (pr, ne):
        ...     assert previous == pr
        ...     assert new.parent == ne
        ...     assert ne == Path.cwd()
        >>>
        >>> with chdir() as (pr, ne):
        ...     assert previous == pr
        ...     if MACOS:
        ...         assert "var" in str(ne)
        ...     assert ne == Path.cwd() # doctest: +SKIP

    Args:
        data: directory or parent if file or True for temp directory

    Returns:
        Old directory and new directory
    """

    def y(new):
        os.chdir(new)
        return oldpwd, new

    oldpwd = Path.cwd()
    try:
        if data is True:
            with TempDir() as tmp:
                yield y(tmp)
        else:
            yield y(parent(data, none=False))
    finally:
        os.chdir(oldpwd)


def clone(
    owner: str | None = None,
    repository: str = NODEPS_PROJECT_NAME,
    scheme: GitSchemeLiteral = GIT_DEFAULT_SCHEME,
    path: Path | str = None,
) -> Path:
    """Clone Repository.

    Examples:
        >>> import os
        >>> from nodeps import TempDir
        >>> from nodeps import clone
        >>>
        >>> with TempDir() as tmp:
        ...     directory = tmp / "1" / "2" / "3"
        >>> if not os.environ.get("CI"):
        ...     rv = clone("octocat", "Hello-World", "git+ssh", directory)
        ...     assert (rv / "README").exists()

    Args:
        owner: github owner, None to use GIT or USER environment variable if not defined (Default: `GIT`)
        repository: github repository (Default: `PROJECT`)
        scheme: url scheme (Default: "https")
        path: path to clone (Default: `repo`)

    Returns:
        CompletedProcess
    """
    path = path or Path.cwd() / repository
    path = Path(path)
    if not path.exists():
        if not path.parent.exists():
            path.parent.mkdir()
        cmd("git", "clone", OwnerRepo(owner, repository, scheme).url, path)
    return path


def cmd(*args, **kwargs) -> subprocess.CompletedProcess:
    """Exec Command.

    Examples:
        >>> from nodeps import TempDir
        >>> with TempDir() as tmp:
        ...     rv = cmd("git", "clone", "https://github.com/octocat/Hello-World.git", tmp)
        ...     assert rv.returncode == 0
        ...     assert (tmp / "README").exists()

    Args:
        *args: command and args
        **kwargs: subprocess.run kwargs

    Raises:
        CmdError

    Returns:
        None
    """
    completed = subprocess.run(args, **kwargs, capture_output=True, text=True)

    if completed.returncode != 0:
        raise CmdError(completed)
    return completed


def cmdrun(
    data: Iterable, exc: bool = False, lines: bool = True, shell: bool = True, py: bool = False, pysite: bool = True
) -> subprocess.CompletedProcess | int | list | str:
    r"""Runs a cmd.

    Examples:
        >>> from nodeps import cmdrun
        >>> from nodeps import in_tox
        >>>
        >>> cmdrun('ls a')  # doctest: +ELLIPSIS
        CompletedProcess(args='ls a', returncode=..., stdout=[], stderr=[...])
        >>> assert 'Requirement already satisfied' in cmdrun('pip install pip', py=True).stdout[0]
        >>> cmdrun('ls a', shell=False, lines=False)  # doctest: +ELLIPSIS
        CompletedProcess(args=['ls', 'a'], returncode=..., stdout='', stderr=...)
        >>> cmdrun('echo a', lines=False)  # Extra '\' added to avoid docstring error.
        CompletedProcess(args='echo a', returncode=0, stdout='a\n', stderr='')
        >>> assert "venv" not in cmdrun("sysconfig", py=True, lines=False).stdout
        >>> if not in_tox():
        ...     assert "venv" in cmdrun("sysconfig", py=True, pysite=False, lines=False).stdout

    Args:
        data: command.
        exc: raise exception.
        lines: split lines so ``\\n`` is removed from all lines (extra '\' added to avoid docstring error).
        py: runs with python executable.
        shell: expands shell variables and one line (shell True expands variables in shell).
        pysite: run on site python if running on a VENV.

    Returns:
        Union[CompletedProcess, int, list, str]: Completed process output.

    Raises:
        CmdError:
    """
    if py:
        m = "-m"
        if isinstance(data, str) and data.startswith("/"):
            m = ""
        data = f"{EXECUTABLE_SITE if pysite else EXECUTABLE} {m} {data}"
    elif not shell:
        data = toiter(data)

    text = not lines

    proc = subprocess.run(data, shell=shell, capture_output=True, text=text)

    def std(out=True):
        if out:
            if lines:
                return proc.stdout.decode("utf-8").splitlines()
            return proc.stdout
        if lines:
            return proc.stderr.decode("utf-8").splitlines()
        return proc.stderr

    rv = subprocess.CompletedProcess(proc.args, proc.returncode, std(), std(False))
    if rv.returncode != 0 and exc:
        raise CmdError(rv)
    return rv


def cmdsudo(*args, user: str = "root", **kwargs) -> subprocess.CompletedProcess | None:
    """Run Program with sudo if user is different that the current user.

    Arguments:
        *args: command and args to run
        user: run as user (Default: False)
        **kwargs: subprocess.run kwargs

    Returns:
        CompletedProcess if the current user is not the same as user, None otherwise
    """
    if not ami(user):
        return cmd(["sudo", "-u", user, *args], **kwargs)
    return None


def command(*args, **kwargs) -> subprocess.CompletedProcess:
    """Exec Command with the following defaults compared to :func:`subprocess.run`.

        - capture_output=True
        - text=True
        - check=True

    Examples:
        >>> from nodeps import TempDir
        >>> with TempDir() as tmp:
        ...     rv = command("git", "clone", "https://github.com/octocat/Hello-World.git", tmp)
        ...     assert rv.returncode == 0
        ...     assert (tmp / ".git").exists()

    Args:
        *args: command and args
        **kwargs: `subprocess.run` kwargs

    Raises:
        CmdError

    Returns:
        None
    """
    completed = subprocess.run(args, **kwargs, capture_output=True, text=True)

    if completed.returncode != 0:
        raise CalledProcessError(completed=completed)
    return completed


def completions(name: str, install: bool = True, uninstall: bool = False) -> str | None:
    """Generate completions for command.

    Args:
        name: command name
        install: install completions to /usr/local/etc/bash_completion.d/ or /etc/bash_completion.d
        uninstall: uninstall completions

    Returns:
        Path to file if installed or prints if not installed
    """
    completion = f"""# shellcheck shell=bash

#
# generated by {__file__}

#######################################
# {name} completion
# Globals:
#   COMPREPLY
#   COMP_CWORD
#   COMP_WORDS
# Arguments:
#   1
# Returns:
#   0 ...
#######################################
_{name}_completion() {{
    local IFS=$'
'
  mapfile -t COMPREPLY < <(env COMP_WORDS="${{COMP_WORDS[*]}}" \\
    COMP_CWORD="${{COMP_CWORD}}" \\
    _{name.upper()}_COMPLETE=complete_bash "$1")
  return 0
}}

complete -o default -F _{name}_completion {name}
"""
    path = Path("/usr/local/etc/bash_completion.d" if MACOS else "/etc/bash_completion.d").mkdir()
    file = Path(path, f"{NODEPS_PROJECT_NAME}:{name}.bash")
    if uninstall:
        file.unlink(missing_ok=True)
        return None
    if install:
        if not file.is_file() or (file.read_text() != completion):
            file.write_text(completion)
            return str(file)
        return None
    print(completion)
    return None


def current_task_name() -> str:
    """Current asyncio task name."""
    return asyncio.current_task().get_name() if aioloop() else ""


def dict_sort(
    data: dict[_KT, _VT], ordered: bool = False, reverse: bool = False
) -> dict[_KT, _VT] | collections.OrderedDict[_KT, _VT]:
    """Order a dict based on keys.

    Examples:
        >>> import platform
        >>> from collections import OrderedDict
        >>> from nodeps import dict_sort
        >>>
        >>> d = {"b": 2, "a": 1, "c": 3}
        >>> dict_sort(d)
        {'a': 1, 'b': 2, 'c': 3}
        >>> dict_sort(d, reverse=True)
        {'c': 3, 'b': 2, 'a': 1}
        >>> v = platform.python_version()
        >>> if "rc" not in v:
        ...     # noinspection PyTypeHints
        ...     assert dict_sort(d, ordered=True) == OrderedDict([('a', 1), ('b', 2), ('c', 3)])

    Args:
        data: dict to be ordered.
        ordered: OrderedDict.
        reverse: reverse.

    Returns:
        Union[dict, collections.OrderedDict]: Dict sorted
    """
    data = {key: data[key] for key in sorted(data.keys(), reverse=reverse)}
    if ordered:
        return collections.OrderedDict(data)
    return data


def dmg(src: Path | str, dest: Path | str) -> None:
    """Open dmg file and copy the app to dest.

    Examples:
        >>> from nodeps import dmg
        >>> dmg(Path("/tmp/JetBrains.dmg"), Path("/tmp/JetBrains"))  # doctest: +SKIP

    Args:
        src: dmg file
        dest: path to copy to

    Returns:
        CompletedProcess
    """
    with TempDir() as tmpdir:
        cmd("hdiutil", "attach", "-mountpoint", tmpdir, "-nobrowse", "-quiet", src)
        for item in src.iterdir():
            if item.name.endswith(".app"):
                cmd("cp", "-r", tmpdir / item.name, dest)
                cmd("xattr", "-r", "-d", "com.apple.quarantine", dest)
                cmd("hdiutil", "detach", tmpdir, "-force")
                break


def effect(apply: Callable, *args: Iterable) -> None:
    """Perform function on iterable.

    Examples:
        >>> from types import SimpleNamespace
        >>> from nodeps import effect
        >>> simple = SimpleNamespace()
        >>> effect(lambda x: simple.__setattr__(x, dict()), 'a b', 'c')
        >>> assert simple.a == {}
        >>> assert simple.b == {}
        >>> assert simple.c == {}

    Args:
        apply: Function to apply.
        *args: Iterable to perform function.

    Returns:
        No Return.
    """
    for arg in toiter(args):
        for item in arg:
            apply(item)


def elementadd(name: str | tuple[str, ...], closing: bool | None = False) -> str:
    """Converts to HTML element.

    Examples:
        >>> from nodeps import elementadd
        >>>
        >>> assert elementadd('light-black') == '<light-black>'
        >>> assert elementadd('light-black', closing=True) == '</light-black>'
        >>> assert elementadd(('green', 'bold',)) == '<green><bold>'
        >>> assert elementadd(('green', 'bold',), closing=True) == '</green></bold>'

    Args:
        name: text or iterable text.
        closing: True if closing/end, False if opening/start.

    Returns:
        Str
    """
    return "".join(f'<{"/" if closing else ""}{i}>' for i in ((name,) if isinstance(name, str) else name))


def exec_module_from_file(file: Path | str, name: str | None = None) -> types.ModuleType:
    """Executes module from file location.

    Examples:
        >>> import nodeps
        >>> from nodeps import exec_module_from_file
        >>> m = exec_module_from_file(nodeps.__file__)
        >>> assert m.__name__ == nodeps.__name__

    Args:
        file: file location
        name: module name (default from file)

    Returns:
        Module instance
    """
    file = Path(file)
    spec = importlib.util.spec_from_file_location(
        name or file.parent.name if file.name == "__init__.py" else file.stem, file
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def filterm(
    d: MutableMapping[_KT, _VT], k: Callable[..., bool] = lambda x: True, v: Callable[..., bool] = lambda x: True
) -> MutableMapping[_KT, _VT]:
    """Filter Mutable Mapping.

    Examples:
        >>> from nodeps import filterm
        >>>
        >>> assert filterm({'d':1}) == {'d': 1}
        >>> # noinspection PyUnresolvedReferences
        >>> assert filterm({'d':1}, lambda x: x.startswith('_')) == {}
        >>> # noinspection PyUnresolvedReferences
        >>> assert filterm({'d': 1, '_a': 2}, lambda x: x.startswith('_'), lambda x: isinstance(x, int)) == {'_a': 2}

    Returns:
        Filtered dict with
    """
    # noinspection PyArgumentList
    return d.__class__({x: y for x, y in d.items() if k(x) and v(y)})


def findfile(pattern, path: StrOrBytesPath = None) -> list[Path]:
    """Find file with pattern.

    Examples:
        >>> from pathlib import Path
        >>> import nodeps
        >>> from nodeps import findfile
        >>>
        >>> assert Path(nodeps.__file__) in findfile("*.py")

    Args:
        pattern: pattern to search files
        path: default cwd

    Returns:
        list of files found
    """
    result = []
    for root, _, files in os.walk(path or Path.cwd()):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(Path(root, name))
    return result


def findup(
    path: StrOrBytesPath = None,
    kind: Literal["exists", "is_dir", "is_file"] = "is_file",
    name: str | Path = ".env",
    uppermost: bool = False,
) -> Path | None:
    """Find up if name exists or is file or directory.

    Examples:
        >>> import email
        >>> import email.mime
        >>> from pathlib import Path
        >>> import nodeps
        >>> from nodeps import chdir, findup, parent
        >>>
        >>>
        >>> file = Path(email.mime.__file__)
        >>>
        >>> with chdir(parent(nodeps.__file__)):
        ...     pyproject_toml = findup(nodeps.__file__, name="pyproject.toml")
        ...     assert pyproject_toml.is_file()
        >>>
        >>> with chdir(parent(email.mime.__file__)):
        ...     email_mime_py = findup(name="__init__.py")
        ...     assert email_mime_py.is_file()
        ...     assert email_mime_py == Path(email.mime.__file__)
        ...     email_py = findup(name="__init__.py", uppermost=True)
        ...     assert email_py.is_file()
        ...     assert email_py == Path(email.__file__)
        >>>
        >>> assert findup(kind="is_dir", name=nodeps.__name__) == Path(nodeps.__name__).parent.resolve()
        >>>
        >>> assert findup(file, kind="exists", name="__init__.py") == file.parent / "__init__.py"
        >>> assert findup(file, name="__init__.py") == file.parent / "__init__.py"
        >>> assert findup(file, name="__init__.py", uppermost=True) == file.parent.parent / "__init__.py"

    Args:
        path: CWD if None or Path.
        kind: Exists, file or directory.
        name: File or directory name.
        uppermost: Find uppermost found if True (return the latest found if more than one) or first if False.

    Returns:
        Path if found.
    """
    name = name.name if isinstance(name, Path) else name
    start = parent(path or Path.cwd())
    latest = None
    while True:
        if getattr(find := start / name, kind)():
            if not uppermost:
                return find
            latest = find
        if (start := start.parent) == Path("/"):
            return latest


def firstfound(data: Iterable, apply: Callable) -> Any:
    """Returns first value in data if apply is True.

    Examples:
        >>> from nodeps import firstfound
        >>>
        >>> assert firstfound([1, 2, 3], lambda x: x == 2) == 2
        >>> assert firstfound([1, 2, 3], lambda x: x == 4) is None

    Args:
        data: iterable.
        apply: function to apply.

    Returns:
        Value if found.
    """
    for i in data:
        if apply(i):
            return i
    return None


def flatten(
    data: tuple | list | set,
    recurse: bool = False,
    unique: bool = False,
    sort: bool = True,
) -> tuple | list | set:
    """Flattens an Iterable.

    Examples:
        >>> from nodeps import flatten
        >>>
        >>> assert flatten([1, 2, 3, [1, 5, 7, [2, 4, 1, ], 7, 6, ]]) == [1, 2, 3, 1, 5, 7, [2, 4, 1], 7, 6]
        >>> assert flatten([1, 2, 3, [1, 5, 7, [2, 4, 1, ], 7, 6, ]], recurse=True) == [1, 1, 1, 2, 2, 3, 4, 5, 6, 7, 7]
        >>> assert flatten((1, 2, 3, [1, 5, 7, [2, 4, 1, ], 7, 6, ]), unique=True) == (1, 2, 3, 4, 5, 6, 7)

    Args:
        data: iterable
        recurse: recurse
        unique: when recurse
        sort: sort

    Returns:
        Union[list, Iterable]:
    """
    if unique:
        recurse = True

    cls = data.__class__

    flat = []
    _ = [
        flat.extend(flatten(item, recurse, unique) if recurse else item)
        if isinstance(item, list)
        else flat.append(item)
        for item in data
        if item
    ]
    value = set(flat) if unique else flat
    if sort:
        try:
            value = cls(sorted(value))
        except TypeError:
            value = cls(value)
    return value


def framesimple(data: inspect.FrameInfo | types.FrameType | types.TracebackType) -> FrameSimple | None:
    """Returns :class:`nodeps.FrameSimple`.

    Examples:
        >>> import inspect
        >>> from nodeps import Path
        >>> from nodeps import framesimple
        >>>
        >>> frameinfo = inspect.stack()[0]
        >>> finfo = framesimple(frameinfo)
        >>> ftype = framesimple(frameinfo.frame)
        >>> assert frameinfo.frame.f_code == finfo.code
        >>> assert frameinfo.frame == finfo.frame
        >>> assert frameinfo.filename == str(finfo.path)
        >>> assert frameinfo.lineno == finfo.lineno

    Returns:
        :class:`FrameSimple`.
    """
    if isinstance(data, inspect.FrameInfo):
        frame = data.frame
        back = frame.f_back
        lineno = data.lineno
    elif isinstance(data, types.FrameType):
        frame = data
        back = data.f_back
        lineno = data.f_lineno
    elif isinstance(data, types.TracebackType):
        frame = data.tb_frame
        back = data.tb_next
        lineno = data.tb_lineno
    else:
        return None

    code = frame.f_code
    f_globals = frame.f_globals
    f_locals = frame.f_locals
    function = code.co_name
    v = f_globals | f_locals
    name = v.get("__name__") or function
    return FrameSimple(
        back=back,
        code=code,
        frame=frame,
        function=function,
        globals=f_globals,
        lineno=lineno,
        locals=f_locals,
        name=name,
        package=v.get("__package__") or name.split(".")[0],
        path=sourcepath(data),
        vars=v,
    )


def from_latin9(*args) -> str:
    """Converts string from latin9 hex.

    Examples:
        >>> from nodeps import from_latin9
        >>>
        >>> from_latin9("f1")
        'ñ'
        >>>
        >>> from_latin9("4a6f73e920416e746f6e696f205075e972746f6c6173204d6f6e7461f1e973")
        'José Antonio Puértolas Montañés'
        >>>
        >>> from_latin9("f1", "6f")
        'ño'

    Args:
        args: strings to convert to latin9

    Returns:
        str
    """
    rv = ""
    if len(args) == 1:
        pairs = split_pairs(args[0])
        for pair in pairs:
            rv += bytes.fromhex("".join(pair)).decode("latin9")
    else:
        for char in args:
            rv += bytes.fromhex(char).decode("latin9")
    return rv


def fromiter(data, *args):
    """Gets attributes from Iterable of objects and returns dict with.

    Examples:
        >>> from types import SimpleNamespace as Simple
        >>> from nodeps import fromiter
        >>>
        >>> assert fromiter([Simple(a=1), Simple(b=1), Simple(a=2)], 'a', 'b', 'c') == {'a': [1, 2], 'b': [1]}
        >>> assert fromiter([Simple(a=1), Simple(b=1), Simple(a=2)], ('a', 'b', ), 'c') == {'a': [1, 2], 'b': [1]}
        >>> assert fromiter([Simple(a=1), Simple(b=1), Simple(a=2)], 'a b c') == {'a': [1, 2], 'b': [1]}

    Args:
        data: object.
        *args: attributes.

    Returns:
        Tuple
    """
    value = {k: [getattr(C, k) for C in data if hasattr(C, k)] for i in args for k in toiter(i)}
    return {k: v for k, v in value.items() if v}


def getpths() -> dict[str, Path] | None:
    """Get list of pths under ``sitedir``.

    Examples:
        >>> from nodeps import getpths
        >>>
        >>> pths = getpths()
        >>> assert "distutils-precedence" in pths

    Returns:
        Dictionary with pth name and file
    """
    try:
        s = getsitedir()
        names = os.listdir(s)
    except OSError:
        return None
    return {re.sub("(-[0-9].*|.pth)", "", name): Path(s / name) for name in names if name.endswith(".pth")}


def getsitedir(index: bool = 2) -> Path:
    """Get site directory from stack if imported by :mod:`site` in a ``.pth`` file or :mod:`sysconfig`.

    Examples:
        >>> from nodeps import getsitedir
        >>> assert "packages" in str(getsitedir())

    Args:
        index: 1 if directly needed by this function (default: 2), for caller to this function

    Returns:
        Path instance with site directory
    """
    if (s := sys._getframe(index).f_locals.get("sitedir")) is None:
        s = sysconfig.get_paths()["purelib"]
    return Path(s)


def group_user(name: int | str = USER) -> GroupUser:
    """Group and User for Name (id if name is str and vice versa).

    Examples:
        >>> import os
        >>> import pathlib
        >>>
        >>> from nodeps import group_user
        >>> from nodeps import PW_USER, PW_ROOT
        >>>
        >>> s = pathlib.Path().stat()
        >>> gr = group_user()
        >>> assert gr.group == s.st_gid and gr.user == s.st_uid
        >>> gr = group_user(name=PW_USER.pw_uid)
        >>> actual_gname = gr.group
        >>> assert gr.group != PW_ROOT.pw_name and gr.user == PW_USER.pw_name
        >>> gr = group_user('root')
        >>> assert gr.group != s.st_gid and gr.user == 0
        >>> gr = group_user(name=0)
        >>> assert gr.group != actual_gname and gr.user == 'root'

    Args:
        name: usename or id (default: `data.ACTUAL.pw_name`)

    Returns:
        GroupUser.
    """
    if isinstance(name, str):
        struct = (
            struct
            if name  # noqa: PLR1714
            == (struct := PW_USER).pw_name
            or name == (struct := PW_ROOT).pw_name
            else pwd.getpwnam(name)
        )
        return GroupUser(group=struct.pw_gid, user=struct.pw_uid)
    struct = (
        struct
        if (
            name  # noqa: PLR1714
            == (struct := PW_USER).pw_uid
            or name == (struct := PW_ROOT).pw_uid
        )
        else pwd.getpwuid(name)
    )
    return GroupUser(group=grp.getgrgid(struct.pw_gid).gr_name, user=struct.pw_name)


def gz(src: Path | str, dest: Path | str = ".") -> Path:
    """Uncompress .gz src to dest (default: current directory).

    It will be uncompressed to the same directory name as src basename.
    Uncompressed directory will be under dest directory.

    Examples:
        >>> from nodeps import TempDir
        >>> from nodeps import gz
        >>> cwd = Path.cwd()
        >>> with TempDir() as workdir:
        ...     os.chdir(workdir)
        ...     with TempDir() as compress:
        ...         file = compress / "test.txt"
        ...         _ = file.touch()
        ...         compressed = tardir(compress)
        ...         with TempDir() as uncompress:
        ...             uncompressed = gz(compressed, uncompress)
        ...             assert uncompressed.is_dir()
        ...             assert Path(uncompressed).joinpath(file.name).exists()
        >>> os.chdir(cwd)

    Args:
        src: file to uncompress
        dest: destination directory to where uncompress directory will be created (default: current directory)

    Returns:
        Absolute Path of the Uncompressed Directory
    """
    dest = Path(dest)
    with tarfile.open(src, "r:gz") as tar:
        tar.extractall(dest)
        return (dest / tar.getmembers()[0].name).parent.absolute()


def in_tox() -> bool:
    """Running in tox."""
    return ".tox" in sysconfig.get_paths()["purelib"]


def noexc(
    func: Callable[..., _T], *args: Any, default_: Any = None, exc_: ExcType = Exception, **kwargs: Any
) -> _T | Any:
    """Execute function suppressing exceptions.

    Examples:
        >>> from nodeps import noexc
        >>> assert noexc(dict(a=1).pop, 'b', default_=2, exc_=KeyError) == 2

    Args:
        func: callable.
        *args: args.
        default_: default value if exception is raised.
        exc_: exception or exceptions.
        **kwargs: kwargs.

    Returns:
        Any: Function return.
    """
    try:
        return func(*args, **kwargs)
    except exc_:
        return default_


def parent(path: StrOrBytesPath = __file__, none: bool = True) -> Path | None:
    """Parent if File or None if it does not exist.

    Examples:
        >>> from nodeps import parent
        >>>
        >>> parent("/bin/ls")
        Path('/bin')
        >>> parent("/bin")
        Path('/bin')
        >>> parent("/bin/foo", none=False)
        Path('/bin')
        >>> parent("/bin/foo")

    Args:
        path: file or dir.
        none: return None if it is not a directory and does not exist (default: True)

    Returns:
        Path
    """
    return path.parent if (path := Path(path)).is_file() else path if path.is_dir() else None if none else path.parent


def parse_str(  # noqa: PLR0911
    data: Any | None = None,
) -> bool | Path | ParseResult | IPv4Address | IPv6Address | int | str | None:
    """Parses str or data.__str__().

    Parses:
        - bool: 1, 0, True, False, yes, no, on, off (case insensitive)
        - int: integer only numeric characters but 1 and 0
        - ipaddress: ipv4/ipv6 address
        - url: if "://" or "@" is found it will be parsed as url
        - path: if "." or start with "/" or "~" or "." and does contain ":"
        - others as string

    Arguments:
        data: variable name to parse from environment (default: USER)

    Examples:
        >>> from nodeps import Path
        >>> from nodeps import parse_str
        >>>
        >>> assert parse_str() is None
        >>>
        >>> assert parse_str("1") is True
        >>> assert parse_str("0") is False
        >>> assert parse_str("TrUe") is True
        >>> assert parse_str("OFF") is False
        >>>
        >>> assert parse_str("https://github.com").geturl() == "https://github.com"
        >>> assert parse_str("git@github.com").geturl() == "git@github.com"
        >>>
        >>> assert parse_str("~/foo") == Path('~/foo')
        >>> assert parse_str("/foo") == Path('/foo')
        >>> assert parse_str("./foo") == Path('foo')
        >>> assert parse_str(".") == Path('.')
        >>> assert parse_str(Path()) == Path()
        >>>
        >>> assert parse_str("0.0.0.0").exploded == "0.0.0.0"
        >>> assert parse_str("::1").exploded.endswith(":0001")
        >>>
        >>> assert parse_str("2") == 2
        >>> assert parse_str("2.0") == "2.0"
        >>> assert parse_str("/usr/share/man:") == "/usr/share/man:"
        >>> if not os.environ.get("CI"):
        ...     assert isinstance(parse_str(os.environ.get("PATH")), str)

    Returns:
        None
    """
    if data is not None:
        if not isinstance(data, str):
            data = str(data)

        if data.lower() in ["1", "true", "yes", "on"]:
            return True
        if data.lower() in ["0", "false", "no", "off"]:
            return False
        if "://" in data or "@" in data:
            return urllib.parse.urlparse(data)
        if (
            (
                data[0] in ["/", "~"] or (len(data) >= 2 and f"{data[0]}{data[1]}" == "./")  # noqa: PLR2004
            )
            and ":" not in data
        ) or data == ".":
            return Path(data)
        try:
            return ipaddress.ip_address(data)
        except ValueError:
            if data.isnumeric():
                return int(data)
    return data


@contextlib.contextmanager
def pipmetapathfinder():
    """Context for :class:`PipMetaPathFinder`.

    Examples:
        >>> from nodeps import pipmetapathfinder
        >>>
        >>> with pipmetapathfinder():  # doctest: +SKIP
        ...    import simplejson  # type: ignore[attr-defined]
    """
    sys.meta_path.append(PipMetaPathFinder)
    try:
        yield
    finally:
        sys.meta_path.pop()


def returncode(c: str | list[str], shell: bool = True) -> int:
    """Runs command in shell and returns returncode showing stdout and stderr.

    No exception is raised

    Examples:
        >>> from nodeps import returncode
        >>>
        >>> assert returncode("ls /bin/ls") == 0
        >>> assert returncode("ls foo") == 1

    Arguments:
        c: command to run
        shell: run in shell (default: True)

    Returns:
        return code

    """
    return subprocess.call(c, shell=shell)


def sourcepath(data: Any) -> Path:
    """Get path of object.

    Examples:
        >>> import asyncio
        >>> import nodeps
        >>> from nodeps import Path
        >>> from nodeps import sourcepath
        >>>
        >>> finfo = inspect.stack()[0]
        >>> globs_locs = (finfo.frame.f_globals | finfo.frame.f_locals).copy()
        >>> assert sourcepath(sourcepath) == Path(nodeps.__file__)
        >>> assert sourcepath(asyncio.__file__) == Path(asyncio.__file__)
        >>> assert sourcepath(dict(a=1)) == Path("{'a': 1}")

    Returns:
        Path.
    """
    if isinstance(data, MutableMapping):
        f = data.get("__file__")
    elif isinstance(data, inspect.FrameInfo):
        f = data.filename
    else:
        try:
            f = inspect.getsourcefile(data) or inspect.getfile(data)
        except TypeError:
            f = None
    return Path(f or str(data))


def siteimported() -> str | None:
    """True if imported by :mod:`site` in a ``.pth`` file."""
    s = None
    _frame = sys._getframe()
    while _frame and (s := _frame.f_locals.get("sitedir")) is None:
        _frame = _frame.f_back
    return s


def split_pairs(text):
    """Split text in pairs for even length.

    Examples:
        >>> from nodeps import split_pairs
        >>>
        >>> split_pairs("123456")
        [('1', '2'), ('3', '4'), ('5', '6')]

    Args:
        text: text to split in pairs

    Returns:
        text
    """
    return list(zip(text[0::2], text[1::2], strict=True))


def stdout(shell: AnyStr, keepends: bool = False, split: bool = False) -> list[str] | str | None:
    """Return stdout of executing cmd in a shell or None if error.

    Execute the string 'cmd' in a shell with 'subprocess.getstatusoutput' and
    return a stdout if success. The locale encoding is used
    to decode the output and process newlines.

    A trailing newline is stripped from the output.

    Examples:
        >>> from nodeps import stdout
        >>>
        >>> stdout("ls /bin/ls")
        '/bin/ls'
        >>> stdout("true")
        ''
        >>> stdout("ls foo")
        >>> stdout("ls /bin/ls", split=True)
        ['/bin/ls']

    Args:
        shell: command to be executed
        keepends: line breaks when ``split`` if true, are not included in the resulting list unless keepends
            is given and true.
        split: return a list of the stdout lines in the string, breaking at line boundaries.(default: False)

    Returns:
        Stdout or None if error.
    """
    exitcode, data = subprocess.getstatusoutput(shell)

    if exitcode == 0:
        if split:
            return data.splitlines(keepends=keepends)
        return data
    return None


@contextlib.contextmanager
def stdquiet() -> tuple[TextIO, TextIO]:
    """Redirect stdout/stderr to StringIO objects to prevent console output from distutils commands.

    Returns:
        Stdout, Stderr
    """
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    new_stdout = sys.stdout = io.StringIO()
    new_stderr = sys.stderr = io.StringIO()
    try:
        yield new_stdout, new_stderr
    finally:
        new_stdout.seek(0)
        new_stderr.seek(0)
        sys.stdout = old_stdout
        sys.stderr = old_stderr


def suppress(
    func: Callable[P, T],
    *args: P.args,
    exception: ExcType | None = Exception,
    **kwargs: P.kwargs,
) -> T:
    """Try and supress exception.

    Args:
        func: function to call
        *args: args to pass to func
        exception: exception to suppress (default: Exception)
        **kwargs: kwargs to pass to func

    Returns:
        result of func
    """
    with contextlib.suppress(exception or Exception):
        return func(*args, **kwargs)


def syssudo(user: str = "root") -> subprocess.CompletedProcess | None:
    """Rerun Program with sudo ``sys.executable`` and ``sys.argv`` if user is different that the current user.

    Arguments:
        user: run as user (Default: False)

    Returns:
        CompletedProcess if the current user is not the same as user, None otherwise
    """
    if not ami(user):
        return cmd(["sudo", "-u", user, sys.executable, *sys.argv])
    return None


def tardir(src: Path | str) -> Path:
    """Compress directory src to <basename src>.tar.gz in cwd.

    Examples:
        >>> from nodeps import TempDir
        >>> from nodeps import tardir
        >>> cwd = Path.cwd()
        >>> with TempDir() as workdir:
        ...     os.chdir(workdir)
        ...     with TempDir() as compress:
        ...         file = compress / "test.txt"
        ...         _ = file.touch()
        ...         compressed = tardir(compress)
        ...         with TempDir() as uncompress:
        ...             uncompressed = gz(compressed, uncompress)
        ...             assert uncompressed.is_dir()
        ...             assert Path(uncompressed).joinpath(file.name).exists()
        >>> os.chdir(cwd)

    Args:
        src: directory to compress

    Raises:
        FileNotFoundError: No such file or directory
        ValueError: Can't compress current working directory

    Returns:
        Compressed Absolute File Path
    """
    src = Path(src)
    if not src.exists():
        msg = f"{src}: No such file or directory"
        raise FileNotFoundError(msg)

    if src.resolve() == Path.cwd().resolve():
        msg = f"{src}: Can't compress current working directory"
        raise ValueError(msg)

    name = Path(src).name + ".tar.gz"
    dest = Path(name)
    with tarfile.open(dest, "w:gz") as tar:
        for root, _, files in os.walk(src):
            for file_name in files:
                tar.add(Path(root, file_name))
        return dest.absolute()


def tilde(path: str | Path = ".") -> str:
    """Replaces $HOME with ~.

    Examples:
        >>> from nodeps import tilde
        >>> assert tilde(f"{Path.home()}/file") == f"~/file"

    Arguments:
        path: path to replace (default: '.')

    Returns:
        str
    """
    return str(path).replace(str(Path.home()), "~")


def timestamp_now(file: Path | str):
    """Set modified and create date of file to now."""
    now = time.time()
    os.utime(file, (now, now))


def to_latin9(chars: str) -> str:
    """Converts string to latin9 hex.

    Examples:
        >>> from nodeps import AUTHOR
        >>> from nodeps import to_latin9
        >>>
        >>> to_latin9("ñ")
        'f1'
        >>>
        >>> to_latin9(AUTHOR)
        '4a6f73e920416e746f6e696f205075e972746f6c6173204d6f6e7461f1e973'

    Args:
        chars: chars to converto to latin9

    Returns:
        hex str
    """
    rv = ""
    for char in chars:
        rv += char.encode("latin9").hex()
    return rv


def toiter(obj: Any, always: bool = False, split: str = " ") -> Any:
    """To iter.

    Examples:
        >>> import pathlib
        >>> from nodeps import toiter
        >>>
        >>> assert toiter('test1') == ['test1']
        >>> assert toiter('test1 test2') == ['test1', 'test2']
        >>> assert toiter({'a': 1}) == {'a': 1}
        >>> assert toiter({'a': 1}, always=True) == [{'a': 1}]
        >>> assert toiter('test1.test2') == ['test1.test2']
        >>> assert toiter('test1.test2', split='.') == ['test1', 'test2']
        >>> assert toiter(pathlib.Path("/tmp/foo")) == ('/', 'tmp', 'foo')

    Args:
        obj: obj.
        always: return any iterable into a list.
        split: split for str.

    Returns:
        Iterable.
    """
    if isinstance(obj, str):
        obj = obj.split(split)
    elif hasattr(obj, "parts"):
        obj = obj.parts
    elif not isinstance(obj, Iterable) or always:
        obj = [obj]
    return obj


def tomodules(obj: Any, suffix: bool = True) -> str:
    """Converts Iterable to A.B.C.

    Examples:
        >>> from nodeps import tomodules
        >>> assert tomodules('a b c') == 'a.b.c'
        >>> assert tomodules('a b c.py') == 'a.b.c'
        >>> assert tomodules('a/b/c.py') == 'a.b.c'
        >>> assert tomodules(['a', 'b', 'c.py']) == 'a.b.c'
        >>> assert tomodules('a/b/c.py', suffix=False) == 'a.b.c.py'
        >>> assert tomodules(['a', 'b', 'c.py'], suffix=False) == 'a.b.c.py'

    Args:
        obj: iterable.
        suffix: remove suffix.

    Returns:
        String A.B.C
    """
    split = "/" if isinstance(obj, str) and "/" in obj else " "
    return ".".join(i.removesuffix(Path(i).suffix if suffix else "") for i in toiter(obj, split=split))


def urljson(
    data: str,
) -> dict:
    """Url open json.

    Examples:
        >>> import os
        >>> from nodeps import urljson
        >>> from nodeps import GIT
        >>> from nodeps import GITHUB_TOKEN
        >>> from nodeps import NODEPS_PROJECT_NAME
        >>>
        >>> if os.environ.get('GITHUB_TOKEN'):
        ...     github = urljson(f"https://api.github.com/repos/{GIT}/{NODEPS_PROJECT_NAME}")
        ...     assert github['name'] == NODEPS_PROJECT_NAME
        >>>
        >>> pypi = urljson(f"https://pypi.org/pypi/{NODEPS_PROJECT_NAME}/json")
        >>> assert pypi['info']['name'] == NODEPS_PROJECT_NAME

    Args:
        data: url

    Returns:
        dict: pypi information
    """
    if data.lower().startswith("https"):
        request = urllib.request.Request(data)
    else:
        msg = f"Non-HTTPS URL: {data}"
        raise ValueError(msg)
    if "github" in data:
        request.add_header("Authorization", f"token {GITHUB_TOKEN}")
    with urllib.request.urlopen(request) as response:  # noqa: S310
        return json.loads(response.read().decode())


def which(data="sudo", raises: bool = False) -> str:
    """Checks if cmd or path is executable or exported bash function.

    Examples:
        # FIXME: Ubuntu

        >>> from nodeps import which
        >>> if which():
        ...    assert "sudo" in which()
        >>> assert which('/usr/local') == ''
        >>> assert which('/usr/bin/python3') == '/usr/bin/python3'
        >>> assert which('let') == 'let'
        >>> assert which('source') == 'source'
        >>> which("foo", raises=True) # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        nodeps.CommandNotFoundError: foo

    Attribute:
        data: command or path.
        raises: raise exception if command not found

    Raises:
        CommandNotFound:

    Returns:
        Cmd path or ""
    """
    rv = (
        shutil.which(data, mode=os.X_OK)
        or subprocess.run(f"command -v {data}", shell=True, text=True, capture_output=True).stdout.rstrip("\n")
        or ""
    )

    if raises and not rv:
        raise CommandNotFoundError(data)
    return rv


EXECUTABLE = Path(sys.executable)
EXECUTABLE_SITE = Path(EXECUTABLE).resolve()

subprocess.CalledProcessError = CalledProcessError

os.environ["PIP_ROOT_USER_ACTION"] = "ignore"
os.environ["PYTHONDONTWRITEBYTECODE"] = ""
os.environ["PY_IGNORE_IMPORTMISMATCH"] = "1"

if "pip._internal.operations.install.wheel" in sys.modules:
    pip._internal.operations.install.wheel.install_wheel = _pip_install_wheel
    pip._internal.cli.base_command.Command.main = _pip_base_command
    pip._internal.req.req_install.InstallRequirement.uninstall = _pip_uninstall_req

venv.CORE_VENV_DEPS = ["build", "ipython", "pip", "setuptools", "wheel"]
venv.EnvBuilder = EnvBuilder
