"""Two canonical K=4 cases for two degree-four roots on one parity.

This uses only fresh-branch, checked local lemmas and the permitted Q7 bound.
UNKNOWN does not exclude a case; INFEASIBLE is not a standalone certificate.
"""
from pathlib import Path
import json
import sys
import time
from ortools.sat.python import cp_model
from cube import Cube

ROOT=Path(__file__).resolve().parent
w=int(sys.argv[1]);assert w in (48,240)
manifest=json.loads((ROOT/'results/low2_star158_certificate_manifest.json').read_text())
assert manifest['low2_case_count']==17 and manifest['low2_verified_additions']==4122060
q=Cube(8);m=cp_model.CpModel()
x=[m.new_bool_var(f'e{e}') for e in range(1024)]
for face in q.squares:m.add(sum(x[e] for e in face)<=3)
m.add(sum(x)==688)
d=[];six=[];q4=[];q7=[]
for v in range(256):
    if v.bit_count()%2==0:
        dv=m.new_int_var(4 if v in (0,w) else 5,4 if v in (0,w) else 6,f'd{v}')
        z=m.new_bool_var(f'six{v}')
        m.add(dv==6).only_enforce_if(z);m.add(dv!=6).only_enforce_if(z.Not())
        six.append((v,z))
    else:
        dv=m.new_int_var(4,7,f'd{v}')
        z4=m.new_bool_var(f'four{v}');z7=m.new_bool_var(f'seven{v}')
        m.add(dv==4).only_enforce_if(z4);m.add(dv!=4).only_enforce_if(z4.Not())
        m.add(dv==7).only_enforce_if(z7);m.add(dv!=7).only_enforce_if(z7.Not())
        q4.append(z4);q7.append(z7)
    m.add(dv==sum(x[e] for e in q.incident[v]));d.append(dv)
m.add(sum(z for _,z in six)==50)
m.add(sum(q4)<=2);m.add(sum(q7)<=1)
has7=m.new_bool_var('Q_has7')
m.add(sum(q7)==1).only_enforce_if(has7);m.add(sum(q7)==0).only_enforce_if(has7.Not())
m.add(sum(q4)==0).only_enforce_if(has7)
for root in (0,w):
    for axis in range(8):
        e=q.index[tuple(sorted((root,root^(1<<axis))))]
        m.add(x[e]==int(axis<4))
six=dict(six)
tables={0:[(304,2),(302,5),(300,8)],
        2:[(304,1),(302,4),(300,7),(298,10),(296,13),(294,16)]}
for axis in range(8):
    for side in range(2):
        vertices=[v for v in range(256) if v.bit_count()%2==0 and (v>>axis&1)==side]
        hs=[];local_degree=[]
        for v in vertices:
            e=q.index[tuple(sorted((v,v^(1<<axis))))]
            z=m.new_bool_var(f'high{axis}_{side}_{v}')
            m.add(z<=six[v]);m.add(z+x[e]<=1);m.add(z>=six[v]-x[e])
            hs.append(z);local_degree.append(d[v]-x[e])
        M=m.new_int_var(0,304,f'M{axis}_{side}');C=m.new_int_var(0,64,f'C{axis}_{side}')
        m.add(M==sum(local_degree));m.add(C==sum(hs))
        b=2 if axis<4 and side==0 else 0
        m.add_allowed_assignments([M,C],tables[b])
solver=cp_model.CpSolver();solver.parameters.max_time_in_seconds=240;solver.parameters.num_search_workers=2
start=time.monotonic();status=solver.solve(m)
result={'K':4,'degree_four_roots':[0,w],'root_selected_directions':[0,1,2,3],
        'target_edges':688,'status':solver.status_name(status),'seconds':time.monotonic()-start,
        'proof_scope':'This fixed two-root K4 family only; full 688 exclusion not claimed',
        'checked_unsat_certificate':False,'response':solver.response_stats()}
if status in (cp_model.FEASIBLE,cp_model.OPTIMAL):result['edges']=[e for i,e in enumerate(q.edges) if solver.value(x[i])]
(ROOT/'results'/f'q8_688_k4_w{w}.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['edges','response']}),flush=True)
