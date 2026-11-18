"""Independent formula reconstruction, exact actual682 calibration, consumer input."""
from pathlib import Path
from math import comb
from collections import Counter
import json,shutil,sys,hashlib
P=Path(__file__).resolve().parent;R=P/'pool_profile1409_vertex_priced';D=R/'edge_vertex_bridge_inputs';SRC=P.parent/'finite8_flags';AUTHOR=P.parent/'finite8_edge_vertex_bridge';sys.path.insert(0,str(SRC/'deps'));sys.path.insert(0,str(SRC));sys.path.insert(0,str(P.parent/'finite8_edge_flags'));import numpy as np
from scipy import sparse
import finite_flags as ff,edge_flags
D.mkdir(exist_ok=False)
for name in ['INTERFACE.json','ORDER.json','BALANCE_CURRENT_36x1751.npz','BALANCE_CURRENT_36x1751.json','C_CURRENT_162x1751.npz','C_CURRENT_162x1751.json','MOMENT_INTERFACE.json','MOMENT_ORDER.json','MOMENT_BETA_CURRENT_27x1751.npz','MOMENT_BETA_CURRENT_27x1751.json','MOMENT_PACKED9_SELECTOR_TWICE_27x45.npz','MOMENT_PACKED9_SELECTOR_TWICE_27x45.json','export_bridge.py']:
 if (AUTHOR/name).exists():shutil.copyfile(AUTHOR/name,D/name)
assert hashlib.sha256((D/'BALANCE_CURRENT_36x1751.json').read_bytes()).hexdigest()=='10fdbab3d504634f5fd6abaf1a6e38f7ce58e9467c8622d7d86ab05a7e74e6af';assert hashlib.sha256((D/'MOMENT_BETA_CURRENT_27x1751.json').read_bytes()).hexdigest()=='370b801b4fe8af67ce1af85176bbb091f29bf886c4378ac16f5e38fc82f5d969';assert hashlib.sha256((D/'MOMENT_PACKED9_SELECTOR_TWICE_27x45.json').read_bytes()).hexdigest()=='67e94a0e6106cdefdcb15d714136df21d26d34112b2034e449086bc9466a3fea'
hist=json.loads((R/'GENERATOR_HISTOGRAMS.json').read_text());de=json.loads((R/'GENERATOR_DEDUPLICATION.json').read_text());sel=de['selected_original_indices'];order=json.loads((D/'ORDER.json').read_text());assert order['current_selected_raw_indices']==sel;reps=(0,1,3,4,5,6,7,12,13);mixed=(1,4,5,8)
def swap(c):return ((c&1)<<1)|((c&2)>>1)|((c&4)<<1)|((c&8)>>1)
def column(h):
 r=h['root_retained'];x=h['counts'];a=r+sum((s&1)*n for s,n in enumerate(x));b=r+sum(((s>>1)&1)*n for s,n in enumerate(x));out=np.zeros(162,dtype=np.int64)
 for s,n in enumerate(x):
  A=s&1;B=(s>>1)&1;O=(s>>2)&1
  for degree,code in [(a,r+2*A+4*B+8*O),(b,r+2*B+4*A+8*O)]:out[r*81+9*degree+reps.index(min(code,swap(code)))]+=n
 assert sum(out)==14;return out
raw=np.stack([column(h) for h in hist],axis=1);C=raw[:,sel];given=sparse.load_npz(D/'C_CURRENT_162x1751.npz').toarray();assert np.array_equal(C,given)
for group,k in zip(de['groups'],sel):
 for j in group:assert np.array_equal(raw[:,j],raw[:,k])
Bmix=np.array([C[81+9*d+j]-C[9*d+j] for d in range(9) for j in mixed],dtype=np.int64);assert np.array_equal(Bmix,sparse.load_npz(D/'BALANCE_CURRENT_36x1751.npz').toarray());groups=((0,3,7),(1,4,5,8),(2,6));Fg=[[comb(8-d,2),d*(8-d),comb(d,2)] for d in range(9)];B=np.array([sum(Fg[d][g]*(C[9*d+i]+C[81+9*d+i]) for d in range(9)) for g in range(3) for i in range(9)],dtype=np.int64);assert np.array_equal(B,sparse.load_npz(D/'MOMENT_BETA_CURRENT_27x1751.npz').toarray());coords=list(zip(*np.triu_indices(9)));W=np.zeros((27,45),dtype=np.int64)
for g in range(3):
 for i in range(9):
  for j in groups[g]:W[g*9+i,coords.index((min(i,j),max(i,j)))]+=2 if i==j else 1
assert np.array_equal(W,sparse.load_npz(D/'MOMENT_PACKED9_SELECTOR_TWICE_27x45.npz').toarray())
# Actual maximal682 graph, one beta and lambda distribution; no use of683alpha cover.
seed=json.loads((SRC/'Q8_seed682_point.json').read_text());E={tuple(map(int,line.split())) for line in Path(seed['source']).read_text().splitlines() if line.strip()};lookup={(hist[k]['root_retained'],tuple(hist[k]['counts'])):i for i,group in enumerate(de['groups']) for k in group};bn=np.zeros(len(sel),dtype=np.int64)
for r,states in edge_flags.root_records(E,8):bn[lookup[r,tuple(states.count(s) for s in range(8-r))]]+=1
assert sum(bn)==1024 and np.max(abs(Bmix@bn))==0
packed=np.zeros(45,dtype=np.int64)
for graph,n in seed['graph_distribution']:
 _,c=ff.local_coefficients(ff.q4_edges_from_mask(graph))
 for (b,i,j),v in c.items():
  if b==5:packed[coords.index((i,j))]+=n*v
assert np.array_equal(W@packed,360*(B@bn))
layout={'base_equalities':89,'balance_start':89,'balance_rows':36,'balance_LP_positive_divisor':7,'moment_start':125,'moment_rows':27,'moment_LP_positive_divisor':129024,'moment_lambda_integer_multiplier':7,'moment_beta_integer_multiplier':-2304,'moment_original_packed_weight_factor':'7/2','balance_matrix':'edge_vertex_bridge_inputs/BALANCE_CURRENT_36x1751.npz','moment_beta_matrix':'edge_vertex_bridge_inputs/MOMENT_BETA_CURRENT_27x1751.npz','moment_selector_matrix':'edge_vertex_bridge_inputs/MOMENT_PACKED9_SELECTOR_TWICE_27x45.npz','same_beta_order':True,'no_independence_claim_for63_rows':True};(R/'EXTRA_EQUALITY_LAYOUT.json').write_text(json.dumps(layout,indent=2)+'\n');out={'status':'INDEPENDENT_RECONSTRUCTION_AND_ACTUAL682_JOINT_CALIBRATION_PASS','all162_by1751_C_entries_match':True,'all3432_raw_and1751_dedup_preserve_map':True,'all36_balance_and27moment_entries_match':True,'actual682_beta_ambient_roots':1024,'actual682_lambda_slices':1120,'actual682_balance_max_integer_residual':0,'actual682_moment_identity':'W*sum_slicec =360 B*beta_counts','actual682_moment_max_integer_residual':0,'all_C4free_anym_necessary_not_maximal_only':True,'semantic_fresh_review':'Root/author full proof and review separately tracked; not claimed by this consumer arithmetic check','same_lambda_alpha_beta':True,'source_hashes':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in D.iterdir() if f.is_file()}};(R/'SCOPE_INCREMENT_002_EDGE_VERTEX.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='source_hashes'}))
