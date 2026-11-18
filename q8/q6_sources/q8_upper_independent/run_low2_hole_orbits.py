"""Complete symmetry cover for the unique degree-two, one-hole Q6 problem."""
from concurrent.futures import ThreadPoolExecutor
from itertools import permutations
from pathlib import Path
import json
import os
import subprocess
import threading

ROOT=Path(__file__).resolve().parent


def permute(v,p):return sum(1<<p[i] for i in range(6) if v>>i&1)


def main():
    group=[p for p in permutations(range(6)) if {p[0],p[1]}=={0,1}]
    assert len(group)==48
    unseen={(m,b) for m in range(64) if m.bit_count()==3 for b in range(64) if not m&b}
    cases=[]
    while unseen:
        m,b=min(unseen);orbit={(permute(m,p),permute(b,p)) for p in group}
        assert orbit<=unseen
        cases.append({'mask':m,'base':b,'orbit_size':len(orbit)})
        unseen-=orbit
    assert len(cases)==16 and sum(c['orbit_size'] for c in cases)==160
    (ROOT/'results/q6_low2_hole_orbit_cover.json').write_text(json.dumps(cases,indent=2)+'\n')
    # The three base-zero cases are already running/completed without the
    # deduced-six-count cut. Do not restart any of their live handles.
    pending=[c for c in cases if c['base']!=0]
    assert len(pending)==13
    stopped=threading.Event()
    def run(case):
        if stopped.is_set():return {'status':'not_started_after_counterexample',**case}
        env=os.environ.copy();env['PYTHONPATH']='/tmp/q8-683-deps'
        cmd=['python3',str(ROOT/'q6_low2_onehole.py'),str(case['mask']),str(case['base']),'two-six']
        p=subprocess.run(cmd,env=env,capture_output=True,text=True)
        assert p.returncode==0,(case,p.stderr)
        result=json.loads(p.stdout)
        if result['status']=='SAT':stopped.set()
        print(json.dumps(result),flush=True)
        return result
    with ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(run,pending))
    (ROOT/'results/q6_low2_remaining_orbit_runs.json').write_text(json.dumps(results,indent=2)+'\n')


if __name__=='__main__':main()
