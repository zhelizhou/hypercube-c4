"""Nonauthor replay. Writes only its own review directory; no optimizer.

Geometry, states, actions, compositions and score are reconstructed here.
Native modules are imported only to compare their output, never to define it.
"""
from pathlib import Path
from itertools import combinations, permutations
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from math import comb, lcm
import hashlib
import json
import sys
from datetime import datetime, timezone

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PKG = HERE.parent
LAUNCH = PKG.parent
DATA = PKG / 'parallel15_master102'
SQUARE = ((0, 1), (0, 2), (1, 3), (2, 3))
ROOTS = (0, 1, 3, 6, 7)

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read(path):
    return json.loads(path.read_text(), parse_float=Fraction)

def canon_edge(a, b):
    return tuple(sorted((a, b)))

def cube_edges(n):
    # Sorting by low endpoint, then differing bit reproduces the public mask order.
    return sorted((a, b) for a in range(1 << n) for b in range(a + 1, 1 << n)
                  if (a ^ b).bit_count() == 1)

# For a fixed low endpoint the differing bit order agrees with high endpoint order.
E3 = cube_edges(3)
ORDER = E3 + [(a + 8, b + 8) for a, b in E3] + [(a, a + 8) for a in range(8)]

def square_faces(n):
    for a, b in combinations(range(n), 2):
        for base in range(1 << n):
            if base & ((1 << a) | (1 << b)):
                continue
            yield (a, b), (base, base + (1 << a), base + (1 << b), base + (1 << a) + (1 << b))

def c4free(edges, n):
    assert edges <= set(cube_edges(n))
    # In a cube every four-cycle is a coordinate square.
    return not any(all(canon_edge(vs[u], vs[v]) in edges for u, v in SQUARE)
                   for _, vs in square_faces(n))

def edge_transform(r, perm):
    return sum(1 << SQUARE.index(canon_edge(perm[u], perm[v]))
               for k, (u, v) in enumerate(SQUARE) if r & (1 << k))

def flag_transform(f, perm):
    c, p = f & 15, f >> 4
    return sum(1 << perm[u] for u in range(4) if c & (1 << u)) + 16 * edge_transform(p, perm)

# Enumerate the graph automorphisms as all preserving permutations, rather than
# taking the author's xor/axis-swap construction as input.
AUTOS = [p for p in permutations(range(4))
         if {canon_edge(p[u], p[v]) for u, v in SQUARE} == set(SQUARE)]
assert len(AUTOS) == 8
assert {tuple(p[q[i]] for i in range(4)) for p in AUTOS for q in AUTOS} == set(AUTOS)

def flag_edges(root, f):
    return ({SQUARE[k] for k in range(4) if root & (1 << k)} |
            {(u + 4, v + 4) for k, (u, v) in enumerate(SQUARE) if f & (1 << (k + 4))} |
            {(u, u + 4) for u in range(4) if f & (1 << u)})

CODES = [[f for f in range(256) if c4free(flag_edges(root, f), 3)] for root in ROOTS]
IDS = [{f: i for i, f in enumerate(codes)} for codes in CODES]
DIMS = list(map(len, CODES))
assert DIMS == [240, 212, 190, 187, 170]
assert sorted({min(edge_transform(r, p) for p in AUTOS) for r in range(15)}) == list(ROOTS)
STABS = [[p for p in AUTOS if edge_transform(r, p) == r] for r in ROOTS]
PERMS = [[[IDS[b][flag_transform(f, p)] for f in codes] for p in STABS[b]]
         for b, codes in enumerate(CODES)]
assert list(map(len, STABS)) == [8, 2, 2, 4, 2]
assert all(sorted(p) == list(range(DIMS[b])) for b, ps in enumerate(PERMS) for p in ps)

@lru_cache(None)
def flags_of_mask(mask):
    assert type(mask) is int and 0 <= mask < (1 << 32)
    edges = {e for k, e in enumerate(ORDER) if mask & (1 << k)}
    assert c4free(edges, 4)
    return tuple(actual_flags(frozenset(edges), 4))

def actual_flags(edges, n):
    for axes, vs in square_faces(n):
        root = sum(1 << k for k, (a, b) in enumerate(SQUARE) if canon_edge(vs[a], vs[b]) in edges)
        assert root != 15
        rootcanon = min(edge_transform(root, p) for p in AUTOS)
        b = ROOTS.index(rootcanon)
        transport = next(p for p in AUTOS if edge_transform(root, p) == rootcanon)
        flags = []
        for a in range(n):
            if a in axes:
                continue
            flag = sum(1 << k for k, v in enumerate(vs) if canon_edge(v, v ^ (1 << a)) in edges)
            flag += sum(1 << (4 + k) for k, (u, v) in enumerate(SQUARE)
                        if canon_edge(vs[u] ^ (1 << a), vs[v] ^ (1 << a)) in edges)
            moved = flag_transform(flag, transport)
            assert moved in IDS[b]
            flags.append(IDS[b][moved])
        yield b, tuple(flags)

