# Data, saving and interchange

The right saved representation depends on the computation you want to do
after loading it. Points, a finite encoding, a feature table and a drawing
contain different information. A drawing lets someone inspect a result; a
finite encoding keeps the spaces, maps and assignment of parameters to labels
available for further questions. [Keeping a selected mathematical
view](../../../../tutorials/live_inspection.ipynb) follows this choice through an encoding
and the parameter queries we want to recover.

For a small example, [save and reopen an interval view](../../../../recipes/reopen_session.md)
keeps a persistence interval together with its representative. A saved
selection identifies which interval we were examining. Retaining the
mathematical object as well lets us resume the supported inspector and ask
another question. The recipe makes this distinction visible by saving and
loading a ring whose hole has a known birth and death.

Sometimes the intended result is the figure itself. [Composing and sharing
mathematical figures](../../../../tutorials/compose_figures.ipynb) develops that route:
combine the relevant views and preserve the coordinates, labels and
annotations that make them readable. A feature table serves another purpose,
carrying numerical values into a subsequent analysis. [Optional
integrations](../../../../optional_integrations.md) explains how table, file and
rendering adapters connect these choices to the surrounding Julia environment.

Recovering a finite encoding means more than recovering its dimensions.
We also need its maps and the assignment from original parameters to finite
labels. Even when those data describe the same module, a reconstructed basis
may give a different matrix for the same map. The [account of serialization
and interchange](../../../../implementation/serialization.md) explains what the stored formats preserve and
how their checks relate to the mathematical object. It is the next place to
look when choosing between a saved result, exact matrix coordinates and an
object that supports new queries.
