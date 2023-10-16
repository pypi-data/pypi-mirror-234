"""CLI for nodeps."""
__all__ = (
    "_browser",
    "_build",
    "_builds",
    "_buildrequires",
    "_clean",
    "_commit",
    "_completions",
    "_dependencies",
    "_dirty",
    "_distribution",
    "_diverge",
    "_docs",
    "_extras",
    "_latest",
    "_needpull",
    "_needpush",
    "_next",
    "_publish",
    "_pull",
    "_push",
    "_pypi",
    "_pytests",
    "_repos",
    "_requirement",
    "_requirements",
    "_secrets",
    "_sha",
    "_superproject",
    "_tests",
    "_version",
    "_venv",
    "_venvs",
)

import copy
import sys
from pathlib import Path
from typing import Annotated

from . import (
    NODEPS_EXECUTABLE,
    NODEPS_PROJECT_NAME,
    PYTHON_DEFAULT_VERSION,
    PYTHON_VERSIONS,
    Bump,
    GitSHA,
    Project,
    ProjectRepos,
    dict_sort,
    pipmetapathfinder,
)

with pipmetapathfinder():
    import typer


def _repos_completions(ctx: typer.Context, args: list[str], incomplete: str):
    from rich.console import Console

    console = Console(stderr=True)
    console.print(f"{args}")
    r = Project().repos(ProjectRepos.DICT)
    valid = list(r.keys()) + [str(item) for item in r.values()]
    provided = ctx.params.get("name") or []
    for item in valid:
        if item.startswith(incomplete) and item not in provided:
            yield item


def _versions_completions(ctx: typer.Context, args: list[str], incomplete: str):
    from rich.console import Console

    console = Console(stderr=True)
    console.print(f"{args}")
    valid = PYTHON_VERSIONS
    provided = ctx.params.get("name") or []
    for item in valid:
        if item.startswith(incomplete) and item not in provided:
            yield item


_cwd = Path.cwd()
app = typer.Typer(no_args_is_help=True, context_settings={"help_option_names": ["-h", "--help"]})

_browser = typer.Typer(
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]},
    name="browser",
)
_build = typer.Typer(
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]},
    name="build",
)
_builds = typer.Typer(
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]},
    name="builds",
)
_buildrequires = typer.Typer(
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]},
    name="buildrequires",
)
_clean = typer.Typer(
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]},
    name="clean",
)
_commit = typer.Typer(
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]},
    name="commit",
)
_completions = typer.Typer(
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]},
    name="completions",
)
_dependencies = typer.Typer(
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]},
    name="dependencies",
)
_dirty = typer.Typer(
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]},
    name="dirty",
)
_distribution = typer.Typer(
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]},
    name="distribution",
)
_diverge = typer.Typer(
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]},
    name="diverge",
)
_docs = typer.Typer(
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]},
    name="docs",
)
_extras = typer.Typer(
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]},
    name="extras",
)
_latest = typer.Typer(
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]},
    name="latest",
)
_needpull = typer.Typer(
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]},
    name="needpull",
)
_needpush = typer.Typer(
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]},
    name="needpush",
)
_next = typer.Typer(
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]},
    name="next",
)
_publish = typer.Typer(
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]},
    name="publish",
)
_pull = typer.Typer(
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]},
    name="pull",
)
_push = typer.Typer(
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]},
    name="push",
)
_pypi = typer.Typer(
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]},
    name="pypi",
)
_pytests = typer.Typer(
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]},
    name="pytests",
)
_repos = typer.Typer(
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]},
    name="repos",
)
_requirement = typer.Typer(
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]},
    name="requirement",
)
_requirements = typer.Typer(
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]},
    name="requirements",
)
_secrets = typer.Typer(
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]},
    name="secrets",
)
_sha = typer.Typer(
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]},
    name="sha",
)
_superproject = typer.Typer(
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]},
    name="superproject",
)
_tests = typer.Typer(
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]},
    name="tests",
)
_version = typer.Typer(
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]},
    name="version",
)
_venv = typer.Typer(
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]},
    name="venv",
)
_venvs = typer.Typer(
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]},
    name="venvs",
)


