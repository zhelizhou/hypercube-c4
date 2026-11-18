"""Maximal-extension six-m union inputs and actual682 joint calibration.
No exact683 maximal assumption; no fixed683 density/even gate survives.
"""
from pathlib import Path
from collections import Counter
from math import comb
from fractions import Fraction as Q
import sys,json,shutil,hashlib,time
P=Path(__file__).resolve().parent;R=P/'pool_maximal_union_dynamic';SRC=P.parent/'finite8_flags';EDGE=P.parent/'finite8_edge_flags';MAX=P.parent/'finite8_maximal_route';sys.path.insert(0,str(SRC/'deps'));sys.path.insert(0,str(SRC));sys.path.insert(0,str(EDGE))
import numpy as np
from scipy import sparse
import finite_flags as ff
import edge_flags,export_cones,verify_obstruction as vo
R.mkdir(exist_ok=True);assert not (R/'PREPARED.json').exists();old=P/'pool_edge_degree_dynamic';start=time.monotonic()
for n in ['INVENTORY_INPUT.bin','POOL_GRAPH_CODES.json','INTEGER_FEATURES.npz','ROUNDING_FEATURES.npz','ROUNDING_FAMILY.json','FAMILY_EXACT_CHECK.json','block1.EXACT_SEPARATOR.json','block4.EXACT_SEPARATOR.json','FINITE6_ROOT_CHECK.json','KERNEL_SOURCE_SNAPSHOT.json','EDGE_U_NUMERATOR.npz']:shutil.copyfile(old/n,R/n)
for n in ['PROFILE_COVER.json','EDGE7_GENERATORS.json','PROOF.md','CHECK.json']:shutil.copyfile(MAX/n,R/('MAXIMAL_'+n))
cover=json.loads((R/'MAXIMAL_PROFILE_COVER.json').read_text());profiles=[];counts={}
for m in range(683,689):
 part=cover[str(m)]['maximal_profiles'];counts[m]=len(part)
 for row in part:
  n=row['n'];assert n[0]==0 and sum(n)==128 and sum(i*v for i,v in enumerate(n))==m
  profiles.append({'m':m,'degrees':n,'C':row['C'],'b':row['b']})
assert counts=={683:783,684:385,685:170,686:66,687:20,688:4}
(R/'PROFILE_SNAPSHOT.json').write_text(json.dumps({'scope':'maximal H with m683..688; convex necessary union; no old23exclusions applied','remaining_count':len(profiles),'remaining':profiles,'fixed683_density':False,'even_square_gate_choice':'DROP entire683-onlygate'},indent=2)+'\n')
new=json.loads((R/'MAXIMAL_EDGE7_GENERATORS.json').read_text());hist=[{'root_retained':r,'counts':x} for r,name in [(0,'root0_maximal'),(1,'root1')] for x in new[name]];assert len(new['root0_maximal'])==len(new['root1'])==1716 and len(hist)==3432
rows=export_cones.ROW_ORDER;ri={tuple(x):i for i,x in enumerate(rows)};Gfull=np.zeros((64,len(hist)),dtype=np.int32);EPfull=np.zeros((18,len(hist)),dtype=np.int32)
for k,h in enumerate(hist):
 r=h['root_retained'];x=h['counts'];d=len(x);assert sum(x)==7 and (r==1 or x[7]>=1)
 for i in range(d):
  for j in range(i,d):Gfull[ri[r,i,j],k]=x[i]*x[j]+x[edge_flags.flip(i)]*x[edge_flags.flip(j)]
 a=sum((s&1)*v for s,v in enumerate(x))+r;b=sum(((s>>1)&1)*v for s,v in enumerate(x))+r;EPfull[9*r+a,k]+=1;EPfull[9*r+b,k]+=1
seen={};groups=[];selected=[]
for k in range(len(hist)):
 key=(Gfull[:,k].tobytes(),EPfull[:,k].tobytes())
 if key in seen:groups[seen[key]].append(k)
 else:seen[key]=len(groups);groups.append([k]);selected.append(k)
assert len({k for gr in groups for k in gr})==3432
for gr in groups:
 for k in gr:assert np.array_equal(Gfull[:,k],Gfull[:,gr[0]]) and np.array_equal(EPfull[:,k],EPfull[:,gr[0]])
