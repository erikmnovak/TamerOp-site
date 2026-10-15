/* Authored mathematical illustrations. The prepared values are checked against
   TamerOp by check_arithmetic_choices.jl; the browser makes no new Julia query. */
(() => {
  "use strict";
  const examples = {
    "cutoff": [
      {"id":"fine","label":"τ = 10⁻¹⁶","exponent":-16,"atol":1e-16,"rank":2,"nullity":0,"explanation":"Both singular values exceed the cutoff, so both coordinate directions remain in the numerical image. Its dimension agrees with the exact rank, which is two for every choice here."},
      {"id":"equal","label":"τ = 10⁻¹⁴","exponent":-14,"atol":1e-14,"rank":1,"nullity":1,"explanation":"The second singular value equals the cutoff. The SVD rule retains values strictly greater than τ, so this direction is discarded. The numerical kernel has dimension one although the exact kernel is zero."},
      {"id":"coarse","label":"τ = 10⁻¹²","exponent":-12,"atol":1e-12,"rank":1,"nullity":1,"explanation":"The second direction lies below the cutoff. The numerical image keeps the first coordinate, while the second coordinate enters the numerical kernel. The underlying matrix is still invertible."}
    ],
    "certificate": [
      {"id":"lower","label":"y₂ = 1","y2":1,"residual":1,"accepted":false,"explanation":"The first and third coordinates still give x = (3, −1). Multiplying by B gives second coordinate 2, so it cannot recover the supplied value 1. The exact solver rejects this vector."},
      {"id":"member","label":"y₂ = 2","y2":2,"residual":0,"accepted":true,"explanation":"The selected rows give x = (3, −1), and the second row agrees too. All three coordinates of Bx equal those of y, so these are the exact coordinates of y in the image of B."},
      {"id":"upper","label":"y₂ = 3","y2":3,"residual":-1,"accepted":false,"explanation":"Changing the second coordinate does not change the candidate from rows 1 and 3. Its second image coordinate remains 2, so the full equation fails. Keeping the inverse alone would miss this failure."}
    ],
    "boundary": [
      {"id":"below","label":"(0, −1): below the segment","x":0,"y":-1,"signature":[0,0],"dimension":0,"explanation":"The upset has not begun because the second coordinate is negative. No active column remains, so the represented vector space is zero."},
      {"id":"lower","label":"(0, 0): lower endpoint","x":0,"y":0,"signature":[1,0],"dimension":1,"explanation":"Both closed inequalities include this endpoint. The active block is [1], whose image is Q. The boundary x₁ = 0 must therefore retain this nonzero space."},
      {"id":"middle","label":"(0, 1): inside the segment","x":0,"y":1,"signature":[1,0],"dimension":1,"explanation":"The point belongs to both indicators, so the active block is [1] and its image is Q. Along this segment the nonzero structure maps are identities."},
      {"id":"upper","label":"(0, 2): upper endpoint","x":0,"y":2,"signature":[1,0],"dimension":1,"explanation":"Equality is included in the downset, so the endpoint still has space Q. Moving above it changes the signature and gives a zero space."},
      {"id":"above","label":"(0, 3): above the segment","x":0,"y":3,"signature":[1,1],"dimension":0,"explanation":"The upset is active but the point is outside the downset. No active row remains, so the represented vector space is zero."},
      {"id":"left","label":"(−1, 1): left of the segment","x":-1,"y":1,"signature":[0,0],"dimension":0,"explanation":"A negative first coordinate lies outside the upset. The nearby open region has a zero space even though the segment itself has space Q."},
      {"id":"right","label":"(1, 1): right of the segment","x":1,"y":1,"signature":[1,1],"dimension":0,"explanation":"A positive first coordinate lies outside the downset. Sampling this open region would not reveal the nonzero space on the segment."}
    ],
    "grades": [
      {"id":"before","label":"r = 1/2: before either merger","offset":-1,"power":1,"components":3,"position":0.1,"explanation":"The radius is below both critical values, so the three covered intervals are disjoint. Increasing the radius to the first critical value joins the first two components."},
      {"id":"first","label":"r = 1: first merger","offset":0,"power":72,"components":2,"position":0.3,"explanation":"The first two intervals meet at their common endpoint. The third is still separate because its gap is slightly larger. Closed membership includes the first merger at r = 1."},
      {"id":"between","label":"r = 1 + 2⁻⁷²: between the mergers","offset":1,"power":72,"components":2,"position":0.5,"explanation":"The first two points remain in one component, and the third has not joined them. This exact radius lies strictly between the two events, although all three radii have Float64 display 1."},
      {"id":"second","label":"r = 1 + 2⁻⁷¹: second merger","offset":1,"power":71,"components":1,"position":0.7,"explanation":"The larger gap now closes too, giving one component. Keeping the exact critical values distinct preserves the intervening state with two components."}
    ]
  };
  const ns = "http://www.w3.org/2000/svg";
  const element = (tag, attrs = {}, text = "") => {
    const node = document.createElementNS(ns, tag);
    for (const [key, value] of Object.entries(attrs)) node.setAttribute(key, value);
    if (text) node.textContent = text;
    return node;
  };
  for (const root of document.querySelectorAll("[data-arithmetic-example]")) {
    if (root.dataset.initialized) continue;
    const kind = root.dataset.arithmeticExample, states = examples[kind];
    if (!states) continue;
    const select = root.querySelector("select"), drawing = root.querySelector(".choice-drawing");
    let state = states.find(item => item.id === select.value);
    const value = (name, text) => { root.querySelector(`[data-value="${name}"]`).textContent = text; };
    function draw() {
      const w = Math.max(230, drawing.clientWidth), h = 230;
      const svg = element("svg", {viewBox:`0 0 ${w} ${h}`, role:"img", "aria-label":state.label + ". " + state.explanation});
      const line = (x1,y1,x2,y2,cls="axis") => svg.append(element("line",{x1,y1,x2,y2,class:cls}));
      const text = (x,y,label,anchor="start",cls="") => svg.append(element("text",{x,y,"text-anchor":anchor,class:cls},label));
      const dot = (x,y,cls,r=5) => svg.append(element("circle",{cx:x,cy:y,r,class:cls}));
      if (kind === "cutoff") {
        const x = exponent => 22 + (w - 44) * (exponent + 16) / 16;
        line(22,167,w-22,167);
        for (const [e,label] of [[-16,"10⁻¹⁶"],[-12,"10⁻¹²"],[-8,"10⁻⁸"],[-4,"10⁻⁴"],[0,"1"]]) {
          line(x(e),164,x(e),171); text(x(e),191,label,"middle","small");
        }
        text(w/2,218,"Singular value (logarithmic scale)","middle","small");
        line(x(state.exponent),40,x(state.exponent),163,"cutoff");
        text(x(state.exponent),25,"τ",state.exponent===-16?"start":"middle");
        dot(x(0),65,"retained"); text(x(0)-12,70,"σ₁ = 1","end");
        dot(x(-14),118,state.rank===2?"retained":"omitted"); text(w*.55,123,"σ₂ = 10⁻¹⁴");
      } else if (kind === "certificate") {
        text(4,25,"Row"); text(w*.46,25,"Supplied y","middle"); text(w*.80,25,"Bx","middle");
        const actual=[1,state.y2,-1], recovered=[1,2,-1];
        for(let i=0;i<3;i++) {
          const y=68+i*54;
          text(8,y,String(i+1)); text(w*.46,y,String(actual[i]),"middle"); text(w*.80,y,String(recovered[i]),"middle");
          text(w*.63,y,actual[i]===recovered[i]?"=":"≠","middle");
          line(3,y+10,w-3,y+10,i===1&&!state.accepted?"cutoff":"axis");
        }
        text(w/2,218,"Rows 1 and 3 determine the candidate.","middle","small");
      } else if (kind === "boundary") {
        const x = a => 35+(w-65)*(a+1.5)/3, y = b => 194-154*(b+1)/4;
        line(x(-1.5),y(0),x(1.5),y(0)); line(x(0),211,x(0),19);
        text(w-12,y(0)-8,"x₁","end"); text(x(0)+10,22,"x₂");
        for(const b of [-1,0,1,2,3]) { line(x(0)-4,y(b),x(0)+4,y(b)); text(x(0)-11,y(b)+5,String(b),"end","small"); }
        line(x(0),y(0),x(0),y(2),"retained"); dot(x(0),y(0),"retained");dot(x(0),y(2),"retained");
        for(const a of [-1,1]) text(x(a),y(0)+19,String(a),"middle","small");
        dot(x(state.x),y(state.y),"query",9);
        text(x(state.x)+(state.x===1?-14:14),y(state.y)-9,"q",state.x===1?"end":"start");
        text(w/2,225,"Filled endpoints belong to the segment.","middle","small");
      } else if (kind === "grades") {
        const xs=[30,w/2,w-30], labels=["0","2","4 + δ"];
        for(let i=0;i<2;i++) line(xs[i]+6,63,xs[i+1]-6,63,state.components<=2-i?"retained":"omitted");
        for(let i=0;i<3;i++){dot(xs[i],63,"retained");text(xs[i],45,labels[i],i===2?"end":i===0?"start":"middle");}
        text(w/2,96,"Joined points lie in one component.","middle","small");
        const x = p => 25+(w-50)*p;
        line(25,160,w-25,160);
        for(const [p,label] of [[.3,"ρ₁"],[.7,"ρ₂"]]) {line(x(p),150,x(p),167);text(x(p),189,label,"middle");}
        dot(x(state.position),142,"query",6); line(x(state.position),149,x(state.position),160,"cutoff");
        text(x(state.position)+10,139,"r");
        text(w/2,219,"The gap between the radii is enlarged.","middle","small");
      }
      drawing.replaceChildren(svg);
    }
    function show() {
      state = states.find(item => item.id === select.value) || states[0];
      if(kind === "cutoff") {value("rank",state.rank);value("nullity",state.nullity);}
      if(kind === "certificate") {value("residual",`(0, ${state.residual}, 0)`);value("accepted",state.accepted?"Yes, Bx = y":"No, Bx ≠ y");}
      if(kind === "boundary") {value("signature",`(${state.signature.join(", ")})`);value("space",state.dimension?"Q (dimension 1)":"Zero space (dimension 0)");}
      if(kind === "grades") {value("components",state.components);value("floating",state.id==="before"?"0.5":"1");}
      root.querySelector("[data-choice-explanation]").textContent=state.explanation;
      root.dataset.selectedState=state.id;
      draw();
    }
    select.addEventListener("change",show);
    new ResizeObserver(draw).observe(drawing);
    show(); select.disabled=false; root.dataset.initialized="true";
  }
})();
