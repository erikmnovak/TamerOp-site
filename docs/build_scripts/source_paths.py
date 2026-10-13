"""Resolve the website's sources and its explicitly selected Julia checkout."""
from pathlib import Path
import os
from urllib.parse import quote

DOCS = Path(__file__).resolve().parents[1]
SITE = DOCS.parent
SITE_REPO = "https://github.com/erikmnovak/TamerOp-site/blob/main/"
PACKAGE_REPO = "https://github.com/erikmnovak/TamerOp.jl/blob/main/"


def package_root():
    return Path(os.environ.get("TAMEROP_SOURCE", SITE.parent / "TamerOp.jl")).resolve()


def source_path(base, name):
    if name.startswith("library:"):
        relative = Path(name.removeprefix("library:"))
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError(f"Invalid library source: {name}")
        return (package_root() / relative).resolve()
    return (Path(base) / name).resolve()


def source_name(path):
    path = Path(path).resolve()
    if path.is_relative_to(SITE):
        return path.relative_to(SITE).as_posix()
    if path.is_relative_to(package_root()):
        return "library:" + path.relative_to(package_root()).as_posix()
    raise ValueError(f"Source outside the selected projects: {path}")


def source_url(path):
    name = source_name(path)
    return (PACKAGE_REPO + quote(name.removeprefix("library:"))
            if name.startswith("library:") else SITE_REPO + quote(name))
