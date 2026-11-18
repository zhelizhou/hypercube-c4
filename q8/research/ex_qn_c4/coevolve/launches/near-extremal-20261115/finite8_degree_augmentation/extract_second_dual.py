"""Find and exactly verify a small integer PSD ray/unary restricted separator."""
from pathlib import Path
import sys,json,math
from fractions import Fraction
P=Path(__file__).resolve().parent;R=P/'pool_second_violation';SRC=P.parent/'finite8_flags';sys.path.insert(0,str(SRC/'deps'))
import numpy as np
z=np.load(R/'COUPLED_COEFFICIENTS.npz');H=z['hist'];C=z['block2'];rays=json.loads((R/'EIGEN_RAYS.json').read_text());ray=rays[152];assert ray['block']==2
fullq=np.array(ray['q'],dtype=np.int64);V=[3*int(h[0])+3*int(h[4])-int(h[2]) for h in H]
def interval(q):
 vv=np.einsum('i,gij,j->g',q,C,q);assert all(int(x)%2==0 for x in vv);raw=[int(x)//2 for x in vv]
 lo=Fraction(0);hi=None
 for v,a in zip(V,raw):
  if a<0:lo=max(lo,Fraction(v*64512,-a))
  elif a>0:
   bound=Fraction(-v*64512,a);hi=bound if hi is None else min(hi,bound)
  elif v>0:return None
 if hi is not None and lo>hi:return None
 return lo,hi,raw
trials=[];winner=None
for scale in range(1,201):
 q=np.rint(fullq*scale/max(abs(fullq))).astype(np.int64);g=math.gcd(*map(abs,map(int,q)))
 if not g:continue
 q=q//g;got=interval(q);trials.append({'scale':scale,'works':got is not None})
 if got:
  lo,hi,raw=got;beta=lo
  # Minimise denominator without leaving the exact feasible interval.
  if hi is not None:
   for den in range(1,1001):
    num=(lo.numerator*den+lo.denominator-1)//lo.denominator
    cand=Fraction(num,den)
    if cand<=hi:beta=cand;break
  scores=[Fraction(v)+beta*Fraction(a,64512) for v,a in zip(V,raw)];assert max(scores)<=0 and beta>=0
  winner={'scale':scale,'q':q.tolist(),'beta':str(beta),'interval_lower':str(lo),'interval_upper':str(hi),'score_min':str(min(scores)),'score_max':str(max(scores))};break
if winner is None:
 got=interval(fullq);assert got is not None;lo,hi,raw=got;beta=lo;q=fullq;winner={'scale':'full_quantized_ray','q':q.tolist(),'beta':str(beta),'interval_lower':str(lo),'interval_upper':str(hi)}
out={'status':'EXACT_RESTRICTED_SECOND_SEPARATOR','graph_columns':len(H),'q_block':2,'q_original_state_support':ray['support'],'q_nonzero':[[i,int(v)] for i,v in zip(ray['support'],q) if v],'unary_score':'v=3h0+3h4-h2','unary_hist_weights':[3,0,-1,0,3],**winner,'coefficient_denominator':64512,'global_mean_v_lower_bound':'3/112','analytic_lower_bound_uses_profile_cover':False,'local_score':'v+beta*q^T M2(K) q','all_current_columns_score_le0':True,'trials':trials,'full_domain_separation_done':False,'primary683_goal':'OPEN'}
(R/'EXACT_SECOND_SEPARATOR.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
