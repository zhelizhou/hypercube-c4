from pathlib import Path
from itertools import combinations
import json,hashlib
BASE=Path(__file__).resolve().parent.parent
reps=[0,1,3,4,5,6,7,12,13]
def swap(c):return ((c&1)<<1)|((c&2)>>1)|((c&4)<<1)|((c&8)>>1)
def run(path):
 E={tuple(sorted(map(int,line.split()))) for line in path.read_text().splitlines() if line.strip()}
 adj=[set() for _ in range(256)]
 for u,v in E:
  assert 0<=u<v<256 and (u^v).bit_count()==1
  adj[u].add(v);adj[v].add(u)
 assert all(len(adj[u]&adj[v])<=1 for u in range(256) for v in range(u))
 def edge(u,v):return int(v in adj[u])
 C=[[[0]*9 for _ in range(9)] for _ in range(2)];T=[[0]*9 for _ in range(9)]
 for v in range(256):
  for a,b in combinations(range(8),2):
   A=v^(1<<a);B=v^(1<<b);AB=A^(1<<b)
   c=edge(v,A)+2*edge(v,B)+4*edge(A,AB)+8*edge(B,AB)
   assert c<15;j=reps.index(min(c,swap(c)));T[len(adj[v])][j]+=1
 for v in range(256):
  for a in range(8):
   if v&(1<<a):continue
   u=v^(1<<a);r=edge(v,u)
   for b in range(8):
    if b==a:continue
    A=v^(1<<b);B=u^(1<<b)
    f=edge(v,A);s=edge(u,B);o=edge(A,B)
    for w,c in [(v,r+2*f+4*s+8*o),(u,r+2*s+4*f+8*o)]:
     assert c<15;j=reps.index(min(c,swap(c)));C[r][len(adj[w])][j]+=1
 for d in range(9):
  for j,c in enumerate(reps):
   k=(c&1)+((c>>1)&1)
   assert C[1][d][j]==k*T[d][j]
   assert C[0][d][j]==(2-k)*T[d][j]
 return {'source':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'edges':len(E),'all162_integer_incidence_identities':'PASS','all36_mixed_conditional_balances':'PASS'}
paths=[BASE.parents[2]/'data/q8_seed682.edges',BASE/'finite8_maximal_leaf_gate/CALIBRATION.edges',BASE/'finite8_maximal_leaf_gate/review/SAME_PARITY_COUNTEREXAMPLE.edges']
rows=[run(p) for p in paths]
Path(__file__).with_name('EDGE_VERTEX_ACTUAL_CHECK.json').write_text(json.dumps({'status':'PASS_INDEPENDENT_LITERAL_CUBE_GEOMETRY','graphs':rows,'scope':'General C4freeQ8 incidence identities; no densityclaim'},indent=2)+'\n')
print(json.dumps(rows))
