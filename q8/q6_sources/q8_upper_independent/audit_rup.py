"""Differential audit of the independent RUP checker and real trace replay."""
import hashlib
import json
from pathlib import Path
import random
import subprocess
import tempfile

ROOT=Path(__file__).resolve().parent
CHECKER='/tmp/q8-independent-check-rup'


def naive_rup(clauses,clause):
    values={}
    for lit in [-x for x in clause]:
        v=abs(lit);s=lit>0
        if v in values and values[v]!=s:return True
        values[v]=s
    changed=True
    while changed:
        changed=False
        for c in clauses:
            if any(abs(x) in values and values[abs(x)]==(x>0) for x in c):continue
            unknown=[x for x in c if abs(x) not in values]
            if not unknown:return True
            if len(unknown)==1:
                x=unknown[0];v=abs(x);s=x>0
                if v in values and values[v]!=s:return True
                if v not in values:values[v]=s;changed=True
    return False


def main():
    rng=random.Random(7491)
    counts={'rup':0,'not_rup':0}
    with tempfile.TemporaryDirectory(prefix='q8-rup-audit-') as tmp:
        tmp=Path(tmp)
        for test in range(300):
            n=rng.randrange(3,8)
            clauses=[]
            for _ in range(rng.randrange(2,16)):
                c=rng.sample(range(1,n+1),rng.randrange(1,min(n,4)+1))
                clauses.append([x if rng.randrange(2) else -x for x in c])
            prefix=[]
            for _ in range(12):
                c=list(rng.choice(clauses))
                extra=rng.randrange(1,n+1)*(1 if rng.randrange(2) else -1)
                if extra not in c:c.append(extra)
                assert naive_rup(clauses+prefix,c)
                prefix.append(c)
            target=[x if rng.randrange(2) else -x for x in rng.sample(range(1,n+1),rng.randrange(n+1))]
            expected=naive_rup(clauses+prefix,target)
            counts['rup' if expected else 'not_rup']+=1
            cnf=tmp/'input.cnf';trace=tmp/'proof.drat'
            cnf.write_text(f'p cnf {n} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses))
            trace.write_text(''.join(' '.join(map(str,c))+' 0\n' for c in prefix+[target]))
            r=subprocess.run([CHECKER,str(cnf),str(trace)],capture_output=True,text=True)
            accepted=r.returncode in (0,10)
            assert accepted==expected, (test,expected,r.returncode,r.stdout,r.stderr)
    replays=[]
    for distance in (4,6):
        prefix=ROOT/'results'/f'q6_fullstar_d{distance}'
        cnf,trace=prefix.with_suffix('.cnf'),prefix.with_suffix('.drat')
        r=subprocess.run([CHECKER,str(cnf),str(trace)],capture_output=True,text=True)
        assert r.returncode==0,(r.stdout,r.stderr)
        checked=json.loads(r.stdout)
        assert checked['valid'] and checked['final_empty_clause']
        checked.update(cnf_sha256=hashlib.sha256(cnf.read_bytes()).hexdigest(),
                       proof_sha256=hashlib.sha256(trace.read_bytes()).hexdigest(),
                       checker_sha256=hashlib.sha256((ROOT/'check_rup.cpp').read_bytes()).hexdigest())
        prefix.with_suffix('.checked.json').write_text(json.dumps(checked,indent=2)+'\n')
        result=json.loads(prefix.with_suffix('.json').read_text())
        result['checked_proof']=True
        prefix.with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
        replays.append(checked)
        print(json.dumps({'distance':distance,**checked}),flush=True)
    result={'differential_cases':300,'valid_prefix_additions':3600,'outcomes':counts,'real_proof_replays':replays}
    (ROOT/'results/rup_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'differential_cases':300,'outcomes':counts}),flush=True)


if __name__=='__main__':main()
