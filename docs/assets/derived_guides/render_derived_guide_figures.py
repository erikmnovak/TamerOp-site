"""Small exact schematics accompanying the derived algebra guides.

Run with Python's standard library. Labels are mathematical inputs and hand
calculations from the articles, not sampled package output.
"""
from pathlib import Path
from html import escape
import argparse
OUT=Path(__file__).parent
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument("--check", action="store_true", help="Compare regenerated SVGs without writing files.")
args=parser.parse_args()
mismatches=[]

def start(title,desc,w,h):
 return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">',f'<title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>', '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="#465f72"/></marker></defs>',f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="12" fill="#fff" stroke="#cbd5df"/>','<g font-family="DejaVu Sans, sans-serif" fill="#183549">']
def txt(out,x,y,s,size=18,anchor='middle',weight='normal'):
 out.append(f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}">{escape(s)}</text>')
def line(out,x1,y1,x2,y2,dash=False):
 out.append(f'<path d="M{x1} {y1}L{x2} {y2}" fill="none" stroke="#465f72" stroke-width="2"'+(' stroke-dasharray="5 4"' if dash else '')+' marker-end="url(#arrow)"/>')
def end(out,name):
 out.extend(['</g>','</svg>'])
 expected='\n'.join(out)+'\n'
 path=OUT/name
 if args.check:
  if not path.exists() or path.read_text()!=expected: mismatches.append(name)
 else: path.write_text(expected)

out=start('A resolution checked at each vertex','The degree 2, degree 1 and degree 0 terms are P4, P2 plus P3 and P1. At vertex 4 the maps are a to (a,-a), then (b,c) to b+c. Other nonzero maps are identities.',560,464)
txt(out,280,32,'The diamond resolution at each vertex',19,weight='bold')
xs=[135,260,380,485]
for x,s in zip(xs,['P₄','P₂ ⊕ P₃','P₁','M']):txt(out,x,76,s,21)
for x,y,label in [(198,70,'d₂'),(320,70,'d₁'),(432,70,'ε')]:txt(out,x,y-20,label,17)
for row,(vertex,vals) in enumerate([(1,['0','0','K','K']),(2,['0','K','K','0']),(3,['0','K','K','0']),(4,['K','K²','K','0'])]):
 y=127+row*66
 out.append(f'<rect x="16" y="{y-29}" width="528" height="53" rx="6" fill="'+('#eef4fa' if row==3 else '#f5f7f9')+'"/>')
 txt(out,60,y+7,f'v = {vertex}',17)
 for x,s in zip(xs,vals):txt(out,x,y+7,s,22)
 for j in range(3):
  line(out,xs[j]+24,y,xs[j+1]-27,y)
  if vals[j]=='K' and vals[j+1]=='K':txt(out,(xs[j]+xs[j+1])/2,y-8,'1',15)
txt(out,280,391,'At v = 4:  d₂(a) = (a, −a)',19)
txt(out,280,421,'d₁(b,c) = b + c,   so ker d₁ = im d₂.',18)
txt(out,280,448,'K = ℚ; zero terms beyond the displayed ends.',15)
end(out,'diamond_resolution.svg')

out=start('The four pieces of the filtered complex','At spectral bidegrees (0,1), (1,1), (1,0), (2,0) sit K squared. Horizontal identity and T maps raise filtration. The middle vertical identity preserves filtration. A later differential follows a horizontal map, a lift against the vertical map, and the next horizontal map.',560,430)
txt(out,280,32,'The supplied pieces and their maps',20,weight='bold')
line(out,60,334,526,334);line(out,60,334,60,71)
txt(out,513,369,'p',19);txt(out,34,77,'q',19)
for x,p in [(125,0),(295,1),(465,2)]:txt(out,x,359,str(p),17)
for y,q in [(255,0),(130,1)]:txt(out,39,y+6,str(q),17)
for x,y in [(125,130),(295,130),(295,255),(465,255)]:
 out.append(f'<rect x="{x-33}" y="{y-23}" width="66" height="46" rx="7" fill="#eaf3fa" stroke="#547e9b"/>');txt(out,x,y+7,'K²',23)
