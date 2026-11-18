"""Independent Python full-domain pricing and literal actual-graph checks. No LP."""
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
from math import comb
from pathlib import Path
import hashlib, json, random, subprocess, sys, time
P=Path(__file__).resolve().parent
BASE=P.parent
sys.dont_write_bytecode=True
sys.path.insert(0,str(BASE/'finite8_flags'))
import finite_flags as ff
G=((0,3,7),(1,4,5,8),(2,6))
L=(-2,-1,0,-2,-1,-1,0,-2,6)
COUNTS=[0,253,22848,75504,89180,50050,13728,1848,29]
def dump(name,value): (P/name).write_text(json.dumps(value,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def composition(n,k):
 if k==1: yield (n,);return
 for i in range(n+1):
  for tail in composition(n-i,k-1):yield (i,)+tail
def all_original(d):
 sums=(comb(8-d,2),d*(8-d),comb(d,2))
 for parts in product(*(list(composition(n,len(g))) for n,g in zip(sums,G))):
  x=[0]*9
  for g,part in zip(G,parts):
   for i,v in zip(g,part):x[i]=v
  yield x
def score(Q,x,b=0):
 return b+sum(Q[i][j]*x[i]*x[j] for i in range(9) for j in range(9))
def query(name,Q,b):
 path=P/(name+'.txt')
 path.write_text('\n'.join(' '.join(map(str,row)) for row in Q)+'\n'+' '.join(map(str,b))+'\n')
 result=subprocess.run([str(P/'price_domain'),str(path)],capture_output=True,text=True,check=True)
 (P/(name+'.oracle.json')).write_text(result.stdout)
 return json.loads(result.stdout)
def domain_check():
 cut=json.loads((P/'pricing_master050/CONDITIONAL_VERTEX_CUT.json').read_text())
 Q=cut['integer_Q']; b=cut['degree_bias_raw']
 rng=random.Random(216718)
 Z=[[0]*9 for _ in range(9)]
 for i in range(9):
  for j in range(i,9):Z[i][j]=Z[j][i]=rng.choice([-(1<<63),(1<<63)-1,rng.randrange(-(1<<63),(1<<63))])
 bias=[-(1<<63) if d%2 else (1<<63)-1 for d in range(9)]
 oracle=query('extreme_int64',Z,bias)
 cutoracle=json.loads((P/'pricing_master050/query_32.oracle.json').read_text())
 original=[]; refined=[]; rows=[]
 for d in range(9):
  count=keep=0;best=None;cbest=None
  for x in all_original(d):
   count+=1
   if x[8]<8-d: continue
   keep+=1
   assert sum(a*v for a,v in zip(L,x))==7*(x[8]-(8-d))>=0
   s=score(Z,x,bias[d]);c=score(Q,x)
   best=s if best is None else min(best,s)
   cbest=c if cbest is None else min(cbest,c)
  original.append(count);refined.append(keep)
  o=oracle['degrees'][d];co=cutoracle['degrees'][d]
  assert o['count']==co['count']==keep==COUNTS[d]
  assert o['minimum']==(None if best is None else str(best))
  assert co['minimum']==(None if cbest is None else str(cbest))
  if d:
   assert score(Z,o['witness'],bias[d])==best
   assert score(Q,co['witness'])==cbest
   assert cbest+b[d]==0
  else:assert o['witness'] is co['witness'] is None
  rows.append(dict(degree=d,count=keep,extreme_minimum=best,cut_minimum=cbest))
 assert sum(original)==674172 and sum(refined)==253440
 # Strictly check malformed, overflowing, and asymmetric queries fail before pricing.
 valid=(P/'extreme_int64.txt').read_text().split()
 tests={
  'missing':valid[:-1], 'trailing':valid+['0'],
  'overflow':[str(1<<63)]+valid[1:], 'underflow':[str(-(1<<63)-1)]+valid[1:],
  'nonnumeric':['1x']+valid[1:],
  'asymmetric':valid[:1]+[str(int(valid[1])+1)]+valid[2:]}
 rejected={}
 for name,tokens in tests.items():
  f=P/('invalid_'+name+'.txt');f.write_text(' '.join(tokens)+'\n')
  r=subprocess.run([str(P/'price_domain'),str(f)],capture_output=True,text=True)
  assert r.returncode==2 and not r.stdout
  rejected[name]=r.stderr.strip()
 return dict(original_counts=original,refined_counts=refined,original_total=sum(original),refined_total=sum(refined),independent_ordered_quadratic_rows=rows,invalid_queries_rejected=rejected)
def graph_check(source):
 E={tuple(sorted(map(int,line.split()))) for line in source.read_text().splitlines() if line.strip() and not line.startswith('#')}
 ambient=set(ff.cube_edges(8));assert E<=ambient
 adj=[set() for _ in range(256)]
 for u,v in E:adj[u].add(v);adj[v].add(u)
 assert all(len(adj[u]&adj[v])<=1 for u in range(256) for v in range(u))
 hist=Counter();N=Counter();X=[[0]*9 for _ in range(9)];closed=Counter();minslack=28
 for v in range(256):
  d=len(adj[v]);N[d]+=1;x=[0]*9;cover=Counter()
  for i,j in combinations(range(8),2):
   vertices=(v,v^(1<<i),v^(1<<j),v^(1<<i)^(1<<j))
   bits=[int(tuple(sorted((vertices[a],vertices[b]))) in E) for a,b in ((0,1),(0,2),(1,3),(2,3))]
   code=sum(bit<<k for k,bit in enumerate(bits));assert code!=15
   swapped=bits[1]+2*bits[0]+4*bits[3]+8*bits[2]
   state=[0,1,3,4,5,6,7,12,13].index(min(code,swapped));x[state]+=1
   if state==8:
    missing=i if not bits[0] else j
    assert bits[0]+bits[1]==1 and bits[2]==bits[3]==1
    cover[missing]+=1
  assert x==[ff.vertex_states(E,8,v).count(i) for i in range(9)]
  for i in range(8):
   if v^(1<<i) not in adj[v]:assert cover[i]>=1
  for i in range(8):
   w=v^(1<<i)
   if v<w and (v,w) not in E:closed[cover[i]]+=1
  assert [sum(x[i] for i in g) for g in G]==[comb(8-d,2),d*(8-d),comb(d,2)]
  assert d>0 and x[8]>=8-d
  assert sum(a*v for a,v in zip(L,x))==7*(x[8]-(8-d))
  if d==1:assert x[8]==7 and sum(x[i] for i in G[1] if i!=8)==0
  minslack=min(minslack,x[8]-(8-d));hist[d,tuple(x)]+=1
  for i in range(9):
   for j in range(9):X[i][j]+=x[i]*x[j]
 U=[[0]*9 for _ in range(9)];restrictions=0
 for K in ff.restrictions(E,8):
  restrictions+=1;_,c=ff.local_coefficients(K)
  for (block,i,j),value in c.items():
   if block!=5:continue
   U[i][j]+=(2 if i==j else 1)*value
   if i!=j:U[j][i]+=value
 assert restrictions==1120 and U==[[720*z for z in row] for row in X]
 for i in range(9):assert sum(X[i][j]*L[j] for j in range(9))>=0
 columns=[dict(degree=d,histogram=list(x),multiplicity=w) for (d,x),w in sorted(hist.items())]
 dump(source.stem+'_GAMMA.json',dict(vertex_denominator=256,columns=columns))
 return dict(source=str(source),sha256=sha(source),edges=len(E),C4_free=True,maximal=True,missing_edges=sum(closed.values()),closing_count_histogram=dict(closed),degree_counts={str(d):N[d] for d in range(9)},histograms=len(hist),minimum_maximality_slack=minslack,Q4_restrictions=restrictions,moment_integer_identity='U_local=720 sum_v x_v x_vT',RLT_all9=True)
def pairing_check():
 run=P/'pricing_master050';cut=json.loads((run/'CONDITIONAL_VERTEX_CUT.json').read_text());point=json.loads((run/'INPUT_POINT.json').read_text());Q=cut['integer_Q'];B=cut['degree_bias_raw']
 lw=[(m,Fraction(str(w))) for m,w in point['lambda']];lz=sum(w for _,w in lw)
 aw=[(Fraction(str(row[1])),row[2]) for row in point['alpha']];az=sum(w for w,_ in aw)
 expected=Fraction()
 for mask,w in lw:
  _,c=ff.local_coefficients(ff.q4_edges_from_mask(mask));U=[[0]*9 for _ in range(9)]
  for (block,i,j),value in c.items():
   if block!=5:continue
   U[i][j]+=(2 if i==j else 1)*value
   if i!=j:U[j][i]+=value
  expected+=w/lz*Fraction(sum(Q[i][j]*U[i][j] for i in range(9) for j in range(9)),2*ff.DEN)
 mass=[sum(w*n[d] for w,n in aw)/(az*128) for d in range(9)]
 assert mass[0]==0 and sum(mass)==1
 expected+=sum(Fraction(B[d],784)*mass[d] for d in range(9))
 assert expected==Fraction(cut['exact_target_pairing'])<0
 return dict(input_sha256=sha(run/'INPUT_POINT.json'),lambda_columns=len(lw),alpha_columns=len(aw),exact_pairing=str(expected),normalized_pairing=str(expected/cut['positive_normalization']),normalized_pairing_float=float(expected/cut['positive_normalization']),maximal_only=True,degree0_mass=str(mass[0]))
def main():
 start=time.monotonic();domain=domain_check();dump('DOMAIN_CHECK.json',domain)
 seed=BASE.parents[2]/'data/q8_seed682.edges';leaf=BASE/'finite8_maximal_leaf_gate/CALIBRATION.edges'
 graphs=[graph_check(seed),graph_check(leaf)];dump('GRAPH_CHECK.json',graphs)
 # Empty graph and a single-edge leaf give actual nonmaximal boundary failures.
 boundary=dict(empty=dict(edges=0,degree=0,histogram=[28,0,0,0,0,0,0,0,0],x8=0,required_x8=8),single_edge_leaf=dict(edges=1,vertex=0,degree=1,histogram=[21,7,0,0,0,0,0,0,0],x8=0,required_x8=7))
 assert [ff.vertex_states(set(),8,0).count(i) for i in range(9)]==boundary['empty']['histogram']
 assert [ff.vertex_states({(0,1)},8,0).count(i) for i in range(9)]==boundary['single_edge_leaf']['histogram']
 dump('NONMAXIMAL_BOUNDARY.json',boundary)
 pairing=pairing_check();dump('CUT_CHECK.json',pairing)
 out=dict(status='PASS_LOCAL_PROOF_SUPPORTING_EXACT_CHECKS',seconds=time.monotonic()-start,scope='MAXIMAL ONLY necessary cone and one exact separating cut, not a density bound',source_sha256={name:sha(P/name) for name in ('price_domain.cpp','check.py','price_point.py')},total_refined_generators=253440,actual_graphs=graphs,cut=pairing)
 dump('CHECK.json',out);print(json.dumps(out,indent=2))
if __name__=='__main__':main()
