"""Direct three-outside-axis edge sampling consistency diagnostic."""
from pathlib import Path
from itertools import combinations,combinations_with_replacement
from fractions import Fraction as F
from collections import Counter,defaultdict
import json,hashlib,sys
from check_vertex_cut import ORDER

def flip(s):return ((s&1)<<1)|((s&2)>>1)|(s&4)
def hist(xs,n):return tuple(xs.count(s) for s in range(n))
def keyflip(key):
 r,z=key;w=[0]*len(z)
 for s,v in enumerate(z):w[flip(s)]=v
 return r,tuple(w)
def local(mask):
 E={e for k,e in enumerate(ORDER) if mask>>k&1};adj=[set() for _ in range(16)]
 for a,b in E:adj[a].add(b);adj[b].add(a)
 assert all(len(adj[a]&adj[b])<=1 for a in range(16) for b in range(a))
 def edge(a,b):return int(b in adj[a])
 c=Counter()
 for v in range(16):
  for a in range(4):
   if v&(1<<a):continue
   u=v^(1<<a);r=edge(v,u);xs=[]
   for b in range(4):
    if a==b:continue
    V=v^(1<<b);U=u^(1<<b);s=edge(v,V)+2*edge(u,U)+4*edge(V,U)
    assert r==0 or s!=7;xs.append(s)
   key=r,hist(xs,8-r);c[key]+=1;c[keyflip(key)]+=1
 assert sum(c.values())==64
 return c

def main():
 p=Path(sys.argv[1]).resolve();q=Path(sys.argv[2]).resolve();point=json.loads(p.read_text(),parse_float=F);scope=p.parent.parent
 generators=json.loads((scope/'GENERATOR_HISTOGRAMS.json').read_text());inds=json.loads((scope/'GENERATOR_DEDUPLICATION.json').read_text())['selected_original_indices']
 L=defaultdict(F);B=defaultdict(F)
 for g,w in point['lambda']:
  for key,n in local(g).items():L[key]+=w*n/64
 for idx,w in point['beta']:
  g=generators[inds[idx]];r=g['root_retained'];y=g['counts'];xs=[s for s,n in enumerate(y) for _ in range(n)];assert len(xs)==7
  c=Counter()
  for positions in combinations(range(7),3):
   z=hist([xs[i] for i in positions],8-r);key=r,z;c[key]+=1;c[keyflip(key)]+=1
  assert sum(c.values())==70
  for key,n in c.items():B[key]+=w*n/70
 keys=[(r,hist(list(xs),8-r)) for r in range(2) for xs in combinations_with_replacement(range(8-r),3)]
 assert len(keys)==204
 rows=[dict(root=r,histogram=list(z),exact_difference=str(L[r,z]-B[r,z]),float_difference=float(L[r,z]-B[r,z])) for r,z in keys]
 out=dict(status='EXACT_EDGE_THREEFLAG_POINT_DIAGNOSTIC',input=str(p),input_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),lambda_columns=len(point['lambda']),beta_columns=len(point['beta']),rows=rows,max_abs_difference=max(abs(row['float_difference']) for row in rows),contract='E_lambda count_both_orientations(z)/64 = sum_beta hypergeom_sym_numerator(y,z)/70; equivalent35Eλcount=32Eβnumerator',scope='New exact same-object sampling identity derivation; no proof ofwholemodelNO/graph. Completeinterface/freshsemanticreview pending.')
 q.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'max_abs':out['max_abs_difference'],'largest':sorted(rows,key=lambda row:-abs(row['float_difference']))[:8]}))
if __name__=='__main__':main()
