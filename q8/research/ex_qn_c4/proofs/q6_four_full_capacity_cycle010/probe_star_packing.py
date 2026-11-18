"""Four-full-code degree-four star packing: exploratory LP, exact dual if found."""
from itertools import combinations
from collections import Counter
from fractions import Fraction
from pathlib import Path
from hashlib import sha256
import json
import numpy as np
from scipy.optimize import linprog

HERE=Path(__file__).resolve().parent
F=[0,15,51,60]
face=lambda v,mask:(mask,v&~mask)
triples=[sum(1<<i for i in t) for t in combinations(range(6),3)]
full_faces={face(v,t) for v in F for t in triples}
columns=[]
local=[]
for v in range(64):
    if v.bit_count()%2 or v in F:continue
    forbidden=[v^f for f in F if (v^f).bit_count()==2]
    allowed=[a for a in range(64) if all(a&d!=d for d in forbidden)]
    local.append({'vertex':v,'forbidden_pairs':forbidden,
                  'allowed_degree_histogram':dict(sorted(Counter(a.bit_count() for a in allowed).items()))})
    for a in allowed:
        if a.bit_count()!=4:continue
        occupied={face(v,t) for t in triples if a&t==t}
        assert len(occupied)==4 and not occupied&full_faces
        columns.append((v,a,occupied))
rows=sorted(set.union(*(o for v,a,o in columns)))
vertices=sorted({v for v,a,o in columns})
A=np.array([[int(f in o) for v,a,o in columns] for f in rows]
           +[[int(v==w) for v,a,o in columns] for w in vertices])
r=linprog(-np.ones(len(columns)),A_ub=A,b_ub=np.ones(len(A)),bounds=(0,None),method='highs')
assert r.success,r.message
dual=[Fraction(float(-x)).limit_denominator(10000) for x in r.ineqlin.marginals]
assert all(x>=0 for x in dual)
assert all(sum(dual[i]*int(A[i,j]) for i in range(len(A)))>=1 for j in range(len(columns)))
value=sum(dual)
output={'status':'EXACT_DUAL_FOR_FOUR_STAR_PACKING_RELAXATION',
        'full_roots':F,'nonfull_local_patterns':local,
        'available_face_rows':len(rows),'degree4_roots':len(vertices),'degree4_patterns':len(columns),
        'numeric_primal':float(-r.fun),'exact_dual_bound':str(value),
        'columns':[{'root':v,'selected':a,'faces':sorted(o)} for v,a,o in columns],
        'row_labels':[['face',list(f)] for f in rows]+[['root',v] for v in vertices],
        'dual_weights':[str(x) for x in dual],
        'scope':'Necessary packing only; maximum number of degree4 vertices after four actual full roots. No minimum assumptions or completion claimed.',
        'code_sha256':sha256(Path(__file__).read_bytes()).hexdigest()}
(HERE/'STAR_PACKING.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps({k:v for k,v in output.items() if k not in ['nonfull_local_patterns','columns','row_labels','dual_weights']},indent=2))
