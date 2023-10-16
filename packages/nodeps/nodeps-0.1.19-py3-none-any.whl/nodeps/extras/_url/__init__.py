"""NoDeps Extras Url Module."""
__all__ = (
    "PYTHON_FTP",
    "python_latest",
    "python_version",
    "python_versions",
    "request_x_api_key_json",
)

import os
import platform
import re

try:
    # nodeps[url] extras
    import bs4  # type: ignore[attr-defined]
    import requests  # type: ignore[attr-defined]
except ModuleNotFoundError:
    bs4 = None
    requests = None

PYTHON_FTP = "https://www.python.org/ftp/python"
"""Python FTP Server URL"""


def _msg_bs4_requests():
    if bs4 is None or requests is None:
        msg = "bs4 and/or requests are not installed: installed with 'pip install nodeps[url]'"
        raise ImportError(msg)


def python_latest(start: str | int | None = None) -> str:
    """Python latest version avaialble.

    Examples:
        >>> import platform
        >>> from nodeps.extras._url import python_latest
        >>>
        >>> v = platform.python_version()
        >>> if "rc" not in v:
        ...     major_minor = v.rpartition(".")[0]
        ...     assert python_latest(v).rpartition(".")[0] == major_minor
        ...     assert python_latest(v).rpartition(".")[2] >= v.rpartition(".")[2]
        ...     assert python_latest(major_minor).rpartition(".")[0] == major_minor
        ...     assert python_latest(major_minor).rpartition(".")[2] >= v.rpartition(".")[2]

    Args:
        start: version startswith match, i.e.: "3", "3.10", "3.10", 3 or None to use `PYTHON_VERSION`
          environment variable or :obj:``sys.version`` if not set (Default: None).

    Returns:
        Latest Python Version
    """
    start = python_version() if start is None else start
    start = start.rpartition(".")[0] if len(start.split(".")) == 3 else start  # noqa: PLR2004
    return [i for i in python_versions() if str(i).startswith(start)][-1]


def python_version() -> str:
    """Major Minor Version ``$PYTHON_VERSION``, ``$PYTHON_REQUIRES``, ``PYTHON_DEFAULT_VERSION`` or :obj:`sys.version`.

    Examples:
        >>> import os
        >>> import platform
        >>> from nodeps.extras._url import python_version
        >>>
        >>> v = python_version()
        >>> assert platform.python_version().startswith(v)
        >>> assert len(v.split(".")) == 2
        >>>
        >>> os.environ["PYTHON_VERSION"] = "3.10"
        >>> assert python_version() == "3.10"
        >>>
        >>> os.environ["PYTHON_VERSION"] = "3.12-dev"
        >>> assert python_version() == "3.12-dev"
        >>>
        >>> os.environ["PYTHON_VERSION"] = "3.12.0b4"
        >>> assert python_version() == "3.12"

    Returns:
        str
    """
    p = platform.python_version()
    ver = (os.environ.get("PYTHON_VERSION", p) or os.environ.get("PYTHON_REQUIRES", p)
           or os.environ.get("PYTHON_DEFAULT_VERSION", p))
    if len(ver.split(".")) == 3:  # noqa: PLR2004
        return ver.rpartition(".")[0]
    return ver


def python_versions() -> list[str]:
    """Python versions avaialble.

    Examples:
        >>> import platform
        >>> from nodeps.extras._url import python_versions
        >>>
        >>> v = platform.python_version()
        >>> if not "rc" in v:
        ...     assert v in python_versions()

    Returns:
        Tuple of Python Versions
    """
    _msg_bs4_requests()
    rv = []
    for link in bs4.BeautifulSoup(requests.get(PYTHON_FTP, timeout=5).text, "html.parser").find_all("a"):
        if link := re.match(r"((3\.([7-9]|[1-9][0-9]))|4).*", link.get("href").rstrip("/")):
            rv.append(link.string)
    rv.sort(key=lambda s: [int(u) for u in s.split(".")])
    return rv


def request_x_api_key_json(url, key: str = "") -> dict[str, str] | None:
    """API request helper with API Key and returning json.

    Examples:
        >>> from nodeps.extras._url import request_x_api_key_json
        >>>
        >>> request_x_api_key_json("https://api.iplocation.net/?ip=8.8.8.8", \
                "rn5ya4fp/tzI/mENxaAvxcMo8GMqmg7eMnCvUFLIV/s=")
        {'ip': '8.8.8.8', 'ip_number': '134744072', 'ip_version': 4, 'country_name': 'United States of America',\
 'country_code2': 'US', 'isp': 'Google LLC', 'response_code': '200', 'response_message': 'OK'}

    Args:
        url: API url
        key: API Key

    Returns:
        response json
    """
    _msg_bs4_requests()

    headers = {"headers": {"X-Api-Key": key}} if key else {}
    response = requests.get(url, **headers, timeout=2)
    if response.status_code == requests.codes.ok:
        return response.json()
    return None