@app.command()
def brew(
    data: Annotated[
        Path,
        typer.Argument(
            help="Path/file to project or name of project",
            autocompletion=_repos_completions,
        ),
    ] = _cwd,
    command: str = typer.Option("", help="Command to check in order to run brew"),
):
    """Clean project."""
    Project(data).brew(command if command else None)


@app.command()
@_browser.command()
def browser(
    data: Annotated[
        Path,
        typer.Argument(
            help="Path/file to project or name of project",
            autocompletion=_repos_completions,
        ),
    ] = _cwd,
    version: Annotated[str, typer.Option(help="python major and minor version",
                                         autocompletion=_versions_completions)] = PYTHON_DEFAULT_VERSION,
    quiet: bool = True,
):
    """Build and serve the documentation with live reloading on file changes."""
    Project(data).browser(version=version, quiet=quiet)


@app.command()
@_build.command()
def build(
    data: Annotated[
        Path,
        typer.Argument(
            help="Path/file to project or name of project",
            autocompletion=_repos_completions,
        ),
    ] = _cwd,
    version: Annotated[str, typer.Option(help="python major and minor version",
                                         autocompletion=_versions_completions)] = PYTHON_DEFAULT_VERSION,
    quiet: bool = True,
):
    """Build a project `venv`, `completions`, `docs` and `clean`."""
    Project(data).build(version=version, quiet=quiet)


@app.command()
@_builds.command()
def builds(
    data: Annotated[
        Path,
        typer.Argument(
            help="Path/file to project or name of project",
            autocompletion=_repos_completions,
        ),
    ] = _cwd,
    quiet: bool = True,
):
    """Build a project `venv`, `completions`, `docs` and `clean` for all versions."""
    Project(data).builds(quiet=quiet)


@app.command()
@_buildrequires.command()
def buildrequires(
    data: Annotated[
        Path,
        typer.Argument(
            help="Path/file to project or name of project",
            autocompletion=_repos_completions,
        ),
    ] = _cwd,
):
    """Build requirements."""
    for item in Project(data).buildrequires():
        print(item)


@app.command()
@_clean.command()
def clean(
    data: Annotated[
        Path,
        typer.Argument(
            help="Path/file to project or name of project",
            autocompletion=_repos_completions,
        ),
    ] = _cwd,
):
    """Clean project."""
    Project(data).clean()


@app.command()
@_commit.command()
def commit(
    data: Annotated[
        Path,
        typer.Argument(
            help="Path/file to project or name of project",
            autocompletion=_repos_completions,
        ),
    ] = _cwd,
    msg: str = typer.Option("", "-m", "--message", "--msg", help="Commit message"),
):
    """Commit a project from path or name."""
    Project(data).commit(msg if msg else None)


@app.command()
@_completions.command()
def completions(
    data: Annotated[
        Path,
        typer.Argument(
            help="Path/file to project or name of project",
            autocompletion=_repos_completions,
        ),
    ] = _cwd,
):
    """Generate completions to /usr/local/etc/bash_completion.d."""
    Project(data).completions()


@app.command()
def coverage(
    data: Annotated[
        Path,
        typer.Argument(
            help="Path/file to project or name of project",
            autocompletion=_repos_completions,
        ),
    ] = _cwd,
):
    """Project coverage."""
    Project(data).coverage()


@app.command()
@_dependencies.command()
def dependencies(
    data: Annotated[
        Path,
        typer.Argument(
            help="Path/file to project or name of project",
            autocompletion=_repos_completions,
        ),
    ] = _cwd,
):
    """Project dependencies from path or name."""
    for item in Project(data).dependencies():
        print(item)


@app.command()
@_dirty.command()
def dirty(
    data: Annotated[
        Path,
        typer.Argument(
            help="Path/file to project or name of project",
            autocompletion=_repos_completions,
        ),
    ] = _cwd,
):
    """Is the repo dirty?: 0 if dirty."""
    if Project(data).dirty():
        sys.exit(0)
    else:
        sys.exit(1)


