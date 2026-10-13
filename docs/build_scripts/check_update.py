"""Avoid rebuilding an unchanged scheduled site; a missing record requests a build."""
import argparse
import json
import os
import subprocess
from pathlib import Path
from urllib.request import Request, urlopen

from source_paths import SITE, package_root


def matches(record, site_sha, package_sha):
    return (record.get("site", {}).get("repository") == "https://github.com/erikmnovak/TamerOp-site"
            and record["site"].get("git_commit") == site_sha
            and record["site"].get("working_tree_dirty") is False
            and record.get("package_repository") == "https://github.com/erikmnovak/TamerOp.jl"
            and record.get("git_commit") == package_sha
            and record.get("working_tree_dirty") is False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scheduled", action="store_true")
    args = parser.parse_args()
    head = lambda root: subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
    site_sha, package_sha = head(SITE), head(package_root())
    needed = True
    if args.scheduled:
        try:
            request = Request("https://tamerop.com/downloads/publication.json", headers={"Cache-Control": "no-cache"})
            with urlopen(request, timeout=30) as response:
                record = json.load(response)
            needed = not matches(record, site_sha, package_sha)
        except (OSError, ValueError, KeyError):
            needed = True
    values = {"needed": str(needed).lower(), "site_sha": site_sha, "package_sha": package_sha}
    text = "".join(f"{key}={value}\n" for key, value in values.items())
    if output := os.environ.get("GITHUB_OUTPUT"):
        with Path(output).open("a") as stream:
            stream.write(text)
    print(text, end="")


if __name__ == "__main__":
    main()
