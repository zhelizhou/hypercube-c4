#!/usr/bin/env python3
"""Read-only reconstruction and strict replay of the one historical import."""
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import json
import subprocess
import sys
import time

HERE=Path(__file__).resolve().parent
SOURCE=Path('q6_sources/q8_upper_independent')
W=Path('/mnt/c/Users/Anony/Desktop/project/research/ex_qn_c4')
CHECKER=W/'proofs/low1_cycle006/orbit_sat/review/direct_rup'
NAME='q6_code_degree_4_score17_low1'


def sha(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    # The imported reconstruction module only defines functions. Its audit
    # returns a comparison and never writes. PYTHONDONTWRITEBYTECODE=1 is used.
    sys.path.insert(0,str(SOURCE))
    from rebuild_degree_cnf import audit
    prefix=SOURCE/'results'/NAME
    cnf=prefix.with_suffix('.cnf')
    proof=prefix.with_suffix('.drat')
    rebuilt=audit(cnf,'4',score=17,low_two=1)
    assert rebuilt=={'variables':1486,'clauses':5905,'independently_rebuilt':True}
    before=time.monotonic()
    run=subprocess.run([str(CHECKER),str(cnf),str(proof)],capture_output=True,text=True)
    seconds=time.monotonic()-before
    (HERE/'import_rup.stdout.txt').write_text(run.stdout)
    (HERE/'import_rup.stderr.txt').write_text(run.stderr)
    assert run.returncode==0,(run.returncode,run.stdout,run.stderr)
    checked=json.loads(run.stdout)
    assert checked['valid'] and checked['final_empty_clause']
    assert checked['verified_additions']==2618

    # Full even-parity code coverage, independently enumerated without quotient.
    even=[v for v in range(64) if v.bit_count()%2==0]
    all_codes=[]
    for code in combinations(even,4):
        if all((a^b).bit_count()>=4 for a,b in combinations(code,2)):
            outside=[v for v in even if v not in code]
            near=[sum((v^c).bit_count()==2 for c in code) for v in outside]
            assert set(near)=={2,3} and near.count(2)==24 and near.count(3)==4
            all_codes.append(code)
    assert len(all_codes)==120
    canonical=(0,15,51,60)
    canonical_near=[{'vertex':v,'distance_two_full_roots':[c for c in canonical if (v^c).bit_count()==2]}
                    for v in even if v not in canonical]
    bounds=[]
    for c in range(5):
        cap=155 if c==4 else 158
        S=max(s for s in range(cap+1) if (s-31-c)%3==0)
        bounds.append({'c6':c,'S_bound':S,'weighted_bound':2*S+c})
    assert [row['S_bound'] for row in bounds]==[157,158,156,157,155]
    assert max(row['weighted_bound'] for row in bounds)==317
    result={'status':'PASS','scope':'one historical CNF reconstructed and strictly replayed; full-root geometry and arithmetic',
            'historical_input':{'name':NAME,'cnf_sha256':sha(cnf),'proof_sha256':sha(proof),'reconstructed':rebuilt},
            'strict_replay':{'returncode':run.returncode,'seconds':seconds,'result':checked,
                             'checker_binary_sha256':sha(CHECKER),'checker_source_sha256':sha(CHECKER.with_suffix('.cpp'))},
            'all_four_full_codes':len(all_codes),'each_code_outside_distance_two_histogram':{'2':24,'3':4},
            'canonical_code':canonical,'canonical_outside_points':canonical_near,
            'one_low_integer_bounds':bounds,
            'source_hashes':{str(SOURCE/name):sha(SOURCE/name) for name in ['REFINEMENT_K3.md','q6_degree_cnf.py','rebuild_degree_cnf.py','rebuild_local_cnf.py']},
            'script_sha256':sha(Path(__file__))}
    (HERE/'IMPORT_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({key:result[key] for key in ['status','historical_input','strict_replay','all_four_full_codes','one_low_integer_bounds']},indent=2))


if __name__=='__main__':
    main()
