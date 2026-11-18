"""Exact common-root/direction bridge regression on all1120 actual Q8 slices."""
from pathlib import Path
from collections import Counter
from math import comb
import json,sys,hashlib
P=Path(__file__).resolve().parent;SRC=P.parent/'finite8_flags';sys.path.insert(0,str(SRC));import finite_flags as ff
source=P.parents[3]/'data/q8_seed682.edges'
E={tuple(map(int,line.split())) for line in source.read_text().splitlines() if line.strip()};degs=Counter()
for v in range(256):degs[sum(v==x or v==y for x,y in E)]+=1
hist=Counter();stars=Counter();slices=0
for K in ff.restrictions(E,8):
 slices+=1;dd=[sum(v==x or v==y for x,y in K) for v in range(16)]
 hist.update(dd)
 for k in range(5):stars[k]+=sum(comb(d,k) for d in dd)
assert slices==1120 and len(E)==682
# sum_K h_j =sum_global N_d*C(d,j)*C(8-d,4-j) exactly.
for j in range(5):
 num=sum(n*comb(d,j)*comb(8-d,4-j) for d,n in degs.items() if j<=d and 4-j<=8-d)
 assert hist[j]==num
for k in range(5):assert stars[k]==comb(8-k,4-k)*sum(n*comb(d,k) for d,n in degs.items())
profiles=json.loads((P/'PROFILE_SNAPSHOT.json').read_text())['remaining'];weights=[-70,-35,-30,-35,-34,-15,30,105,210]
values=[]
for row in profiles:
 n=row['degrees'];assert len(n)==9 and sum(n)==128 and sum(d*n[d] for d in range(9))==683
 values.append(sum(n[d]*weights[d] for d in range(9)))
assert len(profiles)==792 and min(values)==15
out={'status':'PASS_EXACT_COMMON_SAMPLING_AND_PROFILE_SCORE','source':str(source),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'actual_edges':len(E),'actual_Q4_restrictions':slices,'global_degrees':dict(sorted(degs.items())),'local_degree_histogram_total':dict(sorted(hist.items())),'local_choose_degree_totals':dict(stars),'histogram_identity_verified_for_j':list(range(5)),'star_identity_verified_for_k':list(range(5)),'profile_snapshot_rows':len(profiles),'integer_degree_score':weights,'profile_score_min':min(values),'profile_score_max':max(values),'necessary_average_Q4_u_lower_bound':'3/112','u':'3h4-h0-h2','bridge_does_not_assume_independent_stars':True,'restricted_only':True}
(P/'BRIDGE_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
