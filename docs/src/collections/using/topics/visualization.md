# Visualization and interaction

A figure begins with a mathematical question. The parameter plane, a finite
poset drawing, a matrix and a barcode show different aspects of the same
calculation. [Choosing views and inspecting intervals](../../../../visualization.md)
helps you decide which of them makes the part you care about visible, and how
to read its coordinates and selections.

When one choice should be followed across several views, [keeping a selected
mathematical view](../../../../tutorials/live_inspection.ipynb) explains a session: the
retained object and selection that the views share. It follows parameter
queries, finite labels, closing and reopening, and distinguishes prepared
browser choices from fresh queries that require Julia. Use it when preserving
the meaning of a selection matters more than producing one final image.

Comparing different results requires an additional decision about what
corresponds. [Comparing results through declared
correspondences](../../../../tutorials/comparisons.ipynb) establishes that relationship before
sharing coordinates, colors or selections. Changes of basis, coefficient field
and construction have different mathematical effects.
Common scales can make those effects readable, but cannot supply a missing
identification between the objects.

Once the comparison is understood, [composing and sharing mathematical
figures](../../../../tutorials/compose_figures.ipynb) brings compatible layers and panels
together. It explains how to retain labels, scales and annotations when the
figure leaves the notebook. A saved drawing, a mathematical artifact and a
reopenable session preserve different things, so the guide helps choose the
one that supports what the recipient will want to do next.
