# Build the teaching site

The website is built from Markdown, notebooks and the manifests in this
directory. Edit those sources; `docs/.build/` and `docs/build/` contain generated
files. For proposing a lesson or correction, start with
[CONTRIBUTING.md](../CONTRIBUTING.md). This guide covers the tools needed to
build and check that work.

## Prepare the tools

Use Julia 1.12 and Python 3.11 or newer. Keep a
[TamerOp.jl checkout](https://github.com/erikmnovak/TamerOp.jl) beside this
repository:

```text
projects/
    TamerOp.jl/
    TamerOp-site/
```

Run the following from `TamerOp-site`:

```sh
python -m venv docs/.venv
docs/.venv/bin/python -m pip install -r docs/requirements.txt
JULIA_NUM_PRECOMPILE_TASKS=1 julia --startup-file=no --threads=1 docs/bootstrap.jl
```

On Windows, use `docs\.venv\Scripts\python.exe` and your shell's syntax for
environment variables. The bootstrap creates an isolated Julia environment
under `docs/.build/environment`. To select a library checkout elsewhere, set
`TAMEROP_SOURCE` to its absolute path before bootstrapping and building.
The website dependencies remain in this environment.

[Project.toml](Project.toml) and [requirements.txt](requirements.txt) specify
the direct dependency versions. The resolved Julia manifest is included with
the generated downloads. Builds record the selected library sources and the
website revision, so the examples can be associated with the code that ran them.

## Build and preview

```sh
docs/.venv/bin/python -m unittest discover -s docs/build_scripts -p 'test_*.py'
docs/.venv/bin/python docs/build_scripts/publish.py
docs/.venv/bin/python docs/build_scripts/check_site.py
docs/.venv/bin/python docs/build_scripts/preview.py
```

Open <http://localhost:8000/>. Add `--port 8765` to the preview command to use
another port. The preview serves `docs/build` without browser caching; rebuild
after editing sources, then refresh the page. HTML uses ordinary `.html`
links, so `docs/build/index.html` can also be opened directly.

The publisher executes each notebook selected in
[publication.toml](publication.toml) once in a fresh IJulia kernel, using one
Julia and BLAS thread. It creates both the page and its executed download from
that capture. A cell exception, missing output, missing declared figure or
missing alternative text fails the build. Notebook settings in the manifest
bound cell execution time and download size. Compilation time is included in
the recorded execution time.

The build stages sources under `docs/.build/src`.
`site_catalog.py` prepares collections, topic pages and catalog metadata;
`docs/make.jl` runs Documenter. `navigation.py` then adds reading
continuations, and `site_shell.py` applies the sidebar, local heading outline
and search metadata.

### Reuse existing notebook executions

When only Markdown pages, navigation or appearance have changed, reuse a
complete verified capture while rebuilding from the current sources:

```sh
docs/.venv/bin/python docs/build_scripts/publish.py --reuse-executed
docs/.venv/bin/python docs/build_scripts/check_site.py
```

This checks notebook source and download hashes, the selected notebooks,
library sources and the declared execution environment. Any change to notebook
bytes, including Markdown cells, requires execution.

When some notebooks changed, execute those and reuse the unchanged ones with:

```sh
docs/.venv/bin/python docs/build_scripts/publish.py --reuse-unchanged
docs/.venv/bin/python docs/build_scripts/check_site.py
```

This validates every previous download and requires matching package sources,
binary assets, notebook selection, declared environment, Julia version and
the recorded versions of the pinned Python packages. Each reused notebook
retains its execution origin in the new publication record. Use a normal build
if a complete compatible capture is unavailable. All build modes accept
`--julia /path/to/julia`; the two reuse options cannot be combined.

### Inspect the output

`check_site.py` checks publication records, executed downloads, figure hashes,
links, anchors, catalog destinations and reachability from the homepage.
The Python tests cover conversion, optional sections, reading routes, generated
navigation and output handling. Inspect the changed pages in a browser too:
read the equations and figure labels, follow links, try controls and check a
narrow window in light and dark themes.

The outputs include:

| Path under `docs/build/` | Contents |
| --- | --- |
| `tutorials/`, `guides/`, `reference/`, `benchmarks/` and other routed directories | Rendered articles. |
| `collections/`, `topics/`, `reading_map.html` and `topic_map.html` | Navigation and subject or learning maps. |
| `downloads/*.ipynb` | Executed notebooks with their saved outputs. |
| `downloads/figures/` | Files exported by the notebooks. |
| `downloads/publication.json` | Revisions, source hashes, execution origins, timings and tool versions. |
| `downloads/environment/` | Declared dependencies and the resolved build environment. |

Notebook download links are rewritten so they still work when the notebook
is moved. The saved Julia manifest records the selected checkout's build path.
To reproduce a build elsewhere, check out the recorded website and library
revisions, set `TAMEROP_SOURCE`, and bootstrap again; compare the resolved
dependencies with the saved environment. A build with uncommitted library
changes records individual source hashes as well as its commit.

## Sources and catalogs

Each article has one canonical source. Its website page, notebook download and
figures derive from that source.

| File | What it controls |
| --- | --- |
| [article_inventory.toml](article_inventory.toml) | Article identity, question, scope, type, topics and canonical source. See the [schema guide](article_inventory.md). |
| [publication.toml](publication.toml) | Source to page routes, notebook execution and declared outputs. |
| [navigation.toml](navigation.toml) | Collection labels, article placement, grouping and order. |
| [reading_map.toml](reading_map.toml) | Suggested reading routes, diagram positions and lesson continuations. |
| [api_coverage.toml](api_coverage.toml) and [api_inventory.toml](api_inventory.toml) | API reference assignments and generated binding observations. See the [API inventory guide](api_inventory.md). |

Add routes only for usable authored pages. When removing a page, update incoming
links, the catalogs and generated navigation together; a fresh build should
contain no leftover page. Do not add independent source lists to `make.jl`
or generated collection pages.

## Maintain site navigation

The sidebar is generated from the catalogs. A topic's title opens its authored
overview, when one exists; the adjacent arrow expands the article list.
A collection may contain topic groups, giving at most two expandable levels.
The current article's ancestors open automatically. `sessionStorage` retains
expanded branches and scroll positions within the browser tab, while native
disclosures and links remain usable without JavaScript or storage.

An authored topic overview lives at
`docs/src/collections/<collection>/topics/<topic>.md` and has an existing
`resource` record with that topic. The catalog attaches it to the topic title
instead of repeating it as an article. The collection's `order` in
`navigation.toml` determines article order. `[article_collections]` can
place an article in one different collection without changing its type.
The local outline is generated separately from each page's H2/H3 headings.

After a navigation change, rebuild the site and run the browser check:

```sh
cd test/browser
npm ci
npx playwright install chromium
npm test
```

It starts a loopback server and Chromium against the built site, including a
project URL prefix. Screenshots are written under
`test/browser/test-results/documentation/`. Check the images and try the
changed routes:

- Follow topic titles and expansion arrows separately; check focus and the
  current article after arriving through a link or directly.
- Open several branches, navigate and confirm that expansion and scrolling
  are retained. Repeat with JavaScript disabled and storage unavailable.
- Follow the local outline, search results and the contributor footer link.
- Check narrow layouts and both themes for clipped text, controls or overflow.

Library live viewers have their own
[browser tests](https://github.com/erikmnovak/TamerOp.jl/blob/main/test/browser/README.md).
The website navigation check exercises the website shell.

## Maintain the reading map

The map introduction lives in `src/reading_map.md`; its nodes and arrows live
in `reading_map.toml`. Nodes own their titles, questions, source paths and
`next`/`alternate` continuations. The publisher verifies that lesson endings
link to those destinations in order, and uses them for the lesson footer.
Sidebar order and topic membership do not change these reading routes.

Focused diagrams use `[[views]]`. Keep only node IDs and positions in a view's
`placements`, and assign drawn edges with `view = "ID"`.
`display = "focused"` keeps a lesson out of the overview;
`display = "support"` places setup beside a lesson;
`display = "reference"` keeps a node in the outline without a diagram card.
Optional edges use `kind = "optional"` and a label.

The renderer checks destinations, duplicate nodes and edges, cycles across all
views, and overlapping or out of bounds cards. Review the diagram and linked
outline together: check arrows, line wrapping, keyboard focus, narrow-screen
scrolling and light/dark themes. Follow changed continuations in the actual
lessons. The same node should resolve to the same article in every view.

## Notebook figures and optional sections

Give each figure output alternative text in its cell's `tamerop.figure_alt`
metadata. `tamerop.figure_caption` adds a visible plain-text caption. Both
accept a string for one figure or a list in output order; supplied captions
must be nonempty. Captions escape HTML and preserve literal interval brackets.

For a contiguous optional section, mark every cell with the same value:

```json
{"tamerop": {"optional_section": "Optional: Prepare a figure for sharing"}}
```

The first Markdown cell supplies its heading and explanation. The site wraps
the group in an initially closed disclosure, while the executed download keeps
all cells and outputs. All code cells still run during publication. Later
required cells should also work when optional cells are omitted; use a focused
executor's `--main-path` mode where available to check that independence.

If figure labels need more space, set `tamerop.figure_min_width` to a positive
integer width in CSS pixels, or a list of widths in output order. The figure
receives a scrollable region with keyboard focus while its caption stays within
the page. Check the actual labels before setting a minimum width.

Live WGLMakie demonstrations can appear as Julia fences in Markdown cells for
readers to run in their own Julia session. These fences are not executed by
the publication build. Executable optional cells are executed, so optional
metadata cannot be used to skip a live widget. Review both disclosure states,
keyboard use and the complete notebook download.

## Publish prepared examples and downloads

Save exported files under `tamerop_outputs` in the notebook's working directory.
The build copies them to `downloads/figures/<notebook name>/`. Declare public
files in the notebook metadata:

```json
{"tamerop": {"public_outputs": [
  {"path": "square/views.html", "label": "Compare the square selections",
   "embed": true, "height": 800},
  {"path": "square/data.json", "label": "Download the encoding to reopen in Julia"}
]}}
```

Add `tamerop.show_outputs`, containing the relevant paths, to the cell after
which each output belongs. Embedded HTML receives a titled frame; its height
defaults to 720 CSS pixels. A nonembedded HTML file receives a link, and other
files receive download links. Every declared output needs a `show_outputs`
entrance.

For a native saved visual session, the publisher creates a lesson viewer with
its title, caption, selection control, Previous and Next buttons, and figure.
It omits raw selection and type records, serialized values, export buttons
and saved-state links. Ordinary HTML compositions are copied unchanged.
Standalone figure pages do not receive the article sidebar. Embedded frames
allow scripts without access to the parent page.

The publisher rejects missing, empty or oversized files and records their
sizes and hashes. It preserves the original executed exports and records
separate hashes for transformed website copies. Review exported viewers with
the producing Julia process stopped and networking disabled, including
selections, labels, keyboard use and narrow layouts.

## Focused example checks

The executors in `docs/build_scripts/` run the canonical examples directly.
Choose the one for the guide you changed. For example:

```sh
julia --startup-file=no --threads=1 --project=docs/.build/environment docs/build_scripts/check_live_inspection.jl
```

For executors that provide them, `--record` writes the execution outputs into
the source notebook, `--gallery=PATH` saves figures and a review page,
`--recipe` checks the related Markdown recipe, and `--main-path` skips optional
cells. Use a path such as `docs/.build/live-inspection-preview` for a gallery.
Do not combine `--record` with `--main-path`: a partial execution must not
replace the complete notebook's outputs. Review the notebook diff after recording.

| Executor | Example and useful review checks | Options |
| --- | --- | --- |
| `render_spaces_maps.jl` | Static Julia blocks in `spaces_and_maps.md`: dimensions, comparable and incomparable parameters, induced map equations and the two exported figures. | Writes figures to `docs/assets/guides/`. |
| `check_resolution_views.jl` | Resolution multiplicities, selected incidence, equations, support and grades. | `--record`, `--gallery=PATH` |
| `check_signed_views.jl` | Chain intervals, signed rank queries, Hilbert atoms and interval-family ranks; compare cancellation and reconstructed values. | `--record`, `--gallery=PATH` |
| `check_ordinary_analysis.jl` | Public diagram API, hand-derived values and saving/reopening results; executes code cells in source order. | `--record` |
| `check_exact_matching.jl` | The rectangle example in `exact_matching.md`, its bound and optimizing line. | `--render` refreshes the displayed SVG. |
| `check_complexes.jl` | Selected classes and maps, a cone connecting map, spectral pages and their associated graded limit. | `--record`, `--gallery=PATH` |
| `check_source_cells.jl` | Cycles, fillings, cocycles and source memberships; inspect signs, periodic identifications, omitted cells, 3D skeletons and component histories before and at a merge. | `--record`, `--gallery=PATH` |
| `check_compare_encodings.jl` | Refinement, transport and recovered maps over the declared finite base. | `--record`, `--gallery=PATH` |
| `check_generated_submodules.jl` | Propagation of selected vectors and submodules, including their maps in source coordinates. | `--record`, `--gallery=PATH` |
| `check_derived.jl` | Ext and Tor products, representatives and displayed products. | `--record`, `--gallery=PATH`, `--main-path` |
| `check_compose_figures.jl` | Named endpoints after reordering/resizing, shared scalar ranges and annotations; inspect exported HTML and its textual annotation list. | `--record`, `--gallery=PATH`, `--main-path` |
| `check_comparisons.jl` | Fields, degrees, bases, unknown versus zero queries, rounding and tolerance; collections of supplied features and distances. | `--record`, `--gallery=PATH`, `--main-path` |
| `check_multicover.jl` | Geometric construction, radius and depth, source membership and the relationship between the models. | `--record`, `--gallery=PATH`, `--main-path` |
| `check_live_inspection.jl` | Finite encoding and ordinary persistence sessions; retain and reopen the actual JSON/HTML exports. | `--record`, `--gallery=PATH`, `--main-path`, `--recipe` |
| `check_presentations.jl` | Finite module construction, path witnesses and the generated Julia construction; inspect the saved draft and exported construction. | `--record`, `--gallery=PATH`, `--main-path`, `--recipe` |
| `check_relative_pair.jl` | Boundary recipe, quotient bases, displayed barcode and diagram conclusions. | Run without options. |
| `check_decomposition.jl` | Interval summands, retraction and reconstruction, branching residuals, classifier supports and Hom tables. | `--record`, `--gallery=PATH`, `--main-path` |
| `check_generalized_rank.jl` | Fork, signed star, repeated boundary path and continuous quadrant queries. | `--record`, `--gallery=PATH`, `--main-path`, `--recipe` |

For the ring and square lessons, the publication build runs their assertions:
the ring's finite intervals and essential component, and the square's closed
support, map dimensions and zero composite. Inspect the included birth and
excluded death, fixed axes across compared images, pixel borders and small
interval labels. Check optional sections both open and closed and confirm
the required computation works without them. Library tests for these drawing
contracts are described in the
[testing guide](https://github.com/erikmnovak/TamerOp.jl/blob/main/test/README.md).

Focused execution checks the examples; the publication build checks their
pages and downloads, including the matching witness recipe in
`tutorials/distance_witness.ipynb`. For live controls, use the library's
[browser guide](https://github.com/erikmnovak/TamerOp.jl/blob/main/test/browser/README.md),
including tests in a particular notebook host when claiming support for that
host. The [display guide](visualization.md#choose-a-display) explains the choices
for readers.

## Benchmark result pages

Reports live under `docs/benchmarks/`, with article records and publication
routes like other pages. Runnable studies and versioned evidence belong to
[TamerOp-benchmarks](https://github.com/erikmnovak/TamerOp-benchmarks#readme).
The website's measurement files remain exact copies of that evidence.

The [figure tooling guide](build_scripts/BENCHMARK_FIGURES.md) explains the shared
plotting preset, renderer, exports and presentation checksums. A plotting change
redraws the existing measurements. Keep archived data and checksum-covered
READMEs unchanged, and edit the separate authored data dictionaries to improve
their explanations. Review the report and its dictionary together. Reproduction
links identify a benchmark commit or release.

## Publish on GitHub Pages

The [Documentation workflow](../.github/workflows/Documentation.yml) checks out
the website and current library `main`, records both revisions, and builds
against those exact checkouts. Pushes and pull requests build a
`teaching-site` review artifact. Only successful trusted website `main`
builds deploy. A scheduled check twice an hour rebuilds when the published
revision differs from either repository; schedules can be delayed by GitHub.
The workflow also supports **Run workflow** for a requested rebuild.

GitHub Pages must use **GitHub Actions** under **Settings → Pages**.
The deployment job uses GitHub's short-lived workflow token and the
`github-pages` environment, publishing only `docs/build`. The custom domain
is configured there as `tamerop.com`; no personal token or SSH key is required.
Pages artifacts are retained for seven days. A failed deployment can be retried
within that period; afterward, build a fresh artifact.

Before merging a website change, review the rendered output from the proposed
sources. An accepted prototype must be incorporated into those sources so the
ordinary build produces the reviewed result. After deployment, compare
`downloads/publication.json` with the intended revisions and inspect the
changed pages, navigation, figures and downloads on the live site.

Public builds require the tracked website files and the selected library
checkout. Local audits and private references are not build inputs.
