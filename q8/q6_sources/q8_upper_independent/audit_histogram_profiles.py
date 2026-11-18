"""Rebuild exact-profile CNFs without importing their generator or a solver."""
from collections import Counter
from itertools import combinations
from pathlib import Path
import hashlib
import json
import subprocess
from rebuild_local_cnf import atmost, exactly, read_cnf

ROOT = Path(__file__).resolve().parent
CASES = ['q6_hist_M124_3_cQ3_b12_12', 'q6_hist_M125_3_cQ2_b10_13',
         'q6_hist_M131_1_cQ0_b2_4_neighbors2']


def rebuild(spec):
    edges = [(u,v) for u in range(64) for v in range(u+1,64)
             if (u^v).bit_count() == 1]
    ids = {e: i+1 for i,e in enumerate(edges)}
    inc = {v: [i+1 for i,e in enumerate(edges) if v in e] for v in range(64)}
    squares = set()
    for u in range(64):
        for w in range(u+1,64):
            if (u^w).bit_count() != 2:
                continue
            middle = [v for v in range(64) if (u^v).bit_count() == (w^v).bit_count() == 1]
            squares.add(tuple(sorted(ids[tuple(sorted(e))] for v in middle
                                     for e in [(u,v),(w,v)])))
    assert len(squares) == 240
    clauses = [[-e for e in row] for row in squares]
    top = 192
    t = {}
    roots = spec['roots']
    for v in range(64):
        if v in roots:
            clauses.extend([[e] for e in inc[v]])
        else:
            clauses.extend(map(list, combinations(inc[v],4)))
            if v.bit_count()%2 == 0:
                clauses.append([-e for e in inc[v]])
        for r in [4,5,6]:
            top += 1
            t[v,r] = top
            clauses.extend([[-top]+list(row) for row in combinations(inc[v],7-r)])
            clauses.extend([[top]+[-e for e in row] for row in combinations(inc[v],r)])
    for parity in range(2):
        V = [v for v in range(64) if v.bit_count()%2 == parity]
        for inputs,k in [([-t[v,4] for v in V],spec['b3'][parity]),
                         ([t[v,5] for v in V],spec['n5'][parity]+spec['c'][parity]),
                         ([t[v,6] for v in V],spec['c'][parity])]:
            rows,top = exactly(inputs,k,top)
            clauses.extend(rows)
    for v in range(64):
        inputs = [t[v^(1<<i),r] for i in range(6) for r in [4,5,6]]
        rows,top = atmost(inputs,3,top)
        clauses.extend([[-t[v,6]]+row for row in rows])
    if 'root_neighbor_case' in spec:
        assert spec['root_neighbor_case'] == 2
        pattern = [3,3,3,3,5,4]
        for i,d in enumerate(pattern):
            for r in [4,5,6]:
                clauses.append([t[1<<i,r] if d>=r else -t[1<<i,r]])
    return top, Counter(tuple(sorted(row)) for row in clauses)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--case', type=int, choices=range(3))
    args = parser.parse_args()
    summaries = {}
    for index,name in enumerate(CASES):
        if args.case is not None and args.case != index:
            continue
        p = ROOT/'results'/name
        spec = json.loads(p.with_suffix('.json').read_text())
        assert spec['status'] == 'UNSAT'
        expected = rebuild(spec)
        assert expected == read_cnf(p.with_suffix('.cnf'))
        if args.check:
            run = subprocess.run(['/tmp/q8-independent-check-rup-active',
                                  str(p.with_suffix('.cnf')),str(p.with_suffix('.drat'))],
                                 text=True,capture_output=True,check=True)
            result = json.loads(run.stdout)
            assert result['valid'] and result['final_empty_clause']
            result.update(independently_rebuilt=True,
                          cnf_sha256=hashlib.sha256(p.with_suffix('.cnf').read_bytes()).hexdigest(),
                          proof_sha256=hashlib.sha256(p.with_suffix('.drat').read_bytes()).hexdigest(),
                          checker_sha256=hashlib.sha256((ROOT/'check_rup_active.cpp').read_bytes()).hexdigest())
            p.with_suffix('.checked.json').write_text(json.dumps(result,indent=2)+'\n')
            spec['proof_checked'] = True
            p.with_suffix('.json').write_text(json.dumps(spec,indent=2)+'\n')
        summaries[name] = {'variables': expected[0], 'clauses': sum(expected[1].values()),
                           'independently_rebuilt': True,
                           'proof_checked': spec['proof_checked']}
    print(json.dumps(summaries))


if __name__ == '__main__':
    main()
