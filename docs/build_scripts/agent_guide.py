"""Publish the selected library's agent guide without maintaining a second copy."""
from __future__ import annotations

import hashlib
import html
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import tomllib
from urllib.parse import quote
import zipfile

REPOSITORY = "https://github.com/erikmnovak/TamerOp.jl"
DOWNLOAD_ROOT = Path("downloads/agent")
RECORD_PATH = Path("downloads/agent-guide.json")
ARCHIVE_PATH = Path("downloads/tamerop-agent-guide.zip")


def snapshot(package: Path, guides: dict) -> tuple[dict, dict[str, bytes]]:
    """Read a complete public guide and identify the exact selected checkout."""
    package = Path(package).resolve()
    directory = package / "agent"
    if directory.is_symlink():
        raise ValueError("Agent guide inputs cannot be symlinks: agent/")
    routes = {name.removeprefix("library:agent/"): page
              for name, page in guides.items() if name.startswith("library:agent/")}
    if "README.md" not in routes:
        raise ValueError("The agent guide needs an explicit library:agent/README.md publication route")
    required = set(routes) | {"skills/tamerop/SKILL.md", "skills/tamerop/agents/openai.yaml",
                              "install_skill.jl", "check_skill.jl"}
    required.update(f"examples/{Path(name).stem}.jl" for name in routes
                    if name.startswith("workflows/"))
    for name in required:
        path = PurePosixPath(name)
        if path.is_absolute() or ".." in path.parts:
            raise ValueError(f"Invalid agent guide path: {name}")
        if not (directory / name).is_file():
            raise ValueError(f"Missing agent guide input: agent/{name}")
    files = {}
    for path in sorted(directory.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"Agent guide inputs cannot be symlinks: {path}")
        if not path.is_file():
            continue
        name = path.relative_to(directory).as_posix()
        if any(part.startswith(".") or part == "__pycache__" for part in Path(name).parts):
            continue
        if path.suffix not in {".md", ".jl", ".toml", ".py", ".yaml", ".yml"} and path.name != "LICENSE":
            raise ValueError(f"Unexpected agent guide file: agent/{name}")
        files[name] = path.read_bytes()
    project = tomllib.loads((package / "Project.toml").read_text())
    revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=package, text=True).strip()
    if not re.fullmatch(r"[0-9a-f]{40,64}", revision):
        raise ValueError("The agent guide needs a selected library Git revision")
    dirty = bool(subprocess.check_output(["git", "status", "--porcelain"], cwd=package))
    record = {"schema_version": 1, "repository": REPOSITORY,
              "library_version": project["version"], "library_revision": revision,
              "working_tree_dirty": dirty, "routes": routes,
              "files_sha256": {name: hashlib.sha256(data).hexdigest() for name, data in files.items()}}
    return record, files


def stage_downloads(stage: Path, record: dict, files: dict[str, bytes]) -> None:
    """Stage non-Markdown assets and an archive; preserve raw Markdown after HTML rendering."""
    destination = Path(stage) / DOWNLOAD_ROOT
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True)
    for name, data in files.items():
        if Path(name).suffix == ".md":
            continue
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    (Path(stage) / RECORD_PATH).write_text(json.dumps(record, indent=2) + "\n")
    with zipfile.ZipFile(Path(stage) / ARCHIVE_PATH, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in files.items():
            entry = zipfile.ZipInfo("agent/" + name, date_time=(1980, 1, 1, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, data)


def page_note(record: dict, source: Path, package: Path, page: Path, stage: Path) -> str:
    """Small version and download entrance, using raw anchors to retain .md URLs."""
    relative = Path(source).relative_to(Path(package) / "agent").as_posix()
    def link(target: Path, label: str) -> str:
        href = quote(Path(os.path.relpath(Path(stage) / target, Path(page).parent)).as_posix())
        return f'<a href="{href}">{html.escape(label)}</a>'
    version = html.escape(record["library_version"])
    revision = record["library_revision"]
    source_url = f'{REPOSITORY}/blob/{revision}/agent/{quote(relative)}'
    return ('\n\n```@raw html\n<p class="agent-guide-source">'
            f'TamerOp {version} · <a href="{source_url}">library revision {revision[:8]}</a>. '
            + link(DOWNLOAD_ROOT / relative, "Read this page as Markdown") + ' · '
            + link(ARCHIVE_PATH, "Download the guide, examples and skill")
            + '</p>\n```\n')


def install_downloads(root: Path, files: dict[str, bytes]) -> None:
    """Copy byte-identical source files after Documenter, including original .md files."""
    destination = Path(root) / DOWNLOAD_ROOT
    if destination.exists():
        shutil.rmtree(destination)
    for name, data in files.items():
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)


def check_downloads(root: Path, publication: dict, guides: dict) -> None:
    """Reject incomplete/stale source downloads, archives or generated guide routes."""
    root = Path(root)
    record = json.loads((root / RECORD_PATH).read_text())
    if record != publication.get("agent_guide"):
        raise ValueError("Agent guide provenance differs from the publication record")
    expected = {name.removeprefix("library:agent/"): page for name, page in guides.items()
                if name.startswith("library:agent/")}
    if not expected or record.get("routes") != expected:
        raise ValueError("Agent guide publication routes changed; rebuild the website")
    if record["library_revision"] != publication["package_checkout"]["git_commit"]:
        raise ValueError("Agent guide does not describe the selected library revision")
    hashes = record["files_sha256"]
    actual = {path.relative_to(root / DOWNLOAD_ROOT).as_posix()
              for path in (root / DOWNLOAD_ROOT).rglob("*") if path.is_file()}
    if actual != set(hashes):
        raise ValueError("Agent guide download set differs from its source record")
    for name, digest in hashes.items():
        if hashlib.sha256((root / DOWNLOAD_ROOT / name).read_bytes()).hexdigest() != digest:
            raise ValueError(f"Agent guide download changed: {name}")
    with zipfile.ZipFile(root / ARCHIVE_PATH) as archive:
        if set(archive.namelist()) != {"agent/" + name for name in hashes}:
            raise ValueError("Agent guide archive has a different source set")
        for name, digest in hashes.items():
            if hashlib.sha256(archive.read("agent/" + name)).hexdigest() != digest:
                raise ValueError(f"Agent guide archive changed: {name}")
    for source, route in expected.items():
        page = root / Path(route).with_suffix(".html")
        text = page.read_text()
        for target in (DOWNLOAD_ROOT / source, ARCHIVE_PATH):
            href = quote(Path(os.path.relpath(root / target, page.parent)).as_posix())
            if f'href="{href}"' not in text:
                raise ValueError(f"Agent guide page is missing its source download: {route}")