def compositions(total, L):
    if L == 1:
        yield (total,)
    else:
        for first in range(total + 1):
            for tail in compositions(total - first, L - 1):
                yield (first,) + tail

def quadratic(Q, x):
    terms = [(i, v) for i, v in enumerate(x) if v]
    return sum(a * b * Q[i][j] for i, a in terms for j, b in terms)

def lift(Q, mapping, b):
    return [[sum(Q[mapping[p[i]]][mapping[p[j]]] for p in PERMS[b])
             for j in range(DIMS[b])] for i in range(DIMS[b])]

def local_integer(mask, kernels):
    # Denominator 24*12 = 288. No stabilizer factor for invariant full K.
    result = [0] * 5
    for b, (s, t) in flags_of_mask(mask):
        K = kernels[b]
        result[b] += 10 * K[s][t] + K[s][s] + K[t][t]
    return result

def restrictions(edges):
    masks = Counter()
    for axes in combinations(range(8), 4):
        support = sum(1 << a for a in axes)
        for base in range(256):
            if base & support:
                continue
            def embed(x):
                return base + sum(1 << axes[k] for k in range(4) if x & (1 << k))
            mask = sum(1 << k for k, (a, b) in enumerate(ORDER)
                       if canon_edge(embed(a), embed(b)) in edges)
            masks[mask] += 1
    assert sum(masks.values()) == 1120
    return masks

def bridge(edges, kernels):
    assert c4free(edges, 8)
    roots = Counter()
    direct = [0] * 5
    faces = list(actual_flags(frozenset(edges), 8))
    assert len(faces) == 1792
    for b, states in faces:
        assert len(states) == 6
        roots[b] += 1
        x = [0] * DIMS[b]
        for state in states:
            x[state] += 1
        direct[b] += quadratic(kernels[b], x)
    local = [0] * 5
    masks = restrictions(edges)
    for mask, mult in masks.items():
        for b, value in enumerate(local_integer(mask, kernels)):
            local[b] += mult * value
    assert all(Fraction(direct[b], 1792 * 36) == Fraction(local[b], 1120 * 288) for b in range(5))
    assert min(direct) >= 0
    return {'edges': len(edges), 'roots': 1792, 'slices': 1120,
            'root_type_counts': dict(roots), 'distinct_slices': len(masks),
            'direct_sums': direct, 'local_sums': local,
            'raw_values': [str(Fraction(v, 1792 * 36)) for v in direct]}

