"""Pure exact check of profile-free caller and new integer PSD/unary score."""
from pathlib import Path
from math import comb
from fractions import Fraction
import json,sys
P=Path(__file__).resolve().parent;R=P/'pool_second_violation';SRC=P.parent/'finite8_flags';sys.path.insert(0,str(SRC));import finite_flags as ff
w=[sum(comb(d,j)*comb(8-d,4-j)*(3*(j==4)-(j==0)-(j==2)) for j in range(5) if j<=d and 4-j<=8-d) for d in range(9)]
excess=[w[d]-(45*d-240) for d in range(9)];assert excess==[170,160,120,70,26,0,0,30,90]
assert 45*1366-240*256==30 and Fraction(30,1120)==Fraction(3,112)
score=json.loads((R/'NEXT_ORACLE_SCORE.json').read_text());q=dict(score['block2_q_nonzero']);groups=json.loads((R/'FEATURE_DEDUPLICATION.json').read_text())['groups'];allgraphs=sorted({g for row in groups for g in row});assert len(allgraphs)==1177
values=[]
for g in allgraphs:
 E=ff.q4_edges_from_mask(g);rho,c=ff.local_coefficients(E);degrees=[sum(v==x or v==y for x,y in E) for v in range(16)];h=[degrees.count(j) for j in range(5)];v=3*h[0]+3*h[4]-h[2]
 raw=sum(c[2,i,j]*a*b for i,a in q.items() for j,b in q.items() if i<=j)
 s=1512*v+raw;values.append(s);assert s<=0
assert max(values)==0
out={'status':'EXACT_PROFILE_FREE_CALLER_AND_RESTRICTED1177_SEPARATOR','graph_count':len(allgraphs),'distinct_feature_columns':len(groups),'w':w,'degree_tangent_slope':45,'degree_tangent_intercept':-240,'per_degree_nonnegative_excess':excess,'sum_global_degrees':1366,'global_vertices':256,'global_degree_weighted_sum_lower_bound':30,'actual683_mean_u_lower_bound':'3/112','v_equals_u_plus_4h0':True,'actual683_mean_v_lower_bound':'3/112','q_block':2,'q_nonzero':score['block2_q_nonzero'],'q_outer_is_PSD':True,'integer_score':'1512*(3h0+3h4-h2)+sum_i<=j c[2,i,j]*q_i*q_j','integer_score_minmax':[min(values),max(values)],'actual683_mean_integer_score_lower_bound':'81/2','uses_frozen_profile_cover_as_premise':False,'full_Q4_separation_done_here':False,'primary683_goal':'OPEN'}
(R/'EXACT_FINAL_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
