#!/usr/bin/env python3
"""Independent finite coverage checks of the analytic L1 argument only."""
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
from math import comb
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent
EXPECTED = '39e1f9a86971aed331185ce01711a2f507cc4dd95290e123b1bb9fc20569995d'


def marked_q4():
    # Independent domain: all 2^16 masks of the upper edges, then reject
    # multiple downward parents of a triple. The author's code directly
    # generates the 4^4 parent choices instead.
    es = [(a, b) for a in range(16) for b in range(a + 1, 16) if (a ^ b).bit_count() == 1]
    ix = {e: k for k, e in enumerate(es)}
    fixed = sum(1 << k for k, (a, b) in enumerate(es) if a.bit_count() == 1 and b.bit_count() == 2)
    free = [k for k, (a, b) in enumerate(es) if a.bit_count() >= 2]
    assert fixed.bit_count() == 12 and len(free) == 16
    triples = [v for v in range(16) if v.bit_count() == 3]
    down = [sum(1 << k for k, (a, b) in enumerate(es) if b == t and a.bit_count() == 2) for t in triples]
    square_masks = []
    for i, j in combinations(range(4), 2):
        for v in range(16):
            if v & ((1 << i) | (1 << j)):
                continue
            x, y, z = v ^ (1 << i), v ^ (1 << j), v ^ (1 << i) ^ (1 << j)
            square_masks.append(sum(1 << ix[tuple(sorted(e))] for e in ((v, x), (x, z), (z, y), (y, v))))
    incidence = [sum(1 << k for k, e in enumerate(es) if v in e) for v in range(16)]
    legal_parents = c4free = 0
    near = Counter()
    for mask in range(1 << 16):
        G = fixed | sum(1 << k for j, k in enumerate(free) if mask >> j & 1)
        if any((G & d).bit_count() > 1 for d in down):
            continue
        legal_parents += 1
        if any(G & q == q for q in square_masks):
            continue
        c4free += 1
        b = (G & incidence[15]).bit_count()
        t = sum((G & incidence[s]).bit_count() == 4 for s in range(16) if s.bit_count() == 2)
        actual_holes = 0
        actual_stars = 0
        for fixed_bit in range(4):
            vertices = [v for v in range(16) if v >> fixed_bit & 1]
            stars = 0
            for v in vertices:
                if v.bit_count() % 2:
                    continue
                edge_mask = sum(1 << ix[tuple(sorted((v, v ^ (1 << j))))] for j in range(4) if j != fixed_bit)
                stars += G & edge_mask == edge_mask
            assert stars in (0, 1)
            actual_stars += stars
            actual_holes += stars == 0
        assert actual_stars == 2 * t + comb(b, 3) == 4 - actual_holes
        if actual_holes <= 1:
            near[actual_holes, b, t] += 1
    assert legal_parents == 4096 and c4free == 3715
    return {'all_upper_edge_masks': 65536, 'at_most_one_parent_masks': legal_parents,
            'C4_free_masks': c4free, 'near_full_type_counts': {str(k): v for k, v in sorted(near.items())}}


