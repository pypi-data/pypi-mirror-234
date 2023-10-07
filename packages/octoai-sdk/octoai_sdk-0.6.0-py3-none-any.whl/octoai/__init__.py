"""Initializes the octoai module."""
from importlib.metadata import version

from . import client, errors, types, utils

__version__ = version("octoai-sdk")
__all__ = ["client", "errors", "server", "service", "types", "utils"]
