from pathlib import Path
import sys,json,hashlib
P=Path(__file__).resolve().parent;BASE=P.parent
sys.path.insert(0,str(BASE/'finite8_flags/deps'))
import numpy as np
from scipy import sparse
import edge3 as e
SCOPE=BASE/'finite8_degree_augmentation/pool_profile1409_vertex_priced'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def csr(columns,rows=204):
 rr=[];cc=[];vv=[]
 for col,items in enumerate(columns):
  for k,value in items.items():rr.append(e.ROW_INDEX[k]);cc.append(col);vv.append(value)
 return sparse.csr_matrix((np.array(vv,dtype=np.int64),(rr,cc)),shape=(rows,len(columns)))
def main():
 rawpath=P/'SOURCE_0_GENERATOR_HISTOGRAMS.json';raw=json.loads(rawpath.read_text())
 cols=[e.hypergeom_counts(g['root_retained'],g['counts']) for g in raw];H=csr(cols);assert H.shape==(204,5148)
 cgpath=P/'SOURCE_1_GENERATOR_HISTOGRAMS.json';cg=json.loads(cgpath.read_text());dpath=P/'SOURCE_2_GENERATOR_DEDUPLICATION.json';ded=json.loads(dpath.read_text())
 rawindex={(g['root_retained'],tuple(g['counts'])):i for i,g in enumerate(raw)}
 curraw=[rawindex[g['root_retained'],tuple(g['counts'])] for g in cg]
 inds=ded['selected_original_indices'];selected=[curraw[i] for i in inds]
 for group in ded['groups']:
  ref=cols[curraw[group[0]]]
  assert all(cols[curraw[i]]==ref for i in group)
 # Original all-root moment classes must preserve the higher sampler, too.
 oldpath=P/'SOURCE_3_GENERATOR_DEDUPLICATION.json'
 old=json.loads(oldpath.read_text());oldgroups=old['groups']
 assert len(oldgroups)==2788
 for group in oldgroups:
  assert all(cols[i]==cols[group[0]] for i in group)
 graphpath=P/'SOURCE_4_POOL_GRAPH_CODES.json';graphs=json.loads(graphpath.read_text());L=csr([e.local(g) for g in graphs]);assert L.shape==(204,14090)
 sparse.save_npz(P/'BETA_HYPERGEOM_FULL_204x5148.npz',H)
 sparse.save_npz(P/'BETA_HYPERGEOM_CURRENT_204x1751.npz',H[:,selected])
 sparse.save_npz(P/'LOCAL_COUNTS_204x14090.npz',L)
 order=dict(rows=[{'root_retained':r,'counts':list(z)} for r,z in e.ROW_KEYS],current_selected_global5148_indices=selected,current_raw3432_to_full5148=curraw,current_selected_source3432_indices=inds,graphs=graphs)
 (P/'ORDER.json').write_text(json.dumps(order,indent=2)+'\n')
 files=[rawpath,cgpath,dpath,oldpath,graphpath]
 interface=dict(status='EXACT_FULL_THIRD_ORDER_EDGE_SAMPLING_INTERFACE',equation='35 LOCAL_COUNTS lambda =32 BETA_HYPERGEOM beta',rows=204,rows_independent=False,full_beta=5148,current_beta=1751,lambda_library=14090,all_original2788_and_current1751_dedup_classes_preserve_H=True,source_hashes={p.name:sha(p) for p in files},scope='GeneralC4freeQ8 identity; current1751adapter has separately justified maximal/leafdomain. All204localcounts admit the exactfullflagpairlift in ../finite8_degree_augmentation/edge3_quad_lift/; include its K/80 dual contribution in the existingcompleteQ4functional.',extra_oracle_score='For integer204rowweights v, add sum_z v_z*LOCAL_COUNTS_z(K). Localcounts include BOTH endpointorientations; arbitrary suchscore isQ4isometry invariant.')
 (P/'INTERFACE.json').write_text(json.dumps(interface,indent=2)+'\n');print(json.dumps(interface))
if __name__=='__main__':main()
