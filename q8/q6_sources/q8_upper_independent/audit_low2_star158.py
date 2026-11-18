"""Seal the unique-degree-two star158 lemma and the three-full-root gap.

Every input is independently reconstructed before checking its actual proof.
The active/history checker is audited separately against naive propagation.
"""
from concurrent.futures import ThreadPoolExecutor
from math import comb
from pathlib import Path
import hashlib
import json
import subprocess
from rebuild_local_cnf import rebuild,read_cnf

ROOT=Path(__file__).resolve().parent
RESULTS=ROOT/'results'
CHECKER='/tmp/q8-independent-check-rup-active'


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def replay(name):
    prefix=RESULTS/name
    output=prefix.with_suffix('.checked_active.json')
    if output.exists():
        checked=json.loads(output.read_text())
        assert checked['valid'] and checked['final_empty_clause']
        assert checked['cnf_sha256']==digest(prefix.with_suffix('.cnf'))
        assert checked['proof_sha256']==digest(prefix.with_suffix('.drat'))
        assert checked['checker_sha256']==digest(ROOT/'check_rup_active.cpp')
        return checked
    r=subprocess.run([CHECKER,str(prefix.with_suffix('.cnf')),str(prefix.with_suffix('.drat'))],capture_output=True,text=True)
    prefix.with_suffix('.check.log').write_text(r.stdout+r.stderr)
    assert r.returncode==0,(name,r.stdout,r.stderr)
    checked=json.loads(r.stdout)
    assert checked['valid'] and checked['final_empty_clause']
    checked.update(cnf_sha256=digest(prefix.with_suffix('.cnf')),
                   proof_sha256=digest(prefix.with_suffix('.drat')),
                   checker_sha256=digest(ROOT/'check_rup_active.cpp'))
    output.write_text(json.dumps(checked,indent=2)+'\n')
    result=json.loads(prefix.with_suffix('.json').read_text());result['checked_proof']=True
    prefix.with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'case':name,**checked}),flush=True)
    return checked


def main():
    audit=json.loads((RESULTS/'history_checker_audit.json').read_text())
    assert audit['differential_cases']==300 and audit['future_clause_trap_rejected']
    cover=json.loads((RESULTS/'q6_low2_hole_orbit_cover.json').read_text())
    types=set()
    names=[]
    for case in cover:
        mask,base=case['mask'],case['base']
        a=(mask&3).bit_count();b=(base&3).bit_count();c=(base&60).bit_count()
        assert (a,b,c) not in types;types.add((a,b,c))
        assert case['orbit_size']==comb(2,a)*comb(4,3-a)*comb(2-a,b)*comb(1+a,c)
        name=f'q6_low2_hole_m{mask}_b{base}_six2'
        expected=rebuild(special=(0,3),fixed_hole=(mask,base),full_count=2)
        assert expected==read_cnf((RESULTS/name).with_suffix('.cnf')),name
        result=json.loads((RESULTS/name).with_suffix('.json').read_text());assert result['status']=='UNSAT'
        names.append(name)
    assert len(types)==16 and sum(c['orbit_size'] for c in cover)==160
    assert types=={(a,b,c) for a in range(3) for b in range(3-a) for c in range(2+a)}
    full='q6_one_low_full_r2'
    assert rebuild(special=(0,3))==read_cnf((RESULTS/full).with_suffix('.cnf'))
    full_report=replay(full)
    root3='q6_roots3_star158'
    assert rebuild(full_roots=(0,15,51),hole_count=2)==read_cnf((RESULTS/root3).with_suffix('.cnf'))
    # Prioritize the additional full-root case, then check all sixteen holes.
    work=[root3]+names
    reports={full:full_report}
    with ThreadPoolExecutor(max_workers=2) as pool:
        reports.update(zip(work,pool.map(replay,work)))
    low2_names=[full]+names
    result={'status':'all inputs independently rebuilt; all required traces RUP checked',
            'unique_degree_two_lemma':'Specified Q6 parity has exactly one degree-2 vertex and all others degree>=3 => star sum<=158.',
            'hole_orbits':cover,'low2_case_count':len(low2_names),
            'low2_verified_additions':sum(reports[n]['verified_additions'] for n in low2_names),
            'three_full_root_lemma':'Minimum degree>=3 on a Q6 parity and exactly three degree-6 roots => star sum<=155.',
            'certificates':reports,'checker_audit':audit}
    (RESULTS/'low2_star158_certificate_manifest.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'low2_cases':len(low2_names),'low2_verified_additions':result['low2_verified_additions']}),flush=True)


if __name__=='__main__':main()
