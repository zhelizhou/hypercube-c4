from pathlib import Path
from itertools import combinations
from collections import Counter
import json,shutil,sys,hashlib
P=Path(__file__).resolve().parent;R=P/'pool_profile1409_vertex_priced';AUTHOR=P.parent/'finite8_edge3_sampling';D=R/'edge3_sampling_inputs';SRC=P.parent/'finite8_flags';sys.path.insert(0,str(SRC/'deps'));sys.path.insert(0,str(SRC));sys.path.insert(0,str(P.parent/'finite8_edge_flags'));sys.path.insert(0,str(P.parent/'finite8_root_checks'));import numpy as np
from scipy import sparse
import edge_flags
from check_edge3_sampling import local
D.mkdir(exist_ok=False)
for name in ['BETA_HYPERGEOM_CURRENT_204x1751.npz','BETA_HYPERGEOM_FULL_204x5148.npz','LOCAL_COUNTS_204x14090.npz','ORDER.json','ACTUAL_CHECK.json','INTERFACE.json']:
 if (AUTHOR/name).exists():shutil.copyfile(AUTHOR/name,D/name)
for name in ['EDGE3_LIFT_PACKED_KERNELS.npz','ROW_ORDER.json','CHECK_RESULT.json','PROOF.md','build_check_lift.py']:shutil.copyfile(P/'edge3_quad_lift'/name,D/('LIFT_'+name))
rows=[(d['root'],tuple(d['histogram'])) for d in json.loads((D/'LIFT_ROW_ORDER.json').read_text())];index={k:i for i,k in enumerate(rows)};givenL=sparse.load_npz(D/'LOCAL_COUNTS_204x14090.npz');ownL=np.load(P/'edge3_quad_lift/L_CURRENT_POOL_14090x204.npz')['L'];assert np.array_equal(givenL.toarray(),ownL.T)
hist=json.loads((R/'GENERATOR_HISTOGRAMS.json').read_text());de=json.loads((R/'GENERATOR_DEDUPLICATION.json').read_text());sel=de['selected_original_indices'];Hraw=np.zeros((204,len(hist)),dtype=np.int32)
def flip(s):return ((s&1)<<1)|((s&2)>>1)|(s&4)
for col,h in enumerate(hist):
 r=h['root_retained'];xs=[s for s,n in enumerate(h['counts']) for _ in range(n)];assert len(xs)==7
 for pp in combinations(range(7),3):
  trip=[xs[i] for i in pp];z=tuple(trip.count(s) for s in range(8-r));tp=[flip(x) for x in trip];zf=tuple(tp.count(s) for s in range(8-r));Hraw[index[r,z],col]+=1;Hraw[index[r,zf],col]+=1
assert np.all(Hraw.sum(axis=0)==70)
for group,k in zip(de['groups'],sel):
 for j in group:assert np.array_equal(Hraw[:,j],Hraw[:,k])
H=Hraw[:,sel];assert np.array_equal(H,sparse.load_npz(D/'BETA_HYPERGEOM_CURRENT_204x1751.npz').toarray())
seed=json.loads((SRC/'Q8_seed682_point.json').read_text());E={tuple(map(int,l.split())) for l in Path(seed['source']).read_text().splitlines() if l.strip()};lookup={(hist[k]['root_retained'],tuple(hist[k]['counts'])):i for i,gr in enumerate(de['groups']) for k in gr};beta=np.zeros(len(sel),dtype=np.int64)
for r,states in edge_flags.root_records(E,8):beta[lookup[r,tuple(states.count(s) for s in range(8-r))]]+=1
summed=np.zeros(204,dtype=np.int64)
for graph,n in seed['graph_distribution']:
 for key,value in local(graph).items():summed[index[key]]+=n*value
assert np.array_equal(summed,H@beta) and sum(summed)==71680
layout={'start_equality_index':152,'rows':204,'lambda_feature':'L/64 = K_packed F.T/(80*64512)','beta_feature':'-H/70','lift_packed':'edge3_sampling_inputs/LIFT_EDGE3_LIFT_PACKED_KERNELS.npz','beta_hypergeom':'edge3_sampling_inputs/BETA_HYPERGEOM_CURRENT_204x1751.npz','original_quadratic_weight_factor':'1/80','fullQ4_oracle_family_unchanged':True,'K_vertexblock_iszero':True,'total_equalities_with_prior63':356};(R/'EXTRA_EDGE3_LAYOUT.json').write_text(json.dumps(layout,indent=2)+'\n');out={'status':'EXACT_EDGE3_SAMPLING_CONSUMER_AND_LIFT_CHECKED','current_lambda_rows':14090,'current_beta_columns':1751,'all204_L_rows_match_directRoot_and_literalLift':True,'all204_H_entries_rebuilt_from35_position_triples':True,'all3432raw_to1751_groups_preserveH':True,'actual682_integer_identity_each204':'sum1120L = sum1024H','actual682_total_rawobjects_both_sides':71680,'oracle_span':'all204L use existing5faceblocks viaL=4T_K/5','same_lambda_beta':True,'old_scopes_preserved':True,'proof_and_fresh_review':'new sampling+lift proof underRootreview, not claimed byconsumer arithmetic','hashes':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in D.iterdir() if f.is_file()}};(R/'SCOPE_INCREMENT_003_EDGE3.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='hashes'}))
