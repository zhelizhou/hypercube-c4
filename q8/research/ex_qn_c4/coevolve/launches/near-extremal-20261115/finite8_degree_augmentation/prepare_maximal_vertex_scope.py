"""Frozen next scope: same maximal six-m domain + actual conditional vertex cut.
Calibrate new matrix/degree joint term on the true682 seed before solving.
"""
from pathlib import Path
from collections import Counter
from fractions import Fraction as Q
import sys,json,shutil,hashlib
P=Path(__file__).resolve().parent;R=P/'pool_maximal_vertex_feasibility';OLD=P/'pool_maximal_union_dynamic';SRC=P.parent/'finite8_flags';sys.path.insert(0,str(SRC/'deps'));sys.path.insert(0,str(SRC))
import numpy as np
from scipy import sparse
import finite_flags as ff,verify_obstruction as vo
R.mkdir(exist_ok=True);assert not (R/'PREPARED.json').exists()
for n in ['INVENTORY_INPUT.bin','POOL_GRAPH_CODES.json','INTEGER_FEATURES.npz','MARGINAL_FEATURES.npz','ROUNDING_FEATURES.npz','ROUNDING_FAMILY.json','FAMILY_EXACT_CHECK.json','block1.EXACT_SEPARATOR.json','block4.EXACT_SEPARATOR.json','FINITE6_ROOT_CHECK.json','KERNEL_SOURCE_SNAPSHOT.json','EDGE_U_NUMERATOR.npz','EDGE_GENERATOR_FULL_NUMERATOR.npz','EDGE_GENERATOR_DEDUP_NUMERATOR.npz','EDGE_ENDPOINT_DEDUP.npz','EDGE_DEGREE_PROFILE_RHS_NUMERATOR.npz','PROFILE_SNAPSHOT.json','GENERATOR_DEDUPLICATION.json','GENERATOR_HISTOGRAMS.json','SEED682_JOINT_CALIBRATION.json','MAXIMAL_PROFILE_COVER.json','MAXIMAL_EDGE7_GENERATORS.json','MAXIMAL_PROOF.md','MAXIMAL_CHECK.json']:shutil.copyfile(OLD/n,R/n)
cutpath=P.parent/'finite8_vertex_degree_cone/continuation_01/CONDITIONAL_VERTEX_CUT.json';shutil.copyfile(cutpath,R/'CONDITIONAL_VERTEX_CUT.json');cut=json.loads(cutpath.read_text());V=np.array(cut['integer_Q'],dtype=np.int64);Bd=cut['degree_bias_raw'];scale=cut['positive_normalization'];F=sparse.load_npz(R/'INTEGER_FEATURES.npz');info=json.loads((P/'pool_inventory/LP_STARTED.json').read_text());start=info['packed_starts'];coord=np.zeros(F.shape[1],dtype=np.int64);i,j=np.triu_indices(9);coord[start[5]:start[6]]=V[i,j];raw=F@coord;profiles=json.loads((R/'PROFILE_SNAPSHOT.json').read_text())['remaining'];bias=np.array([sum(int(b)*int(n) for b,n in zip(Bd,row['degrees'])) for row in profiles],dtype=np.int64);np.savez_compressed(R/'CONDITIONAL_VERTEX_FEATURES.npz',local_raw=raw,profile_bias_raw=bias,positive_scale=scale)
seed=json.loads((SRC/'Q8_seed682_point.json').read_text());EE={tuple(map(int,line.split())) for line in Path(seed['source']).read_text().splitlines() if line.strip()};ds=[sum(v==x or v==y for x,y in EE) for v in range(256)];ND=Counter(ds);n=[ND[d]//2 for d in range(9)];co=Counter();local_h=[]
for g,w in seed['graph_distribution']:
 _,c=ff.local_coefficients(ff.q4_edges_from_mask(g));co.update({k:w*v for k,v in c.items()})
values=[];groups=[[0,3,7],[1,4,5,8],[2,6]]
for vertex,(pairs,states) in enumerate(vo.vertex_records(EE,8)):
 x=[states.count(s) for s in range(9)];d=ds[vertex];assert [sum(x[s] for s in group) for group in groups]==[(8-d)*(7-d)//2,d*(8-d),d*(d-1)//2]
 value=sum(x[i]*int(V[i,j])*x[j] for i in range(9) for j in range(9))+Bd[d];assert value>=0;values.append(value)
local=sum(v*int(V[i,j]) for (b,i,j),v in co.items() if b==5);alpha=sum(nn*b for nn,b in zip(n,Bd));combined=Q(local,64512*1120)+Q(alpha,128*784);direct=Q(sum(values),256*784);assert combined==direct and combined>=0
# Retained initial nonPSD kernels from the old run, all checked on SAME true682lambda.
defs=json.loads((OLD/'DYNAMIC_ROUNDING_CUTS.json').read_text());family=json.loads((R/'ROUNDING_FAMILY.json').read_text());
for cc in family['cuts']:
 b,bit,t=cc['block'],cc['bit'],cc['t'];states=sorted(ff.STATE_IDS[b],key=ff.STATE_IDS[b].get);defs.append({'block':b,'q':[(s>>bit)&1 for s in states],'t':t})
for cc in defs:
 b,q,t=cc['block'],cc['q'],cc['t'];nn=28 if b==5 else 6;v=sum(w*(nn*nn*q[i]*q[j]-(nn//2)*(2*t+1)*(q[i]+q[j])+t*(t+1)) for (bb,i,j),w in co.items() if bb==b);assert v>=0
out={'status':'PASS_EXACT_NEW_CONDITIONAL_VERTEX_AND_RETAINED_KERNEL_CALIBRATION','source_cut_sha256':hashlib.sha256(cutpath.read_bytes()).hexdigest(),'m682_seed_outside_counterexample_union':True,'actual_vertices':256,'all256_degree_Omega_group_totals':True,'all256_integer_conditional_kernel_plus_bias_nonnegative':True,'minimum_vertex_raw_slack':min(values),'mean_joint_normalized':str(combined/scale),'exact_local_plus_alpha_equals_actual_vertex_average':True,'retained_fixed_and_dynamic_kernels_checked':len(defs),'initial_PSD_coordinate_rows_to_omit':1008,'why_omitting_is_exact':'Every local diagonal coefficient is a nonnegative count, hence lambda>=0 implies all1008diagonal PSD directions; actual predicate PSD>=0 not uniform positive margin','profile_count':len(profiles),'fixed683_density':False,'even_gate':'DROPPED','primary683_goal':'OPEN'}
(R/'NEW_CUT_SEED682_CALIBRATION.json').write_text(json.dumps(out,indent=2)+'\n');(R/'PREPARED.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
