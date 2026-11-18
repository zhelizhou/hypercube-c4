"""Compact exact edge-cut feature and equivalent full-face kernel interface."""
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
import json
import edge_flags
import lift

HERE = Path(__file__).resolve().parent


@lru_cache(None)
def load(name):
    cuts = json.loads((HERE / 'EDGE_CUTS.json').read_text())['cuts']
    return next(cut for cut in cuts if cut['name'] == name)


def value_on_graph(graph_mask, cut_name, normalize=True):
    cut = load(cut_name)
    Q, root = cut['integer_kernel'], cut['root_retained']
    c = edge_flags.local_coefficients(edge_flags.from_mask(graph_mask))
    numerator = sum(value * Q[i][j] for (r, i, j), value in c.items() if r == root)
    scale = cut['positive_normalization'] if normalize else 1
    return Fraction(numerator, 64512 * scale)


@lru_cache(None)
def full_face_lift(cut_name):
    cut = load(cut_name)
    kernels = [[[0] * d for _ in range(d)] for d in edge_flags.DIMS]
    kernels[cut['root_retained']] = cut['integer_kernel']
    numerator, denominator = lift.lift_to_faces(kernels, already_averaged=True)
    assert denominator == 196
    return numerator, denominator * cut['positive_normalization']


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--graph', type=int, required=True)
    parser.add_argument('--cut', required=True)
    args = parser.parse_args()
    v = value_on_graph(args.graph, args.cut)
    print(json.dumps({'value': str(v), 'decimal': float(v), 'cut': args.cut}))