line(out,161,130,256,130);txt(out,211,111,'I',20)
line(out,295,229,295,157);txt(out,315,198,'I',20,anchor='start')
line(out,331,255,426,255);txt(out,379,237,'T',20)
txt(out,125,186,'(p,t) = (0,1)',14);txt(out,295,84,'(p,t) = (1,2)',14)
txt(out,290,298,'(p,t) = (1,1)',14);txt(out,465,298,'(p,t) = (2,2)',14)
txt(out,280,398,'t = p + q;  I = identity;  T = diag(1,0).',17)
end(out,'filtered_staircase.svg')

out=start('Opposite and forward modules in Tor','On the opposite chain, the right simple has K at vertex 2 mapping to zero at vertex 1. On the forward chain, the left simple has K at vertex 1 mapping to zero at vertex 2. Tensoring the right projective resolution with the left module gives K in degree 1 mapping by zero to zero in degree 0.',560,430)
txt(out,280,32,'Follow the order before tensoring',20,weight='bold')
for y,title,x1,x2 in [(111,'R on Pᵒᵖ',420,195),(216,'L on P',195,420)]:
 txt(out,23,y-30,title,19,anchor='start')
 for x,label in [(195,'1'),(420,'2')]:txt(out,x,y+38,'vertex '+label,15)
 if x1>x2:
  txt(out,x1,y+7,'K',24);txt(out,x2,y+7,'0',24);line(out,x1-24,y,x2+25,y)
 else:
  txt(out,x1,y+7,'K',24);txt(out,x2,y+7,'0',24);line(out,x1+24,y,x2-25,y)
 txt(out,308,y-10,'0',17)
out.append('<path d="M22 277H538" stroke="#cbd5df"/>')
txt(out,280,306,'After tensoring the right resolution with L',17)
txt(out,180,345,'K',25);txt(out,405,345,'0',25);line(out,208,338,378,338);txt(out,290,329,'∂₁ = 0',17)
txt(out,180,377,'degree 1',17);txt(out,405,377,'degree 0',17)
txt(out,280,410,'Tor₁(R,L) ≅ K;  Tor₀(R,L) = 0.',19)
end(out,'tor_opposite.svg')

out=start('Checking that a product descends to homology','Decompose cycles in each degree into boundaries B and a chosen complement H. Products involving a boundary must represent zero; only products from H in both degrees contribute homology coordinates.',560,426)
txt(out,280,31,'Expand each cycle into boundary and representative',17,weight='bold')
def indexed_label(x,y,label,size):
 markup=escape(label)
 for degree in ('p','q'):
  markup=markup.replace('['+degree+']', f'<tspan baseline-shift="sub" font-size="{0.7*size:g}">{degree}</tspan>')
 out.append(f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="middle">{markup}</text>')
indexed_label(280,66,'Z[p] = B[p] ⊕ H[p],    Z[q] = B[q] ⊕ H[q]',20)
for x,s in [(275,'B[q]'),(443,'H[q]')]:indexed_label(x,113,s,23)
for y,s in [(173,'B[p]'),(279,'H[p]')]:indexed_label(88,y,s,23)
for row in range(2):
 for col in range(2):
  x=190+col*168;y=132+row*106;active=row==col==1
  out.append(f'<rect x="{x}" y="{y}" width="156" height="91" rx="7" fill="'+('#e8f3ec' if active else '#f2f5f8')+'" stroke="#b5c4ce"/>')
  txt(out,x+78,y+35,'[μ(x,y)]',19)
  txt(out,x+78,y+65,'coordinates' if active else '= 0',19)
txt(out,280,372,'B = boundaries; H = chosen representatives.',17)
txt(out,280,403,'Changing a representative adds only zero classes.',17)
end(out,'tor_descent.svg')

if args.check:
 if mismatches: raise SystemExit("Stale or missing diagrams: " + ", ".join(mismatches))
 print("All four derived-guide diagrams match their generator.")
