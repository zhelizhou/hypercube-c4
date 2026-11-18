"""New scope snapshot for native warm-start L1 master plus genuine new gates.
Global leaf row is on average alpha, never an invalid same-parity deletion.
"""
from pathlib import Path
from collections import Counter
from fractions import Fraction as Q
import sys,json,shutil,hashlib
P=Path(__file__).resolve().parent;O=P/'pool_native_leaf_connector';OLD=P/'pool_maximal_vertex_feasibility';SRC=P.parent/'finite8_flags';LEAF=P.parent/'finite8_maximal_leaf_gate';CON=P.parent/'finite8_connector_frequency';sys.path.insert(0,str(SRC/'deps'));sys.path.insert(0,str(SRC));sys.path.insert(0,str(P.parent/'finite8_edge_flags'))
import numpy as np
from scipy import sparse
import finite_flags as ff,edge_flags,verify_obstruction as vo
O.mkdir(exist_ok=True);assert not (O/'PREPARED.json').exists()
for n in ['PROFILE_SNAPSHOT.json','POOL_GRAPH_CODES.json','INTEGER_FEATURES.npz','MARGINAL_FEATURES.npz','ROUNDING_FEATURES.npz','ROUNDING_FAMILY.json','block1.EXACT_SEPARATOR.json','block4.EXACT_SEPARATOR.json','EDGE_U_NUMERATOR.npz','EDGE_GENERATOR_DEDUP_NUMERATOR.npz','EDGE_ENDPOINT_DEDUP.npz','EDGE_DEGREE_PROFILE_RHS_NUMERATOR.npz','GENERATOR_DEDUPLICATION.json','GENERATOR_HISTOGRAMS.json','CONDITIONAL_VERTEX_CUT.json','CONDITIONAL_VERTEX_FEATURES.npz','NEW_CUT_SEED682_CALIBRATION.json','SEED682_JOINT_CALIBRATION.json']:shutil.copyfile(OLD/n,O/n)
for n in ['PROOF.md','CHECK.json','GENERATORS.json','DEDUP_CLASSES.json','ALPHA_GLOBAL_ROW.json']:shutil.copyfile(LEAF/n,O/('LEAF_'+n))
for n in ['CONNECTOR_CUTS.json','VERIFICATION.json']:shutil.copyfile(CON/n,O/n)
profiles=json.loads((O/'PROFILE_SNAPSHOT.json').read_text())['remaining'];rows=json.loads((O/'LEAF_ALPHA_GLOBAL_ROW.json').read_text())['by_m'];counter={str(m):0 for m in range(683,689)}
for row in profiles:
 m=str(row['m']);z=rows[m][counter[m]];counter[m]+=1;assert z['n']==row['degrees'] and z['coefficient']==row['degrees'][1]-row['degrees'][8]
hist=json.loads((O/'GENERATOR_HISTOGRAMS.json').read_text());dedup=json.loads((O/'GENERATOR_DEDUPLICATION.json').read_text());sel=dedup['selected_original_indices'];author={tuple(x['counts']):x['allowed'] for x in json.loads((O/'LEAF_GENERATORS.json').read_text())['all']}
def allowed(h):
 if h['root_retained']==0:return True
 x=h['counts'];a=sum((s&1)*n for s,n in enumerate(x));b=sum(((s>>1)&1)*n for s,n in enumerate(x));v=(a!=0 or x[6]==7) and (b!=0 or x[5]==7);assert author[tuple(x)]==v;return v
fullok=[allowed(h) for h in hist];assert sum(not x for x in fullok)==230
keep=[]
for k,group in enumerate(dedup['groups']):
 assert len({fullok[i] for i in group})==1
 if fullok[group[0]]:keep.append(k)
G=sparse.load_npz(O/'EDGE_GENERATOR_DEDUP_NUMERATOR.npz')[:,keep];EP=sparse.load_npz(O/'EDGE_ENDPOINT_DEDUP.npz')[:,keep];sparse.save_npz(O/'EDGE_GENERATOR_DEDUP_NUMERATOR.npz',G);sparse.save_npz(O/'EDGE_ENDPOINT_DEDUP.npz',EP);newsel=[sel[k] for k in keep];dedup['selected_original_indices']=newsel;dedup['groups']=[dedup['groups'][k] for k in keep];dedup['source_preleaf_dedup_columns']=len(sel);dedup['dedup_columns']=len(keep);dedup['full_leaf_filtered_columns']=sum(fullok);(O/'GENERATOR_DEDUPLICATION.json').write_text(json.dumps(dedup,indent=2)+'\n')
Ncap=np.zeros((9,len(keep)),dtype=np.int32)
for k,i in enumerate(newsel):
 h=hist[i]
 if h['root_retained']==0:continue
 x=h['counts'];a=1+sum((s&1)*n for s,n in enumerate(x));b=1+sum(((s>>1)&1)*n for s,n in enumerate(x));Ncap[a,k]+=b;Ncap[b,k]+=a
