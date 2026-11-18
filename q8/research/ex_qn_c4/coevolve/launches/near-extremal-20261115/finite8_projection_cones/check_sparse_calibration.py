"""Nonzero actual-Q8 bridge calibration for the new opposite-edge root6 cut."""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
from collections import Counter
import json,sys,hashlib
sys.dont_write_bytecode=True
import check_projection_point as independent
HERE=Path(__file__).resolve().parent;R=HERE/'parallel15_master102';path=R/'block3.EXACT_CUT.json';cut=json.loads(path.read_text());Q=cut['full_Q'];b=cut['block'];scale=cut['positive_normalization']
E={(0,1),(2,3)};independent.legal(E,8);direct=0;roots=0
for block,fs in independent.faces(E,8):
 if block==b:
  roots+=1;assert fs==[0]*6
  direct+=independent.quadratic(Q,Counter(independent.IDS[b][f] for f in fs))
assert roots==1 and direct==36*Q[0][0] and Q[0][0]!=0
local=0;restrictions=0;graphs=Counter()
for axes in combinations(range(8),4):
 support=sum(1<<a for a in axes)
 for v in range(256):
  if v&support:continue
  restrictions+=1;vs=[v^sum(1<<axes[j] for j in range(4) if x>>j&1) for x in range(16)]
  mask=sum(1<<k for k,(x,y) in enumerate(independent.ORDER) if independent.edge(vs[x],vs[y]) in E);graphs[mask]+=1
for mask,multiplicity in graphs.items():
 K={e for k,e in enumerate(independent.ORDER) if mask>>k&1};independent.legal(K,4)
 for block,fs in independent.faces(K,4):
  if block==b:
   s,t=[independent.IDS[b][f] for f in fs];local+=multiplicity*(10*Q[s][t]+Q[s][s]+Q[t][t])
assert restrictions==1120 and F(local,1120*288)==F(direct,1792*36)==F(Q[0][0],1792)
out=dict(status='PASS_NONZERO_LITERAL_SPARSE_ACTUAL_Q8_BRIDGE',actual_Q8_edges=sorted(E),root6_count=roots,root6_flags=[0]*6,full_Q00=Q[0][0],direct_root_quadratic_sum=direct,coordinate_Q4s=restrictions,distinct_Q4s=len(graphs),local_integer_sum=local,exact_raw_bridge_value=str(F(Q[0][0],1792)),exact_normalized_bridge_value=str(F(Q[0][0],1792*scale)),cut_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),checker_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
(R/'NONZERO_Q8_CALIBRATION.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
