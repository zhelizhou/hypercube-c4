"""Probe S=159 on a Q6 parity of minimum degree >=3.

Its degree-six count is 1 mod 3 and at most 4: cases 1 and 4. Four such roots
form the unique size-four distance-four code in length six, up to symmetry.
"""
from itertools import combinations
from pathlib import Path
import json
import subprocess
from pysat.card import CardEnc, EncType
from cube import Cube

ROOT=Path(__file__).resolve().parent
q=Cube(6)
for roots in [(0,), (0,15,51,60)]:
    clauses=[[-(e+1) for e in face] for face in q.squares]
    nv=192
    for v in range(64):
        if v.bit_count()%2:continue
        if v in roots:
            clauses += [[e+1] for e in q.incident[v]]
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
                edges=[q.index[tuple(sorted((v,v^(1<<i))))]+1 for i in directions]
                clauses += [[-nv,e] for e in edges]
                clauses.append([nv]+[-e for e in edges])
            face_stars.append(stars)
    holes=[]
    for stars in face_stars:
        nv+=1;holes.append(nv)
        clauses.append([nv]+stars)
        clauses += [[-nv,-s] for s in stars]
    clauses.append(holes)
    card=CardEnc.atmost(holes,1,top_id=nv,encoding=EncType.seqcounter)
    clauses+=card.clauses;nv=card.nv
    prefix=ROOT/'results'/f'q6_star159_c{len(roots)}'
    cnf=prefix.with_suffix('.cnf')
    cnf.write_text(f'p cnf {nv} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses))
    with prefix.with_suffix('.log').open('w') as log:
        proc=subprocess.run(['/tmp/cadical-master/build/cadical','-t','90','--no-binary',str(cnf),str(prefix.with_suffix('.drat'))],stdout=log,stderr=subprocess.STDOUT)
    result={'six_roots':roots,'returncode':proc.returncode,'status':{10:'SAT',20:'UNSAT',0:'UNKNOWN'}.get(proc.returncode,'ERROR'),'checked_proof':False}
    if proc.returncode==10:
        lines=prefix.with_suffix('.log').read_text().splitlines()
        positive={int(x) for line in lines if line.startswith('v ') for x in line.split()[1:] if int(x)>0}
        result['edges']=[e for i,e in enumerate(q.edges,1) if i in positive]
    if proc.returncode!=20:
        trace=prefix.with_suffix('.drat')
        result['discarded_noncertificate_bytes']=trace.stat().st_size if trace.exists() else 0
        trace.unlink(missing_ok=True)
    prefix.with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='edges'}),flush=True)
