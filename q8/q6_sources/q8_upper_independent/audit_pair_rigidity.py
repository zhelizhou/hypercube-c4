"""Independent reconstruction and orbit coverage for the eight M130 cases."""
from collections import Counter
from itertools import combinations,permutations
from pathlib import Path
import hashlib,json
from rebuild_local_cnf import exactly,read_cnf
ROOT=Path(__file__).resolve().parent
specs=[(15,48,4),(15,17,0),(15,17,4),(15,51,0),(15,51,4),(63,3,0),(15,None,None),(63,None,None)]

def rebuild(spec):
 second,special,missing=spec
 edges=[(u,v) for u in range(64) for v in range(u+1,64) if (u^v).bit_count()==1]
 ids={e:i+1 for i,e in enumerate(edges)};inc={v:[i+1 for i,e in enumerate(edges) if v in e] for v in range(64)}
 squares=set()
 for u in range(64):
  for w in range(u+1,64):
   if (u^w).bit_count()!=2:continue
   middle=[v for v in range(64) if (u^v).bit_count()==1 and (w^v).bit_count()==1]
   squares.add(tuple(sorted(ids[tuple(sorted(e))] for v in middle for e in [(u,v),(w,v)])))
 assert len(squares)==240
 clauses=[[-e for e in row] for row in squares];top=192;four={};five={};Pthree=[];Qthree=[];Qfive=[]
 for v in range(64):
  if v in (0,second):clauses.extend([[e] for e in inc[v]])
  elif v==special:
   for i in range(6):
    e=ids[tuple(sorted((v,v^(1<<i))))]
    clauses.append([-e if i==missing else e])
  else:
   clauses.extend(map(list,combinations(inc[v],4)))
   limit=5 if v.bit_count()%2 else 4
   clauses.extend([[-e for e in row] for row in combinations(inc[v],limit+1)])
   for r,store in [(4,four),(5,five)]:
    top+=1;store[v]=top
    clauses.extend([[-top]+list(row) for row in combinations(inc[v],7-r)])
    clauses.extend([[top]+[-e for e in row] for row in combinations(inc[v],r)])
   if v.bit_count()%2:Qthree.append(-four[v]);Qfive.append(five[v])
   else:Pthree.append(-four[v])
 for inputs,k in [(Pthree,3 if special is not None else 2),(Qthree,6),(Qfive,8)]:
  rows,top=exactly(inputs,k,top);clauses.extend(rows)
 for v in (0,second):
  neighbors=[v^(1<<i) for i in range(6)]
  clauses.extend([[-five[w]] for w in neighbors])
  rows,top=exactly([-four[w] for w in neighbors],3,top);clauses.extend(rows)
 return top,Counter(tuple(sorted(row)) for row in clauses)

def orbit_cover(second,reps):
 def transform(v,p):return sum(1<<p[i] for i in range(6) if v>>i&1)
 group=[p for p in permutations(range(6)) if transform(second,p)==second]
 eligible=set()
 for v in range(64):
  if v.bit_count()%2 or v in (0,second):continue
  for axis in range(6):
   if all((v^r).bit_count()!=2 or (v^r)&(1<<axis) for r in (0,second)):eligible.add((v,axis))
 orbits=[]
 for v,axis in reps:
  orbit={(transform(v,p)^flip,p[axis]) for p in group for flip in (0,second)}
  assert orbit<=eligible
  assert all(orbit.isdisjoint(other) for other in orbits)
  orbits.append(orbit)
 assert set.union(*orbits)==eligible
 return {'stabilizer_order':2*len(group),'eligible_pairs':len(eligible),'orbit_sizes':[len(x) for x in orbits]}

def main():
 coverage={'d4':orbit_cover(15,[(v,i) for r,v,i in specs[:6] if r==15]),
           'd6':orbit_cover(63,[(v,i) for r,v,i in specs[:6] if r==63])}
 checked={}
 for i,spec in enumerate(specs):
  p=ROOT/f'results/q6_pair130_case{i}';expected=rebuild(spec);assert expected==read_cnf(p.with_suffix('.cnf'))
  r=json.loads(p.with_suffix('.checked.json').read_text());assert r['valid'] and r['final_empty_clause']
  r.update(cnf_sha256=hashlib.sha256(p.with_suffix('.cnf').read_bytes()).hexdigest(),
           proof_sha256=hashlib.sha256(p.with_suffix('.drat').read_bytes()).hexdigest(),
           checker_sha256=hashlib.sha256((ROOT/'check_rup_active.cpp').read_bytes()).hexdigest(),
           independently_rebuilt=True,variables=expected[0],clauses=sum(expected[1].values()))
  p.with_suffix('.checked.json').write_text(json.dumps(r,indent=2)+'\n')
  x=json.loads(p.with_suffix('.json').read_text());x['proof_checked']=True;p.with_suffix('.json').write_text(json.dumps(x,indent=2)+'\n')
  checked[str(i)]=r
 result={'status':'PASS','lemma':'Any minimum-degree-three C4-free Q6 with130 edges has at most one degree6 vertex on each parity.',
         'certificate_cases':8,'verified_additions':sum(c['verified_additions'] for c in checked.values()),'coverage':coverage,'certificates':checked}
 (ROOT/'results/pair130_rigidity_audit.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:result[k] for k in ['status','certificate_cases','verified_additions','coverage']}))
if __name__=='__main__':main()
