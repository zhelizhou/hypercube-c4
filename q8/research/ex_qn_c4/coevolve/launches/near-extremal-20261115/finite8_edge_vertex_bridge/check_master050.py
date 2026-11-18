"""Exact decimal-rational diagnostic using independent local geometry."""
from fractions import Fraction as Q
import json
import numpy as np
from scipy import sparse
from check_bridge import HERE,BASE,localR,sha,GROUPS
p=BASE/'finite8_degree_augmentation/pool_profile1409_working_sets/point_bank/master_050.json'
a=json.loads(p.read_text(),parse_float=Q)
b=[Q(0)]*1751
for k,w in a['beta']:b[k]+=w
B=sparse.load_npz(HERE/'BALANCE_CURRENT_36x1751.npz').tocsr()
BM=sparse.load_npz(HERE/'MOMENT_BETA_CURRENT_27x1751.npz').tocsr()
def multiply(M):return [sum((int(v)*b[j] for j,v in zip(M.indices[M.indptr[r]:M.indptr[r+1]],M.data[M.indptr[r]:M.indptr[r+1]])),Q(0)) for r in range(M.shape[0])]
balance=multiply(B);left=multiply(BM);right=[Q(0)]*27
for g,w in a['lambda']:
 R=localR(g)
 for group,ids in enumerate(GROUPS):
  for i in range(9):right[9*group+i]+=w*392*sum(int(R[i,j]) for j in ids)/64512
moment=[x-y for x,y in zip(left,right)]
out={'input':str(p),'input_sha256':sha(p),'arithmetic':'Exact rational values of serialized decimal weights; not re-normalized','balance_rows':[{'degree':d,'state':j,'difference':str(v),'float_difference':float(v)} for (d,j),v in zip([(d,j) for d in range(9) for j in (1,4,5,8)],balance)],'moment_rows':[{'group':g,'state':i,'difference':str(v),'float_difference':float(v)} for (g,i),v in zip([(g,i) for g in range(3) for i in range(9)],moment)],'max_balance':max(map(lambda v:abs(float(v)),balance)),'max_moment':max(map(lambda v:abs(float(v)),moment)),'scope':'Frozen relaxation tuple violates necessary identities, not a Q8 graph or full682 result.'}
assert out['max_balance']>0.029 and out['max_moment']>0.1
(HERE/'MASTER050_DIAGNOSTIC.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ('balance_rows','moment_rows')},indent=2))
