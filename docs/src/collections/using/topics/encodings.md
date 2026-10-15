# Finite descriptions and parameter queries

A finite encoding lets us investigate a module over a large parameter domain
through finitely many vector spaces and maps. It includes the assignment from
original parameters to finite labels, so a query still refers to the domain
in which the problem was posed. [From inputs to computed objects](../../../../tutorials/inputs_to_objects.ipynb)
introduces that common destination using a filtration and a geometric
presentation as two ways to arrive there.

When the module itself is the input, a filtration may have no role in the
question. [Constructing modules without a filtration](../../../../tutorials/presentations.ipynb)
develops finite diagrams, lattice presentations and presentations by regions
and a coefficient matrix. It helps you choose a description that expresses the
spaces, maps and boundaries you intend, then check it before doing algebra.

With an object in hand, [exploring spaces and maps](../../../../spaces_and_maps.md)
connects parameter queries to finite labels and matrices. It is a good place
to begin reading an encoding: ask for a dimension, choose a comparable pair,
and interpret the map between the corresponding spaces. A zero map and the
absence of a prescribed map answer different questions, so the examples keep
that distinction visible.

Some answers are already retained, while others require further computation.
[Inspection and explicit computation](../../../../lazy_inspection.md) explains how to
recognize the difference and reuse work across repeated queries. This becomes
especially helpful when an initial dimension query leads you to request bases,
representatives or a larger batch of related answers.

Eventually we may want to compare two descriptions, restrict the parameters,
or move a module along an order-preserving map. [Refining and transporting
encoded modules](../../../../tutorials/compare_encodings.ipynb) follows the actual comparison maps
needed for those operations. It separates changing a finite description of the
same ambient module from changing the parameter base and therefore the object
being investigated. Start here when that change of description is your question;
the earlier guides remain available for the space and map queries used to
inspect the result.
