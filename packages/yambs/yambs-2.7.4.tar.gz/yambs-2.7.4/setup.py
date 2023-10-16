# =====================================
# generator=datazen
# version=3.1.3
# hash=f3af34a4b5815c617489419b194b30b5
# =====================================

"""
yambs - Package definition for distribution.
"""

# third-party
try:
    from setuptools_wrapper.setup import setup
except (ImportError, ModuleNotFoundError):
    from yambs_bootstrap.setup import setup  # type: ignore

# internal
from yambs import DESCRIPTION, PKG_NAME, VERSION

author_info = {
    "name": "Vaughn Kottler",
    "email": "vaughnkottler@gmail.com",
    "username": "vkottler",
}
pkg_info = {
    "name": PKG_NAME,
    "slug": PKG_NAME.replace("-", "_"),
    "version": VERSION,
    "description": DESCRIPTION,
    "versions": [
        "3.11",
    ],
}
setup(
    pkg_info,
    author_info,
)
