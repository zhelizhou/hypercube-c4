"""Bounded finite8 rank-one column generation on actual common-Q4 slices.

This is restricted-pool optimization, never a full-domain upper certificate.
All1120 slices of the actual682 Q8 seed and both280-slice Q7 points are present.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
os.environ.setdefault('OMP_NUM_THREADS', '1')
from pathlib import Path
import sys
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'deps'))
import argparse
import hashlib
import json
import time
import numpy as np
from scipy import sparse
from scipy.optimize import linprog
import finite_flags as ff


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--rounds', type=int, default=35)
    ap.add_argument('--seconds', type=float, default=45)
    args = ap.parse_args()
    assert not (HERE / 'working_lp.started.json').exists(), 'A bounded run exists; do not silently repeat.'
    points = [json.loads((HERE / name).read_text()) for name in ('Q7_A_point.json', 'Q7_B_point.json', 'Q8_seed682_point.json')]
    graphs = sorted({g for point in points for g, _ in point['graph_distribution']})
    starts = np.cumsum([0] + [d * (d + 1) // 2 for d in ff.DIMS])
    packed = [{(i, j): int(starts[b]) + i * d - i * (i - 1) // 2 + j - i for i in range(d) for j in range(i, d)} for b, d in enumerate(ff.DIMS)]
    coeff_rows, coeff_cols, coeff_vals = [], [], []
    rho = []
    for row, graph in enumerate(graphs):
        r, coefficients = ff.local_coefficients(ff.q4_edges_from_mask(graph))
        rho.append(r / ff.DEN)
        for (b, i, j), value in coefficients.items():
            coeff_rows.append(row)
            coeff_cols.append(packed[b][i, j])
            coeff_vals.append(value / ff.DEN)
    F = sparse.csr_matrix((coeff_vals, (coeff_rows, coeff_cols)), shape=(len(graphs), int(starts[-1])))
    rho = np.array(rho)
    sparse.save_npz(HERE / 'working_features.npz', F)
    np.save(HERE / 'working_density.npy', rho)
    (HERE / 'working_graphs.json').write_text(json.dumps(graphs) + '\n')
    supports = []
    for b, d in enumerate(ff.DIMS):
        support = sorted({i for point in points for i in point['blocks'][b]['support']})
        supports.append(support)

    def matrix_from_packed(packed_vector, block):
        support = supports[block]
        return np.array([[packed_vector[packed[block][min(i, j), max(i, j)]] * (1 if i == j else .5) for j in support] for i in support])

    rays, ray_signatures, columns = [], set(), []

    def add_ray(b, vector, metadata):
        vector = np.asarray(vector, dtype=float)
        vector /= np.linalg.norm(vector)
        if vector[np.argmax(np.abs(vector))] < 0:
            vector = -vector
        signature = (b, tuple(np.round(vector, 10)))
        if signature in ray_signatures:
            return False
        ray_signatures.add(signature)
        dense = np.zeros(ff.DIMS[b])
        dense[supports[b]] = vector
        coordinates = np.zeros(int(starts[-1]))
        for i in supports[b]:
            for j in supports[b]:
                if i <= j:
                    coordinates[packed[b][i, j]] = dense[i] * dense[j]
        columns.append(np.asarray(F @ coordinates))
        rays.append({'block': b, 'support': supports[b], 'vector': vector.tolist(), 'origin': metadata})
        return True

    # Actual negative directions of the two high-density nonfeasible Q7 points.
    for name, point in zip(('Q7_A', 'Q7_B'), points[:2]):
        for b, block in enumerate(point['blocks']):
            old_support = block['support']
            if not old_support:
                continue
            M = np.array(block['twice_integer_matrix'], dtype=float)
            eigenvalues, vectors = np.linalg.eigh(M)
            for k in np.where(eigenvalues < -1e-7)[0]:
                v = np.zeros(len(supports[b]))
                lookup = {x: i for i, x in enumerate(supports[b])}
                for i, state in enumerate(old_support):
                    v[lookup[state]] = vectors[i, k]
                add_ray(b, v, {'point': name, 'eigenvalue_of_twice_integer_matrix': float(eigenvalues[k])})
    initial_rays = len(rays)
    start = time.monotonic()
    started = {'scope': 'Finite8 six-block candidate restricted to the actual common-Q4 working pool, not full-domain acceptance', 'round_limit': args.rounds, 'wall_limit_seconds': args.seconds, 'pool_graphs': len(graphs), 'source_slices': [point['restrictions'] for point in points], 'feature_nnz': F.nnz, 'dimensions': ff.DIMS, 'packed_starts': starts.tolist(), 'block_supports': supports, 'initial_rays': initial_rays, 'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE / 'working_lp.started.json').write_text(json.dumps(started, indent=2) + '\n')
    history = []
    best, best_record = float('inf'), None
    for iteration in range(args.rounds):
        if time.monotonic() - start > args.seconds:
            break
        A = np.column_stack([-np.ones(len(graphs))] + columns)
        result = linprog(np.r_[1., np.zeros(len(rays))], A_ub=A, b_ub=-rho,
                         bounds=[(0, 1)] + [(0, None)] * len(rays), method='highs',
                         options={'dual_feasibility_tolerance': 1e-9, 'primal_feasibility_tolerance': 1e-9})
        if not result.success:
            history.append({'iteration': iteration, 'lp_status': result.status, 'message': result.message})
            break
        weights = np.maximum(result.x[1:], 0)
        values = rho + np.column_stack(columns) @ weights
        current = float(np.max(values))
        assert current + 1e-7 >= 682 / 1024, 'The actual682 mean floor was violated; normalization or LP bug.'
        dual = -np.array(result.ineqlin.marginals)
        moment = np.asarray(F.T @ dual)
        spectra, to_add = [], []
        for b in range(6):
            M = matrix_from_packed(moment, b)
            if not len(M):
                spectra.append(0.)
                continue
            eigenvalues, vectors = np.linalg.eigh(M)
            spectra.append(float(min(0., eigenvalues[0])))
            for k in np.where(eigenvalues < -1e-8)[0][:3]:
                to_add.append((b, vectors[:, k], {'pricing_iteration': iteration, 'eigenvalue': float(eigenvalues[k])}))
        row = {'iteration': iteration, 'restricted_lp_objective': float(result.fun), 'restricted_recomputed_max': current, 'true_Q8_682_floor': 682 / 1024, 'target683_threshold': 683 / 1024, 'dual_density': float(dual @ rho), 'dual_mass': float(dual.sum()), 'dual_block_min_eigenvalues': spectra, 'rays': len(rays), 'positive_weights': int(np.sum(weights > 1e-10)), 'elapsed_seconds': time.monotonic() - start}
        if current < best:
            best = current
            best_record = {'scope': started['scope'], 'finite_model': 'finite8_fullface_vertex_overlap_v1', 'dimensions': ff.DIMS, 'face_root_masks': ff.ROOT_MASKS, 'coefficient_denominator': ff.DEN, 'state_order': 'Original verify_local.cpp ascending legal face flags and vertex canonical reps', 'vertex_reps': ff.VERTEX_REPS, 'pool_graphs': graphs, 'iteration': iteration, 'restricted_upper': best, 'rays': rays.copy(), 'nonnegative_weights': weights.tolist(), 'dual_probabilities': dual.tolist(), 'dual_density': float(dual @ rho), 'dual_block_min_eigenvalues': spectra, 'maximizing_working_graph': graphs[int(np.argmax(values))], 'global_acceptance': False}
            (HERE / 'working_candidate.json').write_text(json.dumps(best_record, indent=2) + '\n')
        added = sum(add_ray(b, v, origin) for b, v, origin in to_add)
        row['rays_added'] = added
        history.append(row)
        (HERE / 'working_lp.history.json').write_text(json.dumps(history, indent=2) + '\n')
        print(json.dumps(row), flush=True)
        if not added:
            break
    summary = {'status': 'RESTRICTED_CANDIDATE_ONLY', 'scope': started['scope'], 'iterations': len(history), 'restricted_best': best, 'primary683_goal': 'OPEN', 'full_domain_separation_done': False, 'integer_gram_acceptance_done': False, 'elapsed_seconds': time.monotonic() - start}
    (HERE / 'working_lp.RESULT.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary), flush=True)


if __name__ == '__main__':
    main()
