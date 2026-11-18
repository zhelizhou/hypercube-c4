"""Probe S=159 with one degree-two vertex and all other parity degrees >=3."""
from itertools import combinations
from pathlib import Path
import json
import subprocess
import sys
from cube import Cube

ROOT=Path(__file__).resolve().parent
free=int(sys.argv[1]);base_hole=int(sys.argv[2]);assert free.bit_count()==3 and not free&base_hole
use_six_count=len(sys.argv)>3 and sys.argv[3]=='two-six'
q=Cube(6);nv=192
clauses=[[-(e+1) for e in face] for face in q.squares]
for v in range(64):
    if v.bit_count()%2:continue
    if v==0:
        for i in range(6):
            e=q.index[(0,1<<i)]+1;clauses.append([e if i<2 else -e])
    else:clauses += [[e+1 for e in group] for group in combinations(q.incident[v],4)]
for directions in combinations(range(6),3):
    mask=sum(1<<i for i in directions)
    for base in range(64):
        if base&mask:continue
        stars=[]
        for sub in range(64):
            if sub&~mask:continue
            v=base|sub
            if v.bit_count()%2:continue
            nv+=1;stars.append(nv)
            ee=[q.index[tuple(sorted((v,v^(1<<i))))]+1 for i in directions]
            clauses += [[-nv,e] for e in ee]
            clauses.append([nv]+[-e for e in ee])
        if (mask,base)==(free,base_hole):clauses += [[-s] for s in stars]
        else:clauses.append(stars)
if use_six_count:
    # In a purported counterexample, S=159 and one degree-2 root imply
    # c6=2 (mod3); full-degree roots are a distance-four code of size <=4.
    # Hence c6=2 exactly. This is a proved necessary condition, not a filter
    # selected from observed examples.
    from pysat.card import CardEnc,EncType
    full=[]
    for v in range(1,64):
        if v.bit_count()%2:continue
        nv+=1;z=nv;full.append(z)
        ee=[e+1 for e in q.incident[v]]
        clauses += [[-z,e] for e in ee]
        clauses.append([z]+[-e for e in ee])
    card=CardEnc.equals(full,2,top_id=nv,encoding=EncType.seqcounter)
    clauses+=card.clauses;nv=card.nv
prefix=ROOT/'results'/f'q6_low2_hole_m{free}_b{base_hole}{"_six2" if use_six_count else ""}'
cnf=prefix.with_suffix('.cnf');trace=prefix.with_suffix('.drat')
cnf.write_text(f'p cnf {nv} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses))
with prefix.with_suffix('.log').open('w') as log:
    run=subprocess.run(['/tmp/cadical-master/build/cadical','-t','90','--no-binary',str(cnf),str(trace)],stdout=log,stderr=subprocess.STDOUT)
result={'special_degree':2,'hole_free_mask':free,'hole_base':base_hole,'target_stars':159,
        'status':{10:'SAT',20:'UNSAT',0:'UNKNOWN'}.get(run.returncode,'ERROR'),'checked_proof':False}
result['deduced_six_count']=2 if use_six_count else None
if run.returncode==10:
    positive={int(x) for line in prefix.with_suffix('.log').read_text().splitlines() if line.startswith('v ') for x in line.split()[1:] if int(x)>0}
    result['edges']=[e for i,e in enumerate(q.edges,1) if i in positive]
if run.returncode!=20:
    result['discarded_noncertificate_bytes']=trace.stat().st_size if trace.exists() else 0
    trace.unlink(missing_ok=True)
prefix.with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='edges'}),flush=True)
