"""Independent literal cube checker. No imports of producer/flag modules."""
from pathlib import Path
from itertools import combinations
from collections import Counter
from fractions import Fraction
from math import comb
import json,hashlib,time
import numpy as np
from scipy import sparse
HERE=Path(__file__).resolve().parent;BASE=HERE.parent
REPS=(0,1,3,4,5,6,7,12,13);GROUPS=((0,3,7),(1,4,5,8),(2,6))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def edge(a,b):return min(a,b),max(a,b)
def ambient(n):return [(v,v^(1<<a)) for v in range(1<<n) for a in range(n) if not v&(1<<a)]
E3=ambient(3);E4=E3+[(a+8,b+8) for a,b in E3]+[(a,a+8) for a in range(8)]
def state(E,v,a,b):
 q=(v,v^(1<<a),v^(1<<b),v^(1<<a)^(1<<b))
 c=sum((edge(q[s],q[t]) in E)<<k for k,(s,t) in enumerate(((0,1),(0,2),(1,3),(2,3))))
 assert c!=15,'C4'
 # Compute second code from explicitly interchanged coordinates, not a bit mask.
 q=(q[0],q[2],q[1],q[3])
 cc=sum((edge(q[s],q[t]) in E)<<k for k,(s,t) in enumerate(((0,1),(0,2),(1,3),(2,3))))
 return REPS.index(min(c,cc))
def localR(mask):
 E={e for k,e in enumerate(E4) if mask>>k&1};pairs=list(combinations(range(4),2));R=np.zeros((9,9),dtype=np.int64)
 for v in range(16):
  ss=[state(E,v,a,b) for a,b in pairs]
  for a,A in enumerate(pairs):
   for b,B in enumerate(pairs):
    R[ss[a],ss[b]]+=24 if a==b else (72 if set(A)&set(B) else 360)
 assert int(R.sum())==64512
 return R
hist=json.loads((BASE/'finite8_edge_flags/GENERATOR_HISTOGRAMS.json').read_text());lookup={(h['root_retained'],tuple(h['counts'])):i for i,h in enumerate(hist)}
C=sparse.load_npz(HERE/'C_FULL_162x5148.npz').toarray().astype(np.int64)
B=sparse.load_npz(HERE/'BALANCE_FULL_36x5148.npz').toarray().astype(np.int64)
BM=sparse.load_npz(HERE/'MOMENT_BETA_FULL_27x5148.npz').toarray().astype(np.int64)
W=sparse.load_npz(HERE/'MOMENT_PACKED9_SELECTOR_TWICE_27x45.npz').toarray().astype(np.int64)
tri=np.triu_indices(9);cache={}
def graph(E,name):
 E=set(E);assert all(0<=a<b<256 and (a^b).bit_count()==1 for a,b in E)
 degree=Counter(v for e in E for v in e);T=np.zeros((9,9),dtype=np.int64);XX=np.zeros((9,9),dtype=np.int64);bc=np.zeros(5148,dtype=np.int64);gamma=Counter();direct=np.zeros((2,9,9),dtype=np.int64)
 for v in range(256):
  x=np.bincount([state(E,v,a,b) for a,b in combinations(range(8),2)],minlength=9)
  assert int(x.sum())==28
  assert sum(((c&1)+((c>>1)&1))*int(x[i]) for i,c in enumerate(REPS))==7*degree[v]
  T[degree[v]]+=x;XX+=np.outer(x,x);gamma[degree[v],tuple(map(int,x))]+=1
 for u,v in ambient(8):
  r=int((u,v) in E);axis=(u^v).bit_length()-1;y=[0]*(8-r)
  for a in range(8):
   if a==axis:continue
   s=int(edge(u,u^(1<<a)) in E)+2*int(edge(v,v^(1<<a)) in E)+4*int(edge(u^(1<<a),v^(1<<a)) in E)
   assert s<8-r;y[s]+=1
   direct[r,degree[u],state(E,u,axis,a)]+=1
   direct[r,degree[v],state(E,v,axis,a)]+=1
  bc[lookup[r,tuple(y)]]+=1
 assert int(bc.sum())==1024
 assert np.array_equal(C@bc,direct.ravel())
 for j,c in enumerate(REPS):
  k=(c&1)+((c>>1)&1)
  assert np.array_equal(direct[1,:,j],k*T[:,j])
  assert np.array_equal(direct[0,:,j],(2-k)*T[:,j])
 assert np.array_equal(direct.sum(axis=0),2*T)
 assert np.all(B@bc==0)
 # Exact gamma normalization: (T/256)=2*(C_all@bc/1024).
 assert np.array_equal(2*256*direct.sum(axis=0),1024*T)
 masks=Counter()
 for axes in combinations(range(8),4):
  bits=sum(1<<a for a in axes)
  for base in range(256):
   if base&bits:continue
   vv=[base^sum(1<<axes[a] for a in range(4) if v>>a&1) for v in range(16)]
   mask=sum(1<<k for k,(a,b) in enumerate(E4) if edge(vv[a],vv[b]) in E);masks[mask]+=1
 assert sum(masks.values())==1120
 RR=np.zeros((9,9),dtype=np.int64)
 for mask,n in masks.items():
  if mask not in cache:cache[mask]=localR(mask)
  RR+=n*cache[mask]
 assert np.array_equal(784*256*RR,1120*64512*XX)
 packed=RR[tri].copy();packed[tri[0]!=tri[1]]*=2
 assert np.array_equal(2304*1120*(BM@bc),7*1024*(W@packed))
 # Integer version of392: B/1024 =392 sumM; wrong factor393 must fail on nonzero graph.
 rhs=np.array([sum(RR[i,j] for j in GROUPS[g]) for g in range(3) for i in range(9)])
 assert np.array_equal(1120*64512*(BM@bc),392*1024*rhs)
 assert np.any(1120*64512*(BM@bc)!=393*1024*rhs)
 return {'name':name,'edges':len(E),'actual1120_Q4_types':len(masks),'gamma_types':len(gamma),'all162_incidence':True,'all36_balances':True,'all27_moment_balances':True,'M5_equals_gamma_secondmoment':True},bc,masks

