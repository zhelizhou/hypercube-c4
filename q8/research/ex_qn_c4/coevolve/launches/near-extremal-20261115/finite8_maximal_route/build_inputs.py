"""Exact necessary profile covers and maximal edge histograms; no optimizer."""
from itertools import combinations_with_replacement
from math import comb
from pathlib import Path
import json, hashlib
HERE=Path(__file__).resolve().parent
C=(735,534,333,177,66,0,0,105,345)
B=tuple(comb(d,3)-10*d+40 for d in range(9))
L=(28,28,28,18,6,0,0,0,0)
D=(0,1,2,3,4,7,8)
def profiles(m,maximal):
    rows=[]; cap=138432-201*m; bcap=6912-10*m
    def visit(i,left,vals):
        if i<len(D):
            d=D[i]
            for x in range(0 if not(maximal and d==0) else 0, (0 if maximal and d==0 else left//C[d])+1):
                visit(i+1,left-x*C[d],vals+[x])
            return
        n=[0]*9
        for d,x in zip(D,vals):n[d]=x
        n[6]=m-sum(d*n[d] for d in D)-5*(128-sum(vals))
        n[5]=128-sum(vals)-n[6]
        b=sum(B[d]*n[d] for d in range(9))
        if min(n[5:7])<0 or b>bcap:return
        assert sum(n)==128 and sum(d*n[d] for d in range(9))==m
        rows.append(dict(n=n,C=cap-left,b=b))
    visit(0,cap,[])
    return rows

def histograms(states,force7=False):
    rows=[]
    for seq in combinations_with_replacement(range(states),7):
        if force7 and 7 not in seq:continue
        rows.append([seq.count(s) for s in range(states)])
    return rows

def main():
    # Check the coefficient identity independently for all nine degrees.
    for d in range(9):
        a=40*comb(d,3)+2*comb(d,6)-5*L[d]
        assert a-402*d+1610==2*C[d]
    cover={str(m):dict(C_max=138432-201*m,b_max=6912-10*m,
                         all_profiles=profiles(m,False),maximal_profiles=profiles(m,True)) for m in range(683,689)}
    old=json.loads((HERE.parent/'q8_equality_profiles/PROFILES.json').read_text())
    assert {tuple(r['n']) for r in cover['683']['all_profiles']}=={tuple(r['degrees']) for r in old['profiles']}
    (HERE/'PROFILE_COVER.json').write_text(json.dumps(cover,indent=2)+'\n')
    hist={'root0_maximal':histograms(8,True),'root1':histograms(7)}
    assert len(hist['root0_maximal'])==comb(13,7)==1716
    assert len(hist['root1'])==comb(13,7)==1716
    assert comb(14,7)==3432
    (HERE/'EDGE7_GENERATORS.json').write_text(json.dumps(hist,indent=2)+'\n')
    source=HERE.parents[3]/'data/q8_seed682.edges'
    # Resolve to the common research root without relying on cwd.
    source=next(p/'data/q8_seed682.edges' for p in HERE.parents if (p/'data/q8_seed682.edges').exists())
    edges={tuple(sorted(map(int,line.split()))) for line in source.read_text().splitlines() if line.strip()}
    ambient={(v,v^(1<<i)) for v in range(256) for i in range(8) if not(v>>i&1)}
    assert edges<=ambient
    counts=[]; retained_full=0; squares=0
    for u,v in ambient:
        axis=(u^v).bit_length()-1
        closed=sum(all(tuple(sorted(e)) in edges for e in ((u,u^(1<<j)),(v,v^(1<<j)),(u^(1<<j),v^(1<<j)))) for j in range(8) if j!=axis)
        if (u,v) not in edges:counts.append(closed)
        else:retained_full+=closed
    assert retained_full==0
    receipt={'scope':'Necessary relaxation rows and complete seven-flag multiset generators, not graph enumeration or an upper bound 682',
      'profile_counts':{m:{k:len(v[k]) for k in ('all_profiles','maximal_profiles')} for m,v in cover.items()},
      'generator_counts':{k:len(v) for k,v in hist.items()},
      'seed':{'path':str(source),'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'edges':len(edges),'C4_free':True,'missing_edges':len(counts),'all_missing_edges_closed':all(counts),'closing_square_histogram':{str(k):counts.count(k) for k in sorted(set(counts))}},
      'historical_683_cover_exact_match':True}
    (HERE/'CHECK.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
