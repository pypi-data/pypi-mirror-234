"""NoDeps Extras Repo Module."""
from __future__ import annotations

__all__ = (
    "Repo",
)

import dataclasses
import os
import pathlib
import tempfile
import urllib
import urllib.parse
from typing import IO, AnyStr, TypeAlias

try:
    # nodeps[repo] extras
    from git import Git as GitCmd  # type: ignore[attr-defined]
    from git import GitCmdObjectDB, GitConfigParser  # type: ignore[attr-defined]
    from git import Repo as GitRepo  # type: ignore[attr-defined]
    from gitdb import LooseObjectDB  # type: ignore[attr-defined]
except ModuleNotFoundError:
    GitCmd = None
    GitCmdObjectDB = None
    GitConfigParser = None
    GitRepo = object
    LooseObjectDB = None

AnyPath: TypeAlias = os.PathLike | AnyStr | IO[AnyStr]


@dataclasses.dataclass
class Repo(GitRepo):
    """Dataclass Wrapper for :class:`git.Repo`.

    Represents a git repository and allows you to query references,
    gather commit information, generate diffs, create and clone repositories query
    the log.

    'working_tree_dir' is the working tree directory, but will raise AssertionError if we are a bare repository.
    """

    git: GitCmd = dataclasses.field(init=False)
    """
    The Repo class manages communication with the Git binary.

    It provides a convenient interface to calling the Git binary, such as in::

     g = Repo( git_dir )
     g.init()                   # calls 'git init' program
     rval = g.ls_files()        # calls 'git ls-files' program

    ``Debugging``
        Set the GIT_PYTHON_TRACE environment variable print each invocation
        of the command to stdout.
        Set its value to 'full' to see details about the returned values.
    """
    git_dir: AnyPath | None = dataclasses.field(default=None, init=False)
    """the .git repository directory, which is always set"""
    odb: type[LooseObjectDB] = dataclasses.field(init=False)
    working_dir: AnyPath | None = dataclasses.field(default=None, init=False)
    """working directory of the git command, which is the working tree
    directory if available or the .git directory in case of bare repositories"""
    path: dataclasses.InitVar[AnyPath | None] = None
    """File or Directory inside the git repository, the default with search_parent_directories"""
    expand_vars: dataclasses.InitVar[bool] = True
    odbt: dataclasses.InitVar[type[LooseObjectDB]] = GitCmdObjectDB
    """the path to either the root git directory or the bare git repo"""
    search_parent_directories: dataclasses.InitVar[bool] = True
    """if True, all parent directories will be searched for a valid repo as well."""

    def __post_init__(
        self, path: AnyPath | None, expand_vars: bool, odbt: type[LooseObjectDB], search_parent_directories: bool
    ):
        """Create a new Repo instance.

        Examples:
            >>> import warnings
            >>> import nodeps
            >>> from nodeps.extras._repo import Repo
            >>> assert Repo(nodeps.__file__)
            >>> Repo("~/repo.git")  # doctest: +ELLIPSIS +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            git.exc.NoSuchPathError: .../repo.git
            >>> warnings.simplefilter("ignore", UserWarning)
            >>> Repo("${HOME}/repo")  # doctest: +ELLIPSIS +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            git.exc.NoSuchPathError: .../repo

        Raises:
            InvalidGitRepositoryError
            NoSuchPathError

        Args:
            path: File or Directory inside the git repository, the default with search_parent_directories set to True
                or the path to either the root git directory or the bare git repo
                if search_parent_directories is changed to False
            expand_vars: if True, environment variables will be expanded in the given path
            odbt: odbt
            search_parent_directories: Search all parent directories for a git repository.

        Returns:
            Repo: Repo instance
        """
        if GitRepo == object:
            msg = "GitPython is not installed: installed with 'pip install nodeps[repo]'"
            raise ImportError(msg)
        if path:
            path = p.parent if (p := pathlib.Path(path)).is_file() else p

        super().__init__(
            path or pathlib.Path.cwd(),
            expand_vars=expand_vars,
            odbt=odbt,
            search_parent_directories=search_parent_directories,
        )

    @classmethod
    def bare(cls, name: str | None = None, repo: Repo = None) -> Repo:
        """Create a bare repository in a temporary directory, to manage global/system config or as a remote for testing.

        Args:
            name: the path of the bare repository
            repo: Repo instance to update git config with remote url of the new bare repository (default: None)

        Returns:
            Repo: Repo instance
        """
        with tempfile.TemporaryDirectory(suffix=".git") as tmpdir:
            bare = cls.init(pathlib.Path(tmpdir) / (f"{name}.git" if name else ""), bare=True)
            if repo:
                repo.config_writer().set_value("remote.origin.url", repo.git_dir).release()
            return bare

    @property
    def git_config(self) -> GitConfigParser:
        """Wrapper for :func:`git.Repo.config_reader`, so it is already read and can be used.

        The configuration will include values from the system, user and repository configuration files.

        Examples:
            >>> import nodeps
            >>> from nodeps.extras._repo import Repo
            >>>
            >>> conf = Repo(nodeps.__file__).git_config
            >>> conf.has_section('remote "origin"')
            True
            >>> conf.has_option('remote "origin"', 'url')
            True
            >>> conf.get('remote "origin"', 'url')  # doctest: +ELLIPSIS
            'https://github.com/...'
            >>> conf.get_value('remote "origin"', 'url', "")  # doctest: +ELLIPSIS
            'https://github.com/...'

        Returns:
            GitConfigParser: GitConfigParser instance
        """
        config = self.config_reader()
        config.read()
        return config

    @property
    def origin_url(self) -> urllib.parse.ParseResult:
        """Git Origin URL.

        Examples:
            >>> import nodeps
            >>> from nodeps.extras._repo import Repo
            >>>
            >>> Repo(nodeps.__file__).origin_url.geturl()   # doctest: +ELLIPSIS
            'https://github.com/.../nodeps'
        """
        return urllib.parse.urlparse(self.git_config.get_value('remote "origin"', "url", ""))

    @property
    def top(self) -> pathlib.Path:
        """Repo Top Directory Path."""
        path = pathlib.Path(self.working_dir)
        return pathlib.Path(path.parent if ".git" in path else path)
