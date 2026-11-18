"""Independent actual-star and complete four-full-code check; no solver or producer imports."""
from itertools import combinations, permutations
from collections import Counter
from pathlib import Path
from hashlib import sha256
from math import comb
import json

HERE=Path(__file__).resolve().parent
canonical=(0,15,51,60)
even=[v for v in range(64) if v.bit_count()%2==0]
neighbors=lambda v,A:{v^(1<<j) for j in range(6) if A>>j&1}
codes={tuple(F) for F in combinations(even,4)
       if all((a^b).bit_count()>=4 for a,b in combinations(F,2))}
orbit=set()
for order in permutations(range(6)):
    perm=lambda x:sum(((x>>j)&1)<<i for i,j in enumerate(order))
    mapped=[perm(x) for x in canonical]
    for v in even:orbit.add(tuple(sorted(x^v for x in mapped)))
assert codes==orbit
full_neighbors={v:neighbors(v,63) for v in canonical}
assert all(len(a&b)<=1 for a,b in combinations(full_neighbors.values(),2))
rows=[];allowed={};forced={}
for v in even:
    if v in canonical:continue
    options=[A for A in range(64) if all(len(neighbors(v,A)&full_neighbors[f])<=1 for f in canonical)]
    allowed[v]=options
    maximum=max(A.bit_count() for A in options)
    assert maximum in (3,4)
    fours=[A for A in options if A.bit_count()==4]
    if fours:
        pair=63
        for A in fours:pair&=A
        assert len(fours)==4 and pair.bit_count()==2
        forced[v]=pair
    rows.append({'vertex':v,'degree_histogram':dict(sorted(Counter(A.bit_count() for A in options).items())),
                 'maximum_degree':maximum,'degree4_masks':fours,'forced_pair':forced.get(v)})
special=[r['vertex'] for r in rows if r['maximum_degree']==3]
assert special==[3,12,48,63] and len(forced)==24
pairs=[];covered=set()
for v,A in sorted(forced.items()):
    w=v^A
    assert w in forced and forced[w]==A and w!=v
    if v>w:continue
    checked=0
    for B in allowed[v]:
        if B.bit_count()!=4:continue
        for C in allowed[w]:
            if C.bit_count()!=4:continue
            assert len(neighbors(v,B)&neighbors(w,C))==2
            checked+=1
    assert checked==16
    assert v not in covered and w not in covered
    covered.update((v,w));pairs.append({'roots':[v,w],'forced_directions_mask':A,'actual_square_pairs_checked':checked})
assert covered==set(forced) and len(pairs)==12
# The scalar identity uses only the proven pointwise degree caps.
assert all(comb(d,3)==int(d>=3)+3*int(d==4) for d in range(5))
calibration=[]
source=Path('q6_sources/q8_upper_independent/results')
for p in sorted(source.glob('*.json')):
    raw=json.loads(p.read_text());E=raw.get('edges') if isinstance(raw,dict) else None
    if not E or not isinstance(E,list) or not all(isinstance(e,list) and len(e)==2 and all(isinstance(x,int) for x in e) for e in E):continue
    if max(map(max,E))>=64:continue
    adj=[set() for _ in range(64)]
    for a,b in E:
        assert 0<=a<64 and 0<=b<64 and (a^b).bit_count()==1
        adj[a].add(b);adj[b].add(a)
    assert len({tuple(sorted(e)) for e in E})==len(E)
    assert all(len(adj[a]&adj[b])<=1 for a,b in combinations(range(64),2))
    for parity in (0,1):
        degrees=[len(adj[v]) for v in range(64) if v.bit_count()%2==parity]
        if degrees.count(6)!=4:continue
        L=sum(d<3 for d in degrees);S=sum(comb(d,3) for d in degrees)
        assert S<=144-L
        calibration.append({'source':str(p),'sha256':sha256(p.read_bytes()).hexdigest(),
                            'parity':parity,'L':L,'S':S,'bound':144-L})
assert any(r['L']==0 and r['S']==144 for r in calibration)
result={'status':'PASS_ALL_FULL_CODES_AND_ACTUAL_STAR_PAIR_CAPACITY',
        'all_even_four_full_codes':len(codes),'generated_code_orbit':len(orbit),
        'odd_parity_transport':'translation by any odd vertex gives the same checked even domain',
        'canonical_full_roots':canonical,'local_root_options':rows,'special_degree_at_most3':special,
        'degree4_possible_roots':24,'actual_forced_pairs':pairs,'paired_roots':len(covered),
        'degree4_count_upper':12,'star_identity':'S=80+(28-L)+3*N4',
        'conclusion':'S<=144-L with no minimum-degree assumption on either parity',
        'actual_source_calibration':calibration,
        'scope':'Complete small local-code proof check, not enumeration of all Q6 graphs. Analytic source and independent review required.',
        'script_sha256':sha256(Path(__file__).read_bytes()).hexdigest()}
(HERE/'PAIR_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['local_root_options','actual_forced_pairs','actual_source_calibration']},indent=2))
