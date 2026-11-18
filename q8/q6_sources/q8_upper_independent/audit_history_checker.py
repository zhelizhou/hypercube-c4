"""Audit active/history RUP checking, including deletion and chronology traps."""
from pathlib import Path
import json
import random
import subprocess
import tempfile
from audit_rup import naive_rup

ROOT=Path(__file__).resolve().parent
CHECKER='/tmp/q8-independent-check-rup-active'


def run(tmp,n,clauses,proof):
    cnf=tmp/'a.cnf';drat=tmp/'a.drat'
    cnf.write_text(f'p cnf {n} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses))
    drat.write_text('\n'.join(proof)+'\n')
    return subprocess.run([CHECKER,str(cnf),str(drat)],capture_output=True,text=True)


def main():
    rng=random.Random(28519);counts={'RUP':0,'non_RUP':0}
    with tempfile.TemporaryDirectory(prefix='q8-history-audit-') as tmp:
        tmp=Path(tmp)
        for test in range(300):
            n=rng.randrange(3,8);clauses=[]
            for _ in range(rng.randrange(2,15)):
                c=[v if rng.randrange(2) else -v for v in rng.sample(range(1,n+1),rng.randrange(1,min(4,n)+1))]
                clauses.append(c)
            prefix=[];proof=[]
            for _ in range(12):
                c=list(rng.choice(clauses));extra=rng.choice([-1,1])*rng.randrange(1,n+1)
                if extra not in c:c.append(extra)
                assert naive_rup(clauses+prefix,c)
                prefix.append(c);proof.append(' '.join(map(str,c))+' 0')
                if rng.randrange(2):proof.append('d '+' '.join(map(str,c))+' 0')
            target=[v if rng.randrange(2) else -v for v in rng.sample(range(1,n+1),rng.randrange(n+1))]
            expected=naive_rup(clauses+prefix,target);proof.append(' '.join(map(str,target))+' 0')
            result=run(tmp,n,clauses,proof)
            assert (result.returncode in (0,10))==expected,(test,result.stdout,result.stderr)
            counts['RUP' if expected else 'non_RUP']+=1
        axioms=[[1,2,3],[1,2,-3],[1,-2,4],[1,-2,-4],[-1]]
        proof=['1 2 0','1 -2 0','d 1 2 0','d 1 -2 0','0']
        result=run(tmp,4,axioms,proof)
        assert result.returncode==0,(result.stdout,result.stderr)
        restoration=json.loads(result.stdout)
        assert restoration['history_fallbacks']>=1 and restoration['restored_prior_reasons']>=1
        circular=run(tmp,4,axioms,['0','1 2 0','1 -2 0'])
        assert circular.returncode==1,'A future proof clause was used before it was checked.'
    result={'differential_cases':300,'valid_prefix_additions':3600,'outcomes':counts,
            'deleted_reason_restoration':restoration,'future_clause_trap_rejected':True}
    (ROOT/'results/history_checker_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result),flush=True)


if __name__=='__main__':main()
