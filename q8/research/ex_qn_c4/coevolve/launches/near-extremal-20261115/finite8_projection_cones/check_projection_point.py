"""Independent standard-library full multisets, literal flags/actions, and true682 bridge."""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations,combinations_with_replacement
from collections import Counter
from math import comb,lcm
import argparse,json,hashlib
HERE=Path(__file__).resolve().parent;BASE=HERE.parent
SQ=((0,1),(0,2),(1,3),(2,3));ROOTS=(0,1,3,6,7);DIMS=(240,212,190,187,170)
E3=[(v,v^(1<<a)) for v in range(8) for a in range(3) if not v&(1<<a)]
ORDER=E3+[(a+8,b+8) for a,b in E3]+[(v,v+8) for v in range(8)]
GROUP=[]
for sw in range(2):
 for t in range(4):
  vm=[t^((((v&1)<<1)|((v&2)>>1)) if sw else v) for v in range(4)]
  em=[SQ.index(tuple(sorted((vm[a],vm[b])))) for a,b in SQ];GROUP.append((vm,em))
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rootmap(r,h):return sum(1<<h[1][i] for i in range(4) if r>>i&1)
def move(f,h):return sum(1<<h[0][i] for i in range(4) if f>>i&1)+sum(1<<(4+h[1][i]) for i in range(4) if f>>(4+i)&1)
def states(r):return [f for f in range(240) if all(not((r>>k&1) and(f>>(k+4)&1) and(f>>x&1) and(f>>y&1)) for k,(x,y) in enumerate(SQ))]
CODES=[states(r) for r in ROOTS];IDS=[{f:i for i,f in enumerate(c)} for c in CODES]
def edge(a,b):return tuple(sorted((a,b)))
def legal(E,n):
 adj=[set() for _ in range(1<<n)]
 for a,b in E:
  assert a<b and (a^b).bit_count()==1;adj[a].add(b);adj[b].add(a)
 assert all(len(adj[a]&adj[b])<=1 for a in range(1<<n) for b in range(a))
 return adj

def faces(E,n):
 for a,b in combinations(range(n),2):
  for v in range(1<<n):
   if v&((1<<a)|(1<<b)):continue
   vs=[v,v^(1<<a),v^(1<<b),v^(1<<a)^(1<<b)]
   r=sum(1<<k for k,(x,y) in enumerate(SQ) if edge(vs[x],vs[y]) in E)
   canonical=min(rootmap(r,h) for h in GROUP);h0=next(h for h in GROUP if rootmap(r,h)==canonical);block=ROOTS.index(canonical)
   fs=[]
   for c in range(n):
    if c in (a,b):continue
    f=sum(1<<k for k,x in enumerate(vs) if edge(x,x^(1<<c)) in E)
    f+=sum(1<<(4+k) for k,(x,y) in enumerate(SQ) if edge(vs[x]^(1<<c),vs[y]^(1<<c)) in E)
    fs.append(move(f,h0));assert fs[-1] in IDS[block]
   yield block,fs

def projection(mask,maps,L):
 E={e for k,e in enumerate(ORDER) if mask>>k&1};legal(E,4)
 U=[[[0]*L for _ in range(L)] for _ in range(5)]
 for b,fs in faces(E,4):
  st=[h for h in GROUP if rootmap(ROOTS[b],h)==ROOTS[b]]
  for h in st:
   s,t=[maps[b][IDS[b][move(f,h)]] for f in fs]
   U[b][s][t]+=2240//len(st);U[b][t][s]+=2240//len(st)
   U[b][s][s]+=448//len(st);U[b][t][t]+=448//len(st)
 assert sum(sum(map(sum,M)) for M in U)==129024
 return U

def full_lift(Q,b,maps):
 st=[h for h in GROUP if rootmap(ROOTS[b],h)==ROOTS[b]]
 perms=[[IDS[b][move(f,h)] for f in CODES[b]] for h in st]
 assert all(sorted(p)==list(range(DIMS[b])) for p in perms)
 Qf=[[sum(Q[maps[b][p[i]]][maps[b][p[j]]] for p in perms) for j in range(DIMS[b])] for i in range(DIMS[b])]
 assert all(Qf[p[i]][p[j]]==Qf[i][j] for p in perms for i in range(DIMS[b]) for j in range(DIMS[b]))
 return Qf,perms

