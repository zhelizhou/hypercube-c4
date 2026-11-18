"""Share seven global finite6 inequalities, without sharing A's case domain."""
from pathlib import Path
from fractions import Fraction
import sys,json,shutil,hashlib,itertools,time
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;R=(P/sys.argv[1]).resolve();A=P.parent/'finite8_case_A_independent/scope001'
sys.path.insert(0,str(P.parent/'finite8_flags/deps'));sys.path.insert(0,str(P.parent/'finite8_flags'))
import numpy as np
from scipy import sparse
import finite_flags as ff
t=time.monotonic();assert not (R/'RUN_STARTED.json').exists();F=sparse.load_npz(R/'INTEGER_FEATURES.npz');graphs=json.loads((R/'POOL_GRAPH_CODES.json').read_text());gi={g:i for i,g in enumerate(graphs)};starts=json.loads((P/'pool_inventory/LP_STARTED.json').read_text())['packed_starts'];meta=json.loads((R/'CUT_ROW_METADATA.json').read_text());before=len(meta);checks=[]
hist=np.zeros((54264,16),dtype=np.int64)
for i,ms in enumerate(itertools.combinations_with_replacement(range(16),6)):
 for j in ms:hist[i,j]+=1
for master,blocks in [(30,[0,1,2,3]),(62,[0,1,3])]:
 source=A/'connector_pricing_runtime'/f'master_{master:03d}';point=json.loads((source/'INPUT_POINT.json').read_text());weights=[(gi[g],Fraction(str(v))) for g,v in point['lambda']];target=R/'connector_pricing/from_A_independent'/f'master_{master:03d}';target.mkdir(parents=True,exist_ok=True)
 for name in ['INPUT_POINT.json','INDEPENDENT_CHECK.json','RESULT.json']:
  if (source/name).exists():shutil.copyfile(source/name,target/name)
 for b in blocks:
  src=source/f'block{b}.EXACT_CUT.json';d=json.loads(src.read_text());shutil.copyfile(src,target/src.name);Q=np.asarray(d['connector_Q'],dtype=np.int64);assert Q.shape==(16,16) and np.array_equal(Q,Q.T);vals=np.sum((hist@Q)*hist,axis=1);assert min(vals)>=0
  codes=np.asarray(d['full_state_connector_codes'],dtype=int);assert len(codes)==ff.DIMS[b];ii,jj=np.triu_indices(ff.DIMS[b]);raw=np.asarray(F[:,starts[b]:starts[b+1]]@Q[codes[ii],codes[jj]],dtype=np.int64);pair=sum((w*int(raw[i])/64512 for i,w in weights),Fraction());assert pair==Fraction(d['exact_target_pairing']) and pair<0
  feature=target/f'block{b}.FEATURES.npz';np.savez_compressed(feature,local_raw=raw);scale=1<<(int(d['positive_normalization'])-1).bit_length();meta.append({'kind':'CONNECTOR_FINITE6_EXTRA','block':b,'source':str((target/src.name).relative_to(R)),'feature_source':str(feature.relative_to(R)),'positive_power2_normalization':scale,'exported_positive_normalization':d['positive_normalization'],'scope':'GENERAL_C4FREE_ANY_M','origin':'A-independent global finite6 parameter shared; Root independent full-domain/literal receipt and consumer complete-domain/exactpair replay'})
  checks.append({'master':master,'block':b,'row':len(meta)-1,'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'complete_histograms':len(hist),'minimum_integer_quadratic':int(min(vals)),'exact_A_target_pair':str(pair),'source_normalized_pair':str(pair/d['positive_normalization']),'LP_pair':float(pair/scale)})
(R/'CUT_ROW_METADATA.json').write_text(json.dumps(meta)+'\n');out={'status':'SEVEN_SHARED_GLOBAL_CONNECTOR_KERNELS_IMPORTED_PASS','before':before,'after':len(meta),'no_A_domain_or_dual_conclusion_transferred':True,'alpha645_beta1751_356eq_unchanged':True,'checks':checks,'seconds':time.monotonic()-t,'goal':'OPEN'};(R/'SCOPE_INCREMENT_007_A_INDEPENDENT_CONNECTOR7.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
