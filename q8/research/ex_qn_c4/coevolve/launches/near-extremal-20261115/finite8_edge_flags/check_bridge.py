"""Exact actualseed regression and nontrivial pointwise lift tests."""
from collections import Counter
from fractions import Fraction
from pathlib import Path
import hashlib
import json
import random
import edge_flags as edge
import lift
import finite_flags as face

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'finite8_flags'


def main():
    seed = json.loads((SOURCE / 'Q8_seed682_point.json').read_text())
    E = {tuple(map(int, row.split())) for row in Path(seed['source']).read_text().splitlines() if row.strip()}
    records = list(edge.restriction_records(E, 8))
    assert len(records) == 1120
    weights = list(Counter(graph for axes, base, graph in records).items())
    local = edge.moment(weights)
    direct = [[[0] * d for _ in range(d)] for d in edge.DIMS]
    roots = Counter()
    for root, states in edge.root_records(E, 8):
        roots[root] += 1
        assert len(states) == 7
        for action in (lambda s: s, edge.flip):
            counts = Counter(action(s) for s in states)
            for i, ni in counts.items():
                for j, nj in counts.items():
                    direct[root][i][j] += 1440 * ni * nj
    assert sum(roots.values()) == 1024 and roots[1] == 682 and direct == local

    # An arbitrary non-PSD pair proves the algebraic identity is not tested
    # only in a PSD special case; all entries remain exact integers.
    kernels = [[[((i + j + 1) * (i * j + 3)) % 17 - 8 for j in range(d)] for i in range(d)] for d in edge.DIMS]
    lifted, denominator = lift.lift_to_faces(kernels)
    assert denominator == 392
    invariance_count = 0
    for block, root in enumerate(face.ROOT_MASKS):
        codes = sorted(face.STATE_IDS[block])
        for r, action in face.TRANSFORMS:
            if r[root] != root:
                continue
            permutation = [face.STATE_IDS[block][action[code]] for code in codes]
            assert all(lifted[block][permutation[i]][permutation[j]] == lifted[block][i][j] for i in range(len(codes)) for j in range(len(codes)))
            invariance_count += 1
    frozen = json.loads((SOURCE / 'FAMILY_OBSTRUCTION.json').read_text())
    graphs = [g for g, w in frozen['probability_numerators']]
    rng = random.Random(20261116)
    # Add64 general C4-free samples outside the odd frozenpoint support.
    for _ in range(64):
        order = edge.original_q4_edges()
        rng.shuffle(order)
        K = set()
        for e in order:
            candidate = K | {e}
            try:
                list(face.face_data(candidate, 4))
            except AssertionError:
                continue
            K = candidate
        graphs.append(sum(1 << i for i, e in enumerate(edge.original_q4_edges()) if e in K))
    maximum_error = Fraction()
    for graph in graphs:
        K = edge.from_mask(graph)
        evalue = sum(c * kernels[b][i][j] for (b, i, j), c in edge.local_coefficients(K).items())
        _, coefficients = face.local_coefficients(K)
        fvalue = sum(c * lifted[b][i][j] for (b, i, j), c in coefficients.items() if b < 5)
        assert fvalue == denominator * evalue
        maximum_error = max(maximum_error, abs(Fraction(fvalue, denominator) - evalue))
    output = {'status': 'PASS_EXACT_EDGE_BRIDGE_AND_POINTWISE_LIFT', 'actual682_seed': {'Q4_restrictions': len(records), 'ambient_roots': sum(roots.values()), 'retained_roots': roots[1], 'missing_roots': roots[0], 'direct7flag_outerproducts_equal1120_local_sums': True}, 'lift': {'graphs_checked': len(graphs), 'all818_frozen_support_plus64_general_samples': True, 'all_root_stabilizer_actions_checked': invariance_count, 'integer_lift_denominator_for_raw_endpoint_kernels': denominator, 'maximum_exact_error': str(maximum_error), 'PSD_redundancy': 'Exact pointwise edgefeature equals existing facefeature of the PSD pullback. No newPSD constraint.', 'finite7_pullback': 'Maps integer6hist to6 times integer7hist; gives validfinite6 facekernel.'}, 'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE / 'BRIDGE_CHECK.json').write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
