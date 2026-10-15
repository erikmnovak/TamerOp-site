```@raw html
<link rel="stylesheet" href="../assets/using_overview.css">
<section class="using-overview" aria-labelledby="using-tamerop">
```

# [Using TamerOp](@id using-tamerop)

```@raw html
  <div class="using-introduction">
```

We can begin with points, images or a growing geometric space, or with vector
spaces and maps that describe a module. A **finite encoding** gives us a common
way to work with these objects: finitely many ordered labels, the vector spaces
and maps on those labels, and an assignment from the original parameters to
the labels.

Once we have a finite encoding, we can follow vectors through it, compare its
behavior along different directions, or extract numbers for a data analysis.
The guides below develop these possibilities, starting with the question you
want to explore.

```@raw html
  </div>

  <figure class="using-map" aria-labelledby="using-map-title" aria-describedby="using-map-caption">
    <div class="using-map-top">
      <h2 id="using-map-title">Many starting points, a finite encoding, many questions</h2>
      <p>Each topic opens its guides. You can also follow a starting point through the diagram.</p>
      <div class="using-route-controls" role="group" aria-label="Highlight a starting point" hidden>
        <button type="button" data-route="all" aria-pressed="true">The whole picture</button>
        <button type="button" data-route="data" aria-pressed="false">I have data</button>
        <button type="button" data-route="module" aria-pressed="false">I have spaces and maps</button>
        <button type="button" data-route="barcode" aria-pressed="false">I want a barcode</button>
      </div>
      <p class="using-route-explanation" aria-live="polite" aria-atomic="true">Choose how to describe your input, build a finite encoding, and explore the questions it makes accessible. Visualization, saving and arithmetic accompany the computation throughout.</p>
    </div>

    <div class="using-flow">
      <svg class="using-connections" aria-hidden="true" focusable="false"></svg>
      <section class="using-inputs using-lane" aria-labelledby="using-inputs-title">
        <h3 id="using-inputs-title"><span>Before the finite encoding</span>Choose an input</h3>
        <a class="using-topic using-geometry" href="using/topics/geometry.html" data-node="geometry">
          <svg class="using-sketch" viewBox="0 0 100 42" aria-hidden="true" focusable="false"><g fill="currentColor" opacity=".12"><circle cx="25" cy="23" r="17"/><circle cx="48" cy="14" r="17"/><circle cx="69" cy="27" r="17"/></g><g stroke="currentColor" stroke-width="1.5" fill="none"><circle cx="25" cy="23" r="17"/><circle cx="48" cy="14" r="17"/><circle cx="69" cy="27" r="17"/></g><g fill="currentColor"><circle cx="25" cy="23" r="2.8"/><circle cx="48" cy="14" r="2.8"/><circle cx="69" cy="27" r="2.8"/></g></svg>
          <strong>Geometric inputs and filtrations</strong>
          <span>Choose how points, images or graphs become a growing family of spaces.</span>
        </a>
        <a class="using-topic using-persistence" href="using/topics/persistence.html" data-node="persistence">
          <svg class="using-sketch" viewBox="0 0 100 42" aria-hidden="true" focusable="false"><g stroke="currentColor" stroke-width="2" fill="none"><path d="M10 30L24 7L38 30Z"/><path d="M60 30L74 7L88 30Z" fill="currentColor" fill-opacity=".15"/><path d="M43 20H55m-5-4 5 4-5 4"/></g></svg>
          <strong>Persistence and filtered complexes</strong>
          <span>Follow holes as a space grows, and find the cells that explain a persistent class.</span>
          <span class="using-barcode"><svg viewBox="0 0 82 30" aria-hidden="true" focusable="false"><path d="M3 5H77M12 15H49M29 25H67" stroke="currentColor" stroke-width="3"/></svg><span>One parameter can lead directly to a barcode.</span></span>
        </a>
        <div class="using-direct" data-node="direct">
          <strong>You can supply the algebra directly.</strong>
          <span>Start with a diagram of spaces and maps, or a presentation describing a module through generators and relations.</span>
        </div>
      </section>

      <div class="using-transition using-transition-in" aria-hidden="true"><span>encode</span><b>→</b></div>

      <section class="using-encoding-lane using-lane" aria-labelledby="using-encoding-title">
        <h3 id="using-encoding-title"><span>The common object</span>Build a finite encoding</h3>
        <div class="using-encoding-body">
          <a class="using-topic using-encoding" href="using/topics/encodings.html" data-node="encodings">
            <span class="using-central-name">Finite encoding</span>
            <svg class="using-encoding-sketch" viewBox="0 0 260 174" role="img" aria-labelledby="encoding-sketch-title encoding-sketch-desc">
              <title id="encoding-sketch-title">Parameters assigned to finite labels</title>
              <desc id="encoding-sketch-desc">A parameter plane is divided into four regions A, B, C and D. These correspond to four labels ordered in a diamond. A chosen parameter q in region B is assigned to label B. Each finite label carries a vector space, and the order carries linear maps.</desc>
              <defs><marker id="using-lookup-tip" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0L8 4L0 8Z" fill="currentColor"/></marker></defs>
              <text x="55" y="17" text-anchor="middle" class="using-diagram-heading">Parameters</text>
              <text x="198" y="17" text-anchor="middle" class="using-diagram-heading">Finite labels</text>
              <g transform="translate(0 12)">
              <g class="using-regions">
                <path d="M12 82H55V125H12Z" class="using-region-a"/>
                <path d="M55 82H98V125H55Z" class="using-region-b"/>
                <path d="M12 39H55V82H12Z" class="using-region-c"/>
                <path d="M55 39H98V82H55Z" class="using-region-d"/>
              </g>
              <path d="M12 34V125H104" class="using-coordinate-axes"/>
              <g class="using-region-labels"><text x="26" y="112">A</text><text x="76" y="112">B</text><text x="26" y="61">C</text><text x="76" y="61">D</text></g>
              <g class="using-order-arrows" marker-end="url(#using-lookup-tip)"><path d="M190 118L166 92"/><path d="M206 118L230 92"/><path d="M166 70L190 44"/><path d="M230 70L206 44"/></g>
              <g class="using-finite-labels"><circle cx="198" cy="130" r="14" class="using-region-a"/><circle cx="157" cy="81" r="14" class="using-region-b"/><circle cx="239" cy="81" r="14" class="using-region-c"/><circle cx="198" cy="32" r="14" class="using-region-d"/><text x="198" y="136">A</text><text x="157" y="87">B</text><text x="239" y="87">C</text><text x="198" y="38">D</text></g>
              <path d="M70 95Q110 59 142 80" class="using-lookup" marker-end="url(#using-lookup-tip)"/>
              <circle cx="70" cy="95" r="3.5" class="using-parameter"/><text x="57" y="92" class="using-parameter-label">q</text>
              </g>
            </svg>
            <span class="using-encoding-definition">A parameter selects a label. Each label has a vector space, and the arrows carry linear maps.</span>
            <strong>Finite descriptions and parameter queries</strong>
            <span>Construct the finite encoding, recover spaces and maps, and compare different finite encodings.</span>
          </a>
          <p class="using-encoding-note">The assignment of parameters to labels lets us interpret the finite encoding back on the original parameter space.</p>
        </div>
      </section>

      <div class="using-transition using-transition-out" aria-hidden="true"><span>explore</span><b>→</b></div>

      <section class="using-questions using-lane" aria-labelledby="using-questions-title">
        <h3 id="using-questions-title"><span>With the finite encoding</span>Choose a question</h3>
        <a class="using-topic using-algebra" href="using/topics/algebra.html" data-node="algebra">
          <svg class="using-sketch" viewBox="0 0 100 42" aria-hidden="true" focusable="false"><g fill="none" stroke="currentColor" stroke-width="1.8"><ellipse cx="20" cy="22" rx="15" ry="12"/><ellipse cx="76" cy="22" rx="19" ry="15"/><path d="M20 22Q45 3 76 22m-7-2 7 2-3-7"/></g><circle cx="20" cy="22" r="3" fill="currentColor"/><circle cx="76" cy="22" r="3" fill="currentColor"/></svg>
          <strong>Modules, maps and derived algebra</strong>
          <span>Follow vectors, construct submodules and quotients, and investigate how modules fit together.</span>
        </a>
        <a class="using-topic using-invariants" href="using/topics/invariants.html" data-node="invariants">
          <svg class="using-sketch" viewBox="0 0 100 42" aria-hidden="true" focusable="false"><path d="M7 36V5M7 36H43M9 32L40 7" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M53 9H94M62 21H84M58 33H99" stroke="currentColor" stroke-width="3"/></svg>
          <strong>Invariants, slices and distances</strong>
          <span>Examine persistence along a line, measure agreement across a region, or compare two modules.</span>
        </a>
        <a class="using-topic using-features" href="using/topics/features.html" data-node="features">
          <svg class="using-sketch" viewBox="0 0 100 42" aria-hidden="true" focusable="false"><path d="M5 35L26 11L47 35L64 17L84 35H96" fill="none" stroke="currentColor" stroke-width="2"/><g fill="currentColor"><circle cx="17" cy="21" r="3"/><circle cx="37" cy="24" r="3"/><circle cx="64" cy="17" r="3"/></g></svg>
          <strong>Features and data analysis</strong>
          <span>Turn persistence results into comparable numerical features and study how repeated results vary.</span>
        </a>
      </section>
    </div>

    <section class="using-companions" aria-labelledby="using-companions-title">
      <h3 id="using-companions-title">Along the way</h3>
      <p>These choices accompany the inputs, the finite encoding and the answers we obtain from it.</p>
      <div class="using-companion-topics">
        <a class="using-topic using-visualization" href="using/topics/visualization.html" data-node="visualization"><span class="using-companion-verb">See what the computation means</span><strong>Visualization and interaction</strong><span>Inspect parameters, maps and selected classes in linked views.</span></a>
        <a class="using-topic using-data-io" href="using/topics/data_io.html" data-node="data_io"><span class="using-companion-verb">Keep what you need</span><strong>Data, saving and interchange</strong><span>Bring data in, save a finite encoding, and return to its spaces and maps later.</span></a>
        <a class="using-topic using-arithmetic" href="using/topics/arithmetic.html" data-node="arithmetic"><span class="using-companion-verb">Choose the arithmetic</span><strong>Fields, grades and numerical arithmetic</strong><span>Choose coefficients, interpret parameter values and understand numerical tolerances.</span></a>
      </div>
    </section>
    <figcaption id="using-map-caption">The arrows lead from an input to a finite encoding, then branch into questions we can ask of that finite encoding. Algebra, invariants and features are different directions to explore. The small drawings illustrate the objects and questions along the way.</figcaption>
  </figure>
</section>
<script src="../assets/using_overview.js"></script>
```
