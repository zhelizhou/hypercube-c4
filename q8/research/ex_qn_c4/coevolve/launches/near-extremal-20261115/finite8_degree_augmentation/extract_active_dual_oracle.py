"""Reconstruct numerical phaseI pricing functional, round its local score,
then exact fullQ4 oracle can supply an actual new column. This is deliberately
not an exact Farkas certificate or fullNO claim.
"""
from pathlib import Path
import sys,json,hashlib
P=Path(__file__).resolve().parent;R=P/(sys.argv[1] if len(sys.argv)>1 else 'pool_vertex3_working_sets');nn=1
while (R/f'full_oracle_{nn:03d}').exists():nn+=1
O=R/f'full_oracle_{nn:03d}';O.mkdir();SRC=P.parent/'finite8_flags';EDGE=P.parent/'finite8_edge_flags';sys.path.insert(0,str(SRC/'deps'));sys.path.insert(0,str(SRC));sys.path.insert(0,str(EDGE));sys.path.insert(0,str(P))
import numpy as np
from scipy import sparse
import finite_flags as ff,edge_flags,lift,dynamic_rounding as dr
result=json.loads((R/'RESULT.json').read_text());assert result['status']=='NUMERIC_LIBRARY_DUAL_CANDIDATE';y=np.array(result['equality_duals']);z=np.array(result['inequality_duals']);meta=json.loads((R/'CUT_ROW_METADATA.json').read_text());F=sparse.load_npz(R/'INTEGER_FEATURES.npz');D=F.shape[1];info=json.loads((P/'pool_inventory/LP_STARTED.json').read_text());starts=info['packed_starts'];W=np.zeros(D);cuts=json.loads((R/'CONNECTOR_CUTS.json').read_text())['cuts']
for row,v in zip(meta,z):
 if abs(v)<1e-13:continue
 kind=row['kind'];b=row.get('block');ss=row.get('positive_power2_normalization',1)
 if kind=='PSD':
  q=np.array(row['q'],dtype=np.int64);ii,jj=np.triu_indices(ff.DIMS[b]);W[starts[b]:starts[b+1]]+=-v*q[ii]*q[jj]/ss
 elif kind=='INTEGER_ROUNDING':
  coords,unused=dr.full_packed(b,row['q'],row['t'],starts,D);W+=-v*coords/ss
 elif kind=='FINITE6_KERNEL':
  mat=np.array(json.loads((R/f'block{b}.EXACT_SEPARATOR.json').read_text())['full_Q'],dtype=np.int64);ii,jj=np.triu_indices(ff.DIMS[b]);W[starts[b]:starts[b+1]]+=-v*mat[ii,jj]/ss
 elif kind in ['CONDITIONAL_VERTEX','CONDITIONAL_VERTEX_EXTRA']:
  c=json.loads((R/row.get('source','CONDITIONAL_VERTEX_CUT.json')).read_text());mat=np.array(c['integer_Q'],dtype=np.int64);ii,jj=np.triu_indices(9);W[starts[5]:starts[6]]+=-v*mat[ii,jj]/ss
 elif kind=='FULL_FINITE6_PROJECTION_EXTRA':
  c=json.loads((R/row['source']).read_text());mat=np.array(c['full_Q']);ii,jj=np.triu_indices(ff.DIMS[b]);W[starts[b]:starts[b+1]]+=-v*mat[ii,jj]/ss
 elif kind=='CONNECTOR_FINITE6_EXTRA':
  c=json.loads((R/row['source']).read_text());codes=np.array(c['full_state_connector_codes']);mat=np.array(c['connector_Q']);ii,jj=np.triu_indices(ff.DIMS[b]);W[starts[b]:starts[b+1]]+=-v*mat[codes[ii],codes[jj]]/ss
 elif kind=='CONNECTOR_FINITE6':
  c=next(c for c in cuts if c['block']==b);codes=np.array(c['full_state_connector_codes']);mat=np.array(c['integer_connector_Q']);ii,jj=np.triu_indices(ff.DIMS[b]);W[starts[b]:starts[b+1]]+=-v*mat[codes[ii],codes[jj]]/ss
 else:assert kind in ['GLOBAL_MAXIMAL_LEAF','RETAINED_NEIGHBOR_DEGREE_CAPACITY']
