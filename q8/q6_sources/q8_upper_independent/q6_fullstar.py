"""Q6 parity full-star saturation with min degree >=3 and a full-degree root.

If S=160 on that parity and degrees lie in 3..6, the number of degree-six
vertices is 2 mod 3. Such vertices form a distance-four code, of size <=4 by
the pairwise-distance bound. Hence there are exactly two, at distance 4 or 6.
This generator covers both cases, without constraints on the other parity.
"""
from itertools import combinations
from pathlib import Path
import json
import subprocess
from cube import Cube

ROOT = Path(__file__).resolve().parent
q = Cube(6)
for distance, other in [(4,15),(6,63)]:
    clauses = [[-(e+1) for e in square] for square in q.squares]
    nv = 192
    for v in range(64):
        if v.bit_count() % 2:
            continue
        if v in (0,other):
            clauses += [[e+1] for e in q.incident[v]]
        else:
            clauses += [[e+1 for e in group] for group in combinations(q.incident[v],4)]
            clauses.append([-(e+1) for e in q.incident[v]])
    for directions in combinations(range(6),3):
        mask = sum(1 << i for i in directions)
        for base in range(64):
            if base & mask:
                continue
            stars = []
            for sub in range(64):
                if sub & ~mask:
                    continue
                v = base | sub
                if v.bit_count() % 2:
                    continue
                nv += 1
                stars.append(nv)
                edges = [q.index[tuple(sorted((v,v^(1<<i))))]+1 for i in directions]
                clauses += [[-nv,e] for e in edges]
                clauses.append([nv]+[-e for e in edges])
            clauses.append(stars)
    assert nv == 832
    prefix = ROOT/'results'/f'q6_fullstar_d{distance}'
    cnf = prefix.with_suffix('.cnf')
    cnf.write_text(f'p cnf {nv} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses))
    with prefix.with_suffix('.log').open('w') as log:
        proc = subprocess.run(['/tmp/cadical-master/build/cadical','-t','60','--no-binary',str(cnf),str(prefix.with_suffix('.drat'))],stdout=log,stderr=subprocess.STDOUT)
    result = {'distance':distance,'root2':other,'returncode':proc.returncode,'variables':nv,'clauses':len(clauses),
              'status': {10:'SAT',20:'UNSAT',0:'UNKNOWN'}.get(proc.returncode,'ERROR'),
              'checked_proof':False}
    prefix.with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result),flush=True)
