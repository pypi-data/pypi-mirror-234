"""Watz Python."""

from importlib.metadata import version

__version__ = version("watz")

from ._utils import add

__all__ = ["add"]
