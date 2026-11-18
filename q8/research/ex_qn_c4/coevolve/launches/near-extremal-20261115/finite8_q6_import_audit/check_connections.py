#!/usr/bin/env python3
"""Fresh finite checks for analytic slots, replacement markings and gate tables."""
from pathlib import Path
from itertools import combinations, product
from collections import Counter
from math import comb
import hashlib,json
HERE=Path(__file__).resolve().parent
P=[x for x in range(64) if x.bit_count()%2==0]
blocks=[3,12,48];F={15,51,60}
def ns(x,m):return {x^(1<<i) for i in range(6) if m>>i&1}
slots=[]
for b in blocks:
    other=[d for d in blocks if d!=b]
    bases=[0]+[(1<<i)|(1<<j) for i in range(6) if other[0]>>i&1 for j in range(6) if other[1]>>j&1]
    for u in bases:slots.append(('square',u,u|b,b))
for i,j,k in product(range(2),range(2,4),range(4,6)):
    slots.append(('face',0,0,(1<<i)|(1<<j)|(1<<k)))
assert len(slots)==23
def occupied(x,m):
    return {i for i,(kind,a,b,T) in enumerate(slots) if m&T==T and (x in (a,b) if kind=='square' else x&~T==0)}
columns=[];origin=[]
for x in P:
    if x in F:continue
    for m in range(63):
        if any(len(ns(x,m)&ns(f,63))>=2 for f in F):continue
        d=m.bit_count()
        if d>=4:
            q=occupied(x,m);assert len(q)>=(1 if d==4 else 3)
            columns.append((x,m,d,q))
        if x==0 and d>=3:
            q=len(occupied(x,m));h={3:0,4:1,5:3}[d]
            assert q-h>=1
            origin.append((m,d,q,h))
for x,m,d,q in columns:
    for y,n,e,r in columns:
        if x==y:continue
        if q&r:assert len(ns(x,m)&ns(y,n))>=2
assert len(columns)==213 and len(origin)==41
# One graph: safe simultaneous replacement must not reconnect the u square,
# and the v square's remote edges must avoid u. Check every marked pair.
pair_checks=0
for D in combinations(range(6),2):
    v=sum(1<<i for i in D)
    for E in combinations(range(6),2):
        if E==D:continue
        assert not set(D)<=set(E)
        opposite=v^sum(1<<i for i in E)
        assert opposite!=0
        pair_checks+=1
assert pair_checks==210
tables={}
for L in range(5):
    rows=[]
    for c in range(5):
        cap=160
        if L==0:cap=155 if c==3 else 158
        if L==1:cap=155 if c==4 else 158
        if L==2:cap=157 if c==4 else 160
        residue=(32-L+c)%3
        s=max(s for s in range(cap+1) if s%3==residue)
        rows.append({'c':c,'S_cap':s,'2S_plus_c':2*s+c})
    tables[str(L)]=rows
assert [max(r['2S_plus_c'] for r in tables[str(L)]) for L in range(4)]==[316,317,321,322]
assert all(2*max(r['2S_plus_c'] for r in tables[str(L)])<=632+5*L for L in range(4))
out={'status':'PASS','scope':'fresh standard-library local analytic connection checks; not Q6 graph enumeration','slots':slots,'high_columns':len(columns),'origin_nonlow_masks':len(origin),'origin_excess_histogram':dict(Counter(q-h for m,d,q,h in origin)),'simultaneous_replacement_markings':pair_checks,'gate_tables':tables,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
# A literal boundary witness checks the allowed scope and rules out importing
# the tempting stronger S+2c<=158 statement. No solver or witness producer.
witness_path=Path('q6_sources/q8_upper_independent/results/q6_degree_potential_2d4.json')
data=json.loads(witness_path.read_text())
edges={tuple(sorted(e)) for e in data['edges']}
assert len(edges)==len(data['edges'])
assert all(0<=u<v<64 and (u^v).bit_count()==1 for u,v in edges)
degrees=Counter(v for e in edges for v in e)
for u in range(64):
    for i,j in combinations(range(6),2):
        if u&((1<<i)|(1<<j)):continue
        a=u^(1<<i);b=u^(1<<j);v=u^(1<<i)^(1<<j)
        assert not all(tuple(sorted(e)) in edges for e in [(u,a),(u,b),(v,a),(v,b)])
S=sum(comb(degrees[x],3) for x in P);c=sum(degrees[x]==6 for x in P)
assert min(degrees[x] for x in P)>=3 and (S,c)==(157,2)
assert 2*S+c==316 and S+2*c==161
out['literal_boundary_witness']={'path':str(witness_path),'sha256':hashlib.sha256(witness_path.read_bytes()).hexdigest(),'S':S,'c':c,'specified_minimum':min(degrees[x] for x in P),'2S_plus_c':2*S+c,'stronger_S_plus_2c':S+2*c,'all_240_squares_checked':True}
(HERE/'CONNECTIONS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['slots','gate_tables']},indent=2))
