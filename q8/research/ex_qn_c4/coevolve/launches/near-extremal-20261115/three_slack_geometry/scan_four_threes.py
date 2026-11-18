"""Complete necessary direction scan for one2/four3 C1146 row."""
import itertools as it,json,collections
from pathlib import Path
P=Path(__file__).resolve().parent
pairs=list(it.combinations(range(8),2))
As=[v for v in range(256) if v.bit_count()==3]
k=lambda v:sum(1<<j for j,(a,b) in enumerate(pairs) if v>>a&1 and v>>b&1)
ks=[k(255^a) for a in As];hist=collections.Counter();survivors=[];count=0
for inds in it.combinations_with_replacement(range(56),4):
 x=((1<<28)-1)^ks[inds[0]]^ks[inds[1]]^ks[inds[2]]^ks[inds[3]]
 w=x.bit_count();hist[w]+=1;count+=1
 if w<=2:survivors.append({'masks':[As[i] for i in inds],'odd_pairs':[pairs[j] for j in range(28) if x>>j&1]})
assert count==455126
out={'domain':'all multisets of four retained3masks on8 coordinates; repeated masks allowed','count':count,'xor_weight_histogram':dict(sorted(hist.items())),'survivors':survivors}
(P/'FOUR_THREE_DIRECTIONS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'count':count,'histogram':dict(sorted(hist.items())),'survivors':len(survivors)}))
