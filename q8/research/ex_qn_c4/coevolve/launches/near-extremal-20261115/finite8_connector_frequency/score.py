"""Exact fullstate feature of a sixteen-connector finite6 kernel."""
from pathlib import Path
from fractions import Fraction
from functools import lru_cache
import json
import sys
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'finite8_flags'
sys.path.insert(0, str(SOURCE))
import finite_flags as face


@lru_cache(None)
def load(block):
    return next(c for c in json.loads((HERE / 'CONNECTOR_CUTS.json').read_text())['cuts'] if c['block'] == block)


def value_on_graph(mask, block, normalize=True):
    cut = load(block)
    Q, mapping = cut['integer_connector_Q'], cut['full_state_connector_codes']
    _, coeff = face.local_coefficients(face.q4_edges_from_mask(mask))
    value = sum(c * Q[mapping[i]][mapping[j]] for (b, i, j), c in coeff.items() if b == block)
    scale = cut['positive_normalization'] if normalize else 1
    return Fraction(value, 64512 * scale)


def full_face_kernel(block, normalize=True):
    cut = load(block)
    Q, mapping = cut['integer_connector_Q'], cut['full_state_connector_codes']
    matrices = [[[0] * d for _ in range(d)] for d in face.DIMS[:5]]
    matrices[block] = [[Q[a][b] for b in mapping] for a in mapping]
    return matrices, cut['positive_normalization'] if normalize else 1


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--graph', type=int, required=True)
    parser.add_argument('--block', type=int, choices=(0, 4), required=True)
    args = parser.parse_args()
    value = value_on_graph(args.graph, args.block)
    print(json.dumps({'value_exact': str(value), 'value_decimal': float(value)}))
