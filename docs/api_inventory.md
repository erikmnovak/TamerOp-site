# Maintaining the API inventory

The [runtime inventory](api_inventory.toml) records the bindings found when
TamerOp is loaded. The [coverage manifest](api_coverage.toml) assigns those
bindings to reference families and records their examples and review state.
For example, several names can refer to one function, while two functions with
the same short name can be different objects. The inventory preserves that
distinction so the documentation can identify which operation it explains.

## Reproduce the inventory

Prepare the [website environment](README.md#prepare-the-tools), then run these
commands from the website root. They use the selected TamerOp checkout:

```sh
julia --startup-file=no --project=docs/.build/environment docs/build_scripts/api_inventory.jl
julia --startup-file=no --project=docs/.build/environment docs/build_scripts/api_inventory.jl --check
julia --startup-file=no docs/build_scripts/check_api_coverage.jl
```

The first command updates the tracked snapshot. The second reloads the package
and compares it with that snapshot, including the Julia version. Changing the
Julia patch version therefore requires a reviewed regeneration. The last
command checks the coverage assignments and referenced files from TOML,
without loading TamerOp.

The generator uses ordinary `import TamerOp`. Its source fingerprints cover
`Project.toml`, Julia files under `src/` and `ext/`, and the generator.
They omit timestamps, checkout paths and Git commits. Optional integrations
are not deliberately activated; any extensions loaded through dependencies
are recorded.

## Read the runtime records

| Record or field | Meaning |
| --- | --- |
| `objects` | Functions, types and modules grouped by runtime object identity. Scalar constants keep separate bindings even when their values compare equal. |
| `canonical_binding` | A stable qualified name used to identify an object in the documentation. |
| `aliases` | Other names that refer to the same runtime object. |
| Defining module, declaration owners and tiers | Where an object is defined, where the public interface declares it and how callers reach it. |
| Per-binding metadata and docstring presence | Observations about each name, including whether documentation is attached. |
| `owner_candidates` | Additional names found in owner modules for which public intent needs review. |
| Reconciliation records | Disagreements between declared names and the runtime objects, including collisions. |

`DataFileIO.artifact` and `Featurizers.artifact`, for example, are distinct
objects. Aliases of one generic function share an identity, but its different
method families can need different explanations. A docstring flag records
presence; review the actual methods, assumptions, outputs and errors when
deciding whether the reference is complete.

The candidate scan includes local functions, types and modules whose names do
not start with an underscore, together with documented or explicitly public
bindings. It includes aliases from an owner's own child modules and omits
unrelated imports. Selection as public API is recorded in the coverage manifest.

## Read the coverage manifest

| Entry | What to maintain |
| --- | --- |
| `families` | Family identity and question, owner modules, reference pages, guides and example sources. |
| `reference_status`, `example_status`, `review_status` | Separate statements about authored reference material, examples and semantic review. |
| `overrides` | Explicit assignment of a binding to a family when owner-based routing is insufficient. |
| `qualified_apis` | Selected operations used through qualified names, with a reason, evidence and family. |
| `first_path` | The introductory reference subset and its examples. |
| `backlog` | Specific reference work still required for the family. |

The routing order is an explicit override, then the canonical owner, then the
declaration owner. Every intended public object needs one unambiguous family.
A planned reference path may be absent while its `reference_status` is
`backlog`; guide and example paths must exist. Paths beginning with `src/`,
`ext/` or `test/` resolve in the selected library checkout, while website
paths resolve here. The checker uses `TAMEROP_SOURCE` or the adjacent
TamerOp.jl checkout.

## Update coverage after a change

Read the affected method families and their current reference before editing
the assignments. Explain their mathematical purpose, inputs, returned values,
field and domain assumptions, meaningful errors and relevant costs. Link a
working example. Shared operations should have one canonical contract, with
links from other contexts.

Record authored material, execution and review in their respective fields.
Regenerate the runtime inventory after an API change, inspect the diff and run
both checks. Review added exports, candidates and collisions as interface
questions; binding counts alone cannot establish that a reference explains
its methods.

The [article catalog](article_inventory.md) gives each reference page its
article identity and source. Update it when adding or changing a reference
destination, then check the rendered API links through the ordinary site build.