@app.command()
@_distribution.command()
def distribution(
    data: Annotated[
        Path,
        typer.Argument(
            help="Path/file to project or name of project",
            autocompletion=_repos_completions,
        ),
    ] = _cwd,
):
    """Clean project."""
    print(Project(data).distribution())


@app.command()
@_diverge.command()
def diverge(
    data: Annotated[
        Path,
        typer.Argument(
            help="Path/file to project or name of project",
            autocompletion=_repos_completions,
        ),
    ] = _cwd,
):
    """Does the repo diverge?: 0: if diverge."""
    if Project(data).diverge():
        sys.exit(0)
    else:
        sys.exit(1)


@app.command()
@_docs.command()
def docs(
    data: Annotated[
        Path,
        typer.Argument(
            help="Path/file to project or name of project",
            autocompletion=_repos_completions,
        ),
    ] = _cwd,
    version: Annotated[str, typer.Option(help="python major and minor version",
                                         autocompletion=_versions_completions)] = PYTHON_DEFAULT_VERSION,
    quiet: bool = True,
):
    """Build the documentation."""
    Project(data).docs(version=version, quiet=quiet)


@app.command()
def executable(
    data: Annotated[
        Path,
        typer.Argument(
            help="Path/file to project or name of project",
            autocompletion=_repos_completions,
        ),
    ] = _cwd,
    version: Annotated[str, typer.Option(help="python major and minor version",
                                         autocompletion=_versions_completions)] = PYTHON_DEFAULT_VERSION,
):
    """Shows executable being used."""
    print(Project(data).executable(version=version))


@app.command()
@_extras.command()
def extras(
    data: Annotated[
        Path,
        typer.Argument(
            help="Path/file to project or name of project",
            autocompletion=_repos_completions,
        ),
    ] = _cwd,
):
    """Project extras."""
    for item in Project(data).extras(as_list=True):
        print(item)


@app.command()
def github(
    data: Annotated[
        Path,
        typer.Argument(
            help="Path/file to project or name of project",
            autocompletion=_repos_completions,
        ),
    ] = _cwd,
):
    """GitHub repo api."""
    print(Project(data).github())


@app.command()
@_latest.command()
def latest(
    data: Annotated[
        Path,
        typer.Argument(
            help="Path/file to project or name of project",
            autocompletion=_repos_completions,
        ),
    ] = _cwd,
):
    """Latest tag."""
    print(Project(data).latest())


@app.command()
@_needpull.command()
def needpull(
    data: Annotated[
        Path,
        typer.Argument(
            help="Path/file to project or name of project",
            autocompletion=_repos_completions,
        ),
    ] = _cwd,
):
    """Does the repo need to be pulled?: 0 if needs pull."""
    if Project(data).needpull():
        sys.exit(0)
    else:
        sys.exit(1)


@app.command()
@_needpush.command()
def needpush(
    data: Annotated[
        Path,
        typer.Argument(
            help="Path/file to project or name of project",
            autocompletion=_repos_completions,
        ),
    ] = _cwd,
):
    """Does the repo need to be pushed?: 0 if needs push."""
    if Project(data).needpush():
        sys.exit(0)
    else:
        sys.exit(1)


@app.command(name="next")
@_next.command(name="next")
def __next(
    data: Annotated[
        Path,
        typer.Argument(
            help="Path/file to project or name of project",
            autocompletion=_repos_completions,
        ),
    ] = _cwd,
    part: Annotated[Bump, typer.Option(help="part to increase if force")] = Bump.PATCH,
    force: Annotated[bool, typer.Option(help="force bump")] = False,
):
    """Show next version based on fix: feat: or BREAKING CHANGE:."""
    print(Project(data).next(part, force))


