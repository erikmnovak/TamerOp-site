# Persistence and filtered complexes

A filtration orders the stages of a growing space. Persistent homology follows
its homology classes through those stages, and a barcode records the intervals
over which they persist. [Ordinary persistent homology](../../../../ordinary_persistence.md)
is the natural starting point when one changing parameter and its intervals
answer your question. It connects the input construction to the returned
intervals, coefficient choices and retained information.

An interval alone does not tell us which cells form a representative of its
class. [From source cells to representative classes](../../../../tutorials/source_cells.ipynb)
follows that correspondence back to the input. It distinguishes a cycle,
whose boundary is zero, from a chain filling that cycle at its death, and from
a cocycle, a linear assignment of values to chains that vanishes on boundaries.
Read it when you want to point to the part of
the source that explains a selected result, or decide what information to
retain during the computation.

A cocycle can also be the starting point for coordinates on the data.
One circular coordinate assigns each point an angle; several circular
coordinates together give a map to a torus.
The coefficient field, chosen scale and lift to the arithmetic used by the
coordinate solver matter here. A colored picture of the result is useful only
after we know which source points the coordinates describe.

Cohomology has multiplication as well as vector spaces. We can ask how
classes multiply and how those products behave as the parameter changes.
Computing with supplied compatible multiplication data and constructing those
products from cochains begin with different information. This is a
different investigation from choosing coordinates, although both benefit
from understanding the retained cocycles and their classes.

If cells can disappear as time passes, the input is no longer simply a growing
filtration. A zigzag is a sequence in which consecutive maps may point in
either direction. Its intervals describe persistence through those changes.
Reusing an earlier reduction after an edit concerns how we compute an answer;
the zigzag determines the mathematical question we are answering.
Correspondence between displayed classes then needs actual maps or certified
update information; matching similar-looking intervals alone does not supply it.
