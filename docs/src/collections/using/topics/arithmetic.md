# Fields, grades and numerical arithmetic

There are several places where arithmetic enters a persistence computation.
The coefficient field belongs to the vector spaces and maps; parameter grades
describe when objects enter; numerical tolerances decide how a floating-point
calculation treats nearly dependent vectors. Consider a differential given
by multiplication by two. Over the rational numbers it has zero kernel; over
the field with two elements it is the zero map. Changing the field can change
the answer, while changing a basis within one field does not.

The [guide to comparing results](../../../../tutorials/comparisons.ipynb) puts coefficient
choices beside changes of basis and input construction. It connects each
comparison to the spaces and maps being compared, so a shared plot has a
mathematical interpretation. Coefficient arithmetic belongs to those spaces
and maps; geometric distances and parameter grades have their own arithmetic.

[Numerical derived algebra](../../../../numerical_algebra.md) examines what happens
when rank and related calculations use numerical tolerances. A singular value
near a threshold can change the reported rank and therefore a later algebraic
answer. The guide helps you inspect that choice, distinguish a small residual
from an exact identity and decide what evidence the computation provides.

For parameter coordinates, [exact rhomboid grades](../../../../exact_grades.md)
supplies a complementary example. Two distinct events can have the same
displayed floating-point coordinate. Keeping their grades exact preserves the
membership query even though the picture rounds them to one location. This
is why the word “exact” needs an object: exact coefficients, exact grades and
an exact optimization answer describe different parts of a calculation.
