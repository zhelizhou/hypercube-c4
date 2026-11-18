#!/usr/bin/env python3
"""Independent integer/Fraction audit; no producer import, LP, SAT or old replay."""
from pathlib import Path
from itertools import combinations, permutations
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from math import comb
import json

HERE=Path(__file__).resolve().parent
OLD=HERE.parents[3]/'q6_sources'/'q8_upper_independent'
# Locate the separate historical source without relying on producer modules.
OLD=Path('q6_sources/q8_upper_independent')
F={0,15,51}
P=[x for x in range(64) if x.bit_count()%2==0]
PAIRS=[(5,53),(6,54),(9,57),(10,58),(12,60),
       (17,29),(18,30),(33,45),(34,46),(48,60),
       (20,23),(24,27),(36,39),(40,43),(60,63)]
TS=[a|b|c for a in (1,2) for b in (4,8) for c in (16,32)]
def ns(v,m):return {v^(1<<i) for i in range(6) if m&(1<<i)}
def trans(x,pi):return sum(1<<pi[i] for i in range(6) if x&(1<<i))
def maximal_cliques(adj):
    # Set-based pivot recursion, independently written from the bitset producer.
    result=set()
    def extend(chosen,candidates,used):
        if not candidates and not used:
            result.add(tuple(sorted(chosen)));return
        pivot=min(candidates|used)
        for v in sorted(candidates-adj[pivot]):
            extend(chosen|{v},candidates&adj[v],used&adj[v])
            candidates.remove(v);used.add(v)
    extend(set(),set(range(len(adj))),set())
    return result
