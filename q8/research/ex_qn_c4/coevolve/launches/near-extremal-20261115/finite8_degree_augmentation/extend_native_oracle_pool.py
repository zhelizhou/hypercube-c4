"""Add one literal full-oracle Q4 column in a new preserved scope."""
from pathlib import Path
import sys,json,shutil,itertools,hashlib
P=Path(__file__).resolve().parent;OLD=P/'pool_native_leaf_simplex';O=P/'pool_native_oracle_extension1';SRC=P.parent/'finite8_flags';sys.path.insert(0,str(SRC/'deps'));sys.path.insert(0,str(SRC));sys.path.insert(0,str(P.parent/'finite8_edge_flags'));sys.path.insert(0,str(P))
import numpy as np
from scipy import sparse
import finite_flags as ff,dynamic_rounding as dr,export_cones
O.mkdir(exist_ok=True);assert not (O/'POOL_EXTENSION.json').exists()
for f in OLD.iterdir():
 if f.suffix in ['.npz','.json','.bas'] and not f.name.startswith(('DUAL_','RESULT','NONOPTIMAL','LAST_NATIVE')) and f.name not in ['FLOAT_CANDIDATE.json','FLOAT_MOMENTS.npz','MASTER_HISTORY.json','STARTED.json','CONTINUED.json','INITIAL_ALIAS_MAP.json','INITIAL_BASIS.json']:shutil.copyfile(f,O/f.name)
g=int(json.loads((OLD/'full_oracle_001/OWN_ORACLE_VIOLATOR.json').read_text())['graph_mask']);graphs=json.loads((O/'POOL_GRAPH_CODES.json').read_text());assert g not in graphs;nold=len(graphs);graphs.append(g);(O/'POOL_GRAPH_CODES.json').write_text(json.dumps(graphs)+'\n');info=json.loads((P/'pool_inventory/LP_STARTED.json').read_text());starts=info['packed_starts'];F=sparse.load_npz(O/'INTEGER_FEATURES.npz');D=F.shape[1];E=ff.q4_edges_from_mask(g);rho,c=ff.local_coefficients(E);indices=[starts[b]+i*ff.DIMS[b]-i*(i-1)//2+j-i for b,i,j in c];row=sparse.csr_matrix((list(c.values()),([0]*len(c),indices)),shape=(1,D),dtype=np.int64);sparse.save_npz(O/'INTEGER_FEATURES.npz',sparse.vstack([F,row],format='csr'))
U=sparse.load_npz(O/'EDGE_U_NUMERATOR.npz');sparse.save_npz(O/'EDGE_U_NUMERATOR.npz',sparse.hstack([U,export_cones.pool_moment_numerators([g])],format='csr'))
x=np.load(O/'MARGINAL_FEATURES.npz');hist=[sum(sum(v==a or v==b for a,b in E)==j for v in range(16)) for j in range(5)];even=0
for a,b in itertools.combinations(range(4),2):
 for v in range(16):
  if v&((1<<a)|(1<<b)):continue
  vs=[v,v^(1<<a),v^(1<<b),v^(1<<a)^(1<<b)];sq=[tuple(sorted((vs[0],vs[1]))),tuple(sorted((vs[0],vs[2]))),tuple(sorted((vs[1],vs[3]))),tuple(sorted((vs[2],vs[3])))];even+=sum(t in E for t in sq) in [0,2]
def score(mat,b):return sum(v*int(mat[i][j]) for (bb,i,j),v in c.items() if bb==b)
kk=[score(json.loads((O/f'block{b}.EXACT_SEPARATOR.json').read_text())['full_Q'],b) for b in [1,4]]
np.savez_compressed(O/'MARGINAL_FEATURES.npz',hist=np.vstack([x['hist'],hist]),even=np.r_[x['even'],even],kernel_raw=np.vstack([x['kernel_raw'],kk]),kernel_scales=x['kernel_scales'],profile_hypergeom=x['profile_hypergeom'])
cv=np.load(O/'CONDITIONAL_VERTEX_FEATURES.npz');cut=json.loads((O/'CONDITIONAL_VERTEX_CUT.json').read_text());np.savez_compressed(O/'CONDITIONAL_VERTEX_FEATURES.npz',local_raw=np.r_[cv['local_raw'],score(cut['integer_Q'],5)],profile_bias_raw=cv['profile_bias_raw'],positive_scale=cv['positive_scale'])
con=np.load(O/'CONNECTOR_FEATURES.npz');vals=[]
for cut in json.loads((O/'CONNECTOR_CUTS.json').read_text())['cuts']:
 M=cut['full_state_connector_codes'];Q=cut['integer_connector_Q'];vals.append(sum(v*Q[M[i]][M[j]] for (b,i,j),v in c.items() if b==cut['block']))
np.savez_compressed(O/'CONNECTOR_FEATURES.npz',raw=np.vstack([con['raw'],vals]),scales=con['scales'])
rr=np.load(O/'ROUNDING_FEATURES.npz');vals=[]
for cut in json.loads((O/'ROUNDING_FAMILY.json').read_text())['cuts']:
 coords,ss=dr.full_packed(cut['block'],dr.BITS[cut['block']][:,cut['bit']].tolist(),cut['t'],starts,D);vals.append(int((row@coords)[0]))
np.savez_compressed(O/'ROUNDING_FEATURES.npz',raw=np.vstack([rr['raw'],vals]),scales=rr['scales'])
# New actual graph is appended as a lower/nonbasic native column. All original
# alpha/beta/artificial positions and the saved basis remain pinned.
a=json.loads((O/'ACTIVE_COLUMNS.json').read_text());a['indices'].append(nold);a['graph_masks'].append(g);maps=json.loads((O/'NATIVE_COLUMN_MAP.json').read_text());newcol=max(list(maps['lambda'].values())+maps['alpha']+maps['beta']+maps['artificial'])+1;maps['lambda'][str(nold)]=newcol;a['native_column_map']=maps['lambda'];(O/'ACTIVE_COLUMNS.json').write_text(json.dumps(a)+'\n');(O/'NATIVE_COLUMN_MAP.json').write_text(json.dumps(maps)+'\n')
# Append one lower status to basis while retaining every native row status.
bas=(O/'checkpoint.bas').read_text().splitlines();i=next(i for i,x in enumerate(bas) if x.startswith('# Columns '));oldn=int(bas[i].split()[-1]);assert oldn==newcol;bas[i]=f'# Columns {oldn+1}';bas.insert(i+1+oldn,f'oracle_new{newcol} 0');(O/'checkpoint.bas').write_text('\n'.join(bas)+'\n')
(O/'MASTER_HISTORY.json').write_text('[]\n');(O/'STARTED.json').write_text(json.dumps({'scope':'same maximal leaf/connector mathematics, new actual full-oracle Q4 column','parent_scope':str(OLD),'continuation_pending':True})+'\n');out={'status':'ACTUAL_FULL_ORACLE_COLUMN_EXACTLY_EXTRACTED','new_graph':g,'edges':len(E),'histogram':hist,'even_squares':even,'old_library':nold,'new_library':nold+1,'new_active_lambda':len(a['indices']),'new_native_column_position':newcol,'native_basis':'old complete basis plus new lower column','old_scope_preserved':True,'new_mathematical_gates':False,'no_fullNO_or_graph':True,'source_oracle_receipt_sha256':hashlib.sha256((OLD/'full_oracle_001/OWN_ORACLE_RUN.json').read_bytes()).hexdigest()};(O/'POOL_EXTENSION.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
