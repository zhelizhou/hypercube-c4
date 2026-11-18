"""Small, solver-free coverage check for the forced paired-facet patterns."""
from collections import Counter
from itertools import combinations, product
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent


def main():
    # At Q7 M300, P degrees4..6 with eight degree6 roots has S_P=552.
    # Its14 Q6 star sums total2208; their full counts total8.
    caps = [158,156,157,152,144]
    assert 6*300-1280+4*8 == 552
    assert 14*158-4*552 == 4
    excess = [2*(158-cap)-c for c,cap in enumerate(caps)]
    assert excess == [0,3,0,9,24]
    # Thus sum excess can vanish only for c=0 or2, and four facets have c=2.
    box_types = Counter()
    for chosen in combinations(list(product(range(7),range(2))),4):
        counts = Counter(axis for axis,side in chosen)
        box_types[sum(n == 2 for n in counts.values())] += 1
    assert box_types == {0:560,1:420,2:21}
    vertices = [v for v in range(32) if v.bit_count()%2 == 0]
    pairs = [(u,v) for u,v in combinations(vertices,2) if (u^v).bit_count() == 4]
    assert len(pairs) == 40
    assert not any(all((u^v).bit_count()>=4 for u,v in combinations(triple,2))
                   for triple in combinations(vertices,3))
    matrix = []
    for a,b,c,d in product(range(3),repeat=4):
        if a+b == c+d == a+c == b+d == 2:
            matrix.append([[a,b],[c,d]])
    assert matrix == [[[0,2],[2,0]],[[1,1],[1,1]],[[2,0],[0,2]]]
    statuses = {}
    for i in range(3):
        name = f'q7_300_eight_boxes{i}_oppmin3_lowlimit2_rigid'
        r = json.loads((ROOT/'results'/(name+'.json')).read_text())
        assert r['opposite_minimum'] == 3 and r['opposite_low_limit'] == 2
        assert r['opposite_seven_limit'] == 1 and r['new_checked_local_cuts']
        assert r['status'] == 'UNKNOWN' and not r['checked_unsat_certificate']
        statuses[str(i)] = r['status']
    result = {'status':'PASS','facet_subset_coverage':dict(box_types),
              'total_four_facet_subsets':sum(box_types.values()),
              'local_star_excess_by_full_count':excess,
              'Q5_full_five_pairs':len(pairs),'Q5_full_five_triples':0,
              'two_doubled_axes_missing_direction_matrices':matrix,
              'stronger_probe_statuses':statuses,
              'these_probes_exclude_no_family':True}
    (ROOT/'results/box_pattern_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
