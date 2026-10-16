# TamerOp website

[tamerop.com](https://tamerop.com) teaches the mathematics behind TamerOp and
shows how to use it through worked examples, library guides, API references
and benchmark reports. This repository contains the pages, notebooks, figures
and tools that build the site.

The three projects have separate repositories:

| Project | What it contains |
| --- | --- |
| [TamerOp.jl](https://github.com/erikmnovak/TamerOp.jl#readme) | The Julia library, its tests and releases. |
| **TamerOp-site** | The teaching site and its build tools. |
| [TamerOp-benchmarks](https://github.com/erikmnovak/TamerOp-benchmarks#readme) | Runnable comparisons, recorded measurements and reproduction instructions. |

For questions about the mathematics or software, use
[Discussions](https://github.com/erikmnovak/TamerOp.jl/discussions). Report a
problem or propose a substantial change in the shared
[issue tracker](https://github.com/erikmnovak/TamerOp.jl/issues), including the
page address when relevant. Website pull requests belong here; the
[contribution guide](CONTRIBUTING.md) explains how to propose a lesson, example
or correction.

## Build and preview

Place a TamerOp.jl checkout beside this repository, then follow the
[build instructions](docs/README.md) to prepare Julia and Python and build the
pages. The build executes the published notebooks and creates their downloadable
copies from the same results. The preview opens at <http://localhost:8000/>.

GitHub Actions builds the site against the current library `main` and publishes
successful website `main` builds to tamerop.com. Pull requests produce a
rendered site for review. The build guide covers source selection, focused
checks and [publication](docs/README.md#publish-on-github-pages).
