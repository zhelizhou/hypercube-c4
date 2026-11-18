"""Bounded complete generic16 connector-histogram cone probe."""
from pathlib import Path
import sys
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'finite8_flags/deps'))
import argparse
import hashlib
import json
import time
import numpy as np
from scipy import sparse
from scipy.optimize import linprog


def load_domain():
    source = HERE.parent / 'finite8_frequency_cone'
    matrix_file, histogram_file = source / 'generator_matrix.npz', source / 'histograms16_sum6.npy'
    A = sparse.load_npz(matrix_file).tocsc()
    X = np.load(histogram_file)
    pairs = [(i, j) for i in range(16) for j in range(i, 16)]
    assert A.shape == (136, 54264) and X.shape == (54264, 16)
    assert np.all(X >= 0) and np.all(X.sum(axis=1) == 6)
    assert len({tuple(row) for row in X.tolist()}) == 54264
    coo = A.tocoo()
    numerators = np.rint(coo.data * 36).astype(int)
    left = np.asarray([i for i, j in pairs])[coo.row]
    right = np.asarray([j for i, j in pairs])[coo.row]
    assert np.allclose(coo.data * 36, numerators, atol=1e-12, rtol=0)
    assert np.all(numerators == X[coo.col, left] * X[coo.col, right])
    support = np.count_nonzero(X, axis=1)
    assert np.all(A.getnnz(axis=0) == support * (support + 1) // 2)
    return A, X, pairs, {'source_matrix_sha256': hashlib.sha256(matrix_file.read_bytes()).hexdigest(), 'source_histogram_sha256': hashlib.sha256(histogram_file.read_bytes()).hexdigest(), 'generic_label_order': list(range(16)), 'coverage': 'All54264 unique nonnegative16-label sum6 vectors; each normalized column=xxT/36. OldsupportstateIDs are not used.'}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--block', required=True, type=int, choices=(0, 4))
    args = ap.parse_args()
    prefix = HERE / f'block{args.block}'
    assert not prefix.with_suffix('.started.json').exists(), 'Probe already exists; no repetition.'
    raw = (HERE / 'PROJECTED_MOMENTS.json').read_bytes()
    projected = json.loads(raw)
    eligible = json.loads((HERE / 'PSD_ELIGIBILITY.json').read_text())
    assert eligible['blocks'][args.block]['status'] == 'EXACT_POSITIVE_LDL'
    U = projected['blocks'][args.block]['twice_integer_matrix']
    A, X, pairs, domain = load_domain()
    mass = sum(map(sum, U))
    b = np.array([U[i][j] / mass for i, j in pairs])
    started = {'block': args.block, 'point_sha256': projected['point_sha256'], 'projection_input_sha256': hashlib.sha256(raw).hexdigest(), 'domain': domain, 'input_matrix': U, 'ordered_mass': mass, 'per_LP_time_limit_seconds': 12, 'eligible_exact_PSD': True, 'scope': 'All16 actualconnectorcodes onallfullstates; noold16supportrestriction. Samefrozen202lambda, notanacceptedgraph/feasiblepoint.'}
    prefix.with_suffix('.started.json').write_text(json.dumps(started, indent=2) + '\n')
    begin = time.monotonic()
    res = linprog(np.zeros(54264), A_eq=A, b_eq=b, bounds=(0, None), method='highs',
                  options={'time_limit': 12, 'primal_feasibility_tolerance': 1e-9, 'dual_feasibility_tolerance': 1e-9})
    result = {'primal_status': int(res.status), 'message': res.message, 'primal_seconds': time.monotonic() - begin, 'exact_status': 'NOT_YET_CERTIFIED'}
    if res.success:
        active = np.where(res.x > 1e-12)[0]
        prefix.with_suffix('.numeric_decomposition.json').write_text(json.dumps({'block': args.block, 'active_histograms': X[active].astype(int).tolist(), 'active_indices': active.tolist(), 'normalized_coefficients': res.x[active].tolist(), 'unscaled_coefficients_for_U': (res.x[active] * mass / 36).tolist(), 'maximum_normalized_residual': float(np.max(np.abs(A @ res.x - b))), 'scope': started['scope']}, indent=2) + '\n')
        result.update({'status': 'NUMERIC_FEASIBLE_EXACT_REPAIR_PENDING', 'active_generators': len(active), 'maximum_residual': float(np.max(np.abs(A @ res.x - b)))})
    elif res.status == 2:
        dual_begin = time.monotonic()
        dual = linprog(b, A_ub=-A.T, b_ub=np.zeros(54264), bounds=[(-1, 1)] * 136, method='highs',
                       options={'time_limit': 12, 'primal_feasibility_tolerance': 1e-9, 'dual_feasibility_tolerance': 1e-9})
        result.update({'status': 'NUMERIC_INFEASIBLE_EXACT_DUAL_PENDING', 'dual_status': int(dual.status), 'dual_seconds': time.monotonic() - dual_begin})
        if dual.success:
            prefix.with_suffix('.numeric_dual.json').write_text(json.dumps({'block': args.block, 'packed_pairs': pairs, 'y': dual.x.tolist(), 'objective': float(dual.fun), 'minimum_generator_value': float(np.min(A.T @ dual.x)), 'scope': started['scope']}, indent=2) + '\n')
            result.update({'dual_objective': float(dual.fun), 'minimum_generator_value': float(np.min(A.T @ dual.x))})
    else:
        result['status'] = 'UNKNOWN_BOUNDED_LP'
    prefix.with_suffix('.RESULT.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
