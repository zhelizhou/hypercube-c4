"""Exact edge-to-full-face pullback, read-only original state definitions."""
from pathlib import Path
import sys
sys.dont_write_bytecode = True
SOURCE = Path(__file__).resolve().parent.parent / 'finite8_flags'
sys.path.insert(0, str(SOURCE))
import finite_flags as face
import edge_flags


def lift_to_faces(kernels, already_averaged=False):
    """Integer face numerator, denominator196 (averaged) or392 (raw).

    The actual face kernel is sum_e V_e^T Qbar_edge V_e /196,
    where V_e(g)=6e_external+e_base.
    """
    K = []
    for root, Q in enumerate(kernels):
        d = edge_flags.DIMS[root]
        assert len(Q) == d and all(len(row) == d for row in Q)
        if already_averaged:
            assert all(Q[i][j] == Q[edge_flags.flip(i)][edge_flags.flip(j)] for i in range(d) for j in range(d))
            K.append(Q)
        else:
            K.append([[Q[i][j] + Q[edge_flags.flip(i)][edge_flags.flip(j)] for j in range(d)] for i in range(d)])
    output = []
    qe = face.Q2_EDGES
    for block, root_mask in enumerate(face.ROOT_MASKS):
        codes = sorted(face.STATE_IDS[block])
        R = [[0] * len(codes) for _ in codes]
        for ei, (u, v) in enumerate(qe):
            root = (root_mask >> ei) & 1
            Q = K[root]
            perpendicular = 3 ^ (u ^ v)
            c0 = qe.index(edge_flags.edge(u, u ^ perpendicular))
            c1 = qe.index(edge_flags.edge(v, v ^ perpendicular))
            opposite = qe.index(edge_flags.edge(u ^ perpendicular, v ^ perpendicular))
            base = ((root_mask >> c0) & 1) | (((root_mask >> c1) & 1) << 1) | (((root_mask >> opposite) & 1) << 2)
            assert base < edge_flags.DIMS[root]
            external = [((code >> u) & 1) | (((code >> v) & 1) << 1) | (((code >> (4 + ei)) & 1) << 2) for code in codes]
            assert all(state < edge_flags.DIMS[root] for state in external)
            for i, a in enumerate(external):
                for j, b in enumerate(external):
                    R[i][j] += 36 * Q[a][b] + 6 * Q[a][base] + 6 * Q[base][b] + Q[base][base]
        output.append(R)
    return output, (196 if already_averaged else 392)
