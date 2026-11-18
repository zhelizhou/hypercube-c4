"""Exact rational separating unary degree score for the frozen restricted pool."""
from pathlib import Path
import sys,json,math
from fractions import Fraction
from functools import reduce
P=Path(__file__).resolve().parent;SRC=P.parent/'finite8_flags';sys.path.insert(0,str(SRC/'deps'))
import numpy as np
from scipy.optimize import linprog
z=np.load(P/'COUPLED_COEFFICIENTS.npz');H=z['hist'];B=z['profile_hypergeom_numerators'];G=len(H);R=len(B)
# First hist-only feasibility, independent of PSD/margin constraints.
E=np.zeros((7,G+R));E[0,:G]=1;E[1,G:]=1;E[2:,:G]=H.T/16;E[2:,G:]=-B.T/8960;b=np.r_[1.,1.,np.zeros(5)]
r=linprog(np.zeros(G+R),A_eq=E,b_eq=b,bounds=(0,None),method='highs')
A=np.zeros((G+R,7));A[:G,:5]=H/16;A[:G,5]=-1;A[G:,:5]=-B/8960;A[G:,6]=1
obj=np.r_[np.zeros(5),1.,-1.];s=linprog(obj,A_ub=A,b_ub=np.zeros(G+R),bounds=[(-1,1)]*5+[(None,None)]*2,method='highs');assert s.success
q=[Fraction(float(v)).limit_denominator(100000) for v in s.x[:5]]
D=math.lcm(*(v.denominator for v in q));c=[int(v*D) for v in q];gg=math.gcd(*c);c=[v//gg for v in c]
local=[sum(int(n)*x for n,x in zip(h,c)) for h in H]
profile=[sum(int(n)*x for n,x in zip(row,c)) for row in B]
a=Fraction(max(local),16);bb=Fraction(min(profile),8960);assert bb>a
unary=[Fraction(sum(c[j]*math.comb(d,j)*math.comb(8-d,4-j) for j in range(5) if j<=d and 4-j<=8-d),70) for d in range(9)]
rows=json.loads((P/'PROFILE_SNAPSHOT.json').read_text())['remaining'];graphs=json.loads((P/'LP_STARTED.json').read_text())['graph_codes']
out={'status':'EXACT_RESTRICTED_MARGINAL_SEPARATION','hist_only_lp_status':int(r.status),'hist_only_lp_message':r.message,'float_separator':s.x.tolist(),'integer_histogram_score':c,'Q4_pool_score_bound':str(a),'profile_hypergeom_score_bound':str(bb),'strict_gap':str(bb-a),'local_integer_scores_minmax':[min(local),max(local)],'profile_integer_scores_minmax':[min(profile),max(profile)],'max_local_graphs':[g for g,x in zip(graphs,local) if x==max(local)],'min_profiles':[{'row':i,'degrees':rows[i]['degrees']} for i,x in enumerate(profile) if x==min(profile)],'global_degree_unary_score':[str(x) for x in unary],'all_local_le_bound':all(Fraction(x,16)<=a for x in local),'all_profile_ge_bound':all(Fraction(x,8960)>=bb for x in profile),'full_Q4_separation_done':False,'primary683_goal':'OPEN'}
(P/'MARGINAL_SEPARATOR.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
