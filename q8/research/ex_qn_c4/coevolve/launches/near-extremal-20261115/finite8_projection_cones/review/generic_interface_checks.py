"""No-LP boundary tests of the actual generic loader and consumer scorer."""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
from fractions import Fraction
import json
import subprocess
import importlib.util
from collections import Counter
import independent_replay as independent

HERE = Path(__file__).resolve().parent
PKG = HERE.parent
sys.path.insert(0, str(PKG))
import price_projection_point as producer
score_spec = importlib.util.spec_from_file_location('review_projection_score', PKG / 'score.py')
score = importlib.util.module_from_spec(score_spec)
score_spec.loader.exec_module(score)
import finite_flags as native

def save(name, obj):
    path = HERE / name
    path.write_text(json.dumps(obj, indent=2) + '\n')
    return path

def main():
    dims = independent.DIMS
    cases = []
    for L in (1, 3, 16):
        maps = [[i % L for i in range(d)] for d in dims]
        path = save(f'VALID_MAP_L{L}.json', {'labels': L, 'full_state_to_label': maps})
        assert producer.mappings('json', path) == (L, maps)
        cases.append({'case': f'valid L={L}', 'accepted': True})
    maps = [[i % 3 for i in range(d)] for d in dims]
    invalid = [
        ('L0', {'labels': 0, 'full_state_to_label': maps}),
        ('L17', {'labels': 17, 'full_state_to_label': maps}),
        ('floatL', {'labels': 3.0, 'full_state_to_label': maps}),
        ('booleanL', {'labels': True, 'full_state_to_label': maps}),
        ('missing_block', {'labels': 3, 'full_state_to_label': maps[:4]}),
        ('extra_block', {'labels': 3, 'full_state_to_label': maps + [maps[0]]}),
        ('missing_state', {'labels': 3, 'full_state_to_label': [maps[0][:-1]] + maps[1:]}),
    ]
    for name, value in [('negative', -1), ('out_of_range', 3), ('boolean', True), ('float', 1.0)]:
        badmaps = [m.copy() for m in maps]
        badmaps[0][0] = value
        invalid.append((name, {'labels': 3, 'full_state_to_label': badmaps}))
    for name, obj in invalid:
        path = save(f'INVALID_MAP_{name}.json', obj)
        rejected = False
        try:
            producer.mappings('json', path)
        except AssertionError:
            rejected = True
        assert rejected, name
        cases.append({'case': name, 'rejected': True})
    assert producer.mappings('parallel15') == (15, [[f >> 4 for f in c] for c in independent.CODES])
    assert producer.mappings('connector16') == (16, [[f & 15 for f in c] for c in independent.CODES])
    help_result = subprocess.run([sys.executable, '-B', str(PKG / 'price_projection_point.py'), '--help'], capture_output=True, text=True)
    assert help_result.returncode == 0 and '--mapping-json' in help_result.stdout
    (HERE / 'GENERIC_CLI_HELP.txt').write_text(help_result.stdout)

    q = [0, 1, 0]
    small = [[36 * q[i] * q[j] - 15 * (q[i] + q[j]) + 6 for j in range(3)] for i in range(3)]
    K = [independent.lift(small, maps[b], b) for b in range(5)]
    # Kernel artifacts are synthetic review fixtures, not claimed discoveries.
    paths = []
    for b, full in enumerate(K):
        scale = max(1, max(abs(v) for row in full for v in row))
        path = save(f'GENERIC_REVIEW_FIXTURE_BLOCK{b}.json', {'block': b, 'full_Q': full, 'positive_normalization': scale, 'scope': 'Synthetic non-equivariant review fixture only'})
        blocks, got_scale = score.full_face_kernel(path)
        assert got_scale == scale and blocks[b] == full
        assert all(not any(any(row) for row in matrix) for bb, matrix in enumerate(blocks) if bb != b)
        paths.append((path, scale))
    point = independent.read(independent.DATA / 'INPUT_POINT.json')
    weights = point['lambda']
    den = independent.lcm(*(w.denominator for _, w in weights))
    U = [[[0] * 3 for _ in range(3)] for _ in range(5)]
    nativeU = [[[0] * 3 for _ in range(3)] for _ in range(5)]
    pairs = [Fraction() for _ in range(5)]
    collision_cases = 0
    for mask, weight in weights:
        n = int(weight * den)
        direct_local = independent.local_integer(mask, K)
        _, coeff = native.local_coefficients(native.q4_edges_from_mask(mask))
        for b, (path, scale) in enumerate(paths):
            assert Fraction(direct_local[b], 288 * scale) == score.value_on_graph(mask, path)
            pairs[b] += weight * Fraction(direct_local[b], 288)
        # Native folded full-state coefficients projected after the FULL action.
        for (b, i, j), v in coeff.items():
            if b >= 5:
                continue
            a, z = maps[b][i], maps[b][j]
            nativeU[b][a][z] += n * v
            nativeU[b][z][a] += n * v
            collision_cases += i != j and a == z
        # Independent ordered reconstruction before projection.
        for b, (s, t) in independent.flags_of_mask(mask):
            for p in independent.PERMS[b]:
                a, z = maps[b][p[s]], maps[b][p[t]]
                h = len(independent.PERMS[b])
                U[b][a][z] += n * (2240 // h)
                U[b][z][a] += n * (2240 // h)
                U[b][a][a] += n * (448 // h)
                U[b][z][z] += n * (448 // h)
    assert U == nativeU
    for b in range(5):
        via_projected = Fraction(len(independent.PERMS[b]) * sum(small[i][j] * U[b][j][i] for i in range(3) for j in range(3)), 129024 * den)
        assert via_projected == pairs[b]
    assert collision_cases > 0
    result = {'status': 'PASS_ACTUAL_GENERIC_LOADER_AND_FULL_KERNEL_CONSUMER',
              'mapping_cases': cases, 'no_lp_run': True,
              'actual_graphs_per_block': len(weights), 'blocks': 5,
              'entrywise_generic_ordered_moments_equal_native_projection': True,
              'distinct_state_same_label_collisions': collision_cases,
              'raw_generic_pairings': list(map(str, pairs)),
              'future_column_scorer_checks': 'Every graph gets literal full-kernel value and native exact scorer value, for all five generic full kernels; arbitrary new legal Q4 columns use the identical stateless formula.',
              'whole682': 'OPEN'}
    save('GENERIC_INTERFACE_RESULTS.json', result)
    print(json.dumps({'status': result['status'], 'mapping_cases': len(cases), 'actual_graphs_per_block': len(weights), 'blocks': 5}))

if __name__ == '__main__':
    main()
