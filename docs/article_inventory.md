# Maintaining the article inventory

[article_inventory.toml](article_inventory.toml) records each article's identity,
reader question, scope, type, topics and canonical source. The build combines
these records with publication routes and navigation settings to create
collections, topic pages and search labels. Use this guide when changing those
records; [CONTRIBUTING.md](../CONTRIBUTING.md) explains how to propose teaching
material.

A notebook has one article record. Its website page and executed download
are generated forms of that article. Supporting maps, data dictionaries and
repository instructions use the `resource` type.

## Read a record

| Field | Meaning |
| --- | --- |
| `id` | Stable article identity. Titles and source paths can change without changing this ID. Older B and C identities are retained for existing records; new IDs can describe the subject. |
| `title` | The article heading or proposed heading. |
| `type` | `lesson`, `library_guide`, `recipe`, `api_reference`, `implementation_account`, `benchmark_report`, `contributor_guide`, or `resource`. These describe the article's purpose. |
| `topics` | Subject IDs from `[topics]`. The first gives the article its home topic; additional topics support discovery. Topic membership does not create a reading prerequisite. |
| `question` | The reader question the article answers. |
| `state` | `existing` when a canonical source exists, otherwise `planned`. Publication is controlled separately. |
| `source` | The existing canonical path relative to this repository, or `library:` followed by a path in the selected library checkout. It must exist and belong to only one record. Planned records have no `source`. |
| `planned_source` | An optional intended path. It need not exist. |
| `scope` | Content and boundaries of the article, including the hypotheses or algorithm needed for a proposed account. |
| `plan_ids` | Optional historical identifiers for related work. The record must remain understandable without that work's private records. |
| `related` | Related article IDs. These associations need not be reciprocal and do not set reading order. |
| `migration` | `retain`, `review`, `split`, or `author`, describing the intended treatment of the source. |
| `migration_note` | Optional explanation of that treatment, used during maintenance. |

An `existing` source can still need review or execution. Likewise, a planned
article can explain software that already exists. Check the relevant source
and tests when making an implementation claim.

## Keep metadata with its owner

| File | What it controls |
| --- | --- |
| [article_inventory.toml](article_inventory.toml) | Article identities, scopes, sources, topics and intended revisions. |
| [publication.toml](publication.toml) | Source to site routes, notebook execution and downloads. |
| [navigation.toml](navigation.toml) | Collection labels, placement, grouping and display order. |
| [reading_map.toml](reading_map.toml) | Learning map nodes, suggested continuations and lesson footer links. |
| [api_coverage.toml](api_coverage.toml) | API family assignments, reference destinations, examples and method review. |
| [api_inventory.toml](api_inventory.toml) | Generated observations of bindings and runtime object identities; see the [API guide](api_inventory.md). |

The catalog builder uses existing sources with published destinations for public
listings. Planned entries do not create empty pages. Each article has one
canonical source and destination, even when the topic map relates it to several
subjects.

The six collections are Mathematics, Using TamerOp, Task recipes, API reference,
Implementation and Benchmarks. Contributor instructions have a sidebar footer
entrance. A collection's default membership comes from article type;
`[article_collections]` in `navigation.toml` can assign an article a different
single home. See [navigation maintenance](README.md#maintain-site-navigation)
for configuration and browser checks.

## Add, revise or remove a record

Look for an existing record that answers the same reader question before adding
one. A planned record needs a coherent scope. Once its source is authored, set
`state = "existing"`, add `source` and remove `planned_source` if it repeats
that path. Publication routes are added when the article is ready to enter
the site.

If a revision splits an article, narrow the original record and add a record
for the separate question. If two records converge on one source, retain one
identity and update their incoming `related`, navigation and reading-route
references. When removing a page, remove its route and repair contextual links
as well as catalog references.

For a change to a question or scope, review the title, topics and related
articles together. Keep canonical source paths out of separate hand-maintained
lists in `make.jl` or navigation generators. Notebook outputs, generated HTML,
plotting assets, raw benchmark data and runtime inventories do not need
additional article records. A data dictionary does, because it is an authored
explanation of the data.

## Check the catalog without Julia

From the repository root, this checks record identities, source paths,
relationships, field values and API reference destinations:

```sh
python - <<'PY'
from pathlib import Path
import sys
import tomllib

sys.path.insert(0, "docs/build_scripts")
from source_paths import source_path

root = Path.cwd()
catalog = tomllib.loads((root / "docs/article_inventory.toml").read_text())
articles = catalog["articles"]
ids = {item["id"] for item in articles}
assert len(ids) == len(articles), "duplicate article ID"
sources = [item["source"] for item in articles if "source" in item]
assert len(set(sources)) == len(sources), "duplicate canonical source"
for item in articles:
    assert item["type"] in catalog["types"], item["id"]
    assert item["topics"] and set(item["topics"]) <= set(catalog["topics"])
    assert item["state"] in {"existing", "planned"}, item["id"]
    assert item["migration"] in {"retain", "review", "split", "author"}
    assert set(item.get("related", [])) <= ids, item["id"]
    assert ("source" in item) == (item["state"] == "existing"), item["id"]
    for key in ("source", "planned_source"):
        if key in item:
            path = Path(item[key])
            assert not path.is_absolute() and ".." not in path.parts, item["id"]
    if "source" in item:
        assert source_path(root, item["source"]).is_file(), item["source"]

coverage = tomllib.loads((root / "docs/api_coverage.toml").read_text())
targets = set(coverage["first_path"]["reference_pages"])
for family in coverage["families"]:
    targets.update(family["reference_pages"])
for target in targets:
    matches = [item for item in articles
               if target in (item.get("source"), item.get("planned_source"))]
    assert len(matches) == 1, (target, len(matches))
print("Article records and API reference destinations are consistent.")
PY
```

The [build checks](README.md#build-and-preview) additionally validate publication
routes and generated navigation. Inspect the changed listings, search results,
topic links and lesson continuations in the rendered site.
