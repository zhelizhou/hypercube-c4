"""Root exact replay using multisets rather than the producer's compositions."""
from collections import Counter
from fractions import Fraction
from itertools import combinations_with_replacement
from pathlib import Path
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(BASE / 'finite8_flags'))
import finite_flags as ff


def quadratic_multiset(matrix, values):
    return sum(matrix[i][j] for i in values for j in values)


def main():
    point_path = BASE / 'finite8_flags/FAMILY_OBSTRUCTION.json'
    point = json.loads(point_path.read_text())
    reports = []
    for block in (1, 4):
        path = BASE / f'finite8_frequency_cone/block{block}.EXACT_SEPARATOR.json'
        cert = json.loads(path.read_text())
        Q = cert['inside_Q']
        support = cert['actual_inside_support']
        full = cert['full_Q']
        outside = cert['outside_J_coefficient']
        assert support == point['blocks'][block]['support']
        assert len(Q) == 16 and all(len(row) == 16 for row in Q)
        lookup = {s: i for i, s in enumerate(support)}
        for i in range(ff.DIMS[block]):
            for j in range(ff.DIMS[block]):
                expected = (Q[lookup[i]][lookup[j]] if i in lookup and j in lookup
                            else 0 if (i in lookup) != (j in lookup) else outside)
                assert full[i][j] == full[j][i] == expected
        count6, min6, zero6 = 0, None, 0
        for multiset in combinations_with_replacement(range(16), 6):
            value = quadratic_multiset(Q, multiset)
            count6 += 1
            min6 = value if min6 is None else min(min6, value)
            zero6 += value == 0
        assert count6 == 54264 and min6 == 0
        assert zero6 == cert['finite6_check']['zero_histograms']
        count_small, min_small, witness = 0, 0, None
        for total in range(6):
            for multiset in combinations_with_replacement(range(16), total):
                value = quadratic_multiset(Q, multiset)
                count_small += 1
                if value < min_small:
                    min_small, witness = value, multiset
        assert count_small == 20349 and min_small == -outside
        assert min_small == cert['small_total_check']['minimum'] < 0
        root = ff.ROOT_MASKS[block]
        inverse = {i: code for code, i in ff.STATE_IDS[block].items()}
        group = []
        for action_root, action_flag in ff.TRANSFORMS:
            if action_root[root] != root:
                continue
            action = [ff.STATE_IDS[block][action_flag[inverse[i]]]
                      for i in range(ff.DIMS[block])]
            assert {action[s] for s in support} == set(support)
            assert all(full[action[i]][action[j]] == full[i][j]
                       for i in range(ff.DIMS[block]) for j in range(ff.DIMS[block]))
            group.append(action)
        U = point['blocks'][block]['twice_integer_matrix']
        trace = sum(Q[i][j]*U[j][i] for i in range(16) for j in range(16))
        value = Fraction(trace, 2*ff.DEN*point['probability_denominator'])
        assert trace < 0 and str(value) == cert['point_pairing']['exact_trace_Q_M']
        reports.append(dict(block=block, count_sum6=count6, minimum_sum6=min6,
                            zero_histograms=zero6, count_sum_le5=count_small,
                            minimum_sum_le5=min_small, outside_J=outside,
                            negative_multiset=list(witness),
                            stabilizer_order=len(group), pairing=str(value),
                            certificate_sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    receipt = dict(status='PASS', implementation='Root independent multiset enumeration',
                   checks=reports, point_sha256=hashlib.sha256(point_path.read_bytes()).hexdigest(),
                   scope='Two finite6 full-state kernels and negative frozen-point pairing; no upper682 conclusion')
    (HERE/'FINITE6_ROOT_CHECK.json').write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
