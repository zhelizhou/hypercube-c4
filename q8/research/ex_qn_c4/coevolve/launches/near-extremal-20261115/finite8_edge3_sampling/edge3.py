"""Exact edge-root three-outside-direction histogram features."""
from itertools import combinations,combinations_with_replacement
from collections import Counter
EDGES3=[(v,v^(1<<a)) for v in range(8) for a in range(3) if not v&(1<<a)]
ORDER=EDGES3+[(u+8,v+8) for u,v in EDGES3]+[(v,v+8) for v in range(8)]
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

ROW_KEYS=[(r,hist(list(xs),8-r)) for r in range(2) for xs in combinations_with_replacement(range(8-r),3)]
assert len(ROW_KEYS)==204
ROW_INDEX={k:i for i,k in enumerate(ROW_KEYS)}
def hypergeom_counts(r,y):
 assert len(y)==8-r and sum(y)==7 and all(type(v) is int and v>=0 for v in y)
 xs=[s for s,n in enumerate(y) for _ in range(n)];out=Counter()
 for positions in combinations(range(7),3):
  key=r,hist([xs[i] for i in positions],8-r);out[key]+=1;out[keyflip(key)]+=1
 assert sum(out.values())==70
 return out