def all_integer_branches():
    rows = []
    survivors = []
    for S in (159, 160):
        h = 160 - S
        for alpha in range(h + 1):
            for beta in range(h - alpha + 1):
                for z4 in range(16):
                    for z3 in range(16 - z4):
                        z2 = 5 - alpha - 2 * z3 - 3 * z4
                        z1 = 15 - z2 - z3 - z4
                        if min(z1, z2) < 0:
                            continue
                        assert z4 <= 1
                        pair_sum = sum(comb(j, 2) * z for j, z in enumerate((z1, z2, z3, z4), 1))
                        a = Fraction(30 - beta - pair_sum, 2)
                        if a.denominator != 1 or not 0 <= a <= 15 - beta:
                            continue
                        a = int(a)
                        S2 = sum(comb(j + 2, 3) * z for j, z in enumerate((z1, z2, z3, z4), 1))
                        for c in range(5):
                            if (31 + c - S) % 3:
                                continue
                            # Unlike the author, distinguish each actual top
                            # degree 3,4,5,6 instead of aggregating <=5 at 5.
                            for top in range(3, 7):
                                c4 = c - z4 - int(top == 6)
                                if not 0 <= c4 <= a or (top == 6 and c4):
                                    continue
                                candidates = []
                                for f0 in range(a + 1):
                                    f1 = a - f0 - c4
                                    if f1 < 0 or f1 + 2 * c4 > 6:
                                        continue
                                    back = 4 * f0 + 10 * f1 + 20 * c4
                                    ordinary_max_degree = 3 if top == 6 else 4
                                    exception_max_degree = 4 if top == 6 else 5
                                    upper = S2 + back + (15 - a - beta) * comb(ordinary_max_degree, 3)
                                    upper += beta * comb(exception_max_degree, 3) + comb(top, 3)
                                    candidates.append((upper, f0, f1, c4))
                                if not candidates:
                                    continue
                                maximum = max(candidates)
                                row = {'target': S, 'alpha': alpha, 'beta': beta,
                                       'z': [z1, z2, z3, z4], 'a': a, 'c': c,
                                       'top_degree': top, 'c4': c4, 'S2': S2,
                                       'upper': maximum[0], 'backward_full_f_counts': list(maximum[1:])}
                                rows.append(row)
                                if maximum[0] >= S:
                                    survivors.append(row)
    assert len(survivors) == 1
    sole = survivors[0]
    assert (sole['target'], sole['alpha'], sole['beta'], sole['z'], sole['a'], sole['top_degree'], sole['c4'], sole['upper']) == (159, 0, 1, [13, 0, 1, 1], 10, 5, 1, 159)
    projected = [{**{k: v for k, v in r.items() if k != 'top_degree'}, 'top_degree_bound': r['top_degree']}
                 for r in rows if r['top_degree'] >= 5]
    author_rows = json.loads((SOURCE / 'integer_branches.json').read_text())
    canonical = lambda r: json.dumps(r, sort_keys=True)
    assert {canonical(r) for r in projected} == {canonical(r) for r in author_rows}
    assert len(projected) == len(author_rows) == 12
    return rows, survivors


def top_capacity():
    result = []
    for missing in range(6):
        top = 63
        W0 = top ^ (1 << missing)
        possible = []
        for R in range(64):
            if R.bit_count() != 4:
                continue
            upper = [R | (1 << i) for i in range(6) if not R >> i & 1]
            assert len(upper) == 2
            # Retain both edges at R; the square closes iff both upper
            # vertices are among the five retained top neighbors.
            if W0 in upper:
                possible.append(R)
        assert len(possible) == 5
        assert all((R & W0) == R for R in possible)
        result.append({'missing_direction': missing, 'eligible_R': possible})
    return result


def main():
    proof = (SOURCE / 'PROOF.md').read_bytes()
    assert sha256(proof).hexdigest() == EXPECTED
    assert all(b >= 32 or b in (9, 10, 13) for b in proof)
    marked = marked_q4()
    rows, sole = all_integer_branches()
    capacities = top_capacity()
    (HERE / 'all_actual_top_degree_branches.json').write_text(json.dumps(rows, indent=2) + '\n')
    results = {'status': 'PASS_INDEPENDENT_FINITE_CHECKS',
               'source_proof_sha256': EXPECTED, 'marked_Q4': marked,
               'integer_rows_with_actual_top_degrees': len(rows),
               'author_12_rows_match_projection': True, 'surviving_upper_bound_rows': sole,
               'forced_distinct_forward_two_R': 6, 'maximum_capacity': 5,
               'all_six_markings': capacities,
               'scope': 'Finite layer identity and arithmetic coverage only. Written review checks the normalization, imports, and full Q6 logical argument.',
               'checker_sha256': sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE / 'independent_checks.json').write_text(json.dumps(results, indent=2) + '\n')
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
