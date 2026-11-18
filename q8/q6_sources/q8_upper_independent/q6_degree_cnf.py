"""Compact degree-threshold CNFs: full-code gaps and a coupled Q6 probe.

All asserted cuts are from this independent branch. SAT is a counterexample;
UNSAT is only a solver report until its trace is checked independently.
"""
import argparse
from itertools import combinations
import json
from pathlib import Path
import subprocess
import time
from pysat.card import CardEnc, EncType
from pysat.formula import CNF, IDPool
from cube import Cube

ROOT=Path(__file__).resolve().parent
ap=argparse.ArgumentParser()
ap.add_argument('code',choices=['1','2d4','2d6','3','4'])
ap.add_argument('--opposite-six',type=int)
ap.add_argument('--score',type=int)
ap.add_argument('--seconds',type=int,default=120)
ap.add_argument('--neighbor-case',type=int,choices=range(6))
ap.add_argument('--sharp-code-cuts',action='store_true')
ap.add_argument('--six-coefficient',type=int,choices=[2,3],default=3)
ap.add_argument('--forbidden-potential',type=int,default=533)
ap.add_argument('--low-two',type=int,default=0)
ap.add_argument('--opposite-minimum',type=int,default=0,choices=range(7))
args=ap.parse_args()
roots={'1':(0,),'2d4':(0,15),'2d6':(0,63),'3':(0,15,51),'4':(0,15,51,60)}[args.code]
q=Cube(6);f=CNF();pool=IDPool(start_from=193)
for face in q.squares:f.append([-e-1 for e in face])
threshold={};weighted=[[],[]];six=[[],[]]
coupled=args.opposite_six is not None
for v in range(64):
    parity=v.bit_count()%2
    inc=[e+1 for e in q.incident[v]]
    if not coupled and parity:
        if args.opposite_minimum:
            for group in combinations(inc,7-args.opposite_minimum):f.append(list(group))
        continue
    if v in roots:
        for e in inc:f.append([e])
    else:
        for group in combinations(inc,5 if args.low_two else 4):f.append(list(group))
        if not parity or (coupled and args.opposite_six==0):f.append([-e for e in inc])
    for r in ([3,4,5,6] if args.low_two else [4,5,6]):
        z=pool.id();threshold[v,r]=z
        # z iff at least r incident edges are selected.
        for group in combinations(inc,7-r):f.append([-z]+list(group))
        for group in combinations(inc,r):f.append([z]+[-e for e in group])
    weighted[parity].extend([threshold[v,4],threshold[v,5],threshold[v,5]])
    six[parity].append(threshold[v,6])

def card(literals,bound,kind):
    method=getattr(CardEnc,kind)
    f.extend(method(literals,bound=bound,vpool=pool,encoding=EncType.seqcounter).clauses)

