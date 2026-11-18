from pathlib import Path
from itertools import combinations
from collections import Counter
import json,hashlib
import edge3 as e
P=Path(__file__).resolve().parent;BASE=P.parent

def run(name,E):
 adj=[set() for _ in range(256)]
 for u,v in E:
  assert 0<=u<v<256 and (u^v).bit_count()==1
  adj[u].add(v);adj[v].add(u)
 assert all(len(adj[u]&adj[v])<=1 for u in range(256) for v in range(u))
 def edge(a,b):return int(b in adj[a])
 H=Counter();L=Counter()
 for v in range(256):
  for a in range(8):
   if v&(1<<a):continue
   u=v^(1<<a);r=edge(v,u);xs=[]
   for b in range(8):
    if a==b:continue
    A=v^(1<<b);B=u^(1<<b)
    s=edge(v,A)+2*edge(u,B)+4*edge(A,B);assert r==0 or s<7;xs.append(s)
   H.update(e.hypergeom_counts(r,[xs.count(s) for s in range(8-r)]))
 for axes in combinations(range(8),4):
  others=[b for b in range(8) if b not in axes]
  for fixed in range(16):
   origin=sum(((fixed>>i)&1)<<b for i,b in enumerate(others))
   vm=[origin^sum(((v>>i)&1)<<b for i,b in enumerate(axes)) for v in range(16)]
   mask=sum(1<<i for i,(a,b) in enumerate(e.ORDER) if edge(vm[a],vm[b]));L.update(e.local(mask))
 assert sum(L.values())==sum(H.values())==71680
 assert all(L[key]==H[key] for key in e.ROW_KEYS)
 return dict(name=name,edges=len(E),rooted_local_objects=71680,all204_integer_equalities=True,nonzero_rows=sum(L[key]>0 for key in e.ROW_KEYS))

def main():
 paths=[BASE.parents[2]/'data/q8_seed682.edges',BASE/'finite8_maximal_leaf_gate/CALIBRATION.edges',BASE/'finite8_maximal_leaf_gate/review/SAME_PARITY_COUNTEREXAMPLE.edges']
 cases=[(p.name,{tuple(sorted(map(int,l.split()))) for l in p.read_text().splitlines() if l.strip()}) for p in paths]
 cases += [('empty',set()),('oneaxis_matching',{(v,v^1) for v in range(256) if v%2==0}),('even_star',{tuple(sorted((0,1<<a))) for a in range(8)}),('odd_star',{tuple(sorted((1,1^(1<<a)))) for a in range(8)})]
 result=[run(*case) for case in cases]
 out=dict(status='PASS_DIRECT_ACTUAL_GLOBAL_Q8_EDGE3_DOUBLECOUNT',graphs=result,source_hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},source_of_proof='Oriented ambientedge and threeoutsideaxes bijection; actual graphs calibrate normalization, not universalproof.',scope='GeneralC4freeQ8 necessaryidentity only; no682claim.')
 (P/'ACTUAL_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':main()