sparse.save_npz(R/'EDGE_GENERATOR_FULL_NUMERATOR.npz',sparse.csr_matrix(Gfull));sparse.save_npz(R/'EDGE_GENERATOR_DEDUP_NUMERATOR.npz',sparse.csr_matrix(Gfull[:,selected]));sparse.save_npz(R/'EDGE_ENDPOINT_DEDUP.npz',sparse.csr_matrix(EPfull[:,selected]));(R/'GENERATOR_HISTOGRAMS.json').write_text(json.dumps(hist)+'\n');(R/'GENERATOR_DEDUPLICATION.json').write_text(json.dumps({'full_columns':3432,'missing_full_columns':1716,'dedup_columns':len(selected),'selected_original_indices':selected,'groups':groups,'all_originals_preserved':True,'key':'exact64moment+18endpointnumerators'},indent=2)+'\n')
z=np.load(old/'MARGINAL_FEATURES.npz');B=np.array([[sum(row['degrees'][d]*comb(d,j)*comb(8-d,4-j) for d in range(9) if j<=d and 4-j<=8-d) for j in range(5)] for row in profiles],dtype=np.int64);np.savez_compressed(R/'MARGINAL_FEATURES.npz',hist=z['hist'],even=z['even'],kernel_raw=z['kernel_raw'],kernel_scales=z['kernel_scales'],profile_hypergeom=B);RHS=np.array([[(d if r==1 else 8-d)*row['degrees'][d] for row in profiles] for r in range(2) for d in range(9)],dtype=np.int32);sparse.save_npz(R/'EDGE_DEGREE_PROFILE_RHS_NUMERATOR.npz',sparse.csr_matrix(RHS))
# True actual682 calibration, with its separate one-row alpha; never inserted
# into the counterexample683..688 profile union.
seed=json.loads((SRC/'Q8_seed682_point.json').read_text());EE={tuple(map(int,line.split())) for line in Path(seed['source']).read_text().splitlines() if line.strip()};degs=[sum(v==x or v==y for x,y in EE) for v in range(256)];ND=Counter(degs);n=[ND[d]//2 for d in range(9)];assert all(ND[d]==2*n[d] for d in range(9)) and sum(n)==128 and sum(d*n[d] for d in range(9))==682
assert all([sum(v.bit_count()%2==p and degs[v]==d for v in range(256)) for d in range(9)]==n for p in [0,1])
lookup={(h['root_retained'],tuple(h['counts'])):i for i,h in enumerate(hist)};counts_beta=np.zeros(len(hist),dtype=np.int64);closing=Counter()
for (u,v),(r,states) in zip(edge_flags.ambient(8),edge_flags.root_records(EE,8)):
 x=[states.count(s) for s in range(8 if r==0 else 7)];assert r==1 or x[7]>=1
 if r==0:closing[x[7]]+=1
 assert r+sum((s&1)*nn for s,nn in enumerate(x))==degs[u] and r+sum(((s>>1)&1)*nn for s,nn in enumerate(x))==degs[v];counts_beta[lookup[r,tuple(x)]]+=1
assert counts_beta.sum()==1024
sg=[int(g) for g,w in seed['graph_distribution']];sw=np.array([int(w) for g,w in seed['graph_distribution']],dtype=np.int64);assert len(sg)==818 and int(sw.sum())==1120
co=Counter();hh=np.zeros(5,dtype=np.int64);edgesum=0
for g,w in zip(sg,sw):
 E=ff.q4_edges_from_mask(g);rho,c=ff.local_coefficients(E);co.update({k:int(w)*v for k,v in c.items()});dd=[sum(v==x or v==y for x,y in E) for v in range(16)];hh+=int(w)*np.array([dd.count(j) for j in range(5)]);edgesum+=int(w)*len(E)
assert 32*edgesum==682*1120
for j in range(5):assert 560*int(hh[j])==1120*sum(n[d]*comb(d,j)*comb(8-d,4-j) for d in range(9) if j<=d and 4-j<=8-d)
UU=export_cones.pool_moment_numerators(sg);assert np.array_equal(98*1024*(UU@sw),129024*1120*(Gfull@counts_beta));assert np.array_equal(EPfull@counts_beta,np.array([(d if r==1 else 8-d)*ND[d] for r in range(2) for d in range(9)]))
# Empirical Gram identity proves all six PSDs exactly, not by tolerance.
direct=Counter();face_roots=0
for b,mapped in vo.face_records(EE,8):
 face_roots+=1
 for states in mapped:
  cc=Counter(states)
  for i,ni in cc.items():
   for j,nj in cc.items():direct[b,i,j]+=(2240//len(mapped))*ni*nj
vertices=0
for pairs,states in vo.vertex_records(EE,8):
 vertices+=1;cc=Counter(states)
 for i,ni in cc.items():
  for j,nj in cc.items():direct[5,i,j]+=720*ni*nj
vo.compare_blocks(direct,seed['blocks']);vo.compare_blocks(direct,ff.dense_blocks(co));assert face_roots==1792 and vertices==256
# All fixed and already generated valid nonPSD features on the same true818 lambda.
kernelmins=[]
for b in [1,4]:
 cert=json.loads((R/f'block{b}.EXACT_SEPARATOR.json').read_text());val=sum(v*cert['full_Q'][i][j] for (bb,i,j),v in co.items() if bb==b);assert val>=0;kernelmins.append(int(val))
valid_defs=json.loads((old/'DYNAMIC_ROUNDING_CUTS.json').read_text())+json.loads((old/'FULL_STATE_EIGEN_ROUNDING_PROBE.json').read_text())['cuts'];family=json.loads((R/'ROUNDING_FAMILY.json').read_text())
for cut in family['cuts']:
 b,bit,t=cut['block'],cut['bit'],cut['t'];states=sorted(ff.STATE_IDS[b],key=ff.STATE_IDS[b].get);valid_defs.append({'block':b,'q':[(s>>bit)&1 for s in states],'t':t})
roundvalues=[]
for cut in valid_defs:
 b,q,t=cut['block'],cut['q'],cut['t'];nn=28 if b==5 else 6;vv=sum(v*(nn*nn*q[i]*q[j]-(nn//2)*(2*t+1)*(q[i]+q[j])+t*(t+1)) for (bb,i,j),v in co.items() if bb==b);assert vv>=0;roundvalues.append(int(vv))
(R/'SEED682_JOINT_CALIBRATION.json').write_text(json.dumps({'status':'PASS_EXACT_ACTUAL682_JOINT_CALIBRATION','source_graph':seed['source'],'actual_m':682,'actual_Q4_unique_types':818,'actual_Q4_faces':1120,'separate_calibration_alpha_row':n,'not_in_counterexample_union':True,'density_exact':'341/512','density_identity':'32 E e(K)=682','maximal_missing_closing_square_counts':dict(closing),'edge_hist_counts':len(hist),'actual_beta_nonzero':int(sum(counts_beta>0)),'edge_moment64_same_lambda_exact':True,'endpoint18_same_alpha_beta_exact':True,'hypergeom5_exact':True,'all6PSD':'Exact equality to sum of actual root empirical outer products','face_roots_checked':face_roots,'vertex_roots_checked':vertices,'frozen_kernel_raw_pairings':kernelmins,'rounding_features_checked':len(roundvalues),'minimum_rounding_raw_pairing':min(roundvalues),'683_only_even_gate':'DROPPED, not wrongly applied to seed or m684..688'},indent=2)+'\n')
meta={'status':'PREPARED_AND_ACTUAL682_CALIBRATED','counterexample_domain':'maximal H, integer m683..688; necessary convex union','profile_count':len(profiles),'profile_counts_by_m':counts,'full_edge_generators':len(hist),'root_full_counts':[1716,1716],'dedup_edge_generators':len(selected),'fixed683_density':False,'density_tie':'32 Eλ e(K)=sum alpha m(profile), via unchanged5Hg equations','683_only_even_gate_choice':'DROP entire gate','original23_exclusions_choice':'not applied to any m','all_old_globalvalid_PSD_and_rounding_cuts_retained':True,'seed_calibration_file':'SEED682_JOINT_CALIBRATION.json','prepare_seconds':time.monotonic()-start,'primary683_goal':'OPEN'}
(R/'PREPARED.json').write_text(json.dumps(meta,indent=2)+'\n');print(json.dumps(meta))
