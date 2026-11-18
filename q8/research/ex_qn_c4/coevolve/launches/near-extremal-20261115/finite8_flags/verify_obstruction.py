"""Standalone author second implementation: geometry, moments, rational PSD.

Does not import finite_flags, numpy, scipy, LP code or precomputed features.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
QE = ((0, 1), (0, 2), (1, 3), (2, 3))
REPS = (0, 1, 3, 6, 7)


def edge(x, y):
    return tuple(sorted((x, y)))


def symmetries():
    out = []
    for swap in (False, True):
        for t in range(4):
            vertices = [t ^ (((v & 1) * 2 + (v >> 1)) if swap else v) for v in range(4)]
            ep = [QE.index(edge(vertices[x], vertices[y])) for x, y in QE]
            roots = [sum(1 << ep[i] for i in range(4) if r >> i & 1) for r in range(16)]
            flags = [sum(1 << vertices[i] for i in range(4) if f >> i & 1) + sum(1 << (4 + ep[i]) for i in range(4) if f >> (4 + i) & 1) for f in range(256)]
            out.append((roots, flags))
    return out


SYMS = symmetries()
IDS = []
for root in REPS:
    states = []
    for code in range(256):
        if code >> 4 == 15:
            continue
        if any(root >> k & 1 and code >> (k + 4) & 1 and code >> x & 1 and code >> y & 1 for k, (x, y) in enumerate(QE)):
            continue
        states.append(code)
    IDS.append({v: i for i, v in enumerate(states)})
assert [len(x) for x in IDS] == [240, 212, 190, 187, 170]


def vstate(code):
    swap = ((code & 1) << 1) | ((code & 2) >> 1) | ((code & 4) << 1) | ((code & 8) >> 1)
    return [0, 1, 3, 4, 5, 6, 7, 12, 13].index(min(code, swap))


def face_records(E, n):
    for i, j in combinations(range(n), 2):
        for v in range(1 << n):
            if v & ((1 << i) | (1 << j)):
                continue
            vs = (v, v ^ (1 << i), v ^ (1 << j), v ^ (1 << i) ^ (1 << j))
            root = sum(1 << k for k, (a, b) in enumerate(QE) if edge(vs[a], vs[b]) in E)
            assert root != 15
            flags = []
            for k in range(n):
                if k in (i, j):
                    continue
                f = sum(1 << a for a in range(4) if edge(vs[a], vs[a] ^ (1 << k)) in E)
                f += sum(1 << (a + 4) for a, (x, y) in enumerate(QE) if edge(vs[x] ^ (1 << k), vs[y] ^ (1 << k)) in E)
                flags.append(f)
            canonical = min(r[root] for r, _ in SYMS)
            maps = [s for r, s in SYMS if r[root] == canonical]
            yield REPS.index(canonical), [[IDS[REPS.index(canonical)][s[f]] for f in flags] for s in maps]


def vertex_records(E, n):
    for v in range(1 << n):
        pairs = list(combinations(range(n), 2))
        states = []
        for i, j in pairs:
            vs = (v, v ^ (1 << i), v ^ (1 << j), v ^ (1 << i) ^ (1 << j))
            code = sum(1 << k for k, (x, y) in enumerate(QE) if edge(vs[x], vs[y]) in E)
            assert code != 15
            states.append(vstate(code))
        yield pairs, states


def e4():
    bottom = [(x, x ^ (1 << i)) for x in range(8) for i in range(3) if not x >> i & 1]
    return bottom + [(x + 8, y + 8) for x, y in bottom] + [(x, x + 8) for x in range(8)]


def local_twice_moments(E):
    U = Counter()
    for b, mapped in face_records(E, 4):
        h = len(mapped)
        for i, j in mapped:
            U[b, i, j] += 2240 // h
            U[b, j, i] += 2240 // h
            U[b, i, i] += 448 // h
            U[b, j, j] += 448 // h
    for pairs, states in vertex_records(E, 4):
        # Ordered pair construction, distinct from the extractor's symmetric
        # packed upper-coordinate accumulation.
        for a in range(6):
            U[5, states[a], states[a]] += 48
            for b in range(6):
                if a == b:
                    continue
                overlap = bool(set(pairs[a]) & set(pairs[b]))
                U[5, states[a], states[b]] += 144 if overlap else 720
    return U


def compare_blocks(expected, blocks):
    reconstructed = {}
    for block in blocks:
        b, support, matrix = block['block'], block['support'], block['twice_integer_matrix']
        assert len(matrix) == len(support)
        for a, i in enumerate(support):
            for c, j in enumerate(support):
                if matrix[a][c]:
                    reconstructed[b, i, j] = matrix[a][c]
    assert {k: v for k, v in expected.items() if v} == reconstructed


def main():
    point = json.loads((HERE / 'FAMILY_OBSTRUCTION.json').read_text())
    weights = point['probability_numerators']
    W = point['probability_denominator']
    assert all(type(g) is int and 0 <= g < (1 << 32) and type(w) is int and w > 0 for g, w in weights) and sum(w for g, w in weights) == W
    assert len({g for g, w in weights}) == len(weights)
    full, edge_total = Counter(), 0
    local_edges = e4()
    for graph, weight in weights:
        E = {e for k, e in enumerate(local_edges) if graph >> k & 1}
        # Includes all24 square C4 checks in face_records, not an assumed label.
        U = local_twice_moments(E)
        for key, value in U.items():
            full[key] += weight * value
        edge_total += weight * len(E)
    compare_blocks(full, point['blocks'])
    rho = Fraction(edge_total, W * 32)
    assert str(rho) == point['density_exact'] and rho > Fraction(683, 1024)
    statuses = []
    for block, certificate in zip(point['blocks'], point['LDL_certificates']):
        A = block['twice_integer_matrix']
        m = len(A)
        assert block['block'] == certificate['block']
        if not m:
            assert certificate['status'] == 'ZERO_PSD'
            statuses.append({'block': block['block'], 'rank': 0, 'status': 'ZERO_PSD'})
            continue
        L = [[Fraction(x) for x in row] for row in certificate['L']]
        D = [Fraction(x) for x in certificate['D']]
        assert len(L) == len(D) == m and all(d > 0 for d in D)
        assert all(L[i][i] == 1 and all(L[i][j] == 0 for j in range(i + 1, m)) for i in range(m))
        assert all(sum(L[i][k] * D[k] * L[j][k] for k in range(min(i, j) + 1)) == A[i][j] for i in range(m) for j in range(m))
        statuses.append({'block': block['block'], 'rank': m, 'status': 'EXACT_LDL_POSITIVE'})

    # Independently verify the whole-Q8 sampling bridge on the actual682 seed:
    # direct root empirical outer products versus its1120 common Q4 moments.
    seed = json.loads((HERE / 'Q8_seed682_point.json').read_text())
    E = {tuple(map(int, line.split())) for line in Path(seed['source']).read_text().splitlines() if line.strip()}
    direct = Counter()
    face_count = 0
    for b, mapped in face_records(E, 8):
        face_count += 1
        h = len(mapped)
        for states in mapped:
            counts = Counter(states)
            for i, ni in counts.items():
                for j, nj in counts.items():
                    direct[b, i, j] += (2240 // h) * ni * nj
    assert face_count == 1792
    vertices = 0
    for pairs, states in vertex_records(E, 8):
        vertices += 1
        assert len(states) == 28
        counts = Counter(states)
        for i, ni in counts.items():
            for j, nj in counts.items():
                direct[5, i, j] += 720 * ni * nj
    assert vertices == 256
    compare_blocks(direct, seed['blocks'])
    out = {'status': 'PASS_EXACT_GEOMETRY_AND_LDL', 'scope': 'Second author implementation of all818 local geometric scores and all six exact PSD moments; exact direct-root/Q4 bridge regression on actual682 Q8. No independent-agent review and no Q8 counterexample.', 'point_support': len(weights), 'density_exact': str(rho), 'threshold': '683/1024', 'strict_gap_exact': str(rho - Fraction(683, 1024)), 'blocks': statuses, 'actual_seed_bridge': {'Q4_restrictions': 1120, 'face_roots': face_count, 'vertex_roots': vertices, 'direct_empirical_outer_product_moments_equal_local_Q4_sum': True}, 'point_sha256': hashlib.sha256((HERE / 'FAMILY_OBSTRUCTION.json').read_bytes()).hexdigest(), 'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE / 'OBSTRUCTION_VERIFICATION.json').write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
