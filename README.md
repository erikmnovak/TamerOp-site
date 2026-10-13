# TamerOp website

This website hosts the documentation for
[TamerOp.jl](https://github.com/erikmnovak/TamerOp.jl), including tutorials,
the API, recipes, and a didactic, pedagogically minded overview of
multiparameter persistence. The published site is [tamerop.com](https://tamerop.com).

Keep the projects in separate folders:

```text
projects/
    TamerOp.jl/
    TamerOp-site/
```

From `TamerOp-site`, prepare and build the website with Julia 1.12 and Python
3.11 or newer:

```sh
python -m venv docs/.venv
docs/.venv/bin/python -m pip install -r docs/requirements.txt
julia --startup-file=no --threads=1 docs/bootstrap.jl
docs/.venv/bin/python -m unittest discover -s docs/build_scripts -p 'test_*.py'
docs/.venv/bin/python docs/build_scripts/publish.py
docs/.venv/bin/python docs/build_scripts/check_site.py
docs/.venv/bin/python docs/build_scripts/preview.py
```

The preview opens at <http://localhost:8000/>. On Windows, the Python executable
is `docs\.venv\Scripts\python.exe`. See [the build guide](docs/README.md) for
notebook execution, source ownership, visual review and publication.

The bootstrap creates an ignored Julia environment under
`docs/.build/environment`. It uses the adjacent `TamerOp.jl` checkout. Set
`TAMEROP_SOURCE` to another checkout's absolute path before both bootstrapping
and building if the folders are elsewhere. Website dependencies stay in this
environment; the library does not depend on the website. Notebook downloads
record the selected package source and the website revision separately.

## Publication

The Documentation workflow checks out this project and the current `main`
of `TamerOp.jl`, records both revisions, and builds against those exact
checkouts. It does not select the Julia General release. Website pushes
trigger a build; pull requests build review artifacts without deploying.

A scheduled check looks for new library commits twice an hour. It skips the
build when the published record already matches both repositories. This keeps
the projects independent and needs no token with access to both repositories.
GitHub may delay scheduled jobs. Use **Actions → Documentation → Run workflow**
for an immediate rebuild after a library update. Scheduled workflows must
remain enabled in the repository.

Only a successful trusted `main` build deploys. GitHub Pages must be configured
to use **GitHub Actions** in this repository's Settings. The custom domain
`tamerop.com` must belong to this repository's Pages configuration before the
domain transfer is complete. The generated website and local authoring records
are ignored by Git.
