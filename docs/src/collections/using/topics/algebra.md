# Modules, maps and derived algebra

Once a module's spaces and maps are available, we can ask algebraic questions
of the whole diagram. A morphism is a family of linear maps that commutes with
the structure maps. Its kernel tells us what it kills, its image what it
reaches, and its cokernel what remains after that image is quotiented out.
[Exploring spaces and maps](../../../../spaces_and_maps.md) gives us a concrete way
to read the spaces and structure maps before investigating these constructions.

For a more concrete starting question, choose a few vectors and follow them.
[Generated submodules](../../../../tutorials/generated_submodules.ipynb) shows how their
images form a submodule and how its inclusion and quotient relate to the
original module. This makes the algebra visible without asking for every map
between two objects. It also explains why a submodule need not have a
complement giving a decomposition as a direct sum.

[Interval multiplicities and splittings](../../../../tutorials/decomposition.ipynb) then
asks when pieces do form such a decomposition. An interval module carries
one copy of the coefficient field on its support, with the specified identity
maps there. Counting one proposed summand, searching a declared family and
producing actual splitting maps are different requests. The guide makes clear
which answer is complete on the chosen finite base and what a remaining
piece means.

To follow cycles, boundaries and maps between them, turn to [complexes and
spectral pages](../../../../tutorials/complexes.ipynb). A complex has differentials whose
successive compositions vanish; its homology records cycles modulo boundaries.
The examples develop these computations before using successive spectral
sequence pages to organize a more involved calculation. Page dimensions are
an economical first look when full representatives are unnecessary.

[Choosing and inspecting resolutions](../../../../tutorials/resolutions.ipynb) explains how
a module can be represented by a complex of specified simpler modules.
The choice of category and resolution family determines the question, while
degree ranges determine how much of the calculation is requested. Start with
the tables you need and then inspect terms and differentials when they help
explain an entry.

Those choices lead to [Ext, Tor and their products](../../../../tutorials/derived.ipynb).
Ext derives the Hom construction, while Tor derives the relevant tensor
construction; both depend on the category being used. The guide follows
dimensions, chosen classes and products through a finite example. It is the
right destination when those derived quantities are the goal, with the
resolution and complex guides available for the underlying computations.
