"""Preserve first diagnostics, enrich B with every verified positive class.

Only universally valid A-discovered parameter inequalities transfer. Its
case domain, alpha arrays, tuples and dual conclusions do not transfer.
"""
from pathlib import Path
import sys,json,shutil,time,hashlib,itertools
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;OLD=P/'pool_case_B684plus';A=P/'pool_case_A683';R=P/'pool_B684plus_enriched1'
sys.path.insert(0,str(P.parent/'finite8_flags/deps'));sys.path.insert(0,str(P.parent/'finite8_flags'));sys.path.insert(0,str(P.parent/'finite8_edge_flags'));sys.path.insert(0,str(P));sys.path.insert(0,str(P.parent/'finite8_root_checks'))
import numpy as np
from scipy import sparse
import finite_flags as ff,export_cones,dynamic_rounding as dr
from check_vertex_cut import matrix as independent_vertex_matrix
from check_edge3_sampling import local
t=time.monotonic();R.mkdir(exist_ok=False)
excluded={'FLOAT_CANDIDATE.json','FLOAT_MOMENTS.npz','MASTER_HISTORY.json','RESULT.json','INITIAL_ALIAS_MAP.json','ADAPTIVE_VERTEX_PRICING.json','ADAPTIVE_CONNECTOR_PRICING.json','RUN_STARTED.json','ACTIVE_CUT_ROWS.json'}
for f in OLD.iterdir():
 if f.is_file() and f.suffix in ('.json','.npz','.md') and not f.name.startswith(('DUAL_','LAST_','RUN_')) and f.name not in excluded:shutil.copyfile(f,R/f.name)
for name in ['profile_exclusion_imports','vertex_pricing','maximal_vertex_parameters','edge_vertex_bridge_inputs','edge3_sampling_inputs','connector_pricing','projection_pricing']:
 if (OLD/name).exists():shutil.copytree(OLD/name,R/name)
oldmeta=json.loads((OLD/'CUT_ROW_METADATA.json').read_text());ameta=json.loads((A/'CUT_ROW_METADATA.json').read_text());assert len(oldmeta)==8002 and ameta[:8002]==oldmeta
newmeta=ameta[8002:];assert len(newmeta)==38 and all(v['kind'] in ['PSD','INTEGER_ROUNDING','CONNECTOR_FINITE6_EXTRA'] for v in newmeta)
for row in newmeta:
 if row['kind']=='CONNECTOR_FINITE6_EXTRA':
  sub=Path(row['source']).parent
  if not (R/sub).exists():shutil.copytree(A/sub,R/sub)
