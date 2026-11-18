"""Standalone exact edge geometry and finite7 checks, independent enumeration."""
from pathlib import Path
from collections import Counter
from fractions import Fraction
from itertools import combinations
from math import lcm
import hashlib
import json

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'finite8_flags'


def flip(s):
    return ((s & 1) << 1) + ((s & 2) >> 1) + (s & 4)


def edges(n):
    return [(u, u ^ (1 << i)) for u in range(1 << n) for i in range(n) if not u >> i & 1]


Q4 = edges(3) + [(u + 8, v + 8) for u, v in edges(3)] + [(u, u + 8) for u in range(8)]


def records(E, n):
    def present(u, v):
        return tuple(sorted((u, v))) in E
    for u, v in edges(n):
        root = int(present(u, v))
        states = []
        for k in range(n):
            if (1 << k) == u ^ v:
                continue
            state = int(present(u, u ^ (1 << k))) + 2 * int(present(v, v ^ (1 << k))) + 4 * int(present(u ^ (1 << k), v ^ (1 << k)))
            assert state < (7 if root else 8)
            states.append(state)
        yield root, states


def local_U(graph):
    assert 0 <= graph < 2**32
    E = {e for k, e in enumerate(Q4) if graph >> k & 1}
    U = [[[0] * d for _ in range(d)] for d in (8, 7)]
    for root, states in records(E, 4):
        for use_flip in (False, True):
            ss = [flip(s) if use_flip else s for s in states]
            for a in range(3):
                U[root][ss[a]][ss[a]] += 96
                for b in range(3):
                    if a != b:
                        U[root][ss[a]][ss[b]] += 288
    return U


def moment(weights):
    U = [[[0] * d for _ in range(d)] for d in (8, 7)]
    for graph, weight in weights:
        local = local_U(graph)
        for root, d in enumerate((8, 7)):
            for i in range(d):
                for j in range(d):
                    U[root][i][j] += weight * local[root][i][j]
    return U


def histograms(total, d):
    x = [0] * d
    def visit(i, rest):
        if i == d - 1:
            x[i] = rest
            yield x[:]
            return
        for count in range(rest + 1):
            x[i] = count
            yield from visit(i + 1, rest - count)
    yield from visit(0, total)


def poly(Q, x):
    return sum(a * Q[i][j] * b for i, a in enumerate(x) if a for j, b in enumerate(x) if b)


