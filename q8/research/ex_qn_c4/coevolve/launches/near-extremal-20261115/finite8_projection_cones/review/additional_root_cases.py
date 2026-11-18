"""Close a calibration coverage detail: the actual682 seed has only types1,4."""
import sys
sys.dont_write_bytecode = True
import json
from fractions import Fraction
from pathlib import Path
import independent_replay as r

HERE = Path(__file__).resolve().parent
maps = [[i % 3 for i in range(d)] for d in r.DIMS]
q = [0, 1, 0]
Q = [[36*q[i]*q[j]-15*(q[i]+q[j])+6 for j in range(3)] for i in range(3)]
full = [r.lift(Q, maps[b], b) for b in range(5)]
adjacent = r.bridge({(0, 1), (0, 2)}, full)
assert adjacent['root_type_counts'][2] == 1 and Fraction(adjacent['raw_values'][2]) > 0
cut = r.read(r.DATA / 'block3.EXACT_CUT.json')
kernels = [[[0] * d for _ in range(d)] for d in r.DIMS]
kernels[3] = cut['full_Q']
point = r.read(r.DATA / 'INPUT_POINT.json')
local = [(Fraction(r.local_integer(mask, kernels)[3], 288 * cut['positive_normalization']), mask) for mask, _ in point['lambda']]
value, mask = min(local)
assert value < 0
out = {'status': 'PASS_ADJACENT_ROOT2_NONZERO_BRIDGE_AND_NEGATIVE_LOCAL_FEATURE',
       'adjacent_two_edge_actualQ8': adjacent,
       'negative_actual_Q4_feature': {'mask': mask, 'exact_normalized_value': str(value)},
       'interpretation': 'The universal inequality concerns the average of one actual Q8, while a legal individual Q4 can have a negative local feature. The actual682 seed itself has only root blocks1,4; it is not a nonzero test for every block.'}
(HERE / 'ADDITIONAL_ROOT_RESULTS.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps(out))
