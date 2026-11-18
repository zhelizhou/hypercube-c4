"""Reconstruct a rational valid-row combination; no solver-status premise.

Writes only OUT.  The complete-Q4 maximum remains a separate obligation.
Every input multiplier is rounded to the explicit denominator, and every
scientific feature is rebuilt from integer data with its actual denominator.
"""
from pathlib import Path
from fractions import Fraction as F
from math import lcm
from collections import Counter
import argparse, hashlib, json, sys, time
sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(BASE/'finite8_flags/deps'), str(BASE/'finite8_flags'),
               str(BASE/'finite8_edge_flags')]
import numpy as np
from scipy import sparse
import finite_flags as ff
import lift


def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p, x): Path(p).write_text(json.dumps(x, separators=(',', ':'))+'\n')
def nearest(x): return (2*x.numerator+x.denominator)//(2*x.denominator)
def asint(a):
    a = np.asarray(a)
    b = a.astype(np.int64)
    assert np.array_equal(a, b), 'noninteger scientific numerator'
    return b


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('SCOPE', type=Path); ap.add_argument('OUT', type=Path)
    ap.add_argument('--multiplier-denominator', type=int, default=10**9)
    ap.add_argument('--query-denominator', type=int, default=10**9)
    args = ap.parse_args(); R = args.SCOPE.resolve(); O = args.OUT.resolve()
    O.mkdir(parents=True, exist_ok=True); assert not (O/'STARTED.json').exists()
    start = time.monotonic(); Dy = args.multiplier_denominator; T = args.query_denominator
    assert Dy > 0 and T > 0
    d = json.loads((R/'RESULT.json').read_text(), parse_float=F)
    assert d['status'] == 'NUMERIC_LIBRARY_DUAL_CANDIDATE'
    y = [nearest(v*Dy) for v in d['equality_duals']]
    z = [min(0, nearest(v*Dy)) for v in d['inequality_duals']]
    assert len(y) == 356 and len(z) == len(json.loads((R/'CUT_ROW_METADATA.json').read_text()))
    meta = json.loads((R/'CUT_ROW_METADATA.json').read_text())
    active = [(i, row, v) for i, (row, v) in enumerate(zip(meta, z)) if v]
    scales = [int(row.get('positive_power2_normalization', 1)) for _, row, _ in active]
    assert all(s > 0 and s & (s-1) == 0 for s in scales)
    maxscale = max(scales, default=1)
    D = Dy*lcm(maxscale*128*784, 8960, 8192, 784, 80, 98, 512, 7, 56, 70, 16)
    starts = [0]
    for dim in ff.DIMS: starts.append(starts[-1]+dim*(dim+1)//2)
    NW = np.zeros(starts[-1], dtype=object)
    profiles = json.loads((R/'PROFILE_SNAPSHOT.json').read_text())['remaining']
    A = len(profiles); EP = sparse.load_npz(R/'EDGE_ENDPOINT_DEDUP.npz')
    Nb = EP.shape[1]; NA = np.zeros(A, dtype=object); NB = np.zeros(Nb, dtype=object)
    source_hashes = {}
    def load(name):
        p = R/name; source_hashes[str(p)] = sha(p)
        return json.loads(p.read_text())
    def coef(n, den):
        assert D % den == 0, den
        return int(n)*(D//den)
    def addvec(dst, values, n, den):
        dst += asint(values).astype(object)*coef(n, den)
    def addsparse(dst, name, yi, den):
        M = sparse.load_npz(R/name).tocoo()
        for i, j, val in zip(M.row, M.col, M.data):
            assert int(val) == val
            dst[j] += int(val)*coef(yi[i], den)
    def addkernel(b, mat, n, den):
        mat = asint(mat); ii, jj = np.triu_indices(ff.DIMS[b])
        assert mat.shape == (ff.DIMS[b], ff.DIMS[b]) and np.array_equal(mat, mat.T)
        addvec(NW[starts[b]:starts[b+1]], mat[ii, jj], n, den)

    save(O/'STARTED.json', {'scope': str(R), 'source_result_sha256': sha(R/'RESULT.json'),
         'metadata_sha256': sha(R/'CUT_ROW_METADATA.json'), 'valid_multiplier_signs': True,
         'multiplier_denominator': Dy, 'working_common_denominator': str(D),
         'main682': 'OPEN', 'fullQ4_max_obligation': 'PENDING'})
    # a = y E + z A = y E + (-z) g, since A=-g and z<=0.
    for index, row, v in active:
        kind = row['kind']; b = row.get('block'); s = int(row.get('positive_power2_normalization', 1))
        if kind == 'PSD':
            q = asint(row['q']); ii, jj = np.triu_indices(ff.DIMS[b])
            addvec(NW[starts[b]:starts[b+1]], q[ii]*q[jj], -v, Dy*s)
        elif kind == 'INTEGER_ROUNDING':
            q = asint(row['q']); n = 28 if b == 5 else 6; t = int(row['t'])
            assert row.get('n', n) == n
            ii, jj = np.triu_indices(ff.DIMS[b])
            raw = n*n*q[ii]*q[jj]-(n//2)*(2*t+1)*(q[ii]+q[jj])+t*(t+1)
            addvec(NW[starts[b]:starts[b+1]], raw, -v, Dy*s)
        elif kind in ('FINITE6_KERNEL', 'FULL_FINITE6_PROJECTION_EXTRA'):
            c = load(row['source']); addkernel(b, c['full_Q'], -v, Dy*s)
        elif kind in ('CONDITIONAL_VERTEX', 'CONDITIONAL_VERTEX_EXTRA'):
            c = load(row.get('source', 'CONDITIONAL_VERTEX_CUT.json'))
            addkernel(5, c['integer_Q'], -v, Dy*s)
            bias = [sum(int(a)*int(n) for a, n in zip(c['degree_bias_raw'], p['degrees'])) for p in profiles]
            addvec(NA, bias, -v, Dy*128*784*s)
        elif kind in ('CONNECTOR_FINITE6', 'CONNECTOR_FINITE6_EXTRA'):
            c = load(row['source'])
            if kind == 'CONNECTOR_FINITE6': c = next(c for c in c['cuts'] if c['block'] == b)
            codes = asint(c['full_state_connector_codes'])
            small = asint(c.get('connector_Q', c.get('integer_connector_Q')))
            addkernel(b, small[np.ix_(codes, codes)], -v, Dy*s)
        elif kind == 'GLOBAL_MAXIMAL_LEAF':
            # In this model the raw counts are deliberately unnormalized.
            leaf = np.load(R/'LEAF_NEIGHBOR_FEATURES.npz')
            expected = [p['degrees'][8]-p['degrees'][1] for p in profiles]
            assert np.array_equal(expected, leaf['leaf_alpha_lower'])
            addvec(NA, expected, -v, Dy)
        elif kind == 'RETAINED_NEIGHBOR_DEGREE_CAPACITY':
            leaf = np.load(R/'LEAF_NEIGHBOR_FEATURES.npz'); t = row['degree']
            addvec(NA, leaf['neighbor_alpha_upper_numerator'][t], -v, Dy*512*16)
            addvec(NB, leaf['neighbor_beta_upper'][t], v, Dy*16)
        else: raise ValueError((index, kind))

    # Exact equality maps in the actual order used by all356 rows.
    marg = np.load(R/'MARGINAL_FEATURES.npz'); H = asint(marg['hist']); B = asint(marg['profile_hypergeom'])
    NH = np.array([coef(y[0]+yi, Dy*16)*64512 for yi in y[2:7]], dtype=object)
    NA += coef(y[1], Dy)
    for j in range(5): addvec(NA, B[:, j], -y[2+j], Dy*8960)
    Qedge = []; k = 7
    for n in (8, 7):
        Q = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                Q[i][j] = Q[j][i] = (2 if i == j else 1)*y[k]; k += 1
        Qedge.append(Q)
    assert k == 71
    lifted, den = lift.lift_to_faces(Qedge, already_averaged=False); assert den == 392
    for b, mat in enumerate(lifted): addkernel(b, mat, 1, Dy*784)
    addsparse(NB, 'EDGE_GENERATOR_DEDUP_NUMERATOR.npz', [-v for v in y[7:71]], Dy*98)
    addsparse(NA, 'EDGE_DEGREE_PROFILE_RHS_NUMERATOR.npz', [-v for v in y[71:89]], Dy*512)
    addsparse(NB, 'EDGE_ENDPOINT_DEDUP.npz', y[71:89], Dy)
    layout = load('EXTRA_EQUALITY_LAYOUT.json')
    assert layout['balance_start'] == 89 and layout['moment_start'] == 125
    addsparse(NB, layout['balance_matrix'], y[89:125], Dy*7)
    addsparse(NB, layout['moment_beta_matrix'], [-v for v in y[125:152]], Dy*56)
    selector = sparse.load_npz(R/layout['moment_selector_matrix']).tocoo()
    for i, j, val in zip(selector.row, selector.col, selector.data):
        assert int(val) == val
        NW[starts[5]+j] += int(val)*coef(7*y[125+i], Dy*2)
    e3 = load('EXTRA_EDGE3_LAYOUT.json'); assert e3['start_equality_index'] == 152
    addsparse(NW, e3['lift_packed'], y[152:356], Dy*80)
    addsparse(NB, e3['beta_hypergeom'], [-v for v in y[152:356]], Dy*70)

    # Exact nearest-integer query, plus a uniform bound on ALL local Q4 graphs.
    query = np.array([nearest(F(int(n)*T, D)) for n in NW], dtype=np.int64)
    qh = np.array([nearest(F(int(n)*T, D)) for n in NH], dtype=np.int64)
    errors = [abs(int(n)*T-int(q)*D) for n, q in zip(NW, query)]
    herr = max(abs(int(n)*T-int(q)*D) for n, q in zip(NH, qh))
    eps = F(max(errors[:starts[5]])+max(errors[starts[5]:]), D*T)+F(16*herr, 64512*D*T)
    assert eps <= F(1, T)+F(8, 64512*T)
    delta = F(y[0]+y[1], Dy); am = F(int(max(NA)), D); bm = F(int(max(NB)), D)
    coords = []
    for b, n in enumerate(ff.DIMS):
        ii, jj = np.triu_indices(n)
        coords.extend([b, int(i), int(j), int(v)] for i, j, v in zip(ii, jj, query[starts[b]:starts[b+1]]) if v)
    query_data = {'status': 'INTEGER_QUERY_FROM_EXACT_VALID_ROW_COMBINATION',
        'original_finite8_upper_coefficient_weights': coords,
        'histogram_weights_j0_to_j4': qh.tolist(), 'edge_weight': 0,
        'integerization_T': T, 'integer_score_positive_denominator': 64512*T,
        'uniform_error_bound': str(eps), 'exact_fullNO_claim': False}
    save(O/'LOCAL_PRICE_SCORE.json', query_data)
    with (O/'oracle_matrices.txt').open('w') as f:
        f.write('1 -1 64512\n')
        for b, n in enumerate(ff.DIMS):
            M = np.zeros((n, n), dtype=np.int64); ii, jj = np.triu_indices(n)
            M[ii, jj] = query[starts[b]:starts[b+1]]; M[jj, ii] = M[ii, jj]
            f.write(str(n)+'\n')
            for row in M: f.write(' '.join(map(str, row))+'\n')
    (O/'oracle_linear.txt').write_text('0 '+' '.join(map(str, qh))+'\n')
    save(O/'EXACT_COMBINATION.json', {'common_denominator': str(D),
        'multiplier_denominator': Dy, 'y': y, 'z': z,
        'packed_kernel_numerators': list(map(int, NW)), 'histogram_packed_numerators': list(map(int, NH)),
        'alpha_numerators': list(map(int, NA)), 'beta_numerators': list(map(int, NB))})
    # Compare exact rebuilt finite maps with the independently exported native maps.
    yl = np.array(y, dtype=float)/Dy; zl = np.array(z, dtype=float)/Dy
    al = json.loads((R/'DUAL_ACTIVE_LAYOUT.json').read_text())['active_rows']
    assert not any(z[i] for i in set(range(len(z)))-set(al))
    native = sparse.load_npz(R/'DUAL_ER.npz').T@yl+sparse.load_npz(R/'DUAL_ACTIVE_AR.npz').T@zl[al]
    rebuilt = np.array([float(F(int(n), D)) for n in list(NA)+list(NB)])
    rest_error = float(max(abs(native-rebuilt))); assert rest_error < 1e-10
    features = sparse.load_npz(R/'INTEGER_FEATURES.npz')
    exact_float = np.array([float(F(int(n), D)) for n in NW])
    rebuilt_lam = features@exact_float/64512+H@np.array([float(F(int(n), 64512*D)) for n in NH])
    native_lam = sparse.load_npz(R/'DUAL_EL.npz').T@yl+sparse.load_npz(R/'DUAL_ACTIVE_AL.npz').T@zl[al]
    lam_error = float(max(abs(native_lam-rebuilt_lam))); assert lam_error < 1e-10
    assert 129024*max(map(abs, map(int, query)))+16*max(map(abs, map(int, qh))) < 2**63
    scores = np.asarray(features@query+H@qh, dtype=np.int64)
    result = {'status': 'EXACT_ROW_RECONSTRUCTION_AND_UNIFORM_QUERY_BOUND_READY',
        'scope': str(R), 'source_result_sha256': sha(R/'RESULT.json'), 'metadata_sha256': sha(R/'CUT_ROW_METADATA.json'),
        'multiplier_denominator': Dy, 'query_denominator': T, 'common_denominator': str(D),
        'valid_inequality_weight_signs': True, 'active_exact_inequalities': len(active),
        'active_kinds': dict(Counter(row['kind'] for _, row, _ in active)),
        'delta_exact': str(delta), 'alpha_max_exact': str(am), 'alpha_argmax': int(np.argmax(NA)),
        'beta_max_exact': str(bm), 'beta_argmax': int(np.argmax(NB)),
        'uniform_error_exact': str(eps), 'uniform_error_float': float(eps),
        'max_allowed_complete_query_value': str(delta-am-bm-eps),
        'library_size': len(scores), 'library_integer_score_minmax': [int(min(scores)), int(max(scores))],
        'native_rest_map_comparison_max': rest_error, 'native_lambda_map_comparison_max': lam_error,
        'parameter_source_hashes': source_hashes, 'solver_status_is_not_premise': True,
        'full_Q4_maximum': 'PENDING', 'semantic_whole_certificate_review': 'PENDING',
        'main682': 'OPEN', 'seconds': time.monotonic()-start}
    # Scientific inputs and comparison-only exports are both bound explicitly.
    # A fresh whole-certificate review must distinguish these roles.
    for name in ['RESULT.json', 'CUT_ROW_METADATA.json', 'PROFILE_SNAPSHOT.json',
                 'MARGINAL_FEATURES.npz', 'LEAF_NEIGHBOR_FEATURES.npz',
                 'EDGE_ENDPOINT_DEDUP.npz', 'EDGE_GENERATOR_DEDUP_NUMERATOR.npz',
                 'EDGE_DEGREE_PROFILE_RHS_NUMERATOR.npz', 'INTEGER_FEATURES.npz',
                 'DUAL_ER.npz', 'DUAL_EL.npz', 'DUAL_ACTIVE_AR.npz',
                 'DUAL_ACTIVE_AL.npz', 'DUAL_ACTIVE_LAYOUT.json',
                 layout['balance_matrix'], layout['moment_beta_matrix'],
                 layout['moment_selector_matrix'], e3['lift_packed'],
                 e3['beta_hypergeom']]:
        source_hashes[str(R/name)] = sha(R/name)
    for p in [Path(__file__), BASE/'finite8_flags/finite_flags.py',
              BASE/'finite8_edge_flags/lift.py', BASE/'finite8_edge_flags/edge_flags.py']:
        source_hashes[str(p)] = sha(p)
    save(O/'RESULT.json', result)
    print(json.dumps({k: v for k, v in result.items() if k != 'parameter_source_hashes'}), flush=True)


if __name__ == '__main__': main()
