"""Independent exact connector geometry, PSD eligibility and complete cuts.

No producer, frozen state module, optimizer or scientific package is imported.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations
from math import lcm
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
QE = ((0, 1), (0, 2), (1, 3), (2, 3))
ROOTS = (0, 1, 3, 6, 7)


def edge(u, v):
    return tuple(sorted((u, v)))


def transformations():
    out = []
    for swap in (False, True):
        for translation in range(4):
            vm = [translation ^ (((v & 1) * 2 + (v >> 1)) if swap else v) for v in range(4)]
            ep = [QE.index(edge(vm[u], vm[v])) for u, v in QE]
            roots = [sum(1 << ep[k] for k in range(4) if r >> k & 1) for r in range(16)]
            connectors = [sum(1 << vm[k] for k in range(4) if c >> k & 1) for c in range(16)]
            flags = [connectors[f & 15] + sum(1 << (4 + ep[k]) for k in range(4) if f >> (4 + k) & 1) for f in range(256)]
            out.append((roots, connectors, flags))
    return out


SYMS = transformations()
BOTTOM = [(u, u ^ (1 << k)) for u in range(8) for k in range(3) if not u >> k & 1]
Q4 = BOTTOM + [(u + 8, v + 8) for u, v in BOTTOM] + [(u, u + 8) for u in range(8)]


def local_projection_U(graph):
    assert 0 <= graph < 2**32
    E = {e for k, e in enumerate(Q4) if graph >> k & 1}
    U = [[[0] * 16 for _ in range(16)] for _ in ROOTS]
    for i, j in combinations(range(4), 2):
        for base in range(16):
            if base & ((1 << i) | (1 << j)):
                continue
            vs = [base, base ^ (1 << i), base ^ (1 << j), base ^ (1 << i) ^ (1 << j)]
            root = sum(1 << k for k, (a, b) in enumerate(QE) if edge(vs[a], vs[b]) in E)
            assert root != 15
            canonical = min(r[root] for r, c, f in SYMS)
            block = ROOTS.index(canonical)
            connector_codes = []
            for outside in range(4):
                if outside in (i, j):
                    continue
                connector_codes.append(sum(1 << a for a in range(4) if edge(vs[a], vs[a] ^ (1 << outside)) in E))
            maps = [c for r, c, f in SYMS if r[root] == canonical]
            for action in maps:
                s, t = [action[c] for c in connector_codes]
                U[block][s][t] += 2240 // len(maps)
                U[block][t][s] += 2240 // len(maps)
                U[block][s][s] += 448 // len(maps)
                U[block][t][t] += 448 // len(maps)
    return U


def histograms(total, d=16):
    values = [0] * d
    def visit(i, remaining):
        if i == d - 1:
            values[i] = remaining
            yield values[:]
            return
        for v in range(remaining + 1):
            values[i] = v
            yield from visit(i + 1, remaining - v)
    yield from visit(0, total)


def poly(Q, x):
    return sum(a * Q[i][j] * b for i, a in enumerate(x) if a for j, b in enumerate(x) if b)


def main():
    input_raw = (HERE / 'INPUT_POINT.json').read_bytes()
    input_point = json.loads(input_raw)
    target = json.loads((HERE / 'PROJECTED_MOMENTS.json').read_text())
    assert hashlib.sha256(input_raw).hexdigest() == target['point_sha256'] == '223b58046502fdd7eae1847fc6fc9ab3f27dfbeca9c1f1647b14f06a54d28aa9'
    weights = [(g, Fraction(str(v))) for g, v in input_point['lambda']]
    D = lcm(*(v.denominator for g, v in weights))
    integer_weights = [(g, int(v * D)) for g, v in weights]
    assert len(integer_weights) == 202
    matrices = [[[0] * 16 for _ in range(16)] for _ in ROOTS]
    for graph, weight in integer_weights:
        local = local_projection_U(graph)
        for b in range(5):
            for i in range(16):
                for j in range(16):
                    matrices[b][i][j] += weight * local[b][i][j]
    assert 2 * 64512 * D == target['moment_denominator']
    assert all(U == target['blocks'][b]['twice_integer_matrix'] for b, U in enumerate(matrices))
    eligibility = json.loads((HERE / 'PSD_ELIGIBILITY.json').read_text())
    for b, record in enumerate(eligibility['blocks']):
        U = matrices[b]
        if b in (0, 4):
            L = [[Fraction(x) for x in row] for row in record['L']]
            diagonal = [Fraction(x) for x in record['D']]
            assert all(x > 0 for x in diagonal)
            assert all(sum(L[i][k] * diagonal[k] * L[j][k] for k in range(min(i, j) + 1)) == U[i][j] for i in range(16) for j in range(16))
        else:
            v = record['integer_direction']
            assert poly(U, v) == record['integer_quadratic'] < 0

    checks, cuts = [], []
    for b in (0, 4):
        file = HERE / f'block{b}.EXACT_SEPARATOR.json'
        certificate = json.loads(file.read_text())
        Q, U = certificate['connector_Q'], matrices[b]
        assert all(Q[i][j] == Q[j][i] for i in range(16) for j in range(16))
        values = [poly(Q, x) for x in histograms(6)]
        assert len(values) == 54264 and min(values) == certificate['finite6']['minimum'] >= 0
        assert sum(v == 0 for v in values) == certificate['finite6']['zeros']
        witness = certificate['small_histograms']['negative_witness']
        assert witness and sum(witness) < 6 and poly(Q, witness) == certificate['small_histograms']['minimum_total_le5'] < 0
        root = ROOTS[b]
        actions = [c for r, c, f in SYMS if r[root] == root]
        assert all(Q[p[i]][p[j]] == Q[i][j] and U[p[i]][p[j]] == U[i][j] for p in actions for i in range(16) for j in range(16))
        states = [code for code in range(240) if not any(root >> k & 1 and code >> (4 + k) & 1 and code >> u & 1 and code >> v & 1 for k, (u, v) in enumerate(QE))]
        projection = [code & 15 for code in states]
        assert len(states) == certificate['full_state_dimension'] == (240 if b == 0 else 170)
        assert projection == certificate['full_state_connector_codes'] and set(projection) == set(range(16))
        full = certificate['full_Q']
        assert all(full[i][j] == Q[projection[i]][projection[j]] for i in range(len(states)) for j in range(len(states)))
        trace = sum(Q[i][j] * U[j][i] for i in range(16) for j in range(16))
        mean = Fraction(trace, 2 * 64512 * D)
        assert trace == certificate['point_pairing']['integer_trace_Q_U'] < 0
        assert str(mean) == certificate['point_pairing']['exact_mean_feature']
        scale = certificate['positive_normalization']
        cuts.append({'name': f'connector_block{b}', 'block': b, 'canonical_root_mask': root, 'connector_order': list(range(16)), 'integer_connector_Q': Q, 'full_state_connector_codes': projection, 'full_state_dimension': len(states), 'positive_normalization': scale, 'normalized_exact_target_feature': str(mean / scale), 'finite6_minimum': min(values), 'histograms': len(values), 'root_connector_actions': actions, 'non_PSD_non_copositive_witness': witness, 'witness_quadratic': poly(Q, witness), 'point_sha256': target['point_sha256'], 'scope': 'Allfullstates byconnector aggregation, nooutside repair. Inputpoint isnot anacceptedfeasiblepoint orgraph.', 'certificate_sha256': hashlib.sha256(file.read_bytes()).hexdigest()})
        checks.append({'block': b, 'projected_moment_exact_PSD': True, 'complete_histograms': len(values), 'minimum': min(values), 'full_states_covered': len(states), 'all16_connector_labels_covered': True, 'negative_witness_total': sum(witness), 'exact_target_feature_raw': str(mean), 'normalization': scale})
    output = {'status': 'PASS_EXACT_CONNECTOR_GEOMETRY_PSD_AND_FINITE6_CUTS', 'same_input_point_sha256': target['point_sha256'], 'actual_graph_weights': len(weights), 'lambda_mass_preserved_exact': str(sum(v for g, v in weights)), 'five_projected_matrices_independently_recomputed': True, 'PSD_eligible_blocks': [0, 4], 'old_PSD_violations_only_blocks': [1, 2, 3], 'checks': checks, 'scope': 'Two validprojectedfrequency kernels cutthe samefrozenpoint. No682claim; inputnotacceptedfeasiblepoint/graph.', 'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE / 'VERIFICATION.json').write_text(json.dumps(output, indent=2) + '\n')
    (HERE / 'CONNECTOR_CUTS.json').write_text(json.dumps({'scope': output['scope'], 'local_denominator': 64512, 'cuts': cuts}, indent=2) + '\n')
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
