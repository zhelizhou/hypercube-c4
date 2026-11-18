#!/usr/bin/env python3
"""Independent finite checks for the analytic L1 proof; Python stdlib only.

This is not a search over Q6 graphs and does not certify the imported low2
theorem. It checks all marked Q4 layer configurations used by the counting
identity and every integer layer-count branch in the final argument.
"""
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
from math import comb
from pathlib import Path
import json


HERE = Path(__file__).resolve().parent


def edge(x, y):
    return (min(x, y), max(x, y))


def squares(n):
    for i, j in combinations(range(n), 2):
        mask = (1 << i) | (1 << j)
        for x in range(1 << n):
            if x & mask == 0:
                yield {edge(x, x ^ (1 << i)), edge(x, x ^ (1 << j)),
                       edge(x ^ (1 << i), x ^ mask),
                       edge(x ^ (1 << j), x ^ mask)}


def check_marked_q4():
    """4^4 choices of triple-parent times 2^4 top edges, without quotienting."""
    n = 4
    top = (1 << n) - 1
    pairs = [x for x in range(1 << n) if x.bit_count() == 2]
    triples = [x for x in range(1 << n) if x.bit_count() == 3]
    fixed = {edge(s, s ^ (1 << i)) for s in pairs
             for i in range(n) if s & (1 << i)}
    assert len(fixed) == 12
    parent_options = [[None] + [t ^ (1 << i) for i in range(n)
                                if t & (1 << i)] for t in triples]
    sq = list(squares(n))
    attempted = legal = near_full = 0
    local_types = Counter()
    for selected in product(*parent_options):
        middle = {edge(t, p) for t, p in zip(triples, selected)
                  if p is not None}
        for top_mask in range(1 << len(triples)):
            attempted += 1
            es = fixed | middle | {edge(top, t) for j, t in enumerate(triples)
                                   if top_mask & (1 << j)}
            if any(q <= es for q in sq):
                continue
            legal += 1
            b = top_mask.bit_count()
            double_pairs = sum(all(edge(s, s | (1 << i)) in es
                                   for i in range(n) if not s & (1 << i))
                               for s in pairs)
            actual_stars = 0
            actual_holes = 0
            for fixed_one in range(n):
                base = 1 << fixed_one
                free = [i for i in range(n) if i != fixed_one]
                vertices = [x for x in range(1 << n) if x & base]
                stars = sum(all(edge(x, x ^ (1 << i)) in es for i in free)
                            for x in vertices if x.bit_count() % 2 == 0)
                assert stars <= 1
                actual_stars += stars
                actual_holes += int(stars == 0)
            assert actual_stars == 2 * double_pairs + comb(b, 3)
            assert actual_stars == 4 - actual_holes
            if actual_holes <= 1:
                near_full += 1
                if actual_holes == 0:
                    assert (b == 4 and double_pairs == 0) or (
                        b <= 2 and double_pairs == 2)
                else:
                    assert b == 3 and double_pairs == 1
                local_types[(actual_holes, b, double_pairs)] += 1
    assert attempted == 4096
    return {"attempted": attempted, "C4_free": legal,
            "at_most_one_hole": near_full,
            "types_h_b_t": [{"h": h, "b": b, "t": t, "count": count}
                            for (h, b, t), count in sorted(local_types.items())]}


def check_integer_branches():
    """Use actual binomial weights and forward-edge counts, not printed bounds."""
    rows = []
    survivors = []
    for target in (159, 160):
        holes = 160 - target
        allowed_c = [c for c in range(5) if (31 + c - target) % 3 == 0]
        for alpha in range(holes + 1):
            for beta in range(holes - alpha + 1):
                for z2, z3, z4 in product(range(16), repeat=3):
                    z1 = 15 - z2 - z3 - z4
                    if z1 < 0 or z1 + 2*z2 + 3*z3 + 4*z4 != 20-alpha:
                        continue
                    pair_count = z2 + 3*z3 + 6*z4
                    numerator = 30-beta-pair_count
                    if numerator % 2:
                        continue
                    a = numerator // 2
                    if not 0 <= a <= 15-beta:
                        continue
                    s2 = sum(z*comb(2+t, 3)
                             for t, z in enumerate((z1, z2, z3, z4), 1))
                    for c in allowed_c:
                        for top_degree in (5, 6):
                            # The top_degree=5 row bounds all top degrees <=5.
                            c4 = c-z4-int(top_degree == 6)
                            if not 0 <= c4 <= a:
                                continue
                            if top_degree == 6 and c4:
                                continue
                            possibilities = []
                            for f1 in range(a-c4+1):
                                f0 = a-f1-c4
                                if f1 + 2*c4 > 6:
                                    continue
                                # Backward-full vertices have degrees 4,5,6.
                                back = f0*comb(4, 3)+f1*comb(5, 3)+c4*comb(6, 3)
                                # All other vertices use b<=2, except beta b=3.
                                max_f = 1 if top_degree == 6 else 2
                                other = (15-a-beta)*comb(2+max_f, 3)
                                exceptional = beta*comb(3+max_f, 3)
                                total = s2+back+other+exceptional+comb(top_degree, 3)
                                possibilities.append((total, f0, f1, c4))
                            if not possibilities:
                                continue
                            best = max(possibilities)
                            row = {"target": target, "alpha": alpha, "beta": beta,
                                   "z": [z1,z2,z3,z4], "a": a, "c": c,
                                   "top_degree_bound": top_degree, "c4": c4,
                                   "S2": s2, "upper": best[0],
                                   "backward_full_f_counts": list(best[1:])}
                            rows.append(row)
                            if best[0] >= target:
                                survivors.append(row)
    assert len(survivors) == 1, survivors
    sole = survivors[0]
    assert sole == {"target":159, "alpha":0, "beta":1, "z":[13,0,1,1],
                    "a":10, "c":2, "top_degree_bound":5, "c4":1,
                    "S2":43, "upper":159,
                    "backward_full_f_counts":[5,4,1]}, sole
    # Equality forces one f=2 backward-full, beta exceptional f=2, and all
    # ordinary non-backward-full vertices to have degree4, hence b=f=2.
    forced_forward_two = sole["c4"] + sole["beta"] + 15-sole["a"]-sole["beta"]
    assert forced_forward_two == 6
    return rows, survivors


def check_top_capacity():
    """All marked choices of the sole absent top edge; direct square check."""
    top = 63
    counts = []
    for absent_direction in range(6):
        retained_top_neighbors = {top ^ (1 << i) for i in range(6)
                                  if i != absent_direction}
        eligible = []
        for R in range(64):
            if R.bit_count() != 4:
                continue
            upper = {R | (1 << i) for i in range(6) if not R & (1 << i)}
            if not upper <= retained_top_neighbors:
                eligible.append(R)
        assert len(eligible) == 5
        absent_neighbor = top ^ (1 << absent_direction)
        assert all((R ^ absent_neighbor).bit_count() == 1 for R in eligible)
        counts.append({"absent_direction": absent_direction,
                       "eligible_four_sets": eligible})
    return counts


def main():
    local = check_marked_q4()
    rows, survivors = check_integer_branches()
    capacity = check_top_capacity()
    (HERE / "integer_branches.json").write_text(
        json.dumps(rows, indent=2)+"\n", encoding="utf-8")
    report = {"status": "PASS", "scope": "finite local identities and integer branches only",
              "marked_Q4": local, "integer_rows": len(rows),
              "surviving_upper_bound_rows": survivors,
              "final_forward_two_required": 6, "top_capacity": capacity,
              "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE / "CHECK_RESULTS.json").write_text(
        json.dumps(report, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
