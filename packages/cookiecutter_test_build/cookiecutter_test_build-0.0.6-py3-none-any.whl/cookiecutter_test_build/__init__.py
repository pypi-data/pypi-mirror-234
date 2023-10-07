"""Python Project."""

from importlib.metadata import version

__version__ = version("cookiecutter_test_build")

from ._utils import add

__all__ = ["add"]
