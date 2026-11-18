"""All actual positive-class maximizers, exact feature dedup, preserved new scope."""
from pathlib import Path
import sys,json,shutil,time,hashlib
P=Path(__file__).resolve().parent;OLD=P/'pool_profile1409_vertex_priced';R=P/'pool_edge3_allclass1';SRC=P.parent/'finite8_flags';sys.path.insert(0,str(SRC/'deps'));sys.path.insert(0,str(SRC));sys.path.insert(0,str(P.parent/'finite8_edge_flags'));sys.path.insert(0,str(P));sys.path.insert(0,str(P.parent/'finite8_root_checks'));import numpy as np
from scipy import sparse
import finite_flags as ff,export_cones,dynamic_rounding as dr
from check_vertex_cut import matrix as independent_vertex_matrix
from check_edge3_sampling import local
st=time.monotonic();R.mkdir(exist_ok=True);assert not (R/'ALLCLASS_POOL_EXTENSION.json').exists()
for f in OLD.iterdir():
 if f.is_file() and f.suffix in ['.npz','.json'] and not f.name.startswith(('DUAL_','RESULT','LAST_','RUN_','CONTROL_','BRIDGE_TRANSITION','MAXIMAL_PARAMETER_TRANSITION')) and f.name not in ['FLOAT_CANDIDATE.json','FLOAT_MOMENTS.npz','MASTER_HISTORY.json','STARTED.json','CONTINUED.json','INITIAL_ALIAS_MAP.json','INITIAL_BASIS.json','ACTIVE_CUT_ROWS.json','NATIVE_COLUMN_MAP.json','ADAPTIVE_VERTEX_PRICING.json']:shutil.copyfile(f,R/f.name)
for name in ['profile_exclusion_imports','vertex_pricing','maximal_vertex_parameters','edge_vertex_bridge_inputs','edge3_sampling_inputs']:
 if (OLD/name).exists():shutil.copytree(OLD/name,R/name,dirs_exist_ok=True)
