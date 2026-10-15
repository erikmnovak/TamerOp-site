/* Highlight mathematical routes; every topic remains an ordinary usable link. */
(() => {
  "use strict";
  const map = document.querySelector('.using-map');
  if (!map) return;
  const flow = map.querySelector('.using-flow');
  const svg = map.querySelector('.using-connections');
  const buttons = [...map.querySelectorAll('[data-route]')];
  const nodes = new Map([...map.querySelectorAll('[data-node]')].map(node => [node.dataset.node, node]));
  const edges = [['geometry', 'encodings'], ['persistence', 'encodings'], ['direct', 'encodings'],
    ['encodings', 'algebra'], ['encodings', 'invariants'], ['encodings', 'features']];
  const companions = ['visualization', 'data_io', 'arithmetic'];
  const routes = {
    all: { nodes: [], text: 'Choose how to describe your input, build a finite encoding, and explore the questions it makes accessible. Visualization, saving and arithmetic accompany the computation throughout.' },
    data: { nodes: ['geometry', 'persistence', 'encodings', 'algebra', 'invariants', 'features', ...companions], text: 'Start by choosing how your data gives a growing family of spaces, called a filtration. Build a finite encoding of the resulting persistence module, then use that finite encoding to investigate its algebra, compare modules or extract numerical features.' },
    module: { nodes: ['direct', 'encodings', 'algebra', 'invariants', 'features', ...companions], text: 'Start with vector spaces and maps, or a presentation of a module. Build a finite encoding that connects them to the original parameters. That finite encoding is then available for algebraic constructions, comparisons and numerical features.' },
    barcode: { nodes: ['persistence', ...companions], text: 'For one changing parameter, follow the direct route from a filtered complex to a barcode: intervals recording when homology classes appear and disappear. The persistence guides connect those intervals to representative cells, coordinates and cohomological products.' },
  };
  let selected = 'all';
  let focused = null;
  let animationTimer;
  let scheduled = false;
  const namespace = 'http://www.w3.org/2000/svg';
  function draw() {
    scheduled = false;
    if (getComputedStyle(svg).display === 'none') return;
    const bounds = flow.getBoundingClientRect();
    svg.setAttribute('viewBox', `0 0 ${bounds.width} ${bounds.height}`);
    svg.replaceChildren();
    const defs = document.createElementNS(namespace, 'defs');
    const marker = document.createElementNS(namespace, 'marker');
    for (const [key, value] of Object.entries({id:'using-route-tip', viewBox:'0 0 8 8', refX:'7', refY:'4', markerWidth:'5', markerHeight:'5', orient:'auto'})) marker.setAttribute(key, value);
    const tip = document.createElementNS(namespace, 'path');
    tip.setAttribute('d', 'M0 0L8 4L0 8Z');
    tip.setAttribute('class', 'using-arrow-tip');
    marker.append(tip); defs.append(marker); svg.append(defs);
    for (const [source, target] of edges) {
      const a = nodes.get(source).getBoundingClientRect(), b = nodes.get(target).getBoundingClientRect();
      const x1 = a.right - bounds.left + 2, y1 = a.top + a.height / 2 - bounds.top;
      const x2 = b.left - bounds.left - 5, y2 = b.top + b.height / 2 - bounds.top;
      const middle = (x1 + x2) / 2;
      const path = document.createElementNS(namespace, 'path');
      path.setAttribute('d', `M${x1} ${y1} C${middle} ${y1},${middle} ${y2},${x2} ${y2}`);
      path.setAttribute('marker-end', 'url(#using-route-tip)');
      path.dataset.source = source; path.dataset.target = target;
      svg.append(path);
    }
    highlight();
  }
  function scheduleDraw() {
    if (!scheduled) { scheduled = true; requestAnimationFrame(draw); }
  }
  function highlight() {
    const active = new Set(routes[selected].nodes);
    for (const [name, node] of nodes) node.classList.toggle('is-route', active.has(name));
    for (const path of svg.querySelectorAll('path[data-source]')) {
      path.classList.toggle('is-route', active.has(path.dataset.source) && active.has(path.dataset.target));
      path.classList.toggle('is-focus', path.dataset.source === focused || path.dataset.target === focused);
    }
  }
  for (const button of buttons) button.addEventListener('click', () => {
    selected = button.dataset.route;
    for (const control of buttons) control.setAttribute('aria-pressed', String(control === button));
    map.querySelector('.using-route-explanation').textContent = routes[selected].text;
    highlight();
    svg.classList.remove('is-changing');
    clearTimeout(animationTimer);
    requestAnimationFrame(() => { svg.classList.add('is-changing'); animationTimer = setTimeout(() => svg.classList.remove('is-changing'), 850); });
    scheduleDraw();
  });
  for (const [name, node] of nodes) {
    const enter = () => { focused = name; highlight(); };
    const leave = () => { focused = null; highlight(); };
    node.addEventListener('pointerenter', enter); node.addEventListener('pointerleave', leave);
    node.addEventListener('focus', enter); node.addEventListener('blur', leave);
  }
  map.querySelector('.using-route-controls').hidden = false;
  flow.dataset.enhanced = 'true';
  if ('ResizeObserver' in window) new ResizeObserver(scheduleDraw).observe(flow);
  window.addEventListener('resize', scheduleDraw);
  document.fonts?.ready.then(scheduleDraw);
  scheduleDraw();
})();