# The64 equality coordinates are true symmetric-upper moments, not packed
# linearQ coefficients. Qdiag=2y, Qoff=y has traceQ M=2 sum_upper y M.
Q=[np.zeros((d,d)) for d in (8,7)];k=7
for b,d in enumerate((8,7)):
 for i in range(d):
  for j in range(i,d):Q[b][i,j]=Q[b][j,i]=(2 if i==j else 1)*y[k];k+=1
assert k==71
num,den=lift.lift_to_faces(Q,already_averaged=False);assert den==392
for b,mat in enumerate(num):
 ii,jj=np.triu_indices(ff.DIMS[b]);W[starts[b]:starts[b+1]]+=np.array(mat)[ii,jj]/784
if (R/'EXTRA_EQUALITY_LAYOUT.json').exists():
 layout=json.loads((R/'EXTRA_EQUALITY_LAYOUT.json').read_text());selector=sparse.load_npz(R/layout['moment_selector_matrix']);k=layout['moment_start'];W[starts[5]:starts[6]]+=(64512*layout['moment_lambda_integer_multiplier']/layout['moment_LP_positive_divisor'])*np.asarray(selector.T@y[k:k+27]).ravel()
if (R/'EXTRA_EDGE3_LAYOUT.json').exists():
 e3=json.loads((R/'EXTRA_EDGE3_LAYOUT.json').read_text());klift=sparse.load_npz(R/e3['lift_packed']);kk=e3['start_equality_index'];W+=np.asarray(klift.T@y[kk:kk+e3['rows']]).ravel()/80
hist=(y[2:7]+y[0])/16
H=np.load(R/'MARGINAL_FEATURES.npz')['hist']
if (R/'DUAL_ACTIVE_LAYOUT.json').exists():
 alayout=json.loads((R/'DUAL_ACTIVE_LAYOUT.json').read_text());ai=np.array(alayout['active_rows'],dtype=int);az=z[ai];assert len(z)==alayout['full_valid_row_count'];assert np.all(z[np.setdiff1d(np.arange(len(z)),ai)]==0)
 actual=sparse.load_npz(R/'DUAL_EL.npz').T@y+sparse.load_npz(R/'DUAL_ACTIVE_AL.npz').T@az
else:actual=sparse.load_npz(R/'DUAL_EL.npz').T@y+sparse.load_npz(R/'DUAL_AL.npz').T@z
recon=H@hist+(F@W)/64512;err=float(max(abs(actual-recon)));assert err<1e-11,err
T=10**9;weights=np.rint(T*W).astype(np.int64);hw=np.rint(T*64512*hist).astype(np.int64);scores=np.asarray(F@weights+H@hw,dtype=np.int64);rounderr=float(max(abs(scores/(64512*T)-actual)))
coords=[]
for b,d in enumerate(ff.DIMS):
 ii,jj=np.triu_indices(d)
 for a,i,j in zip(weights[starts[b]:starts[b+1]],ii,jj):
  if a:coords.append([b,int(i),int(j),int(a)])
out={'status':'EXACT_INTEGER_LOCAL_PRICING_FUNCTION_FROM_NUMERIC_DUAL','source_dual_sha256':hashlib.sha256((R/'RESULT.json').read_bytes()).hexdigest(),'mathematical_scope':'fulllocalQ4 pricing query only, not an exact dual or original theorem','original_finite8_upper_coefficient_weights':coords,'histogram_weights_j0_to_j4':hw.tolist(),'edge_weight':0,'integer_score_positive_denominator':64512*T,'exact_full_library_integer_score_minmax':[int(min(scores)),int(max(scores))],'float_reconstruction_error_max':err,'float_rounding_error_max_on_library':rounderr,'numeric_dual_objective':result['phase1_objective'],'integerization_T':T,'root_edge_lift_denominator':784,'exact_fullNO_claim':False}
(O/'LOCAL_PRICE_SCORE.json').write_text(json.dumps(out,separators=(',',':'))+'\n');np.savez_compressed(O/'NUMERIC_DUAL_PACKED_FUNCTION.npz',weights_float=W,hist_float=hist,weights_integer=weights,hist_integer=hw)
print(json.dumps({k:v for k,v in out.items() if k!='original_finite8_upper_coefficient_weights'}))