@app.command()
@_publish.command()
def publish(
    data: Annotated[
        Path,
        typer.Argument(
            help="Path/file to project or name of project",
            autocompletion=_repos_completions,
        ),
    ] = _cwd,
    part: Annotated[Bump, typer.Option(help="part to increase if force")] = Bump.PATCH,
    force: Annotated[bool, typer.Option(help="force bump")] = False,
    ruff: Annotated[bool, typer.Option(help="run ruff")] = True,
    tox: Annotated[bool, typer.Option(help="run tox")] = False,
    quiet: bool = True,
):
    """Publish runs runs `tests`, `commit`, `tag`, `push`, `twine` and `clean`."""
    Project(data).publish(part=part, force=force, ruff=ruff, tox=tox, quiet=quiet)


@app.command()
@_pull.command()
def pull(
    data: Annotated[
        Path,
        typer.Argument(
            help="Path/file to project or name of project",
            autocompletion=_repos_completions,
        ),
    ] = _cwd,
):
    """Pull repo."""
    Project(data).pull()


@app.command()
@_push.command()
def push(
    data: Annotated[
        Path,
        typer.Argument(
            help="Path/file to project or name of project",
            autocompletion=_repos_completions,
        ),
    ] = _cwd,
):
    """Push repo."""
    Project(data).push()


@app.command()
@_pypi.command()
def pypi(
    data: Annotated[
        Path,
        typer.Argument(
            help="Path/file to project or name of project",
            autocompletion=_repos_completions,
        ),
    ] = _cwd,
):
    """Pypi information for a package."""
    print(Project(data).pypi())


@app.command()
def pytest(
    data: Annotated[
        Path,
        typer.Argument(
            help="Path/file to project or name of project",
            autocompletion=_repos_completions,
        ),
    ] = _cwd,
    version: Annotated[str, typer.Option(help="python major and minor version",
                                         autocompletion=_versions_completions)] = PYTHON_DEFAULT_VERSION,
):
    """Run pytest."""
    sys.exit(Project(data).pytest(version=version))


@app.command()
@_pytests.command()
def pytests(
    data: Annotated[
        Path,
        typer.Argument(
            help="Path/file to project or name of project",
            autocompletion=_repos_completions,
        ),
    ] = _cwd,
):
    """Run pytest for all versions."""
    sys.exit(Project(data).pytests())


@app.command()
@_repos.command()
def repos(
    data: Annotated[
        Path,
        typer.Argument(
            help="Path/file to project or name of project",
            autocompletion=_repos_completions,
        ),
    ] = _cwd,
    ret: Annotated[ProjectRepos, typer.Option(help="return names, paths, dict or instances")] = ProjectRepos.NAMES,
    py: Annotated[bool, typer.Option(help="return only python projects instances")] = False,
    sync: Annotated[bool, typer.Option(help="push or pull all repos")] = False,
    archive: Annotated[bool, typer.Option(help="look for repos under ~/Archive")] = False,
):
    """Manage repos and projects under HOME and HOME/Archive."""
    rv = Project(data).repos(ret=ret, py=py, sync=sync, archive=archive)
    if sync is False:
        if ret == ProjectRepos.PATHS:
            for repo in rv:
                print(str(repo))
        else:
            for repo in rv:
                print(repo)


@app.command()
@_requirement.command()
def requirement(
    data: Annotated[
        Path,
        typer.Argument(
            help="Path/file to project or name of project",
            autocompletion=_repos_completions,
        ),
    ] = _cwd,
    version: Annotated[str, typer.Option(help="python major and minor version",
                                         autocompletion=_versions_completions)] = PYTHON_DEFAULT_VERSION,
    install: Annotated[bool, typer.Option(help="install requirements, dependencies and extras")] = False,
    upgrade: Annotated[bool, typer.Option(help="upgrade requirements, dependencies and extras")] = False,
):
    """Requirements for package."""
    rv = Project(data).requirement(version=version, install=install, upgrade=upgrade)
    if install or upgrade:
        return
    for item in rv:
        print(item)


