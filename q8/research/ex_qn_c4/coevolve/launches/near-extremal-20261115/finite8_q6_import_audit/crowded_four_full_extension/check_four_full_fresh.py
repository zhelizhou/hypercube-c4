#!/usr/bin/env python3
"""Fresh literal-square, full-code and forced-pair audit. Standard library only."""
from pathlib import Path
from itertools import combinations,permutations
from collections import Counter
from math import comb
import hashlib,json,time
HERE=Path(__file__).resolve().parent
W=Path('/mnt/c/users/anony/desktop/project/research/ex_qn_c4')
CANON=(0,15,51,60)
P=[x for x in range(64) if x.bit_count()%2==0]
def edge(x,y):return tuple(sorted((x,y)))
def star(x,m):return {edge(x,x^(1<<i)) for i in range(6) if m>>i&1}
EDGES={edge(x,x^(1<<i)) for x in range(64) for i in range(6)}
SQUARES=[]
for x in range(64):
    for i,j in combinations(range(6),2):
        if x&((1<<i)|(1<<j)):continue
        a=x^(1<<i);b=x^(1<<j);y=a^(1<<j)
        SQUARES.append({edge(x,a),edge(x,b),edge(y,a),edge(y,b)})
assert len(EDGES)==192 and len(SQUARES)==240
base=set.union(*(star(x,63) for x in CANON))
assert len(base)==24 and not any(q<=base for q in SQUARES)
codes={c for c in combinations(P,4) if all((x^y).bit_count()>=4 for x,y in combinations(c,2))}
assert len(codes)==120
orbit=set()
for order in permutations(range(6)):
    def pi(x):return sum(1<<order[i] for i in range(6) if x>>i&1)
    for t in P:orbit.add(tuple(sorted(pi(x)^t for x in CANON)))
assert orbit==codes
maps=[]
for code in sorted(codes):
    t=code[0];a,b=code[1]^t,code[2]^t
    blocks=(a&b,a&~b,b&~a)
    assert all(D.bit_count()==2 for D in blocks)
    dirs=[i for D in blocks for i in range(6) if D>>i&1]
    def iso(x):return sum(1<<j for j,i in enumerate(dirs) if (x^t)>>i&1)
    assert tuple(sorted(iso(x) for x in code))==CANON
    assert len({iso(x) for x in range(64)})==64
    assert {edge(iso(x),iso(y)) for x,y in EDGES}==EDGES
    maps.append({'code':code,'translation':t,'ordered_original_directions':dirs})
rows=[];allowed={};forced={};attempted=0
for x in P:
    if x in CANON:continue
    options=[]
    for m in range(64):
        attempted+=1
        actual=base|star(x,m)
        if not any(q<=actual for q in SQUARES):options.append(m)
    fours=[m for m in options if m.bit_count()==4]
    maximum=max(m.bit_count() for m in options)
    if fours:
        assert len(fours)==4
        F=63
        for m in fours:F&=m
        assert F.bit_count()==2;forced[x]=F
    allowed[x]=options
    rows.append({'vertex':x,'allowed_masks':options,'degree_histogram':dict(sorted(Counter(m.bit_count() for m in options).items())),'maximum_degree':maximum,'degree4_masks':fours,'forced_pair':forced.get(x)})
assert attempted==28*64==1792
assert [r['vertex'] for r in rows if r['maximum_degree']==3]==[3,12,48,63]
assert len(forced)==24 and all(r['maximum_degree']<=4 for r in rows)
pairs=[];covered=set();cross=0
for u,D in sorted(forced.items()):
    v=u^D
    assert v in forced and forced[v]==D
    if u>v:continue
    assert u not in covered and v not in covered
    covered.update([u,v]);paircross=[]
    directions=[i for i in range(6) if D>>i&1]
    i,j=directions;a=u^(1<<i);b=u^(1<<j)
    common_square={edge(u,a),edge(u,b),edge(v,a),edge(v,b)}
    assert common_square in SQUARES
    for m in allowed[u]:
        if m.bit_count()!=4:continue
        for n in allowed[v]:
            if n.bit_count()!=4:continue
            assert common_square<=star(u,m)|star(v,n)
            paircross.append([m,n]);cross+=1
    assert len(paircross)==16
    pairs.append({'roots':[u,v],'forced_pair':D,'literal_common_square':sorted(common_square),'degree4_cross_patterns':paircross})
assert len(pairs)==12 and covered==set(forced) and cross==192
old=json.loads((W/'proofs/q6_four_full_capacity_cycle010/PAIR_CHECK.json').read_text())
for r,s in zip(rows,old['local_root_options']):
    for key in ['vertex','maximum_degree','degree4_masks','forced_pair']:assert r[key]==s[key]
    assert {str(k):v for k,v in r['degree_histogram'].items()}==s['degree_histogram']
assert {tuple(p['roots'])+(p['forced_pair'],) for p in pairs}=={tuple(p['roots'])+(p['forced_directions_mask'],) for p in old['actual_forced_pairs']}
assert all(comb(d,3)+int(d<=2)==1+3*int(d==4) for d in range(5))
# Recompute every caller-local cap for all L, c and residue-compatible S.
caller_caps=[]
for L in range(33):
    t=([0,1,5][L] if L<=2 else {0:6,1:4,2:5}[L%3])
    for c in range(5):
        ss=[s for s in range(161) if (s-(32-L+c))%3==0]
        if L<=2:ss=[s for s in ss if 2*s+c<=316+[0,1,5][L]]
        if c==3:ss=[s for s in ss if s+L<=158]
        if c==4:ss=[s for s in ss if s+L<=144]
        assert all(2*s+c<=316+t for s in ss)
        caller_caps.append({'L':L,'c':c,'t_star':t,'max_allowed_2S_c':max((2*s+c for s in ss),default=None),'bound':316+t})
out={'status':'PASS','scope':'exactly four full specified-parity Q6 roots imply S+L<=144; no opposite restrictions; no graph census','four_full_codes':120,'orbit_isometries_enumerated':23040,'common_isometry_per_code':maps,'local_stars_tested':attempted,'local_allowed_rows':rows,'forced_pairs':pairs,'cross_patterns_tested':cross,'degree4_count_cap':12,'conclusion':'S+L=80+28+3N4<=144','historical_pair_receipt_compared':True,'caller_local_caps':caller_caps,'all_current_C01_local_imports_closed_with_parent_audit':True,'original_main_goal':'OPEN','checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(HERE/'FRESH_FOUR_FULL_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['common_isometry_per_code','local_allowed_rows','forced_pairs','caller_local_caps']},indent=2))
