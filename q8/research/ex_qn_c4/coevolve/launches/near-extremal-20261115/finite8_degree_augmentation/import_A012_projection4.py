"""Consume four Root-reviewed global kernels at an unstarted B boundary."""
from pathlib import Path
from fractions import Fraction
import sys,json,shutil,hashlib,itertools,time
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;R=(P/sys.argv[1]).resolve();ROOT=P.parent/'finite8_root_checks'
sys.path.insert(0,str(P.parent/'finite8_flags/deps'));sys.path.insert(0,str(P.parent/'finite8_flags'))
import numpy as np
from scipy import sparse
import finite_flags as ff
t=time.monotonic();assert not (R/'RUN_STARTED.json').exists()
F=sparse.load_npz(R/'INTEGER_FEATURES.npz');graphs=json.loads((R/'POOL_GRAPH_CODES.json').read_text());gi={g:i for i,g in enumerate(graphs)};starts=json.loads((P/'pool_inventory/LP_STARTED.json').read_text())['packed_starts'];meta=json.loads((R/'CUT_ROW_METADATA.json').read_text());before=len(meta)
sources=[('projection_A012_joint_counts16',0),('projection_A012_parity_parallel_shape10',3),('projection_A012_joint_shape15',0),('projection_A012_joint_shape15',3)];checks=[]
point=json.loads((P/'pool_case_A683/point_bank/master_012.json').read_text());weights=[(gi[g],Fraction(str(v))) for g,v in point['lambda']]
for folder,b in sources:
 src=ROOT/folder/f'block{b}.EXACT_CUT.json';d=json.loads(src.read_text());target=R/'projection_pricing/A012_joint4'/folder;target.mkdir(parents=True,exist_ok=True)
 for f in [src,ROOT/folder/'INDEPENDENT_CHECK.json']:
  shutil.copyfile(f,target/f.name)
 Q=np.asarray(d['small_Q'],dtype=np.int64);L=d['labels'];hist=np.zeros((len(list(itertools.combinations_with_replacement(range(L),6))),L),dtype=np.int64)
 for i,ms in enumerate(itertools.combinations_with_replacement(range(L),6)):
  for j in ms:hist[i,j]+=1
 vals=np.sum((hist@Q)*hist,axis=1);assert min(vals)>=0
 labels=np.asarray(d['full_state_to_label'],dtype=int);perms=d['root_state_permutations'];K=np.asarray(d['full_Q'],dtype=np.int64);rebuilt=np.zeros_like(K)
 for perm in perms:
  pp=labels[np.asarray(perm,dtype=int)];rebuilt+=Q[np.ix_(pp,pp)]
 assert np.array_equal(K,rebuilt)
 for perm in perms:assert np.array_equal(K,K[np.ix_(perm,perm)])
 ii,jj=np.triu_indices(ff.DIMS[b]);raw=np.asarray(F[:,starts[b]:starts[b+1]]@K[ii,jj],dtype=np.int64)
 pair=sum((p*int(raw[i])/64512 for i,p in weights),Fraction());assert pair==Fraction(d['exact_target_pairing']),(folder,b,pair,d['exact_target_pairing']);assert pair<0
 feature=target/f'block{b}.FEATURES.npz';np.savez_compressed(feature,local_raw=raw);scale=1<<(int(d['positive_normalization'])-1).bit_length()
 row={'kind':'FULL_FINITE6_PROJECTION_EXTRA','block':b,'source':str((target/src.name).relative_to(R)),'feature_source':str(feature.relative_to(R)),'positive_power2_normalization':scale,'exported_positive_normalization':d['positive_normalization'],'already_full_root_stabilizer_sum':True,'scope':'GENERAL_C4FREE_ANY_M','origin':'Root fresh general projection semantic PASS same-family/provisional; actual complete-domain/literal Root replay plus this consumer exact replay'}
 meta.append(row);checks.append({'source':str(src),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'row':len(meta)-1,'histograms':len(hist),'minimum_small_count_quadratic':int(min(vals)),'all_full_kernel_entries_rebuilt':True,'all_exported_root_actions_invariant':True,'actual_A012_exact_raw_pair':str(pair),'source_normalized_pair':str(pair/d['positive_normalization']),'LP_positive_normalization':scale,'LP_pair':float(pair/scale),'no_additional_stabilizer_factor':True})
(R/'CUT_ROW_METADATA.json').write_text(json.dumps(meta)+'\n')
result={'status':'FOUR_GLOBAL_PROJECTION_KERNELS_IMPORTED_EXACT_PASS','before':before,'after':len(meta),'alpha_case_unchanged':645,'beta_unchanged':1751,'equalities_unchanged':356,'checks':checks,'seconds':time.monotonic()-t,'goal':'OPEN','generic_review_scope':'fresh Sol ultra same-family/provisional as communicated by Root; no wholeGoal acceptance'};(R/'SCOPE_INCREMENT_006_A012_PROJECTION4.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