def main():
 st=time.monotonic()
 # Independently realize each raw histogram on its literal two endpoint stars.
 # All other cube edges are absent. The only potential full squares use axis0,
 # and r=1 excludes code7, so every such extension is C4-free.
 for col,h in enumerate(hist):
  r=h['root_retained'];E={(0,1)} if r else set();axis=1
  for statecode,n in enumerate(h['counts']):
   for repeat in range(n):
    if statecode&1:E.add((0,1<<axis))
    if statecode&2:E.add((1,1+(1<<axis)))
    if statecode&4:E.add((1<<axis,1+(1<<axis)))
    axis+=1
  assert axis==8
  degree=Counter(v for e in E for v in e)
  literal=np.zeros((2,9,9),dtype=np.int64)
  for a in range(1,8):
   for v in (0,1):literal[r,degree[v],state(E,v,0,a)]+=1
  assert np.array_equal(C[:,col],literal.ravel()),col
 paths=[BASE.parents[2]/'data/q8_seed682.edges',BASE/'finite8_maximal_leaf_gate/CALIBRATION.edges',BASE/'finite8_maximal_leaf_gate/review/SAME_PARITY_COUNTEREXAMPLE.edges']
 EE=[{tuple(map(int,line.split())) for line in p.read_text().splitlines() if line.strip()} for p in paths]
 rows=[];seedbc=None
 cases=list(zip(EE,[str(p) for p in paths]))
 cases +=[(set(),'boundary_empty'),({(v,v^1) for v in range(256) if not v&1},'boundary_perfect_matching'),({(0,1<<a) for a in range(8)},'boundary_full_star')]
 cases +=[(EE[0]-{min(EE[0])},'seed_one_edge_deleted'),({edge(a^137,b^137) for a,b in EE[0]},'seed_translated_137')]
 for E,name in cases:
  rr,bc,_=graph(E,name);rows.append(rr)
  if seedbc is None:seedbc=bc
 # Every stored pool packed9 feature independently rebuilt from its graph, not producer imports.
 current=BASE/'finite8_degree_augmentation/pool_profile1409_working_sets'
 codes=json.loads((current/'POOL_GRAPH_CODES.json').read_text())
 info=json.loads((BASE/'finite8_degree_augmentation/pool_inventory/LP_STARTED.json').read_text())
 FF=sparse.load_npz(current/'INTEGER_FEATURES.npz')[:,info['packed_starts'][5]:info['packed_starts'][6]].toarray()
 for k,mask in enumerate(codes):
  if mask not in cache:cache[mask]=localR(mask)
  p=cache[mask][tri].copy();p[tri[0]!=tri[1]]*=2
  assert np.array_equal(FF[k],p),(k,mask)
 # Mutation checks: exported coefficient perturbation, wrong row sign, missing offdiag2, illegal graph.
 mutated=C.copy();col=int(np.flatnonzero(seedbc)[0]);mutated[0,col]+=1
 assert not np.array_equal(mutated@seedbc,C@seedbc)
 wrong=B.copy();candidates=np.argwhere((wrong!=0)&(seedbc[None,:]>0));a,b=map(int,candidates[0]);wrong[a,b]*=-1
 assert np.any(wrong@seedbc)
 found=False
 for mask,R in cache.items():
  p=R[tri];pp=p.copy();pp[tri[0]!=tri[1]]*=2
  if np.any(W@p!=W@pp):found=True;break
 assert found
 try:state({(0,1),(0,2),(1,3),(2,3)},0,0,1)
 except AssertionError:pass
 else:raise AssertionError('illegal C4 accepted')
 out={'status':'PASS_EXACT_LITERAL_AND_ALL_POOL_PACKED9','graphs':rows,'all_current_graph_vertexfeatures_checked':len(codes),'all_original5148_export':True,'all_original5148_literal_root_extensions':True,'mutations_rejected':['C coefficient+1','one signed balance coefficient reversed','392 replaced by393','offdiagonal packed factor removed','literal C4 graph'],'source_hashes':{str(p):sha(p) for p in paths},'runtime_seconds':time.monotonic()-st,'scope':'General same-object identities and exact interfaces only. No full682 upper bound.'}
 (HERE/'CHECK_RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
