#!/usr/bin/env python3
"""Exact import replay and marked local checks for the two-low extension."""
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


def edge(a,b):
    return tuple(sorted((a,b)))


def square_at(root,pair):
    i,j=pair
    a=root^(1<<i); b=root^(1<<j); opp=root^(1<<i)^(1<<j)
    return {edge(root,a),edge(root,b),edge(a,opp),edge(b,opp)}


def sha(p):
    return sha256(p.read_bytes()).hexdigest()


def main():
    sys.path.insert(0,str(SOURCE))
    from rebuild_degree_cnf import audit
    pref=SOURCE/'results/q6_code_degree_4_score18_low2'
    cnf=pref.with_suffix('.cnf'); proof=pref.with_suffix('.drat')
    rebuilt=audit(cnf,'4',score=18,low_two=2)
    assert rebuilt=={'variables':1612,'clauses':6132,'independently_rebuilt':True}
    start=time.monotonic()
    p=subprocess.run([str(CHECKER),str(cnf),str(proof)],capture_output=True,text=True)
    elapsed=time.monotonic()-start
    (HERE/'two_low_rup.stdout.txt').write_text(p.stdout)
    (HERE/'two_low_rup.stderr.txt').write_text(p.stderr)
    assert p.returncode==0,(p.returncode,p.stdout,p.stderr)
    result=json.loads(p.stdout)
    assert result['valid'] and result['final_empty_clause']
    assert result['verified_additions']==2801
    pairs=list(combinations(range(6),2))
    forced_square_checks=0
    swap_square_checks=0
    for i,j in pairs:
        v=(1<<i)|(1<<j)
        base={edge((1<<a)|(1<<b),1<<a) for a,b in pairs}
        base|={edge((1<<a)|(1<<b),1<<b) for a,b in pairs}
        assert len(base)==30
        for k in range(6):
            if k in (i,j):
                continue
            forced=set(base)
            for E in ((j,k),(i,k)):
                q=square_at(v,E)
                forced|={e for e in q if v not in e}
            p1=(1<<i)|(1<<k);p2=(1<<j)|(1<<k)
            common1=1<<k;common2=v|(1<<k)
            witness={edge(p1,common1),edge(p2,common1),
                     edge(p1,common2),edge(p2,common2)}
            assert witness<=forced
            assert witness==square_at(common1,(i,j))
            forced_square_checks+=1
        D=(i,j)
        for E in pairs:
            if E==D:
                continue
            # The final u-square is D. At least one v-side edge is absent.
            final_v={edge(v,v^(1<<k)) for k in E}
            remote_u={e for e in square_at(0,D) if 0 not in e}
            assert not remote_u<=final_v
            # The only potentially new v-square is E; its remote edges do
            # not touch u because its opposite root differs from u.
            remote_v={e for e in square_at(v,E) if v not in e}
            assert all(0 not in e for e in remote_v)
            swap_square_checks+=1
    assert forced_square_checks==60 and swap_square_checks==210
    rows=[]
    for c in range(5):
        cap=157 if c==4 else 160
        s=max(k for k in range(cap+1) if (k-30-c)%3==0)
        rows.append({'c':c,'S':s,'weighted':2*s+c})
    assert [r['S'] for r in rows]==[159,160,158,159,157]
    assert max(r['weighted'] for r in rows)==321
    out={'status':'PASS','historical_input':rebuilt,
         'cnf_sha256':sha(cnf),'proof_sha256':sha(proof),
         'strict_replay':{'returncode':p.returncode,'seconds':elapsed,'result':result,
                          'checker_binary_sha256':sha(CHECKER),'checker_source_sha256':sha(CHECKER.with_suffix('.cpp'))},
         'forced_square_checks':forced_square_checks,
         'simultaneous_replacement_markings':swap_square_checks,
         'integer_rows':rows,'source_sha256':sha(Path(__file__))}
    (HERE/'TWO_LOW_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':
    main()
