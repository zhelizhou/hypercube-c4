"""Freeze complete edge7 cone plus exact endpoint/global-degree bridge data.
Full generators are preserved; only EXACT duplicate full generator+endpoint
columns are merged. No per-root beta mass is fixed to1.
"""
from pathlib import Path
from collections import Counter
import sys,json,time,shutil,hashlib
P=Path(__file__).resolve().parent;R=P/'pool_edge_degree_dynamic';SRC=P.parent/'finite8_flags';EDGE=P.parent/'finite8_edge_flags'
sys.path.insert(0,str(SRC/'deps'));sys.path.insert(0,str(SRC));sys.path.insert(0,str(EDGE))
import numpy as np
from scipy import sparse
import export_cones,edge_flags
R.mkdir(exist_ok=True);assert not (R/'PREPARED.json').exists();old=P/'pool_inventory_rounding';st=time.monotonic()
for n in ['PROFILE_SNAPSHOT.json','INVENTORY_INPUT.bin','POOL_GRAPH_CODES.json','INTEGER_FEATURES.npz','MARGINAL_FEATURES.npz','ROUNDING_FEATURES.npz','ROUNDING_FAMILY.json','FAMILY_EXACT_CHECK.json','block1.EXACT_SEPARATOR.json','block4.EXACT_SEPARATOR.json','FINITE6_ROOT_CHECK.json','KERNEL_SOURCE_SNAPSHOT.json']:shutil.copyfile(old/n,R/n)
for n in ['GENERATOR_NUMERATOR.npz','GENERATOR_INTERFACE.json','GENERATOR_HISTOGRAMS.json']:shutil.copyfile(EDGE/n,R/n)
graphs=json.loads((R/'POOL_GRAPH_CODES.json').read_text());profiles=json.loads((R/'PROFILE_SNAPSHOT.json').read_text())['remaining'];hist=json.loads((R/'GENERATOR_HISTOGRAMS.json').read_text());GF=sparse.load_npz(R/'GENERATOR_NUMERATOR.npz').tocsc();assert GF.shape==(64,5148) and len(hist)==5148
endpoint=np.zeros((18,5148),dtype=np.int32)
for k,h in enumerate(hist):
 r=h['root_retained'];x=h['counts'];assert sum(x)==7 and len(x)==(8 if r==0 else 7)
 a=sum((s&1)*v for s,v in enumerate(x))+r;b=sum(((s>>1)&1)*v for s,v in enumerate(x))+r;endpoint[9*r+a,k]+=1;endpoint[9*r+b,k]+=1
keys={};groups=[];selected=[]
for k in range(5148):
 p0,p1=GF.indptr[k:k+2];key=(tuple(map(int,GF.indices[p0:p1])),tuple(map(int,GF.data[p0:p1])),tuple(map(int,endpoint[:,k])))
 if key in keys:groups[keys[key]].append(k)
 else:keys[key]=len(groups);groups.append([k]);selected.append(k)
G=GF[:,selected].tocsr();EP=sparse.csr_matrix(endpoint[:,selected]);U=export_cones.pool_moment_numerators(graphs);sparse.save_npz(R/'EDGE_U_NUMERATOR.npz',U);sparse.save_npz(R/'EDGE_GENERATOR_DEDUP_NUMERATOR.npz',G);sparse.save_npz(R/'EDGE_ENDPOINT_DEDUP.npz',EP)
RHS=np.array([[(d if r==1 else 8-d)*row['degrees'][d] for row in profiles] for r in range(2) for d in range(9)],dtype=np.int32);sparse.save_npz(R/'EDGE_DEGREE_PROFILE_RHS_NUMERATOR.npz',sparse.csr_matrix(RHS))
# Reconstruct every original column, so duplicate merging has no lost domain.
assert len({k for gr in groups for k in gr})==5148
for rep,gr in zip(selected,groups):
 for k in gr:
  assert (GF[:,k]!=GF[:,rep]).nnz==0 and np.array_equal(endpoint[:,k],endpoint[:,rep])
# Exact new degree-bridge regression on all1024 ambient edges of actual682 G.
seed=json.loads((SRC/'Q8_seed682_point.json').read_text());source=Path(seed['source']);EE={tuple(map(int,line.split())) for line in source.read_text().splitlines() if line.strip()};degrees=[sum(x==v or y==v for x,y in EE) for v in range(256)];ND=Counter(degrees);lookup={(h['root_retained'],tuple(h['counts'])):i for i,h in enumerate(hist)};counts=np.zeros(5148,dtype=np.int64)
for (u,v),(r,states) in zip(edge_flags.ambient(8),edge_flags.root_records(EE,8)):
 x=[states.count(s) for s in range(8 if r==0 else 7)];aa=sum((s&1)*n for s,n in enumerate(x))+r;bb=sum(((s>>1)&1)*n for s,n in enumerate(x))+r;assert aa==degrees[u] and bb==degrees[v];counts[lookup[r,tuple(x)]]+=1
assert int(counts.sum())==1024
lhs=endpoint@counts;expected=np.array([(d if r==1 else 8-d)*ND[d] for r in range(2) for d in range(9)]);assert np.array_equal(lhs,expected)
seedgraphs=[int(g) for g,n in seed['graph_distribution']];seedweights=np.array([int(n) for g,n in seed['graph_distribution']],dtype=np.int64);UU=export_cones.pool_moment_numerators(seedgraphs);local=UU@seedweights;globalmom=GF@counts;assert np.array_equal(98*1024*local,129024*1120*globalmom)
# Ordered-mass contracts: each generator has fullmatrix sum98; each local U sum129024.
roworder=export_cones.ROW_ORDER;massweights=np.array([1 if i==j else 2 for r,i,j in roworder],dtype=np.int64);assert np.all(massweights@GF==98) and np.all(massweights@U==129024)
(R/'GENERATOR_DEDUPLICATION.json').write_text(json.dumps({'full_columns':5148,'dedup_columns':len(selected),'selected_original_indices':selected,'groups':groups,'key':'exact64momentnumerators AND exact18endpointcounts','all5148reconstructed_exactly':True},indent=2)+'\n')
meta={'status':'EXACT_EDGE7_AND_DEGREE_BRIDGE_INPUT_PREPARED','graphs':len(graphs),'profiles':len(profiles),'profile_sha256':hashlib.sha256((R/'PROFILE_SNAPSHOT.json').read_bytes()).hexdigest(),'edge_full_generators':5148,'edge_unique_generators':len(selected),'edge_moment_rows':64,'endpoint_degree_rows':18,'generator_denominator':98,'local_edge_moment_denominator':129024,'profile_degree_RHS_denominator':512,'equations':['U/129024 @lambda=G/98 @beta','EP@beta=RHS/512 @alpha'],'no_independent_roottype_mass_one':True,'actual682_exact_checks':['all1024individualedgeendpointdegrees','all18globaldegreeincidencecounts','same1120Q4lambda vs empiricaledge7hist moment,all64entries'],'actual682_degree_incidence_vector':expected.tolist(),'prepare_seconds':time.monotonic()-st,'full_Q4_domain_coverage_claim':False,'primary683_goal':'OPEN'}
(R/'PREPARED.json').write_text(json.dumps(meta,indent=2)+'\n');print(json.dumps(meta))
