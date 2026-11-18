from pathlib import Path
from fractions import Fraction as F
import json,hashlib
BASE=Path(__file__).resolve().parent.parent
scope=BASE/'finite8_degree_augmentation/pool_profile1409_working_sets'
p=scope/'point_bank/master_050.json'
d=json.loads(p.read_text(),parse_float=F)
gens=json.loads((scope/'GENERATOR_HISTOGRAMS.json').read_text());inds=json.loads((scope/'GENERATOR_DEDUPLICATION.json').read_text())['selected_original_indices']
def swap(c):return ((c&1)<<1)|((c&2)>>1)|((c&4)<<1)|((c&8)>>1)
reps=[0,1,3,4,5,6,7,12,13];MIX=[1,4,5,8]
C=[[[F() for _ in range(9)] for _ in range(9)] for _ in range(2)]
for k,w in d['beta']:
 row=gens[inds[k]];r=row['root_retained'];ys=row['counts'];ds=[r+sum(n for s,n in enumerate(ys) if s&(1<<a)) for a in range(2)]
 for s,n in enumerate(ys):
  if not n:continue
  for end in range(2):
   c=r+2*((s>>end)&1)+4*((s>>(1-end))&1)+8*((s>>2)&1)
   assert c<15
   j=reps.index(min(c,swap(c)));C[r][ds[end]][j]+=w*n
from check_vertex_cut import matrix
from math import comb
M=[[F() for _ in range(9)] for _ in range(9)]
for g,w in d['lambda']:
 U=matrix(g)
 for i in range(9):
  for j in range(9):M[i][j]+=w*U[i][j]/64512
GROUPS=[[0,3,7],[1,4,5,8],[2,6]]
rows=[]
for group,ids in enumerate(GROUPS):
 for i in range(9):
  beta=sum((C[0][t][i]+C[1][t][i])*[comb(8-t,2),t*(8-t),comb(t,2)][group] for t in range(9))
  local=392*sum(M[i][j] for j in ids)
  rows.append(dict(group=group,state=i,exact_difference=str(beta-local),float_difference=float(beta-local)))
out={'status':'EXACT_BETA_LAMBDA_CONDITIONAL_VERTEX_GROUP_MOMENT_DIAGNOSTIC','input':str(p),'input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'formula':'Sum_beta C_all_(d,i)*F_group(d) =392*sum_(j in group) M5_(i,j)(lambda)','rows':rows,'max_absolute_difference':max(abs(r['float_difference']) for r in rows),'scope':'New Root-derived general sameobject moment identities; complete proof/interface/freshreview pending'}
q=BASE/'finite8_root_checks/EDGE_VERTEX_MOMENT_BALANCE_MASTER050.json';q.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'max_abs':out['max_absolute_difference'],'largest':sorted(rows,key=lambda r:-abs(r['float_difference']))[:10]}))
