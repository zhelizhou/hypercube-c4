"""Direct degree formulation of S+2*N6<=158 with fixed full-root code."""
from pathlib import Path
import json
import sys
from ortools.sat.python import cp_model
from cube import Cube

ROOT=Path(__file__).resolve().parent
code=sys.argv[1]
roots={'2d4':(0,15),'2d6':(0,63),'3':(0,15,51),'4':(0,15,51,60)}[code]
c=len(roots);threshold={2:29,3:22,4:15}[c]
q=Cube(6);m=cp_model.CpModel()
x=[m.new_bool_var(f'e{e}') for e in range(192)]
for face in q.squares:m.add(sum(x[e] for e in face)<=3)
score=[]
for v in range(64):
    if v.bit_count()%2:continue
    if v in roots:
        for e in q.incident[v]:m.add(x[e]==1)
    else:
        d=m.new_int_var(3,5,f'd{v}')
        m.add(d==sum(x[e] for e in q.incident[v]))
        z=m.new_int_var(0,3,f'score{v}')
        m.add_element(d,[0,0,0,0,1,3],z)
        score.append(z)
m.add(sum(score)>=threshold)
# The checked star158 lemma is a valid cut. This is not an observed filter.
m.add(32+19*c+3*sum(score)<=158)
solver=cp_model.CpSolver();solver.parameters.max_time_in_seconds=90;solver.parameters.num_search_workers=2
status=solver.solve(m)
result={'full_roots':roots,'candidate_inequality':'S+2*N6<=158 on minimum-parity-degree 3',
        'threshold_score':threshold,'status':solver.status_name(status),'response':solver.response_stats()}
if status in (cp_model.FEASIBLE,cp_model.OPTIMAL):
    result['edges']=[e for k,e in enumerate(q.edges) if solver.value(x[k])]
    result['score']=sum(solver.value(z) for z in score)
    result['stars']=32+19*c+3*result['score']
(ROOT/'results'/f'q6_degree_potential_{code}.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['edges','response']}),flush=True)
