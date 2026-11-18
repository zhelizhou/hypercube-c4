"""Small-integer rank-two PSD separator, exact rational certification."""
from pathlib import Path
from fractions import Fraction as F
import json,sys,itertools as it,math
P=Path(__file__).resolve().parent;R=P/'pool_fourth_frequency';SRC=P.parent/'finite8_flags';sys.path.insert(0,str(SRC/'deps'))
import numpy as np
from scipy.optimize import linprog
z=np.load(R/'COUPLED_COEFFICIENTS.npz');H=z['hist'];cs=[z['block0'],z['block1']];rays=json.loads((R/'EIGEN_RAYS.json').read_text());rs=[rays[140],rays[147]];assert [r['block'] for r in rs]==[0,1]
base=[np.array(r['q'],dtype=np.int64) for r in rs];t=[21*int(h[4])-7*int(h[2])-24*int(h[0]) for h in H];trials=[];win=None
for s0,s1 in it.product(range(1,11),repeat=2):
 qs=[];raw=[]
 for b,s,C in zip(base,[s0,s1],cs):
  q=np.rint(b*s/max(abs(b))).astype(np.int64);g=math.gcd(*map(abs,map(int,q)))
  if not g:break
  q=q//g;qs.append(q);val=np.einsum('i,gij,j->g',q,C,q);assert all(int(x)%2==0 for x in val);raw.append([int(x)//2 for x in val])
 if len(qs)!=2:continue
 A=np.array(raw,dtype=float).T;bb=-64512*np.array(t,dtype=float)
 lp=linprog([1,1],A_ub=A,b_ub=bb,bounds=(0,None),method='highs');trials.append({'scales':[s0,s1],'lp_feasible':bool(lp.success)})
 if not lp.success:continue
 cons=[(raw[0][i],raw[1][i],-64512*t[i]) for i in range(len(t))]+[(-1,0,0),(0,-1,0)]
 active=[c for c in cons if abs(c[0]*lp.x[0]+c[1]*lp.x[1]-c[2])<1e-6]
 for (a,b,c),(d,e,f) in it.combinations(active,2):
  det=a*e-b*d
  if not det:continue
  x,y=F(c*e-b*f,det),F(a*f-c*d,det)
  if x<0 or y<0:continue
  if all(a*x+b*y<=c for a,b,c in cons):win=(qs,raw,[x,y],[s0,s1]);break
 if win:break
assert win is not None,'No small exact rank-two separator found in this bounded simplification'
qs,raw,beta,scales=win;scores=[F(ti)+(beta[0]*raw[0][i]+beta[1]*raw[1][i])/64512 for i,ti in enumerate(t)];assert max(scores)<=0
weights=[sum(math.comb(d,j)*math.comb(8-d,4-j)*[-24,0,-7,0,21][j] for j in range(5) if j<=d and 4-j<=8-d) for d in range(9)]
excess=[weights[d]-(315*d-1680) for d in range(9)];assert min(excess)>=0 and 315*1366-1680*256==210
out={'status':'EXACT_RESTRICTED_FOURTH_SEPARATOR','columns':len(t),'unary_score':'t=21h4-7h2-24h0','unary_histogram_weights':[-24,0,-7,0,21],'rays':[{'block':r['block'],'q_nonzero':[[i,int(v)] for i,v in zip(r['support'],q) if v],'beta':str(be)} for r,q,be in zip(rs,qs,beta)],'small_scales':scales,'score':'t+beta0*q0^T M0q0+beta1*q1^T M1q1','score_minmax':[str(min(scores)),str(max(scores))],'degree_hypergeom_weights':weights,'tangent_slope':315,'tangent_intercept':-1680,'degree_pointwise_excess':excess,'global_mean_t_lower_bound':'3/16','uses_profile_cover_as_premise':False,'trials':trials,'full_domain_separation_done_here':False,'primary683_goal':'OPEN'}
(R/'EXACT_FOURTH_SEPARATOR.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
