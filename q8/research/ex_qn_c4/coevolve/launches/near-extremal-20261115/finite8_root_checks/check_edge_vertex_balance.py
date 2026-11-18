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
rows=[{'degree':t,'state':j,'exact_difference':str(C[1][t][j]-C[0][t][j]),'float_difference':float(C[1][t][j]-C[0][t][j])} for t in range(9) for j in MIX]
out={'status':'EXACT_LITERAL_BETA_POINT_DIAGNOSTIC_NEW_BALANCE','input':str(p),'input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'formula':'For eachdegree d and mixedvertexQ2state j, retained-rootincidences equal missing-rootincidences: eachactualQ2hasoneeach','rows':rows,'max_absolute_difference':max(abs(r['float_difference']) for r in rows),'scope':'New same-object bridge derived by Root; complete proof/interface/freshreview pending, no whole682claim'}
q=BASE/'finite8_root_checks/EDGE_VERTEX_BALANCE_MASTER050.json';q.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'max_abs':out['max_absolute_difference'],'largest':sorted(rows,key=lambda r:-abs(r['float_difference']))[:10]}))
