"""Freeze full-oracle batch enrichment; all real columns share same lambda."""
from pathlib import Path
import sys,json,shutil,hashlib
P=Path(__file__).resolve().parent;OLD=P/'pool_native_oracle_extension1';O=P/'pool_native_batch2';SRC=P.parent/'finite8_flags';sys.path.insert(0,str(SRC/'deps'));sys.path.insert(0,str(SRC));sys.path.insert(0,str(P.parent/'finite8_edge_flags'));sys.path.insert(0,str(P))
import numpy as np
from scipy import sparse
import finite_flags as ff,dynamic_rounding as dr,export_cones
O.mkdir(exist_ok=True);assert not (O/'POOL_EXTENSION.json').exists()
for f in OLD.iterdir():
 if f.suffix in ['.npz','.json','.bas'] and not f.name.startswith(('DUAL_','RESULT','NONOPTIMAL','LAST_NATIVE')) and f.name not in ['FLOAT_CANDIDATE.json','FLOAT_MOMENTS.npz','MASTER_HISTORY.json','STARTED.json','CONTINUED.json','INITIAL_ALIAS_MAP.json','INITIAL_BASIS.json','POOL_EXTENSION.json']:shutil.copyfile(f,O/f.name)
graphs=json.loads((O/'POOL_GRAPH_CODES.json').read_text());oldset=set(graphs);nold=len(graphs);batch=json.loads((P/'oracle_batch/BATCH_VERIFIED.json').read_text());new=[x for x in batch['graphs'] if x['graph_mask'] not in oldset];ng=[x['graph_mask'] for x in new];graphs+=ng;(O/'POOL_GRAPH_CODES.json').write_text(json.dumps(graphs)+'\n');info=json.loads((P/'pool_inventory/LP_STARTED.json').read_text());starts=info['packed_starts'];F=sparse.load_npz(O/'INTEGER_FEATURES.npz');D=F.shape[1];coeff=[];ri=[];ci=[];vals=[]
for k,g in enumerate(ng):
 rho,c=ff.local_coefficients(ff.q4_edges_from_mask(g));coeff.append(c)
 for (b,i,j),v in c.items():ri.append(k);ci.append(starts[b]+i*ff.DIMS[b]-i*(i-1)//2+j-i);vals.append(v)
newF=sparse.csr_matrix((vals,(ri,ci)),shape=(len(ng),D),dtype=np.int64);sparse.save_npz(O/'INTEGER_FEATURES.npz',sparse.vstack([F,newF],format='csr'));U=sparse.load_npz(O/'EDGE_U_NUMERATOR.npz');sparse.save_npz(O/'EDGE_U_NUMERATOR.npz',sparse.hstack([U,export_cones.pool_moment_numerators(ng)],format='csr'))
def score(c,mat,b):return sum(v*int(mat[i][j]) for (bb,i,j),v in c.items() if bb==b)
x=np.load(O/'MARGINAL_FEATURES.npz');hist=[x['degree_histogram'] for x in new];even=[x['Q2_edgecount_histogram'][0]+x['Q2_edgecount_histogram'][2] for x in new];kernelmat=[json.loads((O/f'block{b}.EXACT_SEPARATOR.json').read_text())['full_Q'] for b in [1,4]];kk=[[score(c,m,b) for m,b in zip(kernelmat,[1,4])] for c in coeff];np.savez_compressed(O/'MARGINAL_FEATURES.npz',hist=np.vstack([x['hist'],hist]),even=np.r_[x['even'],even],kernel_raw=np.vstack([x['kernel_raw'],kk]),kernel_scales=x['kernel_scales'],profile_hypergeom=x['profile_hypergeom'])
cv=np.load(O/'CONDITIONAL_VERTEX_FEATURES.npz');cut=json.loads((O/'CONDITIONAL_VERTEX_CUT.json').read_text());np.savez_compressed(O/'CONDITIONAL_VERTEX_FEATURES.npz',local_raw=np.r_[cv['local_raw'],[score(c,cut['integer_Q'],5) for c in coeff]],profile_bias_raw=cv['profile_bias_raw'],positive_scale=cv['positive_scale'])
con=np.load(O/'CONNECTOR_FEATURES.npz');vals=[]
for c in coeff:
 row=[]
 for cut in json.loads((O/'CONNECTOR_CUTS.json').read_text())['cuts']:
  M=cut['full_state_connector_codes'];Q=cut['integer_connector_Q'];row.append(sum(v*Q[M[i]][M[j]] for (b,i,j),v in c.items() if b==cut['block']))
 vals.append(row)
np.savez_compressed(O/'CONNECTOR_FEATURES.npz',raw=np.vstack([con['raw'],vals]),scales=con['scales'])
rr=np.load(O/'ROUNDING_FEATURES.npz');vals=[]
for cut in json.loads((O/'ROUNDING_FAMILY.json').read_text())['cuts']:
 coords,ss=dr.full_packed(cut['block'],dr.BITS[cut['block']][:,cut['bit']].tolist(),cut['t'],starts,D);vals.append(newF@coords)
np.savez_compressed(O/'ROUNDING_FEATURES.npz',raw=np.vstack([rr['raw'],np.array(vals).T]),scales=rr['scales'])
a=json.loads((O/'ACTIVE_COLUMNS.json').read_text());maps=json.loads((O/'NATIVE_COLUMN_MAP.json').read_text());newcol=max(list(maps['lambda'].values())+maps['alpha']+maps['beta']+maps['artificial'])+1;take=min(64,len(ng))
for k in range(take):a['indices'].append(nold+k);a['graph_masks'].append(ng[k]);maps['lambda'][str(nold+k)]=newcol+k
a['native_column_map']=maps['lambda'];(O/'ACTIVE_COLUMNS.json').write_text(json.dumps(a)+'\n');(O/'NATIVE_COLUMN_MAP.json').write_text(json.dumps(maps)+'\n');bas=(O/'checkpoint.bas').read_text().splitlines();i=next(i for i,x in enumerate(bas) if x.startswith('# Columns '));oldn=int(bas[i].split()[-1]);assert oldn==newcol;bas[i]=f'# Columns {oldn+take}';bas[i+1+oldn:i+1+oldn]=[f'batch_new{newcol+k} 0' for k in range(take)];(O/'checkpoint.bas').write_text('\n'.join(bas)+'\n');(O/'MASTER_HISTORY.json').write_text('[]\n');(O/'STARTED.json').write_text(json.dumps({'scope':'same valid maximal shared lambda model plus batch actual Q4s','parent_scope':str(OLD),'continuation_pending':True})+'\n');out={'status':'FULL_ORACLE_BATCH_EXACT_FEATURES_ADDED','new_actual_graphs':ng,'old_library':nold,'new_library':len(graphs),'new_active_first_batch':take,'active_lambda_total':len(a['indices']),'all_new_library_still_priced':True,'native_positions_pinned':True,'old_scope_preserved':True,'no_new_math_gates':True,'no_fullNO_or_graph':True,'batch_verified_sha256':hashlib.sha256((P/'oracle_batch/BATCH_VERIFIED.json').read_bytes()).hexdigest()};(O/'POOL_EXTENSION.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='new_actual_graphs'}))
