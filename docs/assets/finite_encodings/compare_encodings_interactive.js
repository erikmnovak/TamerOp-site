/* Authored finite-encoding schematic. The exact sample answers are in the
   option data; these controls choose among them without querying TamerOp. */
(() => {
    "use strict";
    const root = document.getElementById("encoding-label-explorer");
    if (!root) return;
    const chooser = root.querySelector("#encoding-parameter");
    const point = root.querySelector("#encoding-selected-point");
    const pointLabel = root.querySelector("#encoding-selected-point-label");
    const equation = root.querySelector("#encoding-lookup-equation");
    const explanation = root.querySelector("#encoding-lookup-explanation");
    const pair = value => `(${value[0]}, ${value[1]})`;

    function showSelection() {
        const option = chooser.selectedOptions[0];
        const { x, y, band, signature } = option.dataset;
        const px = 50 + (Number(x) + 2) * 44;
        const py = 302 - (Number(y) + 2) * 44;
        point.setAttribute("cx", px);
        point.setAttribute("cy", py);
        pointLabel.setAttribute("x", px + 9);
        pointLabel.setAttribute("y", py + 5);
        root.querySelectorAll(".encoding-region").forEach(region => {
            region.classList.toggle("encoding-same-signature", region.dataset.signature === signature);
        });
        root.querySelectorAll(".encoding-band").forEach(label => {
            label.classList.toggle("encoding-selected-band", label.dataset.band === band);
        });
        root.querySelectorAll(".encoding-node").forEach(node => {
            node.classList.toggle("encoding-selected-node", node.dataset.signature === signature);
        });
        equation.textContent = `q = (${x}, ${y}): π₉(q) = ${pair(band)}; ρ(π₉(q)) = ${pair(signature)} = π₄(q).`;
        const space = signature === "10" ? "the coefficient field 𝕜" : "the zero space";
        let detail;
        if (signature === "01") {
            detail = "The upper left and lower right pieces share this signature. Switching between them changes the band label while keeping the signature and recovered space.";
        } else if (signature === "10") {
            detail = option.dataset.boundary === "true"
                ? "The corner belongs to the closed square: coordinates equal to 0 or 2 remain in band C."
                : "The central band pair is exactly the closed square; only its signature carries a nonzero space.";
        } else {
            detail = "The shaded band regions share one signature. Their spaces are zero, while their labels retain how they lie relative to the square.";
        }
        explanation.textContent = `Both lookups recover ${space}. ${detail}`;
        root.dataset.selectedPoint = option.value;
    }

    chooser.addEventListener("change", showSelection);
    showSelection();
    chooser.disabled = false;
    root.dataset.ready = "true";
})();