if coupled:
    cP,cQ=len(roots),args.opposite_six
    card(six[1],cQ,'equals')
    # Checked S<=158 and 2S+c6<=316, with S=32+3H+10c6.
    for parity,c in [(0,cP),(1,cQ)]:
        cap=min((126-10*c)//3,(84-7*c)//2)
        if args.sharp_code_cuts:cap=min(cap,[42,38,35,30,24][c])
        card(weighted[parity],cap,'atmost')
    # 4m+N3+k*N6 = 448+H_P+H_Q+(k+2)*(cP+cQ).
    forbidden_H=args.forbidden_potential-448-(args.six_coefficient+2)*(cP+cQ)
    card(weighted[0]+weighted[1],forbidden_H,'atleast')
    # C4-freeness around a full root implies sum neighbor degrees <=21.
    for v in range(64):
        neighbors=[v^(1<<i) for i in range(6)]
        increments=[threshold[u,r] for u in neighbors for r in [4,5,6]]
        cnf=CardEnc.atmost(increments,bound=3,vpool=pool,encoding=EncType.seqcounter)
        f.extend([[-threshold[v,6]]+c for c in cnf.clauses])
    name=f'q6_coupled_degree_{args.code}_{cQ}'
    target={'potential':f'4m+N3+{args.six_coefficient}N6','forbidden_minimum':args.forbidden_potential,'opposite_six':cQ}
    if args.six_coefficient!=3 or args.forbidden_potential!=533:name+=f'_coef{args.six_coefficient}_target{args.forbidden_potential}'
    if args.sharp_code_cuts:
        caps=[42,38,35,30,24]
        for p,c,other in [(0,cP,cQ),(1,cQ,cP)]:
            card(weighted[p],forbidden_H-caps[other],'atleast')
        name+='_sharp';target['sharp_code_cuts']=True
    if args.neighbor_case is not None:
        assert args.code=='1' and cQ==0
        assert args.six_coefficient==3 and args.forbidden_potential==533
        patterns=[(3,3,3,3,3,3),(4,3,3,3,3,3),(5,3,3,3,3,3),
                  (4,4,3,3,3,3),(5,4,3,3,3,3),(4,4,4,3,3,3)]
        pattern=patterns[args.neighbor_case]
        for i,degree in enumerate(pattern):
            for r in [4,5,6]:f.append([threshold[1<<i,r] if degree>=r else -threshold[1<<i,r]])
        # The existing upper bounds sum exactly to the forbidden lower bound.
        # Thus in this cP=1,cQ=0 family H_P=38 and H_Q=42.
        card(weighted[0],38,'atleast');card(weighted[1],42,'atleast')
        target['root_neighbor_degrees']=pattern
        name+=f'_neighbors{args.neighbor_case}'
else:
    assert args.score is not None
    if args.low_two:
        card([-threshold[v,3] for v in range(64) if not v.bit_count()%2 and v not in roots],args.low_two,'equals')
    # The root contributions are constant. Count H only at the other roots.
    literal_score=[]
    for v in range(64):
        if v.bit_count()%2==0 and v not in roots:
            literal_score.extend([threshold[v,4],threshold[v,5],threshold[v,5]])
    card(literal_score,args.score,'atleast')
    name=f'q6_code_degree_{args.code}_score{args.score}'
    target={'nonroot_H_minimum':args.score,'forbidden_stars_minimum':32+19*len(roots)+3*args.score-args.low_two}
    if args.low_two:name+=f'_low{args.low_two}';target['degree_two_count']=args.low_two
    if args.opposite_minimum:name+=f'_oppmin{args.opposite_minimum}';target['opposite_minimum']=args.opposite_minimum
prefix=ROOT/'results'/name
f.to_file(str(prefix)+'.cnf')
t=time.monotonic()
with Path(str(prefix)+'.log').open('w') as out:
    p=subprocess.run(['/tmp/cadical-master/build/cadical','-t',str(args.seconds),'--no-binary',str(prefix)+'.cnf',str(prefix)+'.drat'],stdout=out,stderr=subprocess.STDOUT)
result={'status':{10:'SAT',20:'UNSAT'}.get(p.returncode,'UNKNOWN'),
        'roots':roots,'minimum_degree':'both_sides_3' if coupled else 'specified_side_3',
        'target':target,'seconds':time.monotonic()-t,'variables':f.nv,'clauses':len(f.clauses),'proof_checked':False}
if args.low_two:result['minimum_degree']='specified_side_2_except_fixed_full_roots';result['degree_two_count']=args.low_two
if p.returncode==10:
    positive={int(s) for line in Path(str(prefix)+'.log').read_text().splitlines() if line.startswith('v ') for s in line[2:].split() if int(s)>0}
    result['edges']=[list(e) for i,e in enumerate(q.edges,1) if i in positive]
if p.returncode!=20:Path(str(prefix)+'.drat').unlink(missing_ok=True)
Path(str(prefix)+'.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='edges'}),flush=True)
