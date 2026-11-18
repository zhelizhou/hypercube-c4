"""Look for Q6 counterexamples to an overstrong intermediate defect bound."""
import json
from pathlib import Path
from ortools.sat.python import cp_model
from cube import Cube

ROOT = Path(__file__).resolve().parent
q = Cube(6)
model = cp_model.CpModel()
x = [model.new_bool_var(f'e{k}') for k in range(192)]
for face in q.squares:
    model.add(sum(x[e] for e in face) <= 3)
d = [model.new_int_var(3,5,f'd{v}') for v in range(64)]
z = [model.new_bool_var(f'z5{v}') for v in range(64)]
for v in range(64):
    model.add(d[v] == sum(x[e] for e in q.incident[v]))
    model.add(d[v] == 5).only_enforce_if(z[v])
    model.add(d[v] <= 4).only_enforce_if(z[v].Not())
model.add(sum(x) == 127)
model.add(sum(z) >= 18)  # D=m+N5-144 >=1 on degrees 3,4,5.
for e in q.squares[0]:
    model.add(x[e] == 0)  # D>0 necessitates an empty face; WLOG fix one.
solver = cp_model.CpSolver()
solver.parameters.max_time_in_seconds = 120
solver.parameters.num_search_workers = 2
status = solver.solve(model)
result = {'status':solver.status_name(status),'response':solver.response_stats(),
          'tested_claim':'D<=0 for minimum-degree-three Q6', 'fixed_edges':127}
if status in (cp_model.FEASIBLE,cp_model.OPTIMAL):
    result['edges']=[e for k,e in enumerate(q.edges) if solver.value(x[k])]
    result['D']=127+sum(solver.value(v) for v in z)-144
    bits=' '.join(str(solver.value(e)) for e in x)
    (ROOT/'results/q6_positive_defect.bits').write_text(bits)
(ROOT/'results/q6_positive_defect.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['edges','response']}),flush=True)