@app.command()
@_requirements.command()
def requirements(
    data: Annotated[
        Path,
        typer.Argument(
            help="Path/file to project or name of project",
            autocompletion=_repos_completions,
        ),
    ] = _cwd,
    upgrade: Annotated[bool, typer.Option(help="upgrade requirements, dependencies and extras")] = False,
):
    """Install requirements for all python versions."""
    Project(data).requirements(upgrade=upgrade)


@app.command(name="ruff")
def _ruff(
    data: Annotated[
        Path,
        typer.Argument(
            help="Path/file to project or name of project",
            autocompletion=_repos_completions,
        ),
    ] = _cwd,
    version: Annotated[str, typer.Option(help="python major and minor version",
                                         autocompletion=_versions_completions)] = PYTHON_DEFAULT_VERSION,
):
    """Run ruff."""
    sys.exit(Project(data).ruff(version=version))


@app.command()
@_secrets.command()
def secrets(
    data: Annotated[
        Path,
        typer.Argument(
            help="Path/file to project or name of project",
            autocompletion=_repos_completions,
        ),
    ] = _cwd,
):
    """Update GitHub repository secrets."""
    Project(data).secrets()


@app.command()
@_sha.command()
def sha(
    data: Annotated[
        Path,
        typer.Argument(
            help="Path/file to project or name of project",
            autocompletion=_repos_completions,
        ),
    ] = _cwd,
    ref: Annotated[GitSHA, typer.Option(help="local, base or remote")] = GitSHA.LOCAL,
):
    """SHA for local, base or remote."""
    print(Project(data).sha(ref))


@app.command()
@_superproject.command()
def superproject(
    data: Annotated[
        Path,
        typer.Argument(
            help="Path/file to project or name of project",
            autocompletion=_repos_completions,
        ),
    ] = _cwd,
):
    """Superproject path."""
    print(Project(data).superproject())


@app.command(name="sync")
def __sync(
    data: Annotated[
        Path,
        typer.Argument(
            help="Path/file to project or name of project",
            autocompletion=_repos_completions,
        ),
    ] = _cwd,
):
    """Sync repo."""
    Project(data).sync()


@app.command("tag")
def __tag(
    tag: str,
    data: Annotated[
        Path,
        typer.Argument(
            help="Path/file to project or name of project",
            autocompletion=_repos_completions,
        ),
    ] = _cwd,
):
    """Tag repo."""
    Project(data).tag(tag)


@app.command(name="test")
def test(
    data: Annotated[
        Path,
        typer.Argument(
            help="Path/file to project or name of project",
            autocompletion=_repos_completions,
        ),
    ] = _cwd,
    version: Annotated[str, typer.Option(help="python major and minor version",
                                         autocompletion=_versions_completions)] = PYTHON_DEFAULT_VERSION,
    ruff: Annotated[bool, typer.Option(help="run ruff")] = True,
    tox: Annotated[bool, typer.Option(help="run tox")] = False,
    quiet: bool = True,
):
    """Test project, runs `build`, `ruff`, `pytest` and `tox`."""
    sys.exit(Project(data).test(version=version, ruff=ruff, tox=tox, quiet=quiet))


@app.command(name="tests")
@_tests.command(name="tests")
def tests(
    data: Annotated[
        Path,
        typer.Argument(
            help="Path/file to project or name of project",
            autocompletion=_repos_completions,
        ),
    ] = _cwd,
    ruff: Annotated[bool, typer.Option(help="run ruff")] = True,
    tox: Annotated[bool, typer.Option(help="run tox")] = False,
    quiet: bool = True,
):
    """Test project, runs `build`, `ruff`, `pytest` and `tox`."""
    sys.exit(Project(data).tests(ruff=ruff, tox=tox, quiet=quiet))


@app.command()
def top(
    data: Annotated[
        Path,
        typer.Argument(
            help="Path/file to project or name of project",
            autocompletion=_repos_completions,
        ),
    ] = _cwd,
):
    """Top path."""
    print(Project(data).top())


