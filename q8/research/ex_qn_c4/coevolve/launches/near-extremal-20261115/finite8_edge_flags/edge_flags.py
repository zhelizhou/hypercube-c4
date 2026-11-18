"""Exact standard-library edge-root finite8 feature, original Q4 edge order."""
from collections import Counter
from itertools import combinations

DEN = 64512
DIMS = (8, 7)  # rootedge missing / retained, state IDs are raw three-bit codes.


def edge(u, v):
    return min(u, v), max(u, v)


def ambient(n):
    return [(u, u ^ (1 << i)) for u in range(1 << n) for i in range(n) if not u & (1 << i)]


def original_q4_edges():
    bottom = ambient(3)
    return bottom + [(u + 8, v + 8) for u, v in bottom] + [(u, u + 8) for u in range(8)]


def from_mask(mask):
    assert type(mask) is int and 0 <= mask < 2**32
    return {e for k, e in enumerate(original_q4_edges()) if mask >> k & 1}


def flip(code):
    return (code & 4) | ((code & 1) << 1) | ((code & 2) >> 1)


def root_records(E, n):
    for u, v in ambient(n):
        root = int((u, v) in E)
        direction = (u ^ v).bit_length() - 1
        states = []
        for a in range(n):
            if a == direction:
                continue
            c = int(edge(u, u ^ (1 << a)) in E)
            c |= int(edge(v, v ^ (1 << a)) in E) << 1
            c |= int(edge(u ^ (1 << a), v ^ (1 << a)) in E) << 2
            assert c < DIMS[root]
            states.append(c)
        yield root, states


def local_coefficients(E):
    """Return upper-coordinate coefficients with denominator64512."""
    result = Counter()
    count = 0
    for root, states in root_records(set(E), 4):
        count += 1
        assert len(states) == 3
        for action in (lambda s: s, flip):
            moved = [action(s) for s in states]
            for i, j in combinations(moved, 2):
                result[root, min(i, j), max(i, j)] += 288
            for i in moved:
                result[root, i, i] += 48
    assert count == 32
    return result


def twice_matrices(coefficients):
    result = [[[0] * d for _ in range(d)] for d in DIMS]
    for (root, i, j), value in coefficients.items():
        result[root][i][j] += value * (2 if i == j else 1)
        if i != j:
            result[root][j][i] += value
    return result


def restriction_records(E, n):
    for axes in combinations(range(n), 4):
        bits = sum(1 << a for a in axes)
        for base in range(1 << n):
            if base & bits:
                continue
            vertices = [base ^ sum(1 << axes[j] for j in range(4) if v >> j & 1) for v in range(16)]
            graph = sum(1 << k for k, (u, v) in enumerate(original_q4_edges()) if edge(vertices[u], vertices[v]) in E)
            yield axes, base, graph


def moment(weights):
    coefficients = Counter()
    for graph, weight in weights:
        for key, value in local_coefficients(from_mask(graph)).items():
            coefficients[key] += weight * value
    return twice_matrices(coefficients)
