"""NoDeps Backend Module."""
from setuptools import build_meta as _orig

# noinspection PyUnresolvedReferences
from setuptools.build_meta import *


def get_requires_for_build_wheel(config_settings=None):
    """Get build dependencies for building a wheel."""
    return _orig.get_requires_for_build_wheel(config_settings)


def get_requires_for_build_sdist(config_settings=None):
    """Get build dependencies for building a source distribution."""
    return _orig.get_requires_for_build_sdist(config_settings)