graphs=json.loads((R/'POOL_GRAPH_CODES.json').read_text());nold=len(graphs);assert nold==14090;oldset=set(graphs);batchfile=OLD/'full_oracle_001/all_positive_classes/BATCH_VERIFIED.json';batch=json.loads(batchfile.read_text());candidates=[v for v in batch['graphs'] if v['graph_mask'] not in oldset];ng=[v['graph_mask'] for v in candidates];F=sparse.load_npz(R/'INTEGER_FEATURES.npz');D=F.shape[1];U=sparse.load_npz(R/'EDGE_U_NUMERATOR.npz');Uc=U.tocsc();zz=np.load(R/'MARGINAL_FEATURES.npz');histold=zz['hist'];starts=json.loads((P/'pool_inventory/LP_STARTED.json').read_text())['packed_starts'];coeff=[];ri=[];ci=[];val=[]
for k,g in enumerate(ng):
 _,co=ff.local_coefficients(ff.q4_edges_from_mask(g));coeff.append(co)
 for (b,i,j),v in co.items():ri.append(k);ci.append(starts[b]+i*ff.DIMS[b]-i*(i-1)//2+j-i);val.append(v)
NF=sparse.csr_matrix((val,(ri,ci)),shape=(len(ng),D),dtype=np.int64);NU=export_cones.pool_moment_numerators(ng);NUc=NU.tocsc();NH=np.array([v['degree_histogram'] for v in candidates],dtype=histold.dtype)
def key(mat,u,h,i):
 a,b=mat.indptr[i:i+2];c,d=u.indptr[i:i+2]
 return mat.indices[a:b].astype(np.int32).tobytes(),mat.data[a:b].astype(np.int64).tobytes(),np.asarray(h[i],dtype=np.int16).tobytes(),u.indices[c:d].astype(np.int32).tobytes(),u.data[c:d].astype(np.int64).tobytes()
seen={key(F,Uc,histold,i):graphs[i] for i in range(nold)};keep=[];aliases=[]
for i,g in enumerate(ng):
 kk=key(NF,NUc,NH,i)
 if kk in seen:aliases.append({'actual_graph_mask':g,'exact_equal_F_hist_edgeU_representative':seen[kk]})
 else:seen[kk]=g;keep.append(i)
ng=[ng[i] for i in keep];candidates=[candidates[i] for i in keep];coeff=[coeff[i] for i in keep];NF=NF[keep];NU=NU[:,keep];NH=NH[keep];graphs+=ng;G=len(graphs);(R/'POOL_GRAPH_CODES.json').write_text(json.dumps(graphs)+'\n');sparse.save_npz(R/'INTEGER_FEATURES.npz',sparse.vstack([F,NF],format='csr'));sparse.save_npz(R/'EDGE_U_NUMERATOR.npz',sparse.hstack([U,NU],format='csr'))
def score(c,Q,b):return sum(v*int(Q[i][j]) for (bb,i,j),v in c.items() if bb==b)
Qold=[json.loads((R/f'block{b}.EXACT_SEPARATOR.json').read_text())['full_Q'] for b in [1,4]];Knew=np.array([[score(c,Q,b) for Q,b in zip(Qold,[1,4])] for c in coeff],dtype=np.int64);even=[v['Q2_edgecount_histogram'][0]+v['Q2_edgecount_histogram'][2] for v in candidates];np.savez_compressed(R/'MARGINAL_FEATURES.npz',hist=np.vstack([histold,NH]),even=np.r_[zz['even'],even],kernel_raw=np.vstack([zz['kernel_raw'],Knew]),kernel_scales=zz['kernel_scales'],profile_hypergeom=zz['profile_hypergeom'])
# Extend every already consumed conditional parameter feature, including
# dynamic general and maximal-only cuts nested in their frozen evidence dirs.
meta=json.loads((R/'CUT_ROW_METADATA.json').read_text());done=set();extended=[]
for row in meta:
 if row['kind'] not in ['CONDITIONAL_VERTEX','CONDITIONAL_VERTEX_EXTRA']:continue
 path=row.get('feature_source','CONDITIONAL_VERTEX_FEATURES.npz');source=row.get('source','CONDITIONAL_VERTEX_CUT.json')
 if path in done:continue
 done.add(path);f=R/path;x=np.load(f);data={k:x[k] for k in x.files};assert data['local_raw'].shape==(nold,);Q=json.loads((R/source).read_text())['integer_Q'];data['local_raw']=np.r_[data['local_raw'],[score(c,Q,5) for c in coeff]];np.savez_compressed(f,**data);extended.append(path)
x=np.load(R/'CONNECTOR_FEATURES.npz');cv=[]
for c in coeff:
 row=[]
 for cut in json.loads((R/'CONNECTOR_CUTS.json').read_text())['cuts']:
  b=cut['block'];M=cut['full_state_connector_codes'];Q=cut['integer_connector_Q'];row.append(sum(v*Q[M[i]][M[j]] for (bb,i,j),v in c.items() if bb==b))
 cv.append(row)
np.savez_compressed(R/'CONNECTOR_FEATURES.npz',raw=np.vstack([x['raw'],cv]),scales=x['scales']);x=np.load(R/'ROUNDING_FEATURES.npz');vals=[]
for cut in json.loads((R/'ROUNDING_FAMILY.json').read_text())['cuts']:
 coords,sc=dr.full_packed(cut['block'],dr.BITS[cut['block']][:,cut['bit']].tolist(),cut['t'],starts,D);vals.append(NF@coords)
np.savez_compressed(R/'ROUNDING_FEATURES.npz',raw=np.vstack([x['raw'],np.array(vals).T]),scales=x['scales'])
# New columns get independent ordered-geometry vertex features and all204
# literal edge3 counts compared with their universal quadratic lift.
ii,jj=np.triu_indices(9)
for g,co in zip(ng,coeff):
 M=np.array(independent_vertex_matrix(g),dtype=np.int64)
 for i,j in zip(ii,jj):assert co.get((5,int(i),int(j)),0)==int(M[i,j])*(1 if i==j else 2)
K=sparse.load_npz(R/'edge3_sampling_inputs/LIFT_EDGE3_LIFT_PACKED_KERNELS.npz');order=[(v['root'],tuple(v['histogram'])) for v in json.loads((R/'edge3_sampling_inputs/LIFT_ROW_ORDER.json').read_text())];zindex={v:i for i,v in enumerate(order)};literal=np.zeros((len(ng),204),dtype=np.int64)
for i,g in enumerate(ng):
 for kk,v in local(g).items():literal[i,zindex[kk]]=v
product=NF@K.T;assert (4*product-5*64512*sparse.csr_matrix(literal)).nnz==0
active=json.loads((R/'ACTIVE_COLUMNS.json').read_text());take=min(64,len(ng));active['indices']+=list(range(nold,nold+take));active['graph_masks']+=ng[:take];active.pop('native_column_map',None);(R/'ACTIVE_COLUMNS.json').write_text(json.dumps(active)+'\n');(R/'STARTED.json').write_text('{"scope":"full positive-class enriched same shared356eq model; prepared"}\n');out={'status':'ALL_POSITIVE_CLASS_ACTUAL_COLUMNS_ADDED_EXACTLY','raw_positive_classes':len(batch['graphs']),'already_identical_graph_masks':len(batch['graphs'])-len(keep)-len(aliases),'exact_F_hist_edgeU_aliases':aliases,'new_unique_feature_columns':len(ng),'old_library':nold,'new_library':G,'active_initial':len(active['indices']),'initial_new_active':take,'all_new_library_priced':True,'all_old_valid_rows':len(meta),'conditional_feature_files_extended':extended,'new_ordered_vertex_geometry_features_checked':len(ng),'all204_new_L_lift_literal_integer_residuals':0,'same_alpha1409_beta1751_356equalities':True,'edge3_moment_lambda_columns_recomputed_from_newF_eachstart':True,'static14090calibration_files_left_frozen':True,'no_complete_feature_classification_claim':True,'source_batch_sha256':hashlib.sha256(batchfile.read_bytes()).hexdigest(),'seconds':time.monotonic()-st};(R/'ALLCLASS_POOL_EXTENSION.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['exact_F_hist_edgeU_aliases','conditional_feature_files_extended']}))
s=(P/'vertex_priced_working_sets.py').read_text().replace("OLD=P/'pool_profile1409_working_sets';NEW=P/'pool_profile1409_vertex_priced'","OLD=P/'pool_profile1409_vertex_priced';NEW=P/'pool_edge3_allclass1'").replace("R=P/'pool_profile1409_vertex_priced'","R=P/'pool_edge3_allclass1'");(P/'edge3_allclass_working_sets.py').write_text(s)