@app.command(name="tox")
def _tox(
    data: Annotated[
        Path,
        typer.Argument(
            help="Path/file to project or name of project",
            autocompletion=_repos_completions,
        ),
    ] = _cwd,
):
    """Run tox."""
    sys.exit(Project(data).tox())


@app.command()
def twine(
    data: Annotated[
        Path,
        typer.Argument(
            help="Path/file to project or name of project",
            autocompletion=_repos_completions,
        ),
    ] = _cwd,
    part: Annotated[Bump, typer.Option(help="part to increase if force")] = Bump.PATCH,
    force: Annotated[bool, typer.Option(help="force bump")] = False,
):
    """Run twine."""
    sys.exit(Project(data).twine(part, force))


@app.command(name="version")
@_version.command(name="version")
def __version(
    data: Annotated[
        Path,
        typer.Argument(
            help="Path/file to project or name of project",
            autocompletion=_repos_completions,
        ),
    ] = _cwd,
):
    """Project version from pyproject.toml, tag, distribution or pypi."""
    print(Project(data).version())


@app.command()
@_venv.command()
def venv(
    data: Annotated[
        Path,
        typer.Argument(
            help="Path/file to project or name of project",
            autocompletion=_repos_completions,
        ),
    ] = _cwd,
    version: Annotated[str, typer.Option(help="python major and minor version",
                                         autocompletion=_versions_completions)] = PYTHON_DEFAULT_VERSION,
    clear: Annotated[bool, typer.Option(help="force removal of venv before")] = False,
    upgrade: Annotated[bool, typer.Option(help="upgrade all dependencies")] = False,
):
    """Creates venv, runs: `write` and `requirements`."""
    Project(data).venv(version=version, clear=clear, upgrade=upgrade)


@app.command()
@_venvs.command()
def venvs(
    data: Annotated[
        Path,
        typer.Argument(
            help="Path/file to project or name of project",
            autocompletion=_repos_completions,
        ),
    ] = _cwd,
    upgrade: Annotated[bool, typer.Option(help="upgrade all dependencies")] = False,
):
    """Creates venv, runs: `write` and `requirements`."""
    Project(data).venvs(upgrade=upgrade)


@app.command()
def write(
    data: Annotated[
        Path,
        typer.Argument(
            help="Path/file to project or name of project",
            autocompletion=_repos_completions,
        ),
    ] = _cwd,
):
    """Updates pyproject.toml and docs conf.py."""
    Project(data).write()


if "sphinx" in sys.modules and __name__ != "__main__":
    with pipmetapathfinder():
        import tomlkit

    text = """# Usage

```{eval-rst}
"""
    root = Path(__file__).parent.parent.parent
    pyproject_toml = root / "pyproject.toml"
    file = root / "docs/usage.md"
    if file.exists():
        original = file.read_text()
        # TODO: escribir el pyproject.toml poner global para el nombre del programa
        with Path.open(pyproject_toml, "rb") as f:
            toml = tomlkit.load(f)

            new = copy.deepcopy(toml)
            new["project"]["scripts"] = {}
        for key, value in globals().copy().items():
            if isinstance(value, typer.Typer):
                program = NODEPS_EXECUTABLE if key == "app" else key.replace("_", "")
                cls = f"{NODEPS_PROJECT_NAME}.__main__:{key}"
                new["project"]["scripts"][program] = cls
                text += f".. click:: {cls}_click\n"
                text += f"    :prog: {program}\n"
                text += "    :nested: full\n\n"
                globals()[f"{key}_click"] = typer.main.get_command(value)
        text += "```\n"
        if original != text:
            file.write_text(text)
            print(f"{file}: updated!")
        new["project"] = dict_sort(new["project"])
        if toml != new:
            with pyproject_toml.open("w") as f:
                tomlkit.dump(new, f)
                print(f"{pyproject_toml}: updated!")

if __name__ == "__main__":
    try:
        sys.exit(app())
    except KeyboardInterrupt:
        print("Aborted!")
        sys.exit(1)
