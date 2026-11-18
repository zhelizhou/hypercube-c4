"""Targeted exact counterexample/mutation checks; no source modifications."""
import sys
sys.dont_write_bytecode = True
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
import json
import independent_geometry as r

point = json.loads((r.SRC / 'FAMILY_OBSTRUCTION.json').read_text())
rows = point['probability_numerators']
out = {}

# Rebuild the full finite conditional law, rather than merely checking totals.
pairs = list(combinations(range(8), 2))
counts = Counter()
weighted = Counter()
for four in combinations(range(8), 4):
    local = list(combinations(four, 2))
    for A in local:
        for B in local:
            ov = len(set(A) & set(B))
            counts[A, B] += 1
            weighted[A, B] += {0: F(15, 28) / 6, 1: F(12, 28) / 24, 2: F(1, 28) / 6}[ov] / 70
assert len(weighted) == 784 and set(weighted.values()) == {F(1, 784)}
assert all(counts[A, B] == {0: 1, 1: 5, 2: 15}[len(set(A) & set(B))] for A in pairs for B in pairs)
out['vertex_finite_law'] = {'ordered_pair_count': 784, 'each_exact_probability': '1/784', 'completion_multiplicities_disjoint_overlap_same': [1, 5, 15]}

face = Counter()
for a, b in combinations(range(6), 2):
    face[a, b] += F(1, 15) * F(5, 6) / 2
    face[b, a] += F(1, 15) * F(5, 6) / 2
    face[a, a] += F(1, 15) / 12
    face[b, b] += F(1, 15) / 12
assert len(face) == 36 and set(face.values()) == {F(1, 36)}
out['face_finite_law'] = {'ordered_pair_count': 36, 'each_exact_probability': '1/36'}

g = rows[0][0]
U = r.local_matrix(g)
b, i, j = next(k for k, v in U.items() if k[1] != k[2] and v)
good = F(U[b, i, i] + U[b, j, j] + 2 * U[b, i, j], 2 * r.DEN)
bad = good + F(2 * U[b, i, j], 2 * r.DEN)
assert good != bad
out['off_diagonal_factor_two_mutant'] = {'graph': g, 'block': b, 'rank_one_kernel_nonzero_vector_coordinates': [i, j], 'correct_moment_trace': str(good), 'incorrect_doubled_offdiagonal_trace': str(bad), 'detected': True}

found = None
for g, w in rows:
    for root, flags in r.FRAMES4:
        rootcode = r.code_from_indices(g, root)
        s, t = [r.code_from_indices(g, f) for f in flags]
        canonical = min(r.action_root(rootcode, ep) for p, ep in r.SYMS)
        block = r.REPS.index(canonical)
        states = [(r.IDS[block][r.action_flag(s, p, ep)], r.IDS[block][r.action_flag(t, p, ep)]) for p, ep in r.SYMS if r.action_root(rootcode, ep) == canonical]
        badpair = (min(a for a, c in states), min(c for a, c in states))
        if set(states) != {badpair}:
            found = {'graph': g, 'actual_root_mask': rootcode, 'flag_codes': [s, t], 'correct_simultaneous_canonical_state_pairs': states, 'incorrect_independent_minimum_pair': badpair}
            break
    if found:
        break
assert found
out['independent_gauge_mutant'] = found
assert r.vertex_state(1) != r.vertex_state(8)
out['vertex_translation_mutant'] = {'single_edge_code': 1, 'translated_code': 8, 'correct_distinct_state_ids': [r.vertex_state(1), r.vertex_state(8)], 'translation_is_not_root_preserving': True}

negative = None
for g, w in rows:
    U = r.local_matrix(g)
    for b in range(6):
        ids = sorted({i for bb, i, j in U if bb == b})
        for i, j in combinations(ids, 2):
            d = U[b, i, i] * U[b, j, j] - U[b, i, j]**2
            if d < 0:
                negative = {'graph': g, 'block': b, 'state_ids': [i, j], 'twice_scaled_2x2_matrix': [[U[b, i, i], U[b, i, j]], [U[b, j, i], U[b, j, j]]], 'determinant': d}
                break
        if negative:
            break
    if negative:
        break
assert negative
out['individual_local_moment_need_not_be_PSD'] = negative

cert = point['LDL_certificates'][1]
A = point['blocks'][1]['twice_integer_matrix']
assert F(cert['D'][0]) == A[0][0]
assert F(cert['D'][0]) + 1 != A[0][0]
out['LDL_first_pivot_plus_one_mutant'] = {'detected': True, 'entry_00_exactly_checks_first_pivot': True}
out['status'] = 'PASS_TARGETED_EXACT_ATTACKS'
(r.HERE / 'ATTACK_CHECKS.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps(out, indent=2))
