"""Check the new certificate hashes, degree arithmetic, and saturation tables."""
from itertools import combinations
from math import comb
from pathlib import Path
import hashlib
import json

ROOT=Path(__file__).resolve().parent


def main():
    manifest=json.loads((ROOT/'results/low2_star158_certificate_manifest.json').read_text())
    assert manifest['low2_case_count']==17 and manifest['low2_verified_additions']==4122060
    for name,c in manifest['certificates'].items():
        assert c['valid'] and c['final_empty_clause']
        for extension,key in [('.cnf','cnf_sha256'),('.drat','proof_sha256')]:
            p=(ROOT/'results'/name).with_suffix(extension)
            assert hashlib.sha256(p.read_bytes()).hexdigest()==c[key]
        assert hashlib.sha256((ROOT/'check_rup_active.cpp').read_bytes()).hexdigest()==c['checker_sha256']
    B8=[comb(d,3)-10*d+40 for d in range(9)]
    A=[];B=[];C=[]
    for d in range(9):
        selected=set(range(d));local=[d-len(selected&set(drop)) for drop in combinations(range(8),2)]
        A.append(sum(k<=1 for k in local));B.append(sum(k==2 for k in local));C.append(sum(k==6 for k in local))
    weights=[20*B8[d]+C[d]-8*A[d]-4*B[d] for d in range(9)]
    assert weights==[576,376,236,136,56,0,1,107,348]
    old=json.loads((ROOT/'results/arithmetic_symmetry_audit.json').read_text())['Q8_688_allowed_parity_histograms']
    remaining=[];excluded=[]
    for row in old:
        if row['N3']:
            assert row['N3']==1 and row['N4']==row['N7']==0
            required=10*(10*688-5120+11);maximum=112*158+2*3
            assert required>maximum
            excluded.append({'profile':row,'reason':'single-global-degree-three star count','required':required,'maximum':maximum})
            continue
        penalty=sum(row[f'N{d}']*weights[d] for d in (3,4,5,6,7))
        if penalty>192:excluded.append({'profile':row,'reason':'weighted penalty exceeds192','penalty':penalty})
        else:remaining.append(row)
    assert {(r['N4'],r['N7']) for r in remaining}=={(0,0),(1,0),(2,0),(0,1)}
    rounded=[]
    for b in range(3):
        for f in range(2):
            feasible=[]
            for s in range(561):
                if s%2!=(b+f)%2:continue
                if b<=1 and 4*s>2212:continue
                if b==2 and 4*s>2218:continue
                if b==0 and 8*s+7*f>4424:continue
                feasible.append(s)
            maximum=max(feasible)
            assert maximum+f<=552+b
            rounded.append({'b3':b,'f7':f,'maximum_star_sum':maximum})
    tables={}
    for b in range(3):
        pairs=[]
        for c in range(9+4*b):
            numerator=916-b-2*c
            if numerator%3:continue
            M=numerator//3
            if M<=304:pairs.append([M,c])
        tables[str(b)]=pairs
    assert tables['0']==[[304,2],[302,5],[300,8]]
    assert tables['1']==[[303,3],[301,6],[299,9],[297,12]]
    assert tables['2']==[[304,1],[302,4],[300,7],[298,10],[296,13],[294,16]]
    selected0=15;K4_positions=[]
    for w in range(1,256):
        if w.bit_count()%2:continue
        for axes in combinations(range(8),4):
            selectedw=sum(1<<i for i in axes)
            common=selected0&selectedw&(~w&255);K=common.bit_count()
            for i in range(8):
                if common>>i&1:
                    local=((selected0&~(1<<i))&(selectedw&~(1<<i))&(~w&255)).bit_count()
                    assert local==K-1
            if K==4:
                assert selectedw==15 and w&15==0
                K4_positions.append(w)
    assert len(K4_positions)==7 and {w.bit_count() for w in K4_positions}=={2,4}
    out={'status':'all checks passed','upper_bound':688,'target_682_proved':False,
         'low2_cases':17,'low2_verified_additions':manifest['low2_verified_additions'],
         'three_full_root_verified_additions':manifest['certificates']['q6_roots3_star158']['verified_additions'],
         'weighted_degree_coefficients':weights,'excluded_profiles':excluded,
         'remaining_688_parity_profiles':remaining,'rounded_Q7_bounds':rounded,
         'saturation_pair_tables':tables,'K4_canonical_roots':[48,240]}
    (ROOT/'results/refinement_audit.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['status','upper_bound','target_682_proved','low2_cases','low2_verified_additions','three_full_root_verified_additions']}))


if __name__=='__main__':main()
