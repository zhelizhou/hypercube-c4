"""Reproduce the rational PSD primal point from the frozen restricted LP dual.

No optimizer is called. Use a fresh --output; original accepted point is frozen.
"""
from collections import Counter
from fractions import Fraction
from pathlib import Path
import argparse
import hashlib
import json
import finite_flags as ff

HERE = Path(__file__).resolve().parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    assert not args.output.exists(), 'Use a new output path.'
    candidate_file, seed_file = HERE / 'working_candidate.json', HERE / 'Q8_seed682_point.json'
    candidate, seed = json.loads(candidate_file.read_text()), json.loads(seed_file.read_text())
    q = dict(seed['graph_distribution'])
    counts = {g: int(round(w * 10**9)) for g, w in zip(candidate['pool_graphs'], candidate['dual_probabilities']) if w > 1e-14}
    N = sum(counts.values())
    assert N > 0 and set(counts) <= set(q)
    weights = {g: 9 * counts.get(g, 0) * 1120 + N * count for g, count in q.items()}
    W = sum(weights.values())
    assert W == 10 * N * 1120 and all(w > 0 for w in weights.values())
    coefficients, density = Counter(), 0
    for graph, weight in weights.items():
        rho, local = ff.local_coefficients(ff.q4_edges_from_mask(graph))
        density += weight * rho
        for key, value in local.items():
            coefficients[key] += weight * value
    blocks = ff.dense_blocks(coefficients)
    certificates = []
    for block in blocks:
        A = block['twice_integer_matrix']
        m = len(A)
        if not m:
            certificates.append({'block': block['block'], 'status': 'ZERO_PSD', 'support': []})
            continue
        L = [[Fraction(int(i == j)) for j in range(m)] for i in range(m)]
        D = []
        for j in range(m):
            pivot = Fraction(A[j][j]) - sum(L[j][k]**2 * D[k] for k in range(j))
            assert pivot > 0
            D.append(pivot)
            for i in range(j + 1, m):
                L[i][j] = (Fraction(A[i][j]) - sum(L[i][k] * D[k] * L[j][k] for k in range(j))) / pivot
        assert all(sum(L[i][k] * D[k] * L[j][k] for k in range(min(i, j) + 1)) == A[i][j] for i in range(m) for j in range(m))
        certificates.append({'block': block['block'], 'status': 'EXACT_POSITIVE_LDL', 'support': block['support'], 'L': [[str(x) for x in row] for row in L], 'D': [str(x) for x in D]})
    bound = Fraction(density, W * ff.DEN)
    assert bound > Fraction(683, 1024)
    output = {'status': 'STRICT_FINITE8_FAMILY_OBSTRUCTION_CANDIDATE', 'scope': 'Rational probability distribution on actual legal Q4 graphs; its finite8 six-block moments are exactly PSD. Not a Q8 graph and not an upper bound on ex(Q8,C4).', 'density_exact': str(bound), 'density_decimal': float(bound), 'target': str(Fraction(683, 1024)), 'gap_exact': str(bound - Fraction(683, 1024)), 'probability_denominator': W, 'probability_numerators': [[g, w] for g, w in sorted(weights.items())], 'coefficient_denominator': ff.DEN, 'blocks': blocks, 'LDL_certificates': certificates, 'construction': {'rounded_dual_denominator': N, 'rounded_dual_counts': [[g, v] for g, v in sorted(counts.items())], 'mixture': '9/10 rounded restricted dual +1/10 actual682 slice distribution', 'source_candidate_sha256': hashlib.sha256(candidate_file.read_bytes()).hexdigest(), 'source_seed_point_sha256': hashlib.sha256(seed_file.read_bytes()).hexdigest()}}
    args.output.write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps({'density': str(bound), 'support': len(weights), 'output': str(args.output)}))


if __name__ == '__main__':
    main()
