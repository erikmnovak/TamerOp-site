# Features and data analysis

To compare many persistence results, we often turn each one into numbers
indexed by common coordinates. The choice of coordinates, window and
normalization determines what those numbers mean. [Reading scalar fields in
their original coordinates](../../../../tutorials/features.ipynb) starts with that
interpretation: inspect a landscape layer or a section of a higher-dimensional
field, then assemble values whose coordinates remain explicit. A feature
vector is useful because of the information it retains, which also makes its
losses part of the explanation.

Repeated computations introduce a second question: how do their answers vary?
[Analyzing ensembles of persistence results](../../../../tutorials/uncertainty.ipynb)
aligns the coordinates and features before summarizing replicates. An ensemble
here is a collection of repeated results with a stated relationship to the
experiment. The guide separates descriptive variation from confidence claims,
whose meaning depends on the sampling assumptions and whether a statement
concerns one point or an entire domain.

Sometimes we want the locations at which we measure a feature to adapt to a
task. For the generalized rank invariant landscape, or GRIL, a probe
specifies where and how the landscape is queried. [Region queries and GRIL
features](../../../../tutorials/generalized_rank_queries.ipynb) explain the quantities from which
such features are built. Adapting probes to a task then introduces choices
about the training objective, the parameters that may vary and which data
remain separate for evaluation. A change in the underlying discrete structure
can require different reasoning from a small change in a continuous parameter.

If your immediate task is to inspect a supplied feature table, distance table
or embedding, [comparing results through declared
correspondences](../../../../tutorials/comparisons.ipynb) provides the adjoining route.
It makes the sample identities and coordinate correspondence explicit before
using shared scales. A visual grouping can then be traced to the values that
produced it, without treating the drawing as a new mathematical guarantee.
