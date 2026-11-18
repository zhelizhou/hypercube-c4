"""Exact integer certificate of restricted1176 rejection and next score.
No floating LP/eigenvalues are imported as a proof premise.
"""
from pathlib import Path
import sys,json,hashlib
from fractions import Fraction
P=Path(__file__).resolve().parent;R=P/'pool_with_violation';SRC=P.parent/'finite8_flags';sys.path.insert(0,str(SRC/'deps'));sys.path.insert(0,str(SRC))
import numpy as np
import finite_flags as ff
z=np.load(R/'COUPLED_COEFFICIENTS.npz');H=z['hist'];C=z['block0'];codes=json.loads((R/'POOL_GRAPH_CODES.json').read_text());old=set(json.loads((P/'pool1160/POOL_GRAPH_CODES.json').read_text()));new=set(json.loads((R/'ORBIT_METADATA.json').read_text())['orbit_graphs']);supports=json.loads((R/'LP_STARTED.json').read_text())['supports'][0]
assert supports==[115,181,218,236]
q=np.array([1,0,0,-1],dtype=np.int64);twice=np.einsum('i,gij,j->g',q,C,q);assert all(int(v)%2==0 for v in twice);raw=[int(v)//2 for v in twice];u=[3*int(h[4])-int(h[0])-int(h[2]) for h in H]
assert set(codes)==old|new and not old&new and len(old)==1160 and len(new)==16
for g,v,uu in zip(codes,raw,u):
 if g in old:assert v==0 and uu<=0
 else:assert v==-5376 and uu==12
scores=[64512*uu+144*v for uu,v in zip(u,raw)];assert max(scores)==0
profiles=json.loads((P/'PROFILE_SNAPSHOT.json').read_text())['remaining'];w=[-70,-35,-30,-35,-34,-15,30,105,210];profile_scores=[sum(n*a for n,a in zip(row['degrees'],w)) for row in profiles];assert min(profile_scores)==15
# Reconstruct all1176 block0 q scores once from literal local graphs, rather
# than trusting just the saved numpy tensors.
for g,v in zip(codes,raw):
 rho,c=ff.local_coefficients(ff.q4_edges_from_mask(g));assert c[0,115,115]+c[0,236,236]-c[0,115,236]==v
out={'status':'EXACT_RESTRICTED1176_PSD_ORBIT_REJECTION','scope':'1160 old Q4s plus16 Aut-images of actual degree-score violator; not fullNO','old_graph_count':1160,'new_orbit_count':16,'profiles':792,'q_block':0,'q_nonzero_full_state_coordinates':[[115,1],[236,-1]],'coefficient_denominator':64512,'raw_q_score_old_exact':0,'raw_q_score_orbit_exact':-5376,'normalized_q_moment_old_exact':'0','normalized_q_moment_orbit_exact':str(Fraction(-5376,64512)),'u_old_bound':0,'u_orbit_exact':12,'profile_u_expectation_lower_bound':'3/112','orbit_mass_required_by_marginals':'1/448','orbit_mass_required_by_PSD':'0','next_local_score':'u(K)+144*q^T M0(K) q','next_integer_score':'64512*(3h4-h0-h2)+144*(c[0,115,115]+c[0,236,236]-c[0,115,236])','all1176_next_integer_score_le0':all(v<=0 for v in scores),'next_score_integer_minmax':[min(scores),max(scores)],'next_global_expectation_lower_bound':'3/112','even_square_gate_needed_for_this_restricted_contradiction':False,'full_Q4_next_score_separation_done':False,'primary683_goal':'OPEN','is_Q8_counterexample':False}
(R/'EXACT_ORBIT_REJECTION.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
