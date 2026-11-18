"""Exact complete16-label connector kernel and fullstate pullback."""
from pathlib import Path
from fractions import Fraction
from collections import Counter
from itertools import combinations_with_replacement
from math import lcm
import argparse
import hashlib
import json
import sys
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'finite8_flags'
sys.path.insert(0, str(SOURCE))
import finite_flags as f


def histograms(total):
    for multiset in combinations_with_replacement(range(16), total):
        c = Counter(multiset)
        yield [c.get(i, 0) for i in range(16)]


def poly(Q, x):
    return sum(a * Q[i][j] * b for i, a in enumerate(x) if a for j, b in enumerate(x) if b)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--block', required=True, type=int, choices=(0, 4))
    block = ap.parse_args().block
    dual_file = HERE / f'block{block}.numeric_dual.json'
    dual = json.loads(dual_file.read_text())
    point_file = HERE / 'PROJECTED_MOMENTS.json'
    projected = json.loads(point_file.read_text())
    U = projected['blocks'][block]['twice_integer_matrix']
    rationals = [Fraction(value).limit_denominator(10**6) for value in dual['y']]
    common = lcm(*(x.denominator for x in rationals))
    method = 'rational_recovery'
    if common > 10**12:
        common, method = 10**6, 'fixed_integer_rounding'
        integers = [int(round(value * common)) for value in dual['y']]
    else:
        integers = [int(x * common) for x in rationals]
    Q = [[0] * 16 for _ in range(16)]
    for (i, j), value in zip(dual['packed_pairs'], integers):
        Q[i][j] = Q[j][i] = value * (2 if i == j else 1)
    repair = 0
    for x in histograms(6):
        value, square = poly(Q, x), sum(v*v for v in x)
        if value < 0:
            repair = max(repair, (-value + square - 1) // square)
    for i in range(16):
        Q[i][i] += repair
    raw_trace = sum(Q[i][j] * U[j][i] for i in range(16) for j in range(16))
    assert raw_trace < 0
    root = f.ROOT_MASKS[block]
    actions = [[s[c] & 15 for c in range(16)] for r, s in f.TRANSFORMS if r[root] == root]
    assert all(U[p[i]][p[j]] == U[i][j] for p in actions for i in range(16) for j in range(16))
    Q = [[sum(Q[p[i]][p[j]] for p in actions) for j in range(16)] for i in range(16)]
    assert all(Q[p[i]][p[j]] == Q[i][j] for p in actions for i in range(16) for j in range(16))
    minimum, minimizing, count, zeros = None, None, 0, 0
    for x in histograms(6):
        value = poly(Q, x)
        count += 1
        if minimum is None or value < minimum:
            minimum, minimizing = value, x
        zeros += value == 0
    assert count == 54264 and minimum >= 0
    small_minimum, small_witness = 0, None
    for total in range(6):
        for x in histograms(total):
            value = poly(Q, x)
            if value < small_minimum:
                small_minimum, small_witness = value, x
    codes = sorted(f.STATE_IDS[block])
    projection = [c & 15 for c in codes]
    assert set(projection) == set(range(16))
    full_Q = [[Q[a][b] for b in projection] for a in projection]
    for r, action in f.TRANSFORMS:
        if r[root] != root:
            continue
        p = [f.STATE_IDS[block][action[c]] for c in codes]
        assert all(full_Q[p[i]][p[j]] == full_Q[i][j] for i in range(len(codes)) for j in range(len(codes)))
    trace = sum(Q[i][j] * U[j][i] for i in range(16) for j in range(16))
    assert trace == len(actions) * raw_trace < 0
    output = {
        'status': 'EXACT_CONNECTOR_FINITE6_SEPARATOR',
        'scope': 'All16 connectorcodes andALL legalfullstates, noold16supportrestriction oroutsideLJrepair. Samefrozen202lambda, notacceptedfeasiblepoint/graph.',
        'block': block, 'canonical_root_mask': root, 'connector_order': list(range(16)),
        'connector_Q': Q, 'full_state_dimension': len(codes),
        'full_state_connector_codes': projection, 'full_Q': full_Q,
        'positive_normalization': max(abs(v) for row in Q for v in row),
        'finite6': {'histograms': count, 'minimum': minimum, 'minimizing_histogram': minimizing, 'zeros': zeros},
        'small_histograms': {'minimum_total_le5': small_minimum, 'negative_witness': small_witness},
        'point_pairing': {'integer_trace_Q_U': trace, 'moment_denominator': projected['moment_denominator'], 'exact_mean_feature': str(Fraction(trace, projected['moment_denominator']))},
        'connector_root_actions': actions,
        'arithmetic_recovery': {'method': method, 'denominator': common, 'diagonal_repair': repair},
        'point_sha256': projected['point_sha256'],
        'projected_moment_sha256': hashlib.sha256(point_file.read_bytes()).hexdigest(),
        'dual_sha256': hashlib.sha256(dual_file.read_bytes()).hexdigest(),
        'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    }
    (HERE / f'block{block}.EXACT_SEPARATOR.json').write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps({k: output[k] for k in ('block', 'canonical_root_mask', 'positive_normalization', 'finite6', 'small_histograms', 'point_pairing', 'arithmetic_recovery')}, indent=2))


if __name__ == '__main__':
    main()
