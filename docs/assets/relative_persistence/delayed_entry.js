/* Authored schematic. check_relative_pair.jl checks these finite states
   against the canonical recipe's complex, field and delayed entry grades. */
(() => {
  "use strict";
  const root = document.getElementById("relative-pair-explorer");
  if (!root || root.dataset.initialized) return;
  root.dataset.initialized = "true";
  const states = [
    {"scale":0,"ambient":[10,20],"subcomplex":[],"quotient":[[10,20],[]],"boundary":[],"homology":[2,0],"explanation":"At zero K has two vertices and A is empty. Both vertex coordinates survive in the quotient. With no edge boundary to identify them, they give two classes in degree zero."},
    {"scale":1,"ambient":[10,20,30],"subcomplex":[],"quotient":[[10,20],[30]],"boundary":[2,1],"homology":[1,0],"explanation":"At one the edge enters K. Its boundary is v₁ − v₀, or 2v₀ + v₁ over F₃. This identifies the two component classes, leaving one degree zero class. The edge itself is not a cycle."},
    {"scale":2,"ambient":[10,20,30],"subcomplex":[10],"quotient":[[20],[30]],"boundary":[1],"homology":[0,0],"explanation":"At two v₀ enters A and its quotient coordinate becomes zero. The edge now has boundary v₁, so the remaining vertex class is a boundary. The edge is still not a cycle; both relative homology spaces are zero."},
    {"scale":3,"ambient":[10,20,30],"subcomplex":[10,20],"quotient":[[],[30]],"boundary":[],"homology":[0,1],"explanation":"At three both endpoints belong to A. Their quotient coordinates are zero, so the edge is a cycle. There are no cells of dimension two to fill it, giving one relative class."},
    {"scale":4,"ambient":[10,20,30],"subcomplex":[10,20,30],"quotient":[[],[]],"boundary":[],"homology":[0,0],"explanation":"At four the edge also enters A. Every quotient chain coordinate is now zero, so the relative class disappears. Its interval includes three and excludes four."}
  ];
  const select = root.querySelector("select");
  const drawing = root.querySelector(".relative-pair-drawing");
  const namespace = "http://www.w3.org/2000/svg";
  const names = new Map([[10, "v₀"], [20, "v₁"], [30, "e"]]);
  let current = states[Number(select.value)];

  function element(tag, attributes = {}, text = "") {
    const node = document.createElementNS(namespace, tag);
    for (const [key, value] of Object.entries(attributes)) node.setAttribute(key, value);
    if (text) node.textContent = text;
    return node;
  }

  function draw() {
    const width = Math.max(210, drawing.clientWidth);
    const left = 72, right = width - 28;
    const svg = element("svg", {viewBox: `0 0 ${width} 190`, role: "img", "aria-labelledby": "relative-pair-svg-title"});
    svg.append(element("title", {id: "relative-pair-svg-title"},
      `At t = ${current.scale}, K contains ${current.ambient.map(id => names.get(id)).join(", ")}. A contains ${current.subcomplex.map(id => names.get(id)).join(", ") || "no cells"}.`));
    for (const [label, cells, y] of [["Kₜ", current.ambient, 45], ["Aₜ", current.subcomplex, 137]]) {
      svg.append(element("text", {x: 8, y: y + 5}, label));
      svg.append(element("line", {x1: left + 7, x2: right - 7, y1: y, y2: y,
        class: cells.includes(30) ? "present-cell" : "absent-cell"}));
      svg.append(element("text", {x: (left + right) / 2, y: y - 13, "text-anchor": "middle"}, "e →"));
      for (const [id, x] of [[10, left], [20, right]]) {
        svg.append(element("circle", {cx: x, cy: y, r: 6,
          class: cells.includes(id) ? "present-cell" : "absent-cell"}));
        svg.append(element("text", {x, y: y + 28, "text-anchor": "middle"}, names.get(id)));
      }
    }
    drawing.replaceChildren(svg);
  }

  function show() {
    current = states[Number(select.value)] || states[3];
    root.querySelector("[data-relative-scale]").textContent = current.scale;
    root.querySelector("[data-relative-vertices]").textContent = current.quotient[0].map(id => names.get(id)).join(", ") || "None";
    root.querySelector("[data-relative-edges]").textContent = current.quotient[1].map(id => names.get(id)).join(", ") || "None";
    const rows = current.quotient[0].length, columns = current.quotient[1].length;
    let boundary;
    if (!columns) boundary = `No edge coordinate (${rows} × 0 matrix)`;
    else if (!rows) boundary = "0 (a 0 × 1 matrix)";
    else boundary = current.boundary.map((coefficient, i) => `${coefficient === 1 ? "" : coefficient}${names.get(current.quotient[0][i])}`).join(" + ");
    root.querySelector("[data-relative-boundary]").textContent = boundary;
    root.querySelector("[data-relative-h0]").textContent = current.homology[0];
    root.querySelector("[data-relative-h1]").textContent = current.homology[1];
    root.querySelector("#relative-pair-status").textContent = current.explanation;
    draw();
  }
  select.addEventListener("change", show);
  new ResizeObserver(draw).observe(drawing);
  show();
  select.disabled = false;
})();
