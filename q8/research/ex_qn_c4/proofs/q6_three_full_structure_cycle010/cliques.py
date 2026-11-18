#!/usr/bin/env python3
"""A bounded strengthening by actual high-star conflict cliques, still an LP."""
from pathlib import Path
from itertools import combinations
from fractions import Fraction
import json
import numpy as np
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent
def maximal_cliques(adj):
    """Bitset Bron--Kerbosch with a maximum-neighbor pivot."""
    found=[]
    def visit(chosen,possible,excluded):
        if not possible and not excluded:
            found.append(tuple(chosen))
            assert len(found)<=100000,'bounded clique attempt exceeded limit'
            return
        union=possible|excluded
        vertices=[]
        while union:
            bit=union&-union;union-=bit;vertices.append(bit.bit_length()-1)
        pivot=max(vertices,key=lambda v:(possible&adj[v]).bit_count())
        candidates=possible&~adj[pivot]
        while candidates:
            bit=candidates&-candidates;candidates-=bit;v=bit.bit_length()-1
            visit(chosen+[v],possible&adj[v],excluded&adj[v])
            possible^=bit;excluded|=bit
    visit([], (1<<len(adj))-1, 0)
    return found
def main():
    source=json.loads((HERE/'PACKING.json').read_text());columns=source['columns']
    adj=[0]*len(columns)
    for i,j in combinations(range(len(columns)),2):
        a,b=columns[i],columns[j]
        if a['root']==b['root'] or len(set(a['neighbors'])&set(b['neighbors']))>=2:
            adj[i]|=1<<j;adj[j]|=1<<i
    rows=sorted(set(tuple(sorted(c)) for c in maximal_cliques(adj)))
    A=np.zeros((len(rows),len(columns)),dtype=np.int8)
    for i,row in enumerate(rows):
        for j in row:A[i,j]=1
    obj=np.array([c['weight'] for c in columns])
    r=linprog(-obj,A_ub=A,b_ub=np.ones(len(rows)),bounds=(0,None),method='highs')
    assert r.success,r.message
    dual=[Fraction(float(-x)).limit_denominator(1000000) for x in r.ineqlin.marginals]
    assert all(x>=0 for x in dual)
    assert all(sum(dual[i] for i,row in enumerate(rows) if j in row)>=int(obj[j]) for j in range(len(columns)))
    primal=[Fraction(float(x)).limit_denominator(1000000) for x in r.x]
    assert all(x>=0 for x in primal)
    assert all(sum(primal[j] for j in row)<=1 for row in rows)
    primal_value=sum(x*int(w) for x,w in zip(primal,obj))
    assert primal_value==sum(dual),'not an exact primal--dual match'
    out={'status':'EXACT_DUAL_FOR_NECESSARY_HIGH_STAR_CLIQUE_RELAXATION','maximal_cliques':len(rows),
         'cliques':rows,'exact_H_bound':str(sum(dual)),'S_plus_L_bound':str(89+3*sum(dual)),
         'nonzero_dual':[[i,str(w)] for i,w in enumerate(dual) if w],
         'numeric_primal':-r.fun,'primal_nonzero':[[i,float(x)] for i,x in enumerate(r.x) if x>1e-8],
         'exact_primal_value':str(primal_value),'exact_primal':[[i,str(x)] for i,x in enumerate(primal) if x],
         'scope':'Only bound on actual high-star choices; fractional solutions not graphs; no claims of completion.'}
    (HERE/'CLIQUES.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ['cliques','nonzero_dual','primal_nonzero']},indent=2))
if __name__=='__main__':main()
