# Contributing to the TamerOp website

A correction, a worked example or a lesson can help someone understand a
mathematical idea that was difficult to approach before. Describe who the
material is for, what question it answers and how a reader can check the result.
For an unclear passage or a broken example, the page address and a description
of where you got stuck are useful starting points.

Use the shared [TamerOp.jl issue tracker](https://github.com/erikmnovak/TamerOp.jl/issues)
for problems and proposals, and
[Discussions](https://github.com/erikmnovak/TamerOp.jl/discussions) for questions
and mathematical ideas. Discuss a substantial new lesson or restructuring
before spending much time on it. Small corrections can go straight to a pull
request.

## Propose teaching material

Fork this repository, make your changes on a branch and open a pull request
here. Link the central issue when there is one. Include the intended audience,
the mathematical purpose and any background the reader needs. Provide runnable
examples and their expected results, cite mathematical and software sources,
and identify reused text, figures or data and their licenses.

Write explanations that help the reader follow the calculation. Define terms
when they first matter, label figures and describe what the reader should
notice. An interactive example is welcome when changing a selection helps
explain the mathematics. A contribution need not arrive with its final placement
or presentation: Erik Novak reviews the mathematical content and works with
contributors on its wording, figures and connections to the rest of the site.
Substantial changes to a contribution's meaning are discussed with its author,
and credit is retained when material is adapted or combined.

## Check the change

The [build guide](docs/README.md) explains setup and preview commands. Edit the
canonical Markdown or notebook rather than generated HTML. For a changed
notebook, execute its examples and check the displayed answers and figures.
For prose, navigation or layout changes, inspect the affected pages in the
preview, including links and a narrow browser window. The guide gives focused
checks for notebook examples and website tooling, so you can select the ones
relevant to the change.

In the pull request, explain the resulting improvement and say which checks
you ran. If you could not run a check, say which one and what prevented it.
Erik reviews and integrates contributions, settles their final presentation
and approves publication.

## Related projects

- For library code or an optimization, see
  [TamerOp.jl's contribution guide](https://github.com/erikmnovak/TamerOp.jl/blob/main/CONTRIBUTING.md).
- For a new comparison or measurements from another computer, see
  [TamerOp-benchmarks' contribution guide](https://github.com/erikmnovak/TamerOp-benchmarks/blob/main/CONTRIBUTING.md).

People interested in becoming a maintainer are welcome to email Erik at
[erikmendesnovak@gmail.com](mailto:erikmendesnovak@gmail.com).
