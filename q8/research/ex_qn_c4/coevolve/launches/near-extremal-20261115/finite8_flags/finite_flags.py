"""Exact finite8 coefficients in the original five full-face +9 vertex states.

Only Python standard library. Sources are read only; all outputs are task-local.
Coefficient denominator64512; symmetric Q upper-triangle entries are coordinates.
"""
from collections import Counter
from functools import lru_cache
from itertools import combinations

Q2_EDGES = ((0, 1), (0, 2), (1, 3), (2, 3))
Q2_EI = {e: i for i, e in enumerate(Q2_EDGES)}
ROOT_MASKS = (0, 1, 3, 6, 7)
DIMS = (240, 212, 190, 187, 170, 9)
DEN = 64512


def edge(x, y):
    return min(x, y), max(x, y)


def cube_edges(n):
    return [(x, x ^ (1 << i)) for x in range(1 << n) for i in range(n) if not x & (1 << i)]


def q4_edges_original():
    e3 = cube_edges(3)
    return e3 + [(x + 8, y + 8) for x, y in e3] + [(x, x + 8) for x in range(8)]


def q4_edges_from_mask(mask):
    return {e for k, e in enumerate(q4_edges_original()) if mask & (1 << k)}


def transforms():
    result = []
    for swap in range(2):
        for translation in range(4):
            vertices = [translation ^ ((((x & 1) << 1) | ((x & 2) >> 1)) if swap else x) for x in range(4)]
            em = [Q2_EI[edge(vertices[x], vertices[y])] for x, y in Q2_EDGES]
            r = [sum(1 << em[k] for k in range(4) if mask & (1 << k)) for mask in range(16)]
            s = [sum(1 << vertices[k] for k in range(4) if flag & (1 << k)) + sum(1 << (4 + em[k]) for k in range(4) if flag & (1 << (4 + k))) for flag in range(256)]
            result.append((r, s))
    return result


TRANSFORMS = transforms()
STATE_IDS = []
for root in ROOT_MASKS:
    valid = []
    for flag in range(240):  # The translated Q2 itself must not be full.
        connect, parallel = flag & 15, flag >> 4
        if any(root & (1 << k) and parallel & (1 << k) and connect & (1 << x) and connect & (1 << y) for k, (x, y) in enumerate(Q2_EDGES)):
            continue
        valid.append(flag)
    STATE_IDS.append({flag: i for i, flag in enumerate(valid)})
assert tuple(map(len, STATE_IDS)) == DIMS[:5]


def vertex_canonical(code):
    swapped = ((code & 1) << 1) | ((code & 2) >> 1) | ((code & 4) << 1) | ((code & 8) >> 1)
    return min(code, swapped)


VERTEX_REPS = sorted({vertex_canonical(code) for code in range(15)})
VERTEX_ID = {code: VERTEX_REPS.index(vertex_canonical(code)) for code in range(15)}
assert len(VERTEX_REPS) == 9


@lru_cache(None)
def face_entries(root, first, second):
    canonical = min(r[root] for r, _ in TRANSFORMS)
    h0 = next(k for k, (r, _) in enumerate(TRANSFORMS) if r[root] == canonical)
    block = ROOT_MASKS.index(canonical)
    first = TRANSFORMS[h0][1][first]
    second = TRANSFORMS[h0][1][second]
    stabilizer = [s for r, s in TRANSFORMS if r[canonical] == canonical]
    output = Counter()
    for action in stabilizer:
        i, j = STATE_IDS[block][action[first]], STATE_IDS[block][action[second]]
        output[block, min(i, j), max(i, j)] += 8 // len(stabilizer)
    assert sum(output.values()) == 8  # Original faceval =8 Qbar.
    return output


def face_data(E, n):
    for i, j in combinations(range(n), 2):
        ij = (1 << i) | (1 << j)
        for x in range(1 << n):
            if x & ij:
                continue
            vertices = [x, x ^ (1 << i), x ^ (1 << j), x ^ ij]
            root = sum(1 << k for k, (a, b) in enumerate(Q2_EDGES) if edge(vertices[a], vertices[b]) in E)
            assert root != 15
            flags = []
            for axis in range(n):
                if axis in (i, j):
                    continue
                bit = 1 << axis
                flag = sum(1 << k for k in range(4) if edge(vertices[k], vertices[k] ^ bit) in E)
                flag += sum(1 << (4 + k) for k, (a, b) in enumerate(Q2_EDGES) if edge(vertices[a] ^ bit, vertices[b] ^ bit) in E)
                flags.append(flag)
            yield root, flags


def vertex_states(E, n, x):
    result = []
    for i, j in combinations(range(n), 2):
        vertices = [x, x ^ (1 << i), x ^ (1 << j), x ^ (1 << i) ^ (1 << j)]
        code = sum(1 << k for k, (a, b) in enumerate(Q2_EDGES) if edge(vertices[a], vertices[b]) in E)
        assert code != 15
        result.append(VERTEX_ID[code])
    return result


def local_coefficients(E):
    """Return rho numerator and integer Q-entry coefficients, denominator64512."""
    E = set(E)
    out = Counter()
    count = 0
    for root, states in face_data(E, 4):
        count += 1
        assert len(states) == 2
        s, t = states
        for key, value in face_entries(root, s, t).items():
            out[key] += 280 * value
        for state in (s, t):
            for key, value in face_entries(root, state, state).items():
                out[key] += 28 * value
    assert count == 24
    pairs = list(combinations(range(4), 2))
    for x in range(16):
        states = vertex_states(E, 4, x)
        for a, b in combinations(range(6), 2):
            overlap = len(set(pairs[a]) & set(pairs[b]))
            weight = 720 if overlap == 0 else 144
            i, j = sorted((states[a], states[b]))
            out[5, i, j] += weight
        for state in states:
            out[5, state, state] += 24
    return 2016 * len(E), out


def restrictions(E, n):
    for axes in combinations(range(n), 4):
        support = sum(1 << i for i in axes)
        for base in range(1 << n):
            if base & support:
                continue
            vertices = [base ^ sum(1 << axes[j] for j in range(4) if x & (1 << j)) for x in range(16)]
            yield {e for e in q4_edges_original() if edge(vertices[e[0]], vertices[e[1]]) in E}


def moment_from_graph(E, n):
    rho_numerator = 0
    moments = Counter()
    graphs = Counter()
    source_edges = q4_edges_original()
    for K in restrictions(E, n):
        rho, coeff = local_coefficients(K)
        rho_numerator += rho
        moments.update(coeff)
        code = sum(1 << i for i, e in enumerate(source_edges) if e in K)
        graphs[code] += 1
    total = sum(graphs.values())
    return {'restrictions': total, 'density_numerator': rho_numerator, 'coefficient_denominator': DEN * total, 'moments': moments, 'graphs': graphs}


def dense_blocks(coeff):
    blocks = []
    for b in range(6):
        support = sorted({i for block, i, j in coeff if block == b} | {j for block, i, j in coeff if block == b})
        lookup = {x: k for k, x in enumerate(support)}
        # Twice the actual symmetric matrix, so every entry remains integer.
        matrix = [[0] * len(support) for _ in support]
        for (block, i, j), c in coeff.items():
            if block != b:
                continue
            u, v = lookup[i], lookup[j]
            matrix[u][v] += c * (2 if i == j else 1)
            if i != j:
                matrix[v][u] += c
        blocks.append({'block': b, 'full_dimension': DIMS[b], 'support': support, 'twice_integer_matrix': matrix})
    return blocks
