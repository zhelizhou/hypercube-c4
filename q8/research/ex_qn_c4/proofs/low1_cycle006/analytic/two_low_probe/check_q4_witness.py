#!/usr/bin/env python3
"""A real Q4 counterexample to the isolated-face relaxation, not a Q6 witness."""
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent


def edge(a, b):
    return tuple(sorted((a, b)))


def main():
    # These are already the final shared coordinates: u=0, v=3,
    # D={0,1}; both degree-one roots retain exactly direction2.
    neighborhoods = {
        0: [4], 3: [7], 5: [1,4,7,13], 6: [2,4,14],
        9: [1,8,11], 10: [2,8], 12: [8,13,14], 15: [7,11,14],
    }
    es = {edge(v,w) for v, ns in neighborhoods.items() for w in ns}
    assert len(es) == 20
    assert all((v^w).bit_count() == 1 for v,w in es)
    degrees = [sum(v in e for e in es) for v in range(16)]
    assert degrees[0] == degrees[3] == 1
    assert (0,4) in es and (3,7) in es
    assert all(degrees[v] >= 2 for v in neighborhoods if v not in (0,3))
    square_counts = []
    for i,j in combinations(range(4),2):
        mask=(1<<i)|(1<<j)
        for x in range(16):
            if x & mask:
                continue
            q={edge(x,x^(1<<i)),edge(x,x^(1<<j)),
               edge(x^(1<<i),x^mask),edge(x^(1<<j),x^mask)}
            square_counts.append(len(q & es))
    assert len(square_counts) == 24 and max(square_counts) <= 3
    faces=[]
    for fixed in range(4):
        free=[i for i in range(4) if i != fixed]
        for bit in (0,1):
            vertices=[v for v in range(16) if ((v>>fixed)&1)==bit]
            stars=[v for v in vertices if v.bit_count()%2==0 and
                   all(edge(v,v^(1<<i)) in es for i in free)]
            assert len(stars)==1
            faces.append({'fixed_direction':fixed,'fixed_bit':bit,'star_root':stars[0]})
    out={'status':'VERIFIED Q4 WITNESS; NOT a Q6 completion',
         'n':4,'edges':[list(e) for e in sorted(es)],'edge_count':len(es),
         'P_even_degrees':{str(v):degrees[v] for v in neighborhoods},
         'low_roots':[0,3],'common_retained_direction':2,
         'square_count':24,'max_edges_per_square':max(square_counts),
         'all_Q3_faces':faces,'specified_star_sum':8,
         'missing_global_obligation':'There is no assignment of the two additional directions or common Q6 edge completion in this artifact.',
         'checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE/'Q4_WITNESS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':
    main()
