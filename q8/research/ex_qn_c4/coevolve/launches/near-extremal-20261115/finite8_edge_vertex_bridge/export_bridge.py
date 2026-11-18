"""Integer edge-to-vertex maps. Reads frozen sources; writes only HERE."""
from pathlib import Path
from itertools import combinations_with_replacement
from collections import Counter
import hashlib,json
import numpy as np
from scipy import sparse
HERE=Path(__file__).resolve().parent
BASE=HERE.parent
FULL=BASE/'finite8_edge_flags'
CURRENT=BASE/'finite8_degree_augmentation/pool_profile1409_working_sets'
OLD=BASE/'finite8_degree_augmentation/pool_edge_degree_dynamic'
REPS=(0,1,3,4,5,6,7,12,13)
MIXED=(1,4,5,8)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def flip(c):return ((c&1)<<1)|((c&2)>>1)|((c&4)<<1)|((c&8)>>1)
def vertexstate(c):
 assert c!=15
 return REPS.index(min(c,flip(c)))
def column(h):
 r=h['root_retained']; y=h['counts']
 assert r in (0,1) and len(y)==8-r and sum(y)==7 and all(type(n)==int and n>=0 for n in y)
 deg=[r+sum(n for s,n in enumerate(y) if (s>>a)&1) for a in (0,1)]
 z=np.zeros(162,dtype=np.int32)
 for s,n in enumerate(y):
  for a in (0,1):
   c=r+2*((s>>a)&1)+4*((s>>(1-a))&1)+8*((s>>2)&1)
   z[r*81+9*deg[a]+vertexstate(c)]+=n
 assert int(z.sum())==14
 return z

def save(name,m):
 m=sparse.csr_matrix(m,dtype=np.int32)
 sparse.save_npz(HERE/(name+'.npz'),m)
 p=HERE/(name+'.json');p.write_text(json.dumps({'shape':list(m.shape),'denominator':1,'indptr':m.indptr.tolist(),'indices':m.indices.tolist(),'data':m.data.tolist()},separators=(',',':'))+'\n')
 return {'npz':name+'.npz','json':name+'.json','shape':list(m.shape),'nnz':int(m.nnz),'json_sha256':sha(p)}

def main():
 hist=json.loads((FULL/'GENERATOR_HISTOGRAMS.json').read_text())
 expected=[]
 for r in (0,1):
  for a in combinations_with_replacement(range(8-r),7):
   c=Counter(a);expected.append({'root_retained':r,'counts':[c.get(i,0) for i in range(8-r)]})
 assert hist==expected and len(hist)==5148
 C=np.stack([column(h) for h in hist],axis=1)
 cr=json.loads((CURRENT/'GENERATOR_HISTOGRAMS.json').read_text())
 de=json.loads((CURRENT/'GENERATOR_DEDUPLICATION.json').read_text())
 old=json.loads((OLD/'GENERATOR_DEDUPLICATION.json').read_text())
 full_lookup={(h['root_retained'],tuple(h['counts'])):i for i,h in enumerate(hist)}
 raw_to_full=[full_lookup[h['root_retained'],tuple(h['counts'])] for h in cr]
 selected=de['selected_original_indices'];adapter=[raw_to_full[k] for k in selected]
 assert len(cr)==3432 and len(selected)==1751
 # Existing duplicate contracts must preserve this stronger map, not just old moments.
 for dedup,rawmap in [(old,list(range(5148))),(de,raw_to_full)]:
  assert len(dedup['groups'])==len(dedup['selected_original_indices'])
  for k,gr in zip(dedup['selected_original_indices'],dedup['groups']):
   assert k in gr
   for j in gr:assert np.array_equal(C[:,rawmap[k]],C[:,rawmap[j]])
 # Independently, endpoint reversal preserves each full C column.
 for h in hist:
  r=h['root_retained'];y=h['counts'];rev=[y[(s&4)|((s&1)<<1)|((s&2)>>1)] for s in range(8-r)]
  assert np.array_equal(column(h),column({'root_retained':r,'counts':rev}))
 rows=[(d,j) for d in range(9) for j in MIXED]
 B=np.stack([C[81+9*d+j]-C[9*d+j] for d,j in rows])
 artifacts={
  'full_C':save('C_FULL_162x5148',C),
  'missing_C':save('C_MISSING_81x5148',C[:81]),
  'retained_C':save('C_RETAINED_81x5148',C[81:]),
  'full_balance':save('BALANCE_FULL_36x5148',B),
  'old_balance':save('BALANCE_OLD_36x2788',B[:,old['selected_original_indices']]),
  'old_C':save('C_OLD_162x2788',C[:,old['selected_original_indices']]),
  'current_balance':save('BALANCE_CURRENT_36x1751',B[:,adapter]),
  'current_C':save('C_CURRENT_162x1751',C[:,adapter])}
 # An independent literal histogram formula for all current entries.
 current_direct=np.stack([column(cr[k]) for k in selected],axis=1)
 assert np.array_equal(current_direct,C[:,adapter])
 sources=[FULL/'GENERATOR_HISTOGRAMS.json',CURRENT/'GENERATOR_HISTOGRAMS.json',CURRENT/'GENERATOR_DEDUPLICATION.json',OLD/'GENERATOR_DEDUPLICATION.json']
 order={'vertex_representatives':REPS,'C_row_order':[(r,d,j) for r in range(2) for d in range(9) for j in range(9)],'balance_row_order':rows,'current_selected_raw_indices':selected,'current_to_original5148_indices':adapter,'current_column_histograms':[cr[k] for k in selected],'old_selected_original_indices':old['selected_original_indices']}
 (HERE/'ORDER.json').write_text(json.dumps(order,separators=(',',':'))+'\n')
 out={'status':'EXACT_MAP_EXPORT_AND_DEDUP_CHECKS_PASS','source_files':{str(p):sha(p) for p in sources},'order_sha256':sha(HERE/'ORDER.json'),'artifacts':artifacts,'current_equation':'BALANCE_CURRENT_36x1751 @ beta = 0; no additional denominator; beta indexed by current selected_original_indices','sign':'retained C minus missing C','full_C_definition':'C[r,d,j] = sum over two endpoints and seven flags, counted by endpoint full degree and canonical vertex state; zero for other root type','coverage':{'original_generators':5148,'old_dedup_classes':2788,'current_raw_histograms':3432,'current_dedup_columns':1751,'every_old_and_current_group_preserves_all162_C_rows':True},'scope':'Necessary identities for actual C4-free Q8, no maximality or fixed-edgecount required. Does not prove upper682.'}
 (HERE/'INTERFACE.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2))
if __name__=='__main__':main()
