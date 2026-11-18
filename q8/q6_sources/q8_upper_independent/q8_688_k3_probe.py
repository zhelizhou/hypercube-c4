"""Nine K3 canonical cases using the new forced Q6/Q7 full-root counts.

The case reduction is in REFINEMENT_K3.md. UNKNOWN is not an exclusion.
"""
import argparse,json,time
from itertools import combinations
from pathlib import Path
from ortools.sat.python import cp_model
from cube import Cube
ROOT=Path(__file__).resolve().parent
cases=[(96,23),(48,23),(240,23),(40,23),(232,23),(24,23),(120,23),(24,15),(120,15)]
ap=argparse.ArgumentParser();ap.add_argument('case',type=int,choices=range(9));ap.add_argument('--seconds',type=int,default=120)
a=ap.parse_args();w,T=cases[a.case]
q=Cube(8);m=cp_model.CpModel();x=[m.new_bool_var(f'e{i}') for i in range(1024)]
for row in q.squares:m.add(sum(x[i] for i in row)<=3)
m.add(sum(x)==688);d=[];six={};fourQ=[];sevenQ=[]
for v in range(256):
 if not v.bit_count()%2:
  dv=m.new_int_var(4 if v in [0,w] else 5,4 if v in [0,w] else 6,f'd{v}')
  z=m.new_bool_var(f'six{v}');m.add(dv==6).only_enforce_if(z);m.add(dv!=6).only_enforce_if(z.Not());six[v]=z
 else:
  dv=m.new_int_var(4,7,f'd{v}')
  z4=m.new_bool_var(f'four{v}');z7=m.new_bool_var(f'seven{v}')
  m.add(dv==4).only_enforce_if(z4);m.add(dv!=4).only_enforce_if(z4.Not())
  m.add(dv==7).only_enforce_if(z7);m.add(dv!=7).only_enforce_if(z7.Not())
  fourQ.append(z4);sevenQ.append(z7)
 m.add(dv==sum(x[i] for i in q.incident[v]));d.append(dv)
m.add(sum(six.values())==50);m.add(sum(fourQ)<=2);m.add(sum(sevenQ)<=1)
has7=m.new_bool_var('has7');m.add(sum(sevenQ)==1).only_enforce_if(has7);m.add(sum(sevenQ)==0).only_enforce_if(has7.Not());m.add(sum(fourQ)==0).only_enforce_if(has7)
for v,selected in [(0,15),(w,T)]:
 for i in range(8):m.add(x[q.index[tuple(sorted((v,v^(1<<i))))]]==((selected>>i)&1))
facet_b={};mid={};facets=[(i,s) for i in range(8) for s in range(2)]
for i,s in facets:
 b=sum(((v>>i)&1)==s and (selected>>i)&1 for v,selected in [(0,15),(w,T)])
 facet_b[i,s]=b
 if b==0:mid[i,s]=m.new_bool_var(f'mid{i}_{s}')
 verts=[v for v in six if (v>>i)&1==s]
 M=sum(d[v]-x[q.index[tuple(sorted((v,v^(1<<i))))]] for v in verts)
 m.add(M==(303 if b==1 else 302 if b==2 else 300+2*mid[i,s]))
m.add(sum(mid.values())==2)
for i in range(8):
 if (i,0) in mid and (i,1) in mid:m.add(mid[i,0]+mid[i,1]<=1)
for i,j in combinations(range(8),2):
 for si in range(2):
  for sj in range(2):
   left,right=(i,si),(j,sj);count=[]
   for v,z6 in six.items():
    if (v>>i)&1!=si or (v>>j)&1!=sj:continue
    ei=x[q.index[tuple(sorted((v,v^(1<<i))))]];ej=x[q.index[tuple(sorted((v,v^(1<<j))))]]
    z=m.new_bool_var(f'full{i}_{si}_{j}_{sj}_{v}')
    m.add(z<=z6);m.add(z+ei<=1);m.add(z+ej<=1);m.add(z>=z6-ei-ej);count.append(z)
   C=m.new_int_var(0,2,f'C{i}_{si}_{j}_{sj}');m.add(C==sum(count))
   if facet_b[left] or facet_b[right]:
    # Nonzero exactly for two b2 facets or one b2 and one b1.
    expected=int(bool(facet_b[left] and facet_b[right] and (facet_b[left]==2 or facet_b[right]==2)))
    m.add(C==expected)
   else:
    both=m.new_bool_var(f'both{i}_{si}_{j}_{sj}')
    m.add(both<=mid[left]);m.add(both<=mid[right]);m.add(both>=mid[left]+mid[right]-1)
    m.add(C==1).only_enforce_if(both);m.add_allowed_assignments([C],[(0,),(2,)]).only_enforce_if(both.Not())
s=cp_model.CpSolver();s.parameters.max_time_in_seconds=a.seconds;s.parameters.num_search_workers=2
t=time.monotonic();status=s.solve(m)
r={'K':3,'case':a.case,'degree4_roots':[0,w],'selected_masks':[15,T],'target_edges':688,
   'status':s.status_name(status),'seconds':time.monotonic()-t,'proof_scope':'This K3 case only; no full 688 exclusion claimed','checked_unsat_certificate':False,'response':s.response_stats()}
if status in (cp_model.FEASIBLE,cp_model.OPTIMAL):r['edges']=[list(e) for i,e in enumerate(q.edges) if s.boolean_value(x[i])]
(ROOT/f'results/q8_688_k3_case{a.case}.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({k:v for k,v in r.items() if k not in ['edges','response']}),flush=True)