def main():
    frozen_file = SOURCE / 'FAMILY_OBSTRUCTION.json'
    frozen = json.loads(frozen_file.read_text())
    W = frozen['probability_denominator']
    U = moment(frozen['probability_numerators'])
    stored = json.loads((HERE / 'FROZEN_EDGE_MOMENTS.json').read_text())
    assert stored['point_sha256'] == hashlib.sha256(frozen_file.read_bytes()).hexdigest()
    for root in (0, 1):
        b = stored['blocks'][root]
        assert U[root] == b['twice_integer_matrix']
        support = b['support']
        assert all(U[root][i][j] == 0 for i in range(len(U[root])) for j in range(len(U[root])) if i not in support or j not in support)
        L = [[Fraction(v) for v in row] for row in b['PSD_LDL']['L']]
        D = [Fraction(v) for v in b['PSD_LDL']['D']]
        assert all(d > 0 for d in D)
        assert all(sum(L[i][k] * D[k] * L[j][k] for k in range(min(i, j) + 1)) == U[root][si][sj] for i, si in enumerate(support) for j, sj in enumerate(support))

    snapshot = json.loads((HERE / 'degree_snapshot.json').read_text())
    rational = [(g, Fraction(str(v))) for g, v in snapshot['lambda']]
    denominator = lcm(*(v.denominator for g, v in rational))
    sw = [(g, int(v * denominator)) for g, v in rational]
    S = sum(w for g, w in sw)
    su = moment(sw)
    snap_stored = json.loads((HERE / 'DEGREE_SNAPSHOT_EDGE_MOMENTS.json').read_text())
    assert all(su[r] == snap_stored['blocks'][r]['twice_integer_matrix'] for r in (0, 1))
    assert S == snap_stored['probability_denominator']

    checks, cuts = [], []
    for label, root, target, mass in (('frozen', 0, U, W), ('frozen', 1, U, W), ('degree_snapshot', 0, su, S)):
        file = HERE / f'{label}_root{root}.RESULT.json'
        result = json.loads(file.read_text())
        Q = result['kernel']
        d = 8 if root == 0 else 7
        assert len(Q) == d and all(len(row) == d for row in Q)
        assert all(Q[i][j] == Q[j][i] == Q[flip(i)][flip(j)] for i in range(d) for j in range(d))
        values = [poly(Q, x) for x in histograms(7, d)]
        assert len(values) == (3432 if root == 0 else 1716) and min(values) == result['minimum_all_generators'] == 0
        trace = sum(Q[i][j] * target[root][j][i] for i in range(d) for j in range(d))
        mean = Fraction(trace, 2 * 64512 * mass)
        assert trace == result['integer_pairing_with_U'] < 0 and str(mean) == result['pairing_actual_moment']
        small_minimum, witness = 0, None
        for total in range(7):
            for x in histograms(total, d):
                value = poly(Q, x)
                if value < small_minimum:
                    small_minimum, witness = value, x
        assert small_minimum < 0
        scale = max(abs(v) for row in Q for v in row)
        name = f'{label}_root{root}'
        cut = {'name': name, 'root_retained': root, 'dimension': d, 'state_order': f'Raw threebit codes0..{d-1}; endpointflip swapsbits0/1.', 'integer_kernel': Q, 'positive_normalization': scale, 'finite7_generators': len(values), 'minimum_all_integer7_histograms': min(values), 'non_PSD_non_copositive_witness': witness, 'negative_witness_total': sum(witness), 'negative_witness_quadratic': small_minimum, 'strict_target_pairing_raw': str(mean), 'target_pairing_normalized': str(mean / scale), 'target_scope': result['scope'], 'lift': 'Face kernel Σ V_e^T Qedge V_e /196, V_e(g)=6e_ext+e_base; finite7 pulls tofinite6, PSDedge isredundant.', 'input_result_sha256': hashlib.sha256(file.read_bytes()).hexdigest()}
        cuts.append(cut)
        checks.append({k: v for k, v in cut.items() if k != 'integer_kernel'})

    seed = json.loads((SOURCE / 'Q8_seed682_point.json').read_text())
    E = {tuple(map(int, line.split())) for line in Path(seed['source']).read_text().splitlines() if line.strip()}
    direct = [[[0] * d for _ in range(d)] for d in (8, 7)]
    roots = Counter()
    for root, states in records(E, 8):
        roots[root] += 1
        for action in (lambda s: s, flip):
            c = Counter(action(s) for s in states)
            for i in c:
                for j in c:
                    direct[root][i][j] += 1440 * c[i] * c[j]
    local = moment(seed['graph_distribution'])
    assert sum(roots.values()) == 1024 and roots[1] == 682 and local == direct
    output = {'status': 'PASS_EXACT_GEOMETRY_PSD_AND_FINITE7_CUTS', 'scope': 'Frozen edge moments and three validfinite7 kernels; degree target is onlyan eigen-cut intermediate snapshot. NoQ8 upperclaim.', 'frozen_PSD_ranks': [4, 4], 'finite7_checks': checks, 'direct_actual682_seed_regression': {'ambient_roots': 1024, 'local_Q4_restrictions': 1120, 'exact_outerproduct_equality': True}, 'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE / 'VERIFICATION.json').write_text(json.dumps(output, indent=2) + '\n')
    (HERE / 'EDGE_CUTS.json').write_text(json.dumps({'scope': 'Complete small-state finite7-valid kernel columns, nonnegativeweights only; endpointinvariant; PSDedge blocks themselves arepointwise redundant.', 'local_denominator': 64512, 'cuts': cuts}, indent=2) + '\n')
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
