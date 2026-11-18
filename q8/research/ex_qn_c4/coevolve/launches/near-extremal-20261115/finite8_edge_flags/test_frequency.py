"""Small complete integer-seven frequency cone tests, with exact certificates."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
os.environ.setdefault('OMP_NUM_THREADS', '1')
from pathlib import Path
import sys
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'finite8_flags/deps'))
from fractions import Fraction
from itertools import combinations_with_replacement
from collections import Counter
from math import lcm
import argparse
import hashlib
import json
import time
import numpy as np
from scipy import sparse
from scipy.optimize import linprog
import edge_flags


def solve_exact(A, b):
    """Exact solution of a full-column-rank overdetermined rational system."""
    rows = [[Fraction(v) for v in row] + [Fraction(rhs)] for row, rhs in zip(A, b)]
    n = len(A[0])
    rank = 0
    for column in range(n):
        pivot = next((i for i in range(rank, len(rows)) if rows[i][column]), None)
        assert pivot is not None, 'Active columns are dependent.'
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        d = rows[rank][column]
        rows[rank] = [v / d for v in rows[rank]]
        for i in range(len(rows)):
            if i != rank and rows[i][column]:
                a = rows[i][column]
                rows[i] = [x - a * y for x, y in zip(rows[i], rows[rank])]
        rank += 1
    assert all(not any(row[:n]) and row[n] == 0 for row in rows[n:])
    return [rows[i][n] for i in range(n)]


def histograms(d):
    result = []
    for multiset in combinations_with_replacement(range(d), 7):
        counts = Counter(multiset)
        result.append([counts.get(i, 0) for i in range(d)])
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', type=Path, default=HERE / 'FROZEN_EDGE_MOMENTS.json')
    ap.add_argument('--label', default='frozen')
    ap.add_argument('--root', type=int, choices=(0, 1), required=True)
    args = ap.parse_args()
    output = HERE / f'{args.label}_root{args.root}'
    assert not output.with_suffix('.started.json').exists()
    raw = args.input.read_bytes()
    data = json.loads(raw)
    U = data['blocks'][args.root]['twice_integer_matrix']
    d = len(U)
    xs = histograms(d)
    assert len(xs) == (3432 if d == 8 else 1716)
    pairs = [(i, j) for i in range(d) for j in range(i, d)]
    cols = np.asarray([[x[i] * x[j] for i, j in pairs] for x in xs], dtype=float).T
    A = sparse.csc_matrix(cols / 49.)
    S = sum(map(sum, U))
    b = np.array([U[i][j] / S for i, j in pairs])
    started = {'input': str(args.input), 'input_sha256': hashlib.sha256(raw).hexdigest(), 'root': args.root, 'dimension': d, 'complete_generators': len(xs), 'time_limit_per_LP': 10, 'scope': data['scope']}
    output.with_suffix('.started.json').write_text(json.dumps(started, indent=2) + '\n')
    begin = time.monotonic()
    res = linprog(np.zeros(len(xs)), A_eq=A, b_eq=b, bounds=(0, None), method='highs',
                  options={'time_limit': 10, 'primal_feasibility_tolerance': 1e-9, 'dual_feasibility_tolerance': 1e-9})
    result = {'numeric_status': int(res.status), 'message': res.message, 'primal_seconds': time.monotonic() - begin, 'scope': data['scope']}
    if res.success:
        active = np.where(res.x > 1e-12)[0].tolist()
        integers = [[xs[k][i] * xs[k][j] for k in active] for i, j in pairs]
        coefficients = solve_exact(integers, [U[i][j] for i, j in pairs])
        assert all(c >= 0 for c in coefficients)
        assert all(sum(c * xs[k][i] * xs[k][j] for c, k in zip(coefficients, active)) == U[i][j] for i in range(d) for j in range(d))
        result.update({'status': 'EXACT_NONNEGATIVE_DECOMPOSITION', 'active_generators': len(active), 'histograms': [xs[k] for k in active], 'coefficients_for_stored_U': [str(c) for c in coefficients], 'numeric_max_residual': float(np.max(np.abs(A @ res.x - b)))})
    elif res.status == 2:
        dual_begin = time.monotonic()
        dual = linprog(b, A_ub=-A.T, b_ub=np.zeros(len(xs)), bounds=[(-1, 1)] * len(pairs), method='highs',
                       options={'time_limit': 10, 'primal_feasibility_tolerance': 1e-9, 'dual_feasibility_tolerance': 1e-9})
        result.update({'dual_status': int(dual.status), 'dual_seconds': time.monotonic() - dual_begin})
        assert dual.success
        ys = [Fraction(v).limit_denominator(10**6) for v in dual.x]
        den = lcm(*(y.denominator for y in ys))
        Q = [[0] * d for _ in range(d)]
        for (i, j), y in zip(pairs, ys):
            Q[i][j] = Q[j][i] = int(y * den) * (2 if i == j else 1)
        repair = max([0] + [(-sum(x[i] * Q[i][j] * x[j] for i in range(d) for j in range(d)) + sum(v*v for v in x) - 1) // sum(v*v for v in x) for x in xs])
        for i in range(d):
            Q[i][i] += repair
        Q = [[Q[i][j] + Q[edge_flags.flip(i)][edge_flags.flip(j)] for j in range(d)] for i in range(d)]
        values = [sum(x[i] * Q[i][j] * x[j] for i in range(d) for j in range(d)) for x in xs]
        pairing = sum(Q[i][j] * U[j][i] for i in range(d) for j in range(d))
        assert min(values) >= 0 and pairing < 0
        result.update({'status': 'EXACT_FINITE7_SEPARATOR', 'kernel': Q, 'minimum_all_generators': min(values), 'minimizing_histogram': xs[values.index(min(values))], 'integer_pairing_with_U': pairing, 'pairing_actual_moment': str(Fraction(pairing, data['moment_denominator'])), 'rational_denominator': den, 'diagonal_repair': repair, 'endpoint_flip_invariant': True})
    else:
        result['status'] = 'UNKNOWN_BOUNDED_LP'
    output.with_suffix('.RESULT.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
