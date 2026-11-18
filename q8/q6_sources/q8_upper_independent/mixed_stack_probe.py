"""Restricted mixed-seed test; every output is independently checked.

Absence of a counterexample in these 21 families is not a universal proof.
"""
from itertools import combinations
from pathlib import Path
import hashlib
import json
import subprocess
from verify_examples import inspect

ROOT = Path(__file__).resolve().parent
SEEDS = ['q6_seed', 'q6_hist_M130_1_cQ1_b4_4_qroot7',
         'q6_hist_M130_1_cQ1_b4_4_qroot31', 'q6_degree_potential_2d4',
         'q6_positive_defect', 'q6_code_degree_3_score21_oppmin3',
         'q6_code_degree_4_score12_oppmin3']


def main():
    edges = [(v,v^(1<<i)) for v in range(64) for i in range(6) if not v>>i&1]
    inputs = {}
    for name in SEEDS:
        p = ROOT/'results'/(name+'.mask')
        mask = list(map(int,p.read_text().split()))
        assert len(mask) == 192 and set(mask) <= {0,1}
        checked, degrees = inspect(6,[e for e,b in zip(edges,mask) if b])
        assert min(degrees) >= 3
        inputs[name] = dict(checked, sha256=hashlib.sha256(p.read_bytes()).hexdigest())
    cases = {}
    for i,j in combinations(range(len(SEEDS)),2):
        p = ROOT/'results'/f'parity_mixed_seed{i}_{j}.json'
        run = subprocess.run(['/tmp/q6-stack-parity-mixed',
                              str(ROOT/'results'/(SEEDS[i]+'.mask')),
                              str(ROOT/'results'/(SEEDS[j]+'.mask')),str(p)],
                             capture_output=True,text=True,check=True)
        data = json.loads(p.read_text())
        checked, degrees = inspect(7,data['edges'])
        P = [v for v in range(128) if v.bit_count()%2 == 0]
        assert min(degrees[v] for v in P) >= 4
        score = checked['edges']+sum(degrees[v] == 6 for v in P)
        score += 3*sum(degrees[v] == 7 for v in P)
        assert score == data['best_parity_score']
        if score <= 304:
            assert data['automorphisms_checked'] == 46080
        cases[f'{i}_{j}'] = {'inputs': [SEEDS[i],SEEDS[j]],
                              'automorphisms_checked': data['automorphisms_checked'],
                              'best_parity_score': score, 'witness_check': checked,
                              'output_sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
        print(json.dumps({'case':[i,j],'score':score,'edges':checked['edges']}),flush=True)
        if score > 304:
            break
    result = {'status':'PASS','meaning':'restricted-family search only',
              'inputs':inputs,'families':cases,
              'automorphic_pairs_tested':sum(v['automorphisms_checked'] for v in cases.values()),
              'counterexample_found':any(v['best_parity_score']>304 for v in cases.values()),
              'universal_inequality_proved':False,
              'source_sha256':hashlib.sha256((ROOT/'q6_stack_parity.cpp').read_bytes()).hexdigest()}
    (ROOT/'results/mixed_stack_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','automorphic_pairs_tested',
                                          'counterexample_found','universal_inequality_proved']}))


if __name__ == '__main__':
    main()
