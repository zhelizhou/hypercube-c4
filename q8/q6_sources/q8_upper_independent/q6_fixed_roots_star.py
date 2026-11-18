"""Test a prescribed near-maximal star count with full Q6 roots fixed."""
from itertools import combinations
from pathlib import Path
import json
import subprocess
import sys
from pysat.card import CardEnc,EncType
from cube import Cube

ROOT=Path(__file__).resolve().parent
code=sys.argv[1];target=int(sys.argv[2]);assert target<=160
roots={'2d4':(0,15),'2d6':(0,63),'3':(0,15,51),'4':(0,15,51,60)}[code]
q=Cube(6);nv=192;clauses=[[-(e+1) for e in face] for face in q.squares]
for v in range(64):
    if v.bit_count()%2:continue
    if v in roots:clauses += [[e+1] for e in q.incident[v]]
    else:
        clauses += [[e+1 for e in group] for group in combinations(q.incident[v],4)]
        clauses.append([-(e+1) for e in q.incident[v]])
face_stars=[]
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
        face_stars.append(stars)
holes=[]
for stars in face_stars:
    nv+=1;holes.append(nv)
    clauses.append([nv]+stars)
    clauses += [[-nv,-s] for s in stars]
card=CardEnc.equals(holes,160-target,top_id=nv,encoding=EncType.seqcounter)
clauses+=card.clauses;nv=card.nv
prefix=ROOT/'results'/f'q6_roots{code}_star{target}'
cnf=prefix.with_suffix('.cnf');trace=prefix.with_suffix('.drat')
cnf.write_text(f'p cnf {nv} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses))
with prefix.with_suffix('.log').open('w') as log:
    run=subprocess.run(['/tmp/cadical-master/build/cadical','-t','90','--no-binary',str(cnf),str(trace)],stdout=log,stderr=subprocess.STDOUT)
result={'full_roots':roots,'target_stars':target,'other_specified_side_degrees':[3,5],
        'status':{10:'SAT',20:'UNSAT',0:'UNKNOWN'}.get(run.returncode,'ERROR'),'checked_proof':False}
if run.returncode==10:
    positive={int(x) for line in prefix.with_suffix('.log').read_text().splitlines() if line.startswith('v ') for x in line.split()[1:] if int(x)>0}
    result['edges']=[e for i,e in enumerate(q.edges,1) if i in positive]
if run.returncode!=20:
    result['discarded_noncertificate_bytes']=trace.stat().st_size if trace.exists() else 0
    trace.unlink(missing_ok=True)
prefix.with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='edges'}),flush=True)