def main():
    started = datetime.now(timezone.utc).isoformat()
    mapping = read(DATA / 'MAPPING.json')
    cut = read(DATA / 'block3.EXACT_CUT.json')
    point = read(DATA / 'INPUT_POINT.json')
    stored = read(DATA / 'PROJECTED_MOMENTS.json')
    assert mapping['full_state_codes'] == CODES
    assert mapping['labels'] == 15
    maps = [[f >> 4 for f in codes] for codes in CODES]
    assert maps == mapping['full_state_to_label']
    assert all(set(m) == set(range(15)) for m in maps)
    b, small = cut['block'], cut['small_Q']
    assert b == 3 and cut['root_mask'] == 6
    assert all(type(x) is int for row in small for x in row)
    assert all(small[i][j] == small[j][i] for i in range(15) for j in range(15))
    full = lift(small, maps[b], b)
    assert full == cut['full_Q'] and cut['full_state_codes'] == CODES[b]
    assert set(map(tuple, PERMS[b])) == set(map(tuple, cut['root_state_permutations']))
    assert all(full[p[i]][p[j]] == full[i][j] for p in PERMS[b] for i in range(DIMS[b]) for j in range(DIMS[b]))
    scale = max(1, max(abs(x) for row in full for x in row))
    assert scale == cut['positive_normalization'] == 8000004
    histogram_values = [(quadratic(small, x), x) for x in compositions(6, 15)]
    minimum, minimizer = min(histogram_values)
    assert len(histogram_values) == 38760 and minimum == cut['finite6']['minimum'] == 28
    assert min(quadratic([[x - 1 for x in row] for row in small], x) for x in compositions(6, 15)) == -8
    fullwitness = {32: 1, 64: 1, 112: 2}
    x = [0] * DIMS[b]
    for f, amount in fullwitness.items():
        x[IDS[b][f]] = amount
    assert sum(x) == 4 and quadratic(full, x) == -1454496

    # All decimal weights exactly, no renormalization or root mass division.
    weights = point['lambda']
    assert len(weights) == len({mask for mask, _ in weights}) == 762
    assert all(w > 0 for _, w in weights)
    den = lcm(*(w.denominator for _, w in weights))
    U = [[[0] * 15 for _ in range(15)] for _ in range(5)]
    point_raw = Fraction()
    zeros = [[[0] * d for _ in range(d)] for d in DIMS]
    kernels = list(zeros)
    kernels[b] = full
    sys.path.insert(0, str(PKG))
    import score
    import finite_flags as native
    assert native.q4_edges_original() == ORDER
    assert [sorted(x) for x in native.STATE_IDS] == CODES
    assert native.DEN == 64512
    collisions = 0
    for mask, weight in weights:
        n = int(weight * den)
        flags = flags_of_mask(mask)
        # Reconstruct all five ORDERED projected moments from root geometry.
        for bb, states in flags:
            for p in PERMS[bb]:
                i, j = (maps[bb][p[state]] for state in states)
                U[bb][i][j] += n * (2240 // len(PERMS[bb]))
                U[bb][j][i] += n * (2240 // len(PERMS[bb]))
                U[bb][i][i] += n * (448 // len(PERMS[bb]))
                U[bb][j][j] += n * (448 // len(PERMS[bb]))
                collisions += i == j and p[states[0]] != p[states[1]]
        direct = Fraction(local_integer(mask, kernels)[b], 288)
        assert direct == score.value_on_graph(mask, DATA / 'block3.EXACT_CUT.json', normalize=False)
        assert direct / scale == score.value_on_graph(mask, DATA / 'block3.EXACT_CUT.json')
        point_raw += weight * direct
    assert U == stored['blocks'] and stored['moment_denominator'] == 129024 * den
    assert stored['lambda_sum'] == str(sum(w for _, w in weights))
    via_small = Fraction(len(PERMS[b]) * sum(small[i][j] * U[b][j][i] for i in range(15) for j in range(15)), 129024 * den)
    assert point_raw == via_small == Fraction(cut['exact_target_pairing'])
    assert str(point_raw / scale) == cut['normalized_pairing'] and point_raw / scale < Fraction(-1, 10000000)
    consumer, consumer_scale = score.full_face_kernel(DATA / 'block3.EXACT_CUT.json')
    assert consumer == kernels and consumer_scale == scale
    assert score.full_face_kernel(DATA / 'block3.EXACT_CUT.json', normalize=False)[1] == 1

    # Source-domain evidence uses numpy only for reading actual array files.
    sys.path.insert(0, str(LAUNCH / 'finite8_flags' / 'deps'))
    import numpy as np
    from scipy import sparse
    X = np.load(LAUNCH / 'finite8_frequency_cone' / 'histograms16_sum6.npy')
    A = sparse.load_npz(LAUNCH / 'finite8_frequency_cone' / 'generator_matrix.npz').tocsc()
    assert X.shape == (54264, 16) and A.shape == (136, 54264)
    actual = {tuple(map(int, row)) for row in X}
    assert len(actual) == 54264 and actual == set(compositions(6, 16))
    pairs = [(i, j) for i in range(16) for j in range(i, 16)]
    for k, row in enumerate(X):
        col = A.getcol(k)
        expected = {r: int(row[i]) * int(row[j]) for r, (i, j) in enumerate(pairs) if row[i] and row[j]}
        assert set(col.indices) == set(expected)
        assert all(abs(float(v) * 36 - expected[int(r)]) < 1e-12 for r, v in zip(col.indices, col.data))
    boundary = []
    for L in range(1, 17):
        filtered = {tuple(row[:L]) for row in actual if all(v == 0 for v in row[L:])}
        assert filtered == set(compositions(6, L)) and len(filtered) == comb(L + 5, 6)
        boundary.append({'L': L, 'count': len(filtered)})

    # Arbitrary non-equivariant map, including action-incompatibility witnesses.
    generic_maps = [[i % 3 for i in range(d)] for d in DIMS]
    q = [0, 1, 0]
    genericQ = [[36 * q[i] * q[j] - 15 * (q[i] + q[j]) + 6 for j in range(3)] for i in range(3)]
    assert min(quadratic(genericQ, x) for x in compositions(6, 3)) == 0
    nongauge = []
    generic_full = []
    for bb, mapping3 in enumerate(generic_maps):
        K = lift(genericQ, mapping3, bb)
        assert all(K[p[i]][p[j]] == K[i][j] for p in PERMS[bb] for i in range(DIMS[bb]) for j in range(DIMS[bb]))
        generic_full.append(K)
        for p in PERMS[bb]:
            found = False
            for i in range(DIMS[bb]):
                for j in range(i):
                    if mapping3[i] == mapping3[j] and mapping3[p[i]] != mapping3[p[j]]:
                        nongauge.append({'block': bb, 'states': [i, j], 'label': mapping3[i],
                                         'image_labels': [mapping3[p[i]], mapping3[p[j]]]})
                        found = True
                        break
                if found:
                    break
            if found:
                break
    assert nongauge
    # Unused-label and L=1/16 boundary algebra tests; no actual realizability assumed.
    boundary_pullbacks = []
    for L in (1, 2, 3, 15, 16):
        bits = [int(i == 1) for i in range(L)]
        Q = [[36 * bits[i] * bits[j] - 15 * (bits[i] + bits[j]) + 6 for j in range(L)] for i in range(L)]
        assert min(quadratic(Q, y) for y in compositions(6, L)) >= 0
        mappingL = [0] * DIMS[0] if L > 1 else [0] * DIMS[0]
        lifted = lift(Q, mappingL, 0)
        assert lifted[0][0] == 8 * Q[0][0]
        boundary_pullbacks.append({'L': L, 'unused_labels': L - 1, 'all_six_on_one_state': 36 * lifted[0][0]})

    seed = LAUNCH.parents[2] / 'data/q8_seed682.edges'
    edges = {tuple(map(int, row.split())) for row in seed.read_text().splitlines() if row.strip()}
    assert len(edges) == 682 and digest(seed) == '185d2857fa64b4ff8f53314363333f5ca1ee85c3560d254027d1b2e623c56a2c'
    calibrated = list(generic_full)
    calibrated[b] = full
    seedcal = bridge(edges, calibrated)
    genericcal = bridge(edges, generic_full)
    assert seedcal['root_type_counts'].get(b, 0) == 0 and seedcal['raw_values'][b] == '0'
    sparsecal = bridge({(0, 1), (2, 3)}, kernels)
    assert sparsecal['root_type_counts'][b] == 1
    assert Fraction(sparsecal['raw_values'][b]) == Fraction(full[0][0], 1792)
    assert Fraction(sparsecal['raw_values'][b]) / scale == Fraction(1, 1792)
    # Zero graph and an all-one-direction matching exercise legal degenerate inputs.
    emptycal = bridge(set(), generic_full)
    matchingcal = bridge({(v, v + 1) for v in range(0, 256, 2)}, generic_full)
    out = {'status': 'INDEPENDENT_EXACT_REPLAY_COMPLETE', 'started_at': started,
           'completed_at': datetime.now(timezone.utc).isoformat(),
           'state_dimensions': DIMS, 'stabilizer_sizes': list(map(len, STABS)),
           'histogram_counts': boundary, 'finite6_minimum': minimum, 'minimizer': minimizer,
           'before_repair_minimum': -8, 'J_repair': 1, 'full_kernel_scale': scale,
           'noncopositive_full_witness': {'code_counts': fullwitness, 'total': 4, 'quadratic': quadratic(full, x)},
           'actual_graphs_checked': len(weights), 'exact_lambda_sum': str(sum(w for _, w in weights)),
           'raw_pairing': str(point_raw), 'normalized_pairing': str(point_raw / scale),
           'projected_moments_entrywise_equal': True, 'projection_collisions_exercised': collisions,
           'native_scorer_all_actual_graphs_equal': True, 'full_kernel_consumer_equal': True,
           'generic_non_equivariance_witnesses': nongauge, 'unused_label_boundaries': boundary_pullbacks,
           'actual682_calibration': seedcal, 'non_equivariant682_calibration': genericcal,
           'nonzero_sparseQ8_calibration': sparsecal, 'empty_graph_calibration': emptycal,
           'one_direction_matching_calibration': matchingcal,
           'no_lp_run': True, 'main_upper682': 'OPEN', 'script_sha256': digest(Path(__file__))}
    (HERE / 'INDEPENDENT_RESULTS.json').write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps({k: out[k] for k in ('status', 'finite6_minimum', 'actual_graphs_checked', 'raw_pairing', 'normalized_pairing', 'exact_lambda_sum')}), flush=True)

if __name__ == '__main__':
    main()
