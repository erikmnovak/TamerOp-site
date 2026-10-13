# Visualization support and acceptance

The [published support matrix](https://tamerop.com/contributing/visualization_support.html)
is generated from the selected library checkout. Its maintained data is
[`test/visualization_support.toml`](https://github.com/erikmnovak/TamerOp.jl/blob/main/test/visualization_support.toml).
The library validates the declared display paths and their assigned tests;
the website renders the explanation and table during publication.

To change a support claim, update that library manifest and its acceptance
evidence. To change the presentation, edit
[`build_scripts/visualization_support.py`](build_scripts/visualization_support.py).
A normal website build regenerates the page, so this repository does not keep
a second copy of the library's support data.
