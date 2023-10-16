from pathlib import Path

import toml

from .core import *

# Removing this for now. It doesn't work when the package is install because the package directory isn't there.
# # Credit to @unruffled-nightingale: https://github.com/unruffled-nightingale/fastapi-template/blob/main/fastapi_template/__init__.py
# def get_version() -> str:
#     path = Path(__file__).resolve().parents[1] / "pyproject.toml"
#     pyproject = toml.load(str(path))
#     version: str = pyproject["tool"]["poetry"]["version"]
#     return version


# __version__ = get_version()
