"""Probe the coupled Q6 potential 4m+N3+3N6<=532, minimum degree three."""
from pathlib import Path
import json
from ortools.sat.python import cp_model
from cube import Cube

ROOT=Path(__file__).resolve().parent
q=Cube(6);m=cp_model.CpModel()
x=[m.new_bool_var(f'e{e}') for e in range(192)]
for face in q.squares:m.add(sum(x[e] for e in face)<=3)
d=[];three=[];six=[];star=[]
for v in range(64):
    dv=m.new_int_var(3,6,f'd{v}');m.add(dv==sum(x[e] for e in q.incident[v]));d.append(dv)
    z3=m.new_bool_var(f'z3_{v}');z6=m.new_bool_var(f'z6_{v}')
    m.add(dv==3).only_enforce_if(z3);m.add(dv!=3).only_enforce_if(z3.Not())
    m.add(dv==6).only_enforce_if(z6);m.add(dv!=6).only_enforce_if(z6.Not())
    three.append(z3);six.append(z6)
    s=m.new_int_var(1,20,f's{v}');m.add_element(dv,[0,0,0,1,4,10,20],s);star.append(s)
for v in range(64):m.add(sum(d[v^(1<<i)] for i in range(6))<=21).only_enforce_if(six[v])
for p in range(2):
    indices=[v for v in range(64) if v.bit_count()%2==p]
    S=sum(star[v] for v in indices);C=sum(six[v] for v in indices)
    m.add(S<=158);m.add(2*S+C<=316)
m.add(sum(x)<=132)
m.add(4*sum(x)+sum(three)+3*sum(six)>=533)
# With no degree-six vertex the proved star158 bounds already imply <=532,
# so a violating graph has a full-degree root, movable to0 by symmetry.
for e in q.incident[0]:m.add(x[e]==1)
solver=cp_model.CpSolver();solver.parameters.max_time_in_seconds=120;solver.parameters.num_search_workers=2
status=solver.solve(m)
result={'candidate':'4m+N3+3N6<=532 for C4-free Q6, minimum degree3',
        'status':solver.status_name(status),'response':solver.response_stats()}
if status in (cp_model.FEASIBLE,cp_model.OPTIMAL):
    result['edges']=[e for i,e in enumerate(q.edges) if solver.value(x[i])]
    result['potential']=4*len(result['edges'])+sum(solver.value(z) for z in three)+3*sum(solver.value(z) for z in six)
(ROOT/'results/q6_coupled_potential.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['edges','response']}),flush=True)
