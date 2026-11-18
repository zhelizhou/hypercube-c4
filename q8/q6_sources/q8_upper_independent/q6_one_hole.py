"""Exactly one degree-six root and exactly one parity-star hole in Q6.

The root is 0. Its stabilizer has three orbits of possible holes, according
to distance 1,2,3 from the root. Free directions are 0,1,2 and bases 8,24,56.
"""
from itertools import combinations
from pathlib import Path
import json
import subprocess
import sys
from cube import Cube

ROOT=Path(__file__).resolve().parent
base_hole=int(sys.argv[1]);assert base_hole in (8,24,56)
q=Cube(6)
clauses=[[-(e+1) for e in face] for face in q.squares]
nv=192
for v in range(64):
    if v.bit_count()%2:continue
    if v==0:clauses += [[e+1] for e in q.incident[v]]
    else:
        clauses += [[e+1 for e in group] for group in combinations(q.incident[v],4)]
        clauses.append([-(e+1) for e in q.incident[v]])
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
            edges=[q.index[tuple(sorted((v,v^(1<<i))))]+1 for i in directions]
            clauses += [[-nv,e] for e in edges]
            clauses.append([nv]+[-e for e in edges])
        if mask==7 and base==base_hole:clauses += [[-s] for s in stars]
        else:clauses.append(stars)
prefix=ROOT/'results'/f'q6_one_hole_b{base_hole}'
cnf=prefix.with_suffix('.cnf');trace=prefix.with_suffix('.drat')
cnf.write_text(f'p cnf {nv} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses))
with prefix.with_suffix('.log').open('w') as log:
    proc=subprocess.run(['/tmp/cadical-master/build/cadical','-t','90','--no-binary',str(cnf),str(trace)],stdout=log,stderr=subprocess.STDOUT)
result={'root':0,'hole_free_mask':7,'hole_base':base_hole,'status':{10:'SAT',20:'UNSAT',0:'UNKNOWN'}.get(proc.returncode,'ERROR'),'checked_proof':False}
if proc.returncode==10:
    lines=prefix.with_suffix('.log').read_text().splitlines()
    positive={int(x) for line in lines if line.startswith('v ') for x in line.split()[1:] if int(x)>0}
    result['edges']=[e for i,e in enumerate(q.edges,1) if i in positive]
if proc.returncode!=20:
    result['discarded_noncertificate_bytes']=trace.stat().st_size if trace.exists() else 0
    trace.unlink(missing_ok=True)
prefix.with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='edges'}),flush=True)