meta=oldmeta+newmeta;(R/'CUT_ROW_METADATA.json').write_text(json.dumps(meta)+'\n')
graphs=json.loads((R/'POOL_GRAPH_CODES.json').read_text());nold=len(graphs);assert nold==14838;oldset=set(graphs)
batchfile=OLD/'full_oracle_001/all_positive_classes/BATCH_VERIFIED.json';batch=json.loads(batchfile.read_text());cand=[v for v in batch['graphs'] if v['graph_mask'] not in oldset];assert len(cand)==171
F=sparse.load_npz(R/'INTEGER_FEATURES.npz');D=F.shape[1];U=sparse.load_npz(R/'EDGE_U_NUMERATOR.npz');Uc=U.tocsc();zz=np.load(R/'MARGINAL_FEATURES.npz');H=zz['hist'];starts=json.loads((P/'pool_inventory/LP_STARTED.json').read_text())['packed_starts']
coeff=[];ri=[];ci=[];val=[]
for k,row in enumerate(cand):
 _,co=ff.local_coefficients(ff.q4_edges_from_mask(row['graph_mask']));coeff.append(co)
 for (b,i,j),v in co.items():ri.append(k);ci.append(starts[b]+i*ff.DIMS[b]-i*(i-1)//2+j-i);val.append(v)
NF=sparse.csr_matrix((val,(ri,ci)),shape=(len(cand),D),dtype=np.int64);NU=export_cones.pool_moment_numerators([v['graph_mask'] for v in cand]);NUc=NU.tocsc();NH=np.array([v['degree_histogram'] for v in cand],dtype=H.dtype)
def key(f,u,h,i):
 a,b=f.indptr[i:i+2];c,d=u.indptr[i:i+2]
 return f.indices[a:b].astype(np.int32).tobytes(),f.data[a:b].astype(np.int64).tobytes(),np.asarray(h[i],dtype=np.int16).tobytes(),u.indices[c:d].astype(np.int32).tobytes(),u.data[c:d].astype(np.int64).tobytes()
seen={key(F,Uc,H,i):graphs[i] for i in range(nold)};keep=[];aliases=[]
for i,row in enumerate(cand):
 k=key(NF,NUc,NH,i)
 if k in seen:aliases.append({'actual_mask':row['graph_mask'],'equal_F_hist_edgeU_mask':seen[k]})
 else:seen[k]=row['graph_mask'];keep.append(i)
cand=[cand[i] for i in keep];coeff=[coeff[i] for i in keep];NF=NF[keep];NU=NU[:,keep];NH=NH[keep];ng=[v['graph_mask'] for v in cand];graphs+=ng;G=len(graphs)
(R/'POOL_GRAPH_CODES.json').write_text(json.dumps(graphs)+'\n');sparse.save_npz(R/'INTEGER_FEATURES.npz',sparse.vstack([F,NF],format='csr'));sparse.save_npz(R/'EDGE_U_NUMERATOR.npz',sparse.hstack([U,NU],format='csr'))
def score(c,Q,b):return sum(v*int(Q[i][j]) for (bb,i,j),v in c.items() if bb==b)
Qold=[json.loads((R/f'block{b}.EXACT_SEPARATOR.json').read_text())['full_Q'] for b in [1,4]];Knew=np.array([[score(c,Q,b) for Q,b in zip(Qold,[1,4])] for c in coeff],dtype=np.int64)
even=[v['Q2_edgecount_histogram'][0]+v['Q2_edgecount_histogram'][2] for v in cand];np.savez_compressed(R/'MARGINAL_FEATURES.npz',hist=np.vstack([H,NH]),even=np.r_[zz['even'],even],kernel_raw=np.vstack([zz['kernel_raw'],Knew]),kernel_scales=zz['kernel_scales'],profile_hypergeom=zz['profile_hypergeom'])
done=set();extended=[]
for row in meta:
 kind=row['kind']
 if kind not in ['CONDITIONAL_VERTEX','CONDITIONAL_VERTEX_EXTRA','CONNECTOR_FINITE6_EXTRA','FULL_FINITE6_PROJECTION_EXTRA']:continue
 path=row.get('feature_source','CONDITIONAL_VERTEX_FEATURES.npz')
 if path in done:continue
 done.add(path);f=R/path;x=np.load(f);data={k:x[k] for k in x.files};assert data['local_raw'].shape==(nold,)
 q=json.loads((R/row.get('source','CONDITIONAL_VERTEX_CUT.json')).read_text());b=row.get('block',5)
 if kind in ['CONDITIONAL_VERTEX','CONDITIONAL_VERTEX_EXTRA']:Q=q['integer_Q']
 elif kind=='FULL_FINITE6_PROJECTION_EXTRA':Q=q['full_Q']
 else:
  codes=q['full_state_connector_codes'];Q=[[q['connector_Q'][i][j] for j in codes] for i in codes]
 data['local_raw']=np.r_[data['local_raw'],[score(c,Q,b) for c in coeff]];np.savez_compressed(f,**data);extended.append(path)
x=np.load(R/'CONNECTOR_FEATURES.npz');cv=[]
for c in coeff:
 vals=[]
 for cut in json.loads((R/'CONNECTOR_CUTS.json').read_text())['cuts']:
  b=cut['block'];mp=cut['full_state_connector_codes'];Q=cut['integer_connector_Q'];vals.append(sum(v*Q[mp[i]][mp[j]] for (bb,i,j),v in c.items() if bb==b))
 cv.append(vals)
np.savez_compressed(R/'CONNECTOR_FEATURES.npz',raw=np.vstack([x['raw'],cv]),scales=x['scales'])
x=np.load(R/'ROUNDING_FEATURES.npz');vals=[]
for cut in json.loads((R/'ROUNDING_FAMILY.json').read_text())['cuts']:
 coords,sc=dr.full_packed(cut['block'],dr.BITS[cut['block']][:,cut['bit']].tolist(),cut['t'],starts,D);vals.append(NF@coords)
np.savez_compressed(R/'ROUNDING_FEATURES.npz',raw=np.vstack([x['raw'],np.array(vals).T]),scales=x['scales'])
ii,jj=np.triu_indices(9)
for g,c in zip(ng,coeff):
 M=np.array(independent_vertex_matrix(g),dtype=np.int64)
 for i,j in zip(ii,jj):assert c.get((5,int(i),int(j)),0)==int(M[i,j])*(1 if i==j else 2)
K=sparse.load_npz(R/'edge3_sampling_inputs/LIFT_EDGE3_LIFT_PACKED_KERNELS.npz');order=[(v['root'],tuple(v['histogram'])) for v in json.loads((R/'edge3_sampling_inputs/LIFT_ROW_ORDER.json').read_text())];zi={v:i for i,v in enumerate(order)};L=np.zeros((len(ng),204),dtype=np.int64)
for i,g in enumerate(ng):
 for k,v in local(g).items():L[i,zi[k]]=v
assert (4*(NF@K.T)-5*64512*sparse.csr_matrix(L)).nnz==0
assert len(json.loads((R/'PROFILE_SNAPSHOT.json').read_text())['remaining'])==645
for name in ['PROFILE_SNAPSHOT.json','EDGE_DEGREE_PROFILE_RHS_NUMERATOR.npz','LEAF_NEIGHBOR_FEATURES.npz','EDGE_GENERATOR_DEDUP_NUMERATOR.npz']:
 assert hashlib.sha256((R/name).read_bytes()).digest()==hashlib.sha256((OLD/name).read_bytes()).digest()
active=json.loads((R/'ACTIVE_COLUMNS.json').read_text());active['indices']+=list(range(nold,nold+min(64,len(ng))));active['graph_masks']+=ng[:64];(R/'ACTIVE_COLUMNS.json').write_text(json.dumps(active)+'\n')
(R/'STARTED.json').write_text('{"scope":"enriched B684plus with A global-valid inequalities, prepared"}\n')
out={'status':'B684PLUS_ENRICHED_ACTUAL_INPUTS_READY','source_B_case_preserved':True,'source_A_domain_not_transferred':True,'old_library':nold,'verified_positive_class_representatives':len(batch['graphs']),'new_mask_candidates':171,'exact_F_hist_edgeU_aliases':aliases,'new_unique_columns':len(ng),'new_library':G,'active_initial':len(active['indices']),'A_global_valid_rows_added':len(newmeta),'A_added_kinds':{k:sum(v['kind']==k for v in newmeta) for k in ['PSD','INTEGER_ROUNDING','CONNECTOR_FINITE6_EXTRA']},'all_stored_rows':len(meta),'alpha':645,'beta':1751,'common_equalities':356,'same_B_alpha_beta_array_hashes_pass':True,'all_new_vertex45_and_edge3_204_literal_checks':'PASS','extended_parameter_feature_files':extended,'positive_class_input_sha256':hashlib.sha256(batchfile.read_bytes()).hexdigest(),'seconds':time.monotonic()-t,'goal':'OPEN'}
(R/'ENRICHED_SCOPE_INPUT.json').write_text(json.dumps(out,indent=2)+'\n')
s=(P/'pool_case_B684plus_run_active_dual.py').read_text().replace("R=P/'pool_case_B684plus'","R=P/'pool_B684plus_enriched1'")
(P/'B684plus_enriched_run.py').write_text(s)
print(json.dumps({k:v for k,v in out.items() if k not in ['exact_F_hist_edgeU_aliases','extended_parameter_feature_files']}))
