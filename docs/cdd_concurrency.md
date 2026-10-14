# Concurrent polyhedral computations

Several encodings can be constructed by separate Julia tasks, for example when
a collection of presentations will be compared later. Their surrounding work
may run concurrently, but TamerOp admits only one task at a time into CDD, the
library used for general polyhedral computations. This coordination is
automatic; you do not need to arrange the CDD calls yourself.

## Construct several presentations concurrently

Start Julia with more than one worker thread. For example, from a terminal in
the environment containing TamerOp:

```sh
julia --project=. --threads=2
```

We will construct three modules, each equal to $\mathbb Q$ on a closed interval
$[a,a+1]$ and zero outside it. The structure maps within the interval are
identities. An upset beginning at $a$, a downset ending at $a+1$, and the
coefficient matrix $[1]$ give this presentation, as explained in [Indicator
presentations](indicator_presentations.md).

Run the following in Julia:

```julia
import TamerOp as OP
import TamerOp.Advanced as A

starts = [0.0, 1.0, 2.0]
tasks = map(starts) do a
    Threads.@spawn begin
        ups = [A.BoxUpset([a])]
        downs = [A.BoxDownset([a + 1])]
        coefficients = fill(OP.QQ(1), 1, 1)
        options = A.EncodingOptions(backend=:pl, field=OP.CoreModules.QQField())
        OP.encode(ups, downs, coefficients, options; cache=nothing)
    end
end
encodings = fetch.(tasks)
```

`backend=:pl` deliberately selects the general polyhedral computation. These
particular intervals could also use the specialized box encoder, which avoids
CDD; the explicit choice makes the concurrency behavior under discussion part
of this example. Each task owns its input arrays and result, and
`cache=nothing` avoids sharing a session cache. `fetch` waits for each task and
propagates any failure; the collected encodings stay in the order of `starts`.

We can check the result by querying a point before, within and after each
interval:

```julia
observed = map(starts, encodings) do a, enc
    M = OP.encoding_module(enc)
    pi = OP.encoding_map(enc)
    [A.dim_at(M, A.locate(pi, (x,))) for x in (a - 1, a + 0.5, a + 2)]
end
@assert observed == [[0, 1, 0], [0, 1, 0], [0, 1, 0]]
```

The middle point lies inside the interval and the other two lie outside it.
These queries check the expected fibers after all tasks finish. The use of
several tasks does not alter the represented modules or their coefficient
field, and it does not promise a speedup: time spent in CDD is still
serialized.

## What is protected, and what remains your responsibility

The same internal lock protects exact rational and floating CDD operations
across PL geometry and incremental rhomboid construction. A lock lets one task
use this shared library while the others wait. Its protection includes delayed
conversions, construction of points and facets, incidence, volume and centroid
calculations. There is no option to disable it.

Incremental rhomboid construction copies facets into Julia data before
continuing outside the lock. Polyhedral caches may instead retain CDD
representations, so later TamerOp accesses to those representations are
protected too. When code also needs a session or region cache lock, it acquires
that lock before the CDD lock; code inside the CDD operation does not acquire
them in the opposite order. This ordering prevents those locks from waiting on
each other.

The protection covers calls made through TamerOp. An independent CDDLib call,
or a Polyhedra operation using CDD in another package, does not join this lock.
Run such external work in a separate process if it would overlap with TamerOp's
polyhedral computations. Keep CDD's solver, logging and arithmetic
configuration fixed after initialization.

Input arrays must remain unchanged while a task reads them. Likewise, finish
all users of a PL geometry cache before clearing it, and use the supported
query functions to access retained backend objects. Directly editing their
fields bypasses the coordination on which these guarantees depend.