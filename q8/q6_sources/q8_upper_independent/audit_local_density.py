"""Degree arithmetic and independent checks of this continuation's witnesses.

No SAT solver or graph generator is imported. The hypotheses used in the
arithmetic are recorded explicitly; feasible histograms need not be graphs.
"""
from pathlib import Path
import hashlib
import json
from verify_examples import inspect

ROOT = Path(__file__).resolve().parent


def main():
    caps = [158, 156, 157, 152, 144]
    bands = {}
    rigid_bands = {}
    for m in range(96, 133):
        profiles = []
        for c in range(5):
            for b in range(33-c):
                n5 = m-128+b-2*c
                n4 = 32-b-c-n5
                stars = 6*m-640+3*b+4*c
                if min(n4, n5) >= 0 and stars <= caps[c]:
                    profiles.append((b, c, n4, n5, stars))
        pairs = [(p, q) for p in profiles for q in profiles
                 if p[0] >= 3*q[1] and q[0] >= 3*p[1]]
        if pairs:
            maximum = max(p[1]+q[1] for p, q in pairs)
            assert m+maximum <= 132
            bands[str(m)] = maximum
            rigid_pairs = [(p,q) for p,q in pairs
                           if m != 130 or max(p[1],q[1]) <= 1]
            if rigid_pairs:
                max_side = max(max(p[1],q[1]) for p,q in rigid_pairs)
                assert m+2*max_side <= 133
                rigid_bands[str(m)] = max_side
    # The new rigidity lemma is NOT needed for this density inequality.
    assert {m: bands[str(m)] for m in range(125, 133)} == {
        125: 6, 126: 5, 127: 4, 128: 4, 129: 3, 130: 2, 131: 1, 132: 0}

    witnesses = {}
    paths = sorted((ROOT/'results').glob('parity_stack*.json'))
    paths += sorted((ROOT/'results').glob('q6_130_twofull_stack_r*.json'))
    for path in paths:
        raw = json.loads(path.read_text())
        checked, degrees = inspect(7, raw['edges'])
        if path.name.startswith('parity_stack'):
            P = [v for v in range(128) if v.bit_count()%2 == 0]
            assert min(degrees[v] for v in P) >= 4
            score = checked['edges']+sum(degrees[v] == 6 for v in P)
            score += 3*sum(degrees[v] == 7 for v in P)
            assert score == raw['best_parity_score']
            checked['parity_score'] = score
            checked['specified_parity_minimum'] = min(degrees[v] for v in P)
        else:
            assert checked['weighted_score'] == raw['best_weighted']
        checked['source_sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
        witnesses[path.name] = checked
    assert len(witnesses) == 7
    output = {
        'status': 'PASS',
        'density_lemma': 'For every C4-free Q6 with minimum degree at least 3, m+N6_total<=132.',
        'hypotheses': ['m<=132 (separate hole-counting proof)',
                       'each parity has 32 vertices, degrees in 3..6',
                       'parity stars at most [158,156,157,152,144] for c6=0..4',
                       'opposite degree3 count >= 3 times this parity degree6 count'],
        'max_total_full_roots_by_edges': bands,
        'rigidity_corollary': 'm+2*N6(P)<=133 for either parity P, assuming whole minimum degree3',
        'max_one_side_full_roots_after_M130_rigidity': rigid_bands,
        'checked_witnesses': witnesses,
        'restricted_search_is_not_a_universal_proof': True,
    }
    (ROOT/'results/local_density_audit.json').write_text(json.dumps(output, indent=2)+'\n')
    print(json.dumps({'status': 'PASS', 'density_bands': len(bands),
                      'witnesses': len(witnesses)}))


if __name__ == '__main__':
    main()
