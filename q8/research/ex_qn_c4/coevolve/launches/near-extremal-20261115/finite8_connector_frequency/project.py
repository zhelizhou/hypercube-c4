"""Exact sixteen-connector projection of the same frozen graphlambda."""
from pathlib import Path
from fractions import Fraction
from collections import Counter
from math import lcm
import hashlib
import json
import sys
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'finite8_flags'
sys.path.insert(0, str(SOURCE))
import finite_flags as f


def main():
    raw = (HERE / 'INPUT_POINT.json').read_bytes()
    point = json.loads(raw)
    rational = [(g, Fraction(str(value))) for g, value in point['lambda']]
    denominator = lcm(*(v.denominator for g, v in rational))
    weights = [(g, int(v * denominator)) for g, v in rational]
    assert len(weights) == 202
    codes = [sorted(ids) for ids in f.STATE_IDS]
    projected = Counter()
    full = Counter()
    for graph, weight in weights:
        _, coefficients = f.local_coefficients(f.q4_edges_from_mask(graph))
        for (b, i, j), value in coefficients.items():
            if b >= 5:
                continue
            ci, cj = codes[b][i] & 15, codes[b][j] & 15
            projected[b, min(ci, cj), max(ci, cj)] += weight * value
            full[b, i, j] += weight * value
    blocks = []
    for b in range(5):
        U = [[0] * 16 for _ in range(16)]
        for (block, i, j), value in projected.items():
            if block != b:
                continue
            U[i][j] += value * (2 if i == j else 1)
            if i != j:
                U[j][i] += value
        # Independent linear projection from ordered fullmoment entries:
        check = [[0] * 16 for _ in range(16)]
        for (block, i, j), value in full.items():
            if block != b:
                continue
            a, c = codes[b][i] & 15, codes[b][j] & 15
            check[a][c] += value * (2 if i == j else 1)
            if i != j:
                check[c][a] += value
        assert check == U
        blocks.append({'block': b, 'canonical_root_mask': f.ROOT_MASKS[b], 'connector_state_order': list(range(16)), 'twice_integer_matrix': U, 'positive_diagonal_support': [i for i in range(16) if U[i][i]]})
    output = {'scope': 'Exact actualfive face moment projections of the same202-weight frozenedge-stage lambda. Noexactfeasiblepoint orgraph assertion.', 'point_sha256': hashlib.sha256(raw).hexdigest(), 'input_status': point['status'], 'input_iteration': point['iteration'], 'lambda_integer_numerators': weights, 'lambda_decimal_denominator': denominator, 'lambda_mass_exact': str(Fraction(sum(w for g, w in weights), denominator)), 'moment_denominator': 2 * f.DEN * denominator, 'projection': 'A_b[c,i]=1 when originalascendinglegalflagcode_i &15 ==c. Mconn=A Mfull A^T.', 'blocks': blocks, 'state_source_sha256': hashlib.sha256((SOURCE / 'finite_flags.py').read_bytes()).hexdigest(), 'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE / 'PROJECTED_MOMENTS.json').write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps({'blocks': [(b['block'], b['positive_diagonal_support']) for b in blocks], 'lambda_mass': output['lambda_mass_exact'], 'point_sha256': output['point_sha256']}, indent=2))


if __name__ == '__main__':
    main()