def quadratic(Q,x):return sum(a*Q[i][j]*b for i,a in x.items() for j,b in x.items())
def calibration(maps,L,Qs):
 seed=BASE.parents[2]/'data/q8_seed682.edges'
 E={tuple(map(int,line.split())) for line in seed.read_text().splitlines() if line.strip()};assert len(E)==682;legal(E,8)
 # All kernels are full invariant integer lifts. Compare actual six-count root values
 # with the exact 5/6 cross plus 1/12 two-diagonal local Q4 feature.
 direct=[0]*5
 for b,fs in faces(E,8):direct[b]+=quadratic(Qs[b],Counter(IDS[b][f] for f in fs))
 masks=Counter()
 for axes in combinations(range(8),4):
  support=sum(1<<a for a in axes)
  for v in range(256):
   if v&support:continue
   vs=[v^sum(1<<axes[j] for j in range(4) if x>>j&1) for x in range(16)]
   mask=sum(1<<k for k,(a,b) in enumerate(ORDER) if edge(vs[a],vs[b]) in E);masks[mask]+=1
 assert sum(masks.values())==1120
 local=[0]*5
 for mask,multiplicity in masks.items():
  K={e for k,e in enumerate(ORDER) if mask>>k&1}
  for b,fs in faces(K,4):
   s,t=[IDS[b][f] for f in fs];Q=Qs[b]
   local[b]+=multiplicity*(10*Q[s][t]+Q[s][s]+Q[t][t])
 assert all(F(local[b],1120*288)==F(direct[b],1792*36) for b in range(5))
 assert min(direct)>=0
 return dict(seed_sha256=digest(seed),edges=682,actual_root_squares=1792,coordinate_Q4s=1120,distinct_Q4_masks=len(masks),direct_quadratic_sums=direct,local_feature_numerators=local,bridge_values=[str(F(v,1792*36)) for v in direct])

def main():
 ap=argparse.ArgumentParser();ap.add_argument('OUTPUT_DIR',type=Path);args=ap.parse_args();R=args.OUTPUT_DIR
 point=json.loads((R/'INPUT_POINT.json').read_text(),parse_float=F);mapping=json.loads((R/'MAPPING.json').read_text());L=mapping['labels'];maps=mapping['full_state_to_label']
 assert CODES==mapping['full_state_codes'] and tuple(map(len,CODES))==DIMS
 assert 1<=L<=16 and all(len(m)==d for m,d in zip(maps,DIMS)) and all(type(v) is int and 0<=v<L for m in maps for v in m)
 if mapping['mode']=='parallel15':assert L==15 and maps==[[f>>4 for f in c] for c in CODES]
 if mapping['mode']=='connector16':assert L==16 and maps==[[f&15 for f in c] for c in CODES]
 den=lcm(*(w.denominator for _,w in point['lambda']));U=[[[0]*L for _ in range(L)] for _ in range(5)]
 for mask,w in point['lambda']:
  M=projection(mask,maps,L);n=int(w*den)
  for b in range(5):
   for i in range(L):
    for j in range(L):U[b][i][j]+=n*M[b][i][j]
 stored=json.loads((R/'PROJECTED_MOMENTS.json').read_text());assert U==stored['blocks'] and stored['moment_denominator']==129024*den
 results=[];Qs=[]
 # A signed finite-six rounding kernel exercises cross, diagonal, and collision terms
 # even if the bounded probe emits no separator.
 q=[i%2 for i in range(L)];synthetic=[[36*q[i]*q[j]-15*(q[i]+q[j])+6 for j in range(L)] for i in range(L)]
 for b in range(5):Qs.append(full_lift(synthetic,b,maps)[0])
 for path in sorted(R.glob('block*.EXACT_CUT.json')):
  cut=json.loads(path.read_text());Q=cut['small_Q'];b=cut['block'];scale=cut['positive_normalization'];assert cut['input_sha256']==digest(R/'INPUT_POINT.json') and cut['mapping_sha256']==digest(R/'MAPPING.json')
  assert len(Q)==L and all(len(r)==L for r in Q);assert all(type(Q[i][j]) is int and Q[i][j]==Q[j][i] for i in range(L) for j in range(L))
  full,perms=full_lift(Q,b,maps);assert full==cut['full_Q'] and perms==cut['root_state_permutations'] and cut['full_state_to_label']==maps[b] and cut['full_state_codes']==CODES[b]
  values=[quadratic(Q,Counter(xs)) for xs in combinations_with_replacement(range(L),6)];assert len(values)==comb(L+5,6);minimum=min(values);assert minimum>=0 and minimum==cut['finite6']['minimum']
  val=F(len(perms)*sum(Q[i][j]*U[b][j][i] for i in range(L) for j in range(L)),129024*den)
  assert str(val)==cut['exact_target_pairing'] and str(val/scale)==cut['normalized_pairing'] and val/scale<F(-1,10000000)
  assert scale==max(1,max(abs(v) for row in full for v in row));Qs[b]=full
  results.append(dict(block=b,status='PASS_EXACT_LITERAL_FULL_STATES_AND_COMPLETE_MULTISET_DOMAIN',histograms=len(values),minimum=minimum,exact_pairing=str(val),normalized_pairing=str(val/scale),cut_sha256=digest(path)))
 cal=calibration(maps,L,Qs)
 out=dict(status='PASS_LITERAL_PROJECTION_COMPLETE_DOMAINS_AND_TRUE682_CALIBRATION',input_sha256=digest(R/'INPUT_POINT.json'),mapping_sha256=digest(R/'MAPPING.json'),checker_sha256=digest(__file__),actual_Q4_masks=len(point['lambda']),exact_projected_moments_match=True,results=results,true682_calibration=cal,scope='Local exact projection/kernel replay; no cone membership from NoCut, no new whole682 proof.')
 (R/'INDEPENDENT_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out),flush=True)
if __name__=='__main__':main()
