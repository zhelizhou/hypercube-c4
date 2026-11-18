"""Independent literal cube projection and full multiset replay of emitted cuts."""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations,combinations_with_replacement
from collections import Counter
import json,sys,hashlib
from check_vertex_cut import ORDER
ROOTS=[0,1,3,6,7];SQ=[(0,1),(0,2),(1,3),(2,3)];GROUP=[]
for sw in range(2):
 for t in range(4):
  vm=[t^((((v&1)<<1)|((v&2)>>1)) if sw else v) for v in range(4)]
  em=[SQ.index(tuple(sorted((vm[a],vm[b])))) for a,b in SQ];GROUP.append((vm,em))
def rootmap(r,h):return sum(1<<h[1][i] for i in range(4) if r>>i&1)
def conn(c,h):return sum(1<<h[0][i] for i in range(4) if c>>i&1)
def literal_projection(mask):
 E={edge for k,edge in enumerate(ORDER) if mask>>k&1};adj=[set() for _ in range(16)]
 for a,b in E:adj[a].add(b);adj[b].add(a)
 assert all(len(adj[a]&adj[b])<=1 for a in range(16) for b in range(a))
 def edge(a,b):return b in adj[a]
 U=[[[0]*16 for _ in range(16)] for _ in range(5)]
 for a,b in combinations(range(4),2):
  for v in range(16):
   if v&((1<<a)|(1<<b)):continue
   vs=[v,v^(1<<a),v^(1<<b),v^(1<<a)^(1<<b)];r=sum(1<<k for k,(x,y) in enumerate(SQ) if edge(vs[x],vs[y]));cr=min(rootmap(r,h) for h in GROUP);h0=next(h for h in GROUP if rootmap(r,h)==cr);st=[h for h in GROUP if rootmap(cr,h)==cr];block=ROOTS.index(cr)
   codes=[sum(1<<k for k,x in enumerate(vs) if edge(x,x^(1<<c))) for c in range(4) if c not in [a,b]]
   codes=[conn(c,h0) for c in codes]
   for h in st:
    s,t=[conn(c,h) for c in codes];U[block][s][t]+=2240//len(st);U[block][t][s]+=2240//len(st);U[block][s][s]+=448//len(st);U[block][t][t]+=448//len(st)
 assert sum(sum(map(sum,M)) for M in U)==129024
 return U

def quadratic(Q,x):return sum(a*Q[i][j]*b for i,a in x.items() for j,b in x.items())
def main():
 R=Path(sys.argv[1]).resolve();point=json.loads((R/'INPUT_POINT.json').read_text(),parse_float=F);P=[[[F() for _ in range(16)] for _ in range(16)] for _ in range(5)]
 for mask,w in point['lambda']:
  U=literal_projection(mask)
  for b in range(5):
   for i in range(16):
    for j in range(16):P[b][i][j]+=w*U[b][i][j]/129024
 results=[]
 for path in sorted(R.glob('block*.EXACT_CUT.json')):
  cut=json.loads(path.read_text());Q=cut['connector_Q'];b=cut['block'];scale=cut['positive_normalization'];assert cut['input_sha256']==hashlib.sha256((R/'INPUT_POINT.json').read_bytes()).hexdigest()
  assert all(type(Q[i][j]) is int and Q[i][j]==Q[j][i] for i in range(16) for j in range(16));st=[h for h in GROUP if rootmap(ROOTS[b],h)==ROOTS[b]]
  assert all(Q[conn(i,h)][conn(j,h)]==Q[i][j] for h in st for i in range(16) for j in range(16))
  values=[quadratic(Q,Counter(xs)) for xs in combinations_with_replacement(range(16),6)];minimum=min(values);assert len(values)==54264 and minimum>=0 and minimum==cut['finite6']['minimum']
  value=sum(Q[i][j]*P[b][j][i] for i in range(16) for j in range(16));assert value<0 and str(value)==cut['exact_target_pairing'] and str(value/scale)==cut['normalized_pairing']
  r=ROOTS[b];legal=[]
  for flag in range(240):
   if all(not((r>>k&1) and(flag>>(k+4)&1) and(flag>>x&1) and(flag>>y&1)) for k,(x,y) in enumerate(SQ)):legal.append(flag)
  assert [f&15 for f in legal]==cut['full_state_connector_codes'] and set(f&15 for f in legal)==set(range(16))
  witness=None
  for xs in combinations_with_replacement(range(16),4):
   v=quadratic(Q,Counter(xs))
   if v<0:witness={'total':4,'histogram':dict(Counter(xs)),'quadratic':v};break
  results.append(dict(block=b,status='PASS_EXACT_INDEPENDENT_DOMAIN_AND_LITERAL_GEOMETRY',histograms=54264,finite6_minimum=minimum,normalized_pairing=str(value/scale),float_normalized_pairing=float(value/scale),full_state_dimension=len(legal),exact_nonPSD_noncopositive_witness=witness,cut_sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
 out=dict(status='ALL_EMITTED_CUTS_EXACTLY_REPLAYED',actual_Q4_masks=len(point['lambda']),results=results,scope='Concrete parameter replay of the alreadyfreshreviewed universal connectorfinite6 implication; not wholefamilyNO orfullPSD/graphacceptance')
 (R/'INDEPENDENT_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':main()