def main():
    packing=json.loads((HERE/'PACKING.json').read_text())
    clique_data=json.loads((HERE/'CLIQUES.json').read_text())
    # All parity-preserving translations and coordinate maps of one canonical triple.
    orbit=set()
    for pi in permutations(range(6)):
        images=[trans(x,pi) for x in F]
        for t in P:orbit.add(tuple(sorted(x^t for x in images)))
    actual={q for q in combinations(P,3) if all((x^y).bit_count()>=4 for x,y in combinations(q,2))}
    assert actual==orbit
    assert all(all((x^y).bit_count()==4 for x,y in combinations(q,2)) for q in actual)
    cols=[];local=[]
    for x in P:
        if x in F:continue
        allowed=[]
        for m in range(64):
            if m==63:continue # Exactly three full roots, not at least three.
            neigh=ns(x,m)
            if any(len(neigh&ns(f,63))>=2 for f in F):continue
            allowed.append(m)
            if m.bit_count()>=4:cols.append((x,m,m.bit_count()))
        local.append((x,allowed))
    assert [(c['root'],c['mask'],c['degree']) for c in packing['columns']]==cols
    assert [(r['root'],r['allowed_masks']) for r in packing['local_rows']]==local
    assert len(cols)==213
    neighbors=[ns(x,m) for x,m,d in cols]
    adj=[set() for _ in cols]
    for i,j in combinations(range(len(cols)),2):
        if cols[i][0]==cols[j][0] or len(neighbors[i]&neighbors[j])>=2:
            adj[i].add(j);adj[j].add(i)
    all_cliques=maximal_cliques(adj)
    supplied={tuple(row) for row in clique_data['cliques']}
    assert supplied==all_cliques and len(supplied)==422
    for row in supplied:
        assert all(j in adj[i] for i,j in combinations(row,2))
        assert not set.intersection(*(adj[i] for i in row))
    # Reconstruct the short 15-square / 8-three-face certificate geometrically.
    slots=[];slot_labels=[]
    for x,y in PAIRS:
        D=x^y;assert D.bit_count()==2
        row=tuple(i for i,(v,m,d) in enumerate(cols) if v in (x,y) and m&D==D)
        slots.append(row);slot_labels.append({'kind':'square','roots':[x,y],'directions':D})
    for T in TS:
        base=60&~T
        assert all(f&~T!=base for f in F)
        row=tuple(i for i,(v,m,d) in enumerate(cols) if v&~T==base and m&T==T)
        slots.append(row);slot_labels.append({'kind':'three_face','directions':T,'base':base})
    assert len(set(slots))==23 and all(row in supplied for row in slots)
    selected=[tuple(clique_data['cliques'][i]) for i,w in clique_data['nonzero_dual']]
    assert set(selected)==set(slots)
    assert all(Fraction(w)==1 for i,w in clique_data['nonzero_dual'])
    coverage=[sum(i in row for row in slots) for i in range(len(cols))]
    weights=[1 if d==4 else 3 for x,m,d in cols]
    assert all(c>=w for c,w in zip(coverage,weights))
    primal=[Fraction(0) for _ in cols]
    for i,w in clique_data['exact_primal']:primal[i]=Fraction(w)
    assert all(x>=0 for x in primal)
    assert all(sum(primal[i] for i in row)<=1 for row in supplied)
    assert sum(w*x for w,x in zip(weights,primal))==23
    # Independently verify the earlier weaker dual for all original rows.
    oldrows=[]
    for label in packing['row_labels']:
        if label[0]=='root':row=[i for i,c in enumerate(cols) if c[0]==label[1]]
        elif label[0]=='conflict':
            i,j=label[1:];assert j in adj[i];row=[i,j]
        else:
            assert label[0]=='face';T,base=label[1]
            row=[i for i,(v,m,d) in enumerate(cols) if v&~T==base and m&T==T]
            assert all(j in adj[i] for i,j in combinations(row,2))
        oldrows.append(row)
    dual={i:Fraction(w) for i,w in packing['dual_nonzero']}
    assert all(w>=0 for w in dual.values()) and sum(dual.values())==27
    assert all(sum(w for r,w in dual.items() if i in oldrows[r])>=weights[i] for i in range(len(cols)))
    # Two named historical examples only: literal edge and square validation.
    witnesses=[]
    for name in ('q6_code_degree_3_score21.json','q6_code_degree_3_score21_oppmin3.json'):
        path=OLD/'results'/name;data=json.loads(path.read_text())
        edges={tuple(sorted(e)) for e in data['edges']}
        assert len(edges)==len(data['edges'])
        assert all(0<=a<b<64 and (a^b).bit_count()==1 for a,b in edges)
        degrees=Counter(v for edge in edges for v in edge)
        squares=0
        for i,j in combinations(range(6),2):
            for v in range(64):
                if v&((1<<i)|(1<<j)):continue
                a=v^(1<<i);b=v^(1<<j);c=a^(1<<j)
                squares+=1
                assert not all(tuple(sorted(e)) in edges for e in ((v,a),(v,b),(a,c),(b,c)))
        assert squares==240
        S=sum(comb(degrees[v],3) for v in P)
        full=[v for v in P if degrees[v]==6]
        assert S==152 and set(full)==F and min(degrees[v] for v in P)>=3
        witnesses.append({'path':str(path),'sha256':sha256(path.read_bytes()).hexdigest(),
                          'edges':len(edges),'S':S,'L':0,'full':full,'squares_checked':squares,
                          'specified_histogram':dict(sorted(Counter(degrees[v] for v in P).items()))})
    out={'status':'PASS','scope':'Exact 23-slot upper certificate and exact clique-LP primal; not graph attainment or a full-graph search.',
         'full_triples':len(actual),'parity_preserving_isometries_checked':32*720,
         'local_cap_histogram':dict(Counter(max(m.bit_count() for m in ms) for x,ms in local)),
         'all_allowable_local_masks':sum(len(ms) for x,ms in local),'high_columns':len(cols),
         'conflict_edges_including_same_root':sum(map(len,adj))//2,'maximal_cliques':len(supplied),
         'certificate_slots':slot_labels,'coverage_histogram':{str(k):v for k,v in sorted(Counter((d,coverage[i]) for i,(x,m,d) in enumerate(cols)).items())},
         'exact_H_upper':23,'exact_relaxation_primal':23,'S_plus_L_upper':158,
         'older_face_relaxation_dual_H':27,'witnesses':witnesses,
         'source_hashes':{p.name:sha256(p.read_bytes()).hexdigest() for p in [HERE/'PACKING.json',HERE/'CLIQUES.json',Path(__file__)]}}
    (HERE/'EXACT_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
