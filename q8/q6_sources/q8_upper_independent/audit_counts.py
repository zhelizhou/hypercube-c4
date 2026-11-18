"""Independent finite arithmetic and symmetry audit for the interim 688 proof."""
from itertools import combinations, permutations
from math import comb
from pathlib import Path
import hashlib
import json

ROOT=Path(__file__).resolve().parent


def permute(mask,p):
    return sum(1<<p[i] for i in range(6) if mask>>i&1)


def main():
    even=[v for v in range(64) if v.bit_count()%2==0]
    possible=[v for v in even if v.bit_count()>=4]
    assert len(possible)==16
    codes4=[]
    for triple in combinations(possible,3):
        if all((u^v).bit_count()>=4 for u,v in combinations((0,)+triple,2)):
            codes4.append(frozenset((0,)+triple))
    for four in combinations(possible,4):
        assert not all((u^v).bit_count()>=4 for u,v in combinations((0,)+four,2))
    group=list(permutations(range(6)))
    canonical_code=(0,15,51,60)
    orbit={frozenset(permute(v,p) for v in canonical_code) for p in group}
    assert set(codes4)==orbit and len(orbit)==15
    all_faces={(mask,base) for mask in range(64) if mask.bit_count()==3 for base in range(64) if not base&mask}
    nonroot={face for face in all_faces if face[1]!=0}
    hole_orbits=[{(permute(7,p),permute(base,p)) for p in group} for base in (8,24,56)]
    assert list(map(len,hole_orbits))==[60,60,20]
    assert set.union(*hole_orbits)==nonroot
    assert sum(map(len,hole_orbits))==len(nonroot)==140
    penalties=[comb(d,3)-10*d+40 for d in range(9)]
    losses=[]
    for d in range(9):
        selected=set(range(d))
        losses.append(sum(d-len(selected&set(drop))<=2 for drop in combinations(range(8),2)))
    weights=[10*b-2*l for b,l in zip(penalties,losses)]
    assert losses==[28,28,28,18,6,0,0,0,0]
    assert weights==[344,244,144,74,28,0,0,50,160]
    assert min(weights)==0
    upper=(128*40*10+comb(8,6)*4*158)//100
    assert upper==688
    profiles=[]
    for n3 in range(2):
        for n4 in range(4):
            for n7 in range(2):
                cost=74*n3+28*n4+50*n7
                if cost>96:continue
                n6=48+2*n3+n4-2*n7
                n5=80-3*n3-2*n4+n7
                assert n3+n4+n5+n6+n7==128
                assert 3*n3+4*n4+5*n5+6*n6+7*n7==688
                profiles.append({'N3':n3,'N4':n4,'N5':n5,'N6':n6,'N7':n7,'penalty':cost})
    assert len(profiles)==7
    manifest=json.loads((ROOT/'results/q6_star158_certificate_manifest.json').read_text())
    assert len(manifest['certificates'])==6 and manifest['total_verified_additions']==256403
    for name,checked in manifest['certificates'].items():
        assert checked['valid'] and checked['final_empty_clause']
        assert hashlib.sha256((ROOT/'results'/f'{name}.cnf').read_bytes()).hexdigest()==checked['cnf_sha256']
        assert hashlib.sha256((ROOT/'results'/f'{name}.drat').read_bytes()).hexdigest()==checked['proof_sha256']
    result={'status':'all arithmetic, symmetry-cover, and certificate-hash checks passed',
            'intermediate_upper_bound':upper,'target_682_proved':False,
            'parity_degree_penalty_weights':weights,'Q6_code_rooted_orbit_size':len(orbit),
            'one_hole_orbit_sizes':list(map(len,hole_orbits)),
            'Q8_688_allowed_parity_histograms':profiles}
    (ROOT/'results/arithmetic_symmetry_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