capalpha=np.array([[(8*t-t*(t-1)//2)*p['degrees'][t] for p in profiles] for t in range(9)],dtype=np.int32);leafalpha=np.array([p['degrees'][8]-p['degrees'][1] for p in profiles],dtype=np.int32);np.savez_compressed(O/'LEAF_NEIGHBOR_FEATURES.npz',leaf_alpha_lower=leafalpha,neighbor_beta_upper=Ncap,neighbor_alpha_upper_numerator=capalpha)
F=sparse.load_npz(O/'INTEGER_FEATURES.npz');info=json.loads((P/'pool_inventory/LP_STARTED.json').read_text());starts=info['packed_starts'];cuts=json.loads((O/'CONNECTOR_CUTS.json').read_text())['cuts'];features=[];scales=[]
for cut in cuts:
 b=cut['block'];states=sorted(ff.STATE_IDS[b],key=ff.STATE_IDS[b].get);mapping=cut['full_state_connector_codes'];assert mapping==[s&15 for s in states];Qconn=np.array(cut['integer_connector_Q'],dtype=np.int64);i,j=np.triu_indices(ff.DIMS[b]);coords=np.zeros(F.shape[1],dtype=np.int64);coords[starts[b]:starts[b+1]]=Qconn[np.array(mapping)[i],np.array(mapping)[j]];features.append(F@coords);scales.append(cut['positive_normalization'])
np.savez_compressed(O/'CONNECTOR_FEATURES.npz',raw=np.array(features,dtype=np.int64).T,scales=np.array(scales,dtype=np.int64))
# New input calibration on true682 and a positive maximal leaf-containing576 graph.
seed=json.loads((SRC/'Q8_seed682_point.json').read_text());EE={tuple(map(int,line.split())) for line in Path(seed['source']).read_text().splitlines() if line.strip()};co=Counter()
for g,w in seed['graph_distribution']:
 _,c=ff.local_coefficients(ff.q4_edges_from_mask(g));co.update({k:w*v for k,v in c.items()})
cm=[]
for cut in cuts:
 b=cut['block'];M=cut['full_state_connector_codes'];QQ=cut['integer_connector_Q'];raw=sum(v*QQ[M[i]][M[j]] for (bb,i,j),v in co.items() if bb==b);direct=0;count=0
 for bb,mapped in vo.face_records(EE,8):
  if bb!=b:continue
  for states in mapped:
   xx=[sum(M[s]==a for s in states) for a in range(16)];val=sum(xx[i]*QQ[i][j]*xx[j] for i in range(16) for j in range(16));assert val>=0;direct+=(1120//len(mapped))*val;count+=1
 assert raw==direct and raw>=0;cm.append({'block':b,'raw_pairing':int(raw),'normalized':str(Q(raw,64512*1120*cut['positive_normalization'])),'actual_root_maps':count})
calibrations=[]
for label,E in [('seed682',EE),('positive_leaf576',{tuple(map(int,line.split())) for line in (LEAF/'CALIBRATION.edges').read_text().splitlines() if line.strip()})]:
 deg=[sum(x==v or y==v for x,y in E) for v in range(256)];nd=Counter(deg);assert nd[1]<=nd[8];beta_hist=Counter()
 for (u,v),(r,states) in zip(edge_flags.ambient(8),edge_flags.root_records(E,8)):
  x=[states.count(s) for s in range(8 if r==0 else 7)];h={'root_retained':r,'counts':x};assert r==1 or x[7]>=1;assert allowed(h);beta_hist[r,tuple(x)]+=1
 for t in range(9):
  lhs=sum(sum(deg[u] for u in range(256) if (min(v,u),max(v,u)) in E) for v in range(256) if deg[v]==t);assert lhs <= (8*t-t*(t-1)//2)*nd[t]
 calibrations.append({'label':label,'edges':len(E),'N1':nd[1],'N8':nd[8],'all_retained_hist_filters':True,'maximal_missing_hist_filters':True,'all9retained_neighbor_capacities':True})
out={'status':'EXACT_NEW_GATE_INPUTS_CALIBRATED','alpha_columns':len(profiles),'no_individual_alpha_profile_deleted':True,'source_beta_dedup':len(sel),'kept_beta_dedup':len(keep),'retained_raw_deleted':230,'retained_raw_kept':1486,'root0_raw_kept':1716,'global_leaf_row':'sumα(n8−n1)>=0','neighbor_rows':9,'connector_cuts':cm,'literal_calibrations':calibrations,'original_scope_files_preserved':True,'no_graph_or682claim':True}
(O/'PREPARED.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
