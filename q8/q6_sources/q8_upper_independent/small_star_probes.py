"""Small-cube tests of possible structural explanations for star deficits."""
from pathlib import Path
import json
from ortools.sat.python import cp_model
from cube import Cube

ROOT=Path(__file__).resolve().parent
records=[]
for n,minimum,target in [(4,1,7),(4,1,8),(5,2,39),(5,2,40)]:
    q=Cube(n);m=cp_model.CpModel()
    x=[m.new_bool_var(f'e{k}') for k in range(len(q.edges))]
    for face in q.squares:m.add(sum(x[e] for e in face)<=3)
    stars=[]
    for v in q.vertices:
        if v.bit_count()%2:continue
        d=m.new_int_var(minimum,n,f'd{v}')
        m.add(d==sum(x[e] for e in q.incident[v]))
        s=m.new_int_var(0,10,f's{v}')
        m.add_element(d,[0,0,0,1,4,10][:n+1],s)
        stars.append(s)
    for e in q.incident[0]:m.add(x[e]==1)
    m.add(sum(stars)==target)
    solver=cp_model.CpSolver();solver.parameters.max_time_in_seconds=15;solver.parameters.num_search_workers=1
    status=solver.solve(m)
    record={'n':n,'minimum_degree_on_even_side':minimum,'root_degree':n,'target_stars':target,'status':solver.status_name(status)}
    if status in (cp_model.FEASIBLE,cp_model.OPTIMAL):record['edges']=[edge for e,edge in enumerate(q.edges) if solver.value(x[e])]
    records.append(record);print(json.dumps({k:v for k,v in record.items() if k!='edges'}),flush=True)
(ROOT/'results/small_star_probes.json').write_text(json.dumps(records,indent=2)+'\n')
