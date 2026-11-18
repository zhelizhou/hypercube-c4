#!/usr/bin/env python3
"""Three-full actual-star capacity relaxation; no graph SAT or old replay."""
from pathlib import Path
from itertools import combinations
from collections import Counter
from hashlib import sha256
from fractions import Fraction
import json
import numpy as np
from scipy.optimize import linprog

HERE=Path(__file__).resolve().parent
FULL=(0,15,51)
EVEN=[x for x in range(64) if x.bit_count()%2==0]
def neighbors(v,m):return {v^(1<<j) for j in range(6) if m>>j&1}
FULLN=[neighbors(f,63) for f in FULL]
triples=[sum(1<<j for j in ds) for ds in combinations(range(6),3)]
full_faces={(t,f&~t) for f in FULL for t in triples}
def main():
    local=[];columns=[]
    for v in EVEN:
        if v in FULL:continue
        allowed=[m for m in range(63) if all(len(neighbors(v,m)&N)<=1 for N in FULLN)]
        local.append({'root':v,'forbidden_pairs':[v^f for f in FULL if (v^f).bit_count()==2],
                      'allowed_masks':allowed,'max_degree':max(m.bit_count() for m in allowed)})
        for m in allowed:
            d=m.bit_count()
            if d<4:continue
            faces={(t,v&~t) for t in triples if m&t==t}
            assert not faces&full_faces
            columns.append({'root':v,'mask':m,'degree':d,'weight':1 if d==4 else 3,
                            'neighbors':sorted(neighbors(v,m)),'faces':sorted(faces)})
    rows=[];labels=[]
    def add(label,indices):
        if not indices:return
        row=[0]*len(columns)
        for j in indices:row[j]=1
        rows.append(row);labels.append(label)
    for v in EVEN:
        add(['root',v],[i for i,c in enumerate(columns) if c['root']==v])
    pairs=[]
    for i,j in combinations(range(len(columns)),2):
        a,b=columns[i],columns[j]
        if a['root']==b['root']:continue
        if len(set(a['neighbors'])&set(b['neighbors']))>=2:
            add(['conflict',i,j],[i,j]);pairs.append([i,j])
    faces=sorted(set(tuple(f) for c in columns for f in c['faces']))
    for f in faces:
        add(['face',list(f)],[i for i,c in enumerate(columns) if list(f) in c['faces'] or tuple(f) in c['faces']])
    A=np.array(rows,dtype=float);b=np.ones(len(rows));objective=np.array([c['weight'] for c in columns],dtype=float)
    solved=linprog(-objective,A_ub=A,b_ub=b,bounds=(0,None),method='highs')
    assert solved.success,solved.message
    dual=[Fraction(float(-x)).limit_denominator(1000000) for x in solved.ineqlin.marginals]
    exact=all(x>=0 for x in dual) and all(sum(dual[i]*rows[i][j] for i in range(len(rows)))>=int(objective[j]) for j in range(len(columns)))
    out={'scope':'Exactlythree actual full P roots, no degree lower assumptions, other full roots forbidden. Necessary high-star packing only.',
         'full_roots':FULL,'local_rows':local,'local_cap_histogram':dict(Counter(r['max_degree'] for r in local)),
         'column_count':len(columns),'column_degree_histogram':dict(Counter(c['degree'] for c in columns)),
         'columns':columns,'row_labels':labels,'pair_conflict_count':len(pairs),'face_rows':len(faces),
         'numeric_H_bound':-solved.fun,'dual_exactly_valid':exact,'exact_H_bound':str(sum(dual)) if exact else None,
         'dual_nonzero':[[i,str(x)] for i,x in enumerate(dual) if x],
         'relaxation_primal_nonzero':[[i,float(x)] for i,x in enumerate(solved.x) if x>1e-8],
         'identity':'S+L=89+3H, H=N4+3N5',
         'script_sha256':sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE/'PACKING.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('local_rows','columns','row_labels','dual_nonzero','relaxation_primal_nonzero')},indent=2))
if __name__=='__main__':main()
