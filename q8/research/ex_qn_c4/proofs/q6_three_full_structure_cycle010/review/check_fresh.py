#!/usr/bin/env python3
"""Reviewer reconstruction. Stdlib only; imports no producer and runs no solver."""
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
from math import comb
from pathlib import Path
import json

OUT = Path(__file__).resolve().parent
SRC = OUT.parent
OLD = Path('q6_sources/q8_upper_independent/results')
EVEN = tuple(v for v in range(64) if v.bit_count() % 2 == 0)
FULL = (0, 15, 51)
BLOCKS = (3, 12, 48)

def dirs(mask):
    return tuple(i for i in range(6) if mask >> i & 1)

def star(v, mask):
    return frozenset(tuple(sorted((v, v ^ (1 << i)))) for i in dirs(mask))

SQUARES = []
for a, b in combinations(range(6), 2):
    mask = (1 << a) | (1 << b)
    for v in range(64):
        if v & mask:
            continue
        SQUARES.append(frozenset((tuple(sorted((v, v ^ (1 << a)))),
                                 tuple(sorted((v, v ^ (1 << b)))),
                                 tuple(sorted((v ^ (1 << a), v ^ mask))),
                                 tuple(sorted((v ^ (1 << b), v ^ mask))))))
assert len(SQUARES) == 240

def has_square(edges):
    return any(square <= edges for square in SQUARES)

def literal_conflict(c, d):
    return c[0] == d[0] or has_square(star(*c) | star(*d))

def permute(v, order):
    return sum(((v >> old) & 1) << new for new, old in enumerate(order))

def independent_maximal_cliques(adj):
    # Iterative Bron--Kerbosch, a stack of immutable states, no producer import.
    done = set()
    stack = [(frozenset(), frozenset(range(len(adj))), frozenset())]
    while stack:
        chosen, available, excluded = stack.pop()
        if not available and not excluded:
            done.add(tuple(sorted(chosen)))
            continue
        pivot = max(available | excluded)
        candidates = available - adj[pivot]
        remaining = set(available)
        previous = set(excluded)
        for v in sorted(candidates, reverse=True):
            stack.append((chosen | {v}, frozenset(remaining & adj[v]),
                          frozenset(previous & adj[v])))
            remaining.remove(v)
            previous.add(v)
    return done

def main():
    packing = json.loads((SRC / 'PACKING.json').read_text())
    saved = json.loads((SRC / 'CLIQUES.json').read_text())
    # Exhaust every triple and construct its ONE common coordinate map explicitly.
    valid = []
    for triple in combinations(EVEN, 3):
        if any((a ^ b).bit_count() < 4 for a, b in combinations(triple, 2)):
            continue
        u, v, w = triple
        a, b = u ^ v, u ^ w
        assert a.bit_count() == b.bit_count() == (a ^ b).bit_count() == 4
        order = dirs(a & b) + dirs(a & ~b) + dirs(b & ~a)
        assert sorted(order) == list(range(6))
        assert {permute(x ^ u, order) for x in triple} == set(FULL)
        assert {permute((x ^ 1) ^ (u ^ 1), order) for x in triple} == set(FULL)
        valid.append(triple)
    # Enumerate complete local stars using literal edges and the 240 actual squares.
    fixed = frozenset().union(*(star(f, 63) for f in FULL))
    assert not has_square(fixed)
    local = {}
    columns = []
    for v in EVEN:
        if v in FULL:
            continue
        allowed = tuple(m for m in range(63) if not has_square(fixed | star(v, m)))
        local[v] = allowed
        columns.extend((v, m) for m in allowed if m.bit_count() >= 4)
    assert [(r['root'], tuple(r['allowed_masks'])) for r in packing['local_rows']] == list(local.items())
    assert columns == [(r['root'], r['mask']) for r in packing['columns']]
    assert len(columns) == 213
    weights = [1 if m.bit_count() == 4 else 3 for v, m in columns]
    for (v, m), weight, row in zip(columns, weights, packing['columns']):
        neighbors = sorted(v ^ (1 << i) for i in dirs(m))
        faces = sorted([sum(1 << i for i in t), v & ~sum(1 << i for i in t)]
                       for t in combinations(dirs(m), 3))
        assert row['neighbors'] == neighbors and row['weight'] == weight
        assert row['degree'] == m.bit_count() and row['faces'] == faces
    # Conflict is rebuilt by actual four-edge cycles, including all same-root pairs.
    adjacency = [set() for _ in columns]
    cross_conflicts = []
    for i, j in combinations(range(len(columns)), 2):
        if literal_conflict(columns[i], columns[j]):
            adjacency[i].add(j)
            adjacency[j].add(i)
            if columns[i][0] != columns[j][0]:
                cross_conflicts.append((i, j))
    # Generate the symmetric 23 slots directly in the translated coordinate gauge.
    slot_labels, slots = [], []
    for block in BLOCKS:
        other = [d for d in BLOCKS if d != block]
        bases = [0] + [(1 << a) | (1 << b) for a, b in product(dirs(other[0]), dirs(other[1]))]
        for base in bases:
            endpoints = (base, base | block)
            slots.append(tuple(i for i, (v, m) in enumerate(columns)
                               if (v ^ 60) in endpoints and m & block == block))
            slot_labels.append({'kind': 'square', 'translated_roots': endpoints, 'directions': block})
    for a, b, c in product(*(dirs(block) for block in BLOCKS)):
        mask = (1 << a) | (1 << b) | (1 << c)
        slots.append(tuple(i for i, (v, m) in enumerate(columns)
                           if (v ^ 60) & ~mask == 0 and m & mask == mask))
        slot_labels.append({'kind': 'Q3', 'translated_base': 0, 'directions': mask})
    assert len(slots) == len(set(slots)) == 23
    for slot in slots:
        assert all(j in adjacency[i] for i, j in combinations(slot, 2))
    cover = [sum(i in slot for slot in slots) for i in range(len(columns))]
    assert all(k >= w for k, w in zip(cover, weights))
    # Extra origin occupancy for the separately stated corollary (if supplied).
    origin_coverage = {}
    for mask in local[60]:
        occupied = sum(mask & block == block for block in BLOCKS)
        occupied += sum(mask & t == t for t in (sum(1 << i for i in s) for s in product(*(dirs(b) for b in BLOCKS))))
        origin_coverage[mask] = occupied
        if mask.bit_count() == 3:
            assert occupied >= 1
        if mask.bit_count() == 4:
            assert occupied >= 2
        if mask.bit_count() == 5:
            assert occupied >= 6
    # The entire claimed maximal-clique catalogue, not only the 23 certificate rows.
    supplied = [tuple(row) for row in saved['cliques']]
    assert len(supplied) == len(set(supplied)) == 422
    for row in supplied:
        assert len(row) == len(set(row)) and all(0 <= i < len(columns) for i in row)
        assert all(j in adjacency[i] for i, j in combinations(row, 2))
        assert all(any(j not in adjacency[i] for i in row) for j in set(range(len(columns))) - set(row))
    rebuilt = independent_maximal_cliques(adjacency)
    assert rebuilt == set(supplied)
    assert set(slots) <= rebuilt
    # Independently reconstruct every base row; a clique-only LP includes these.
    roots = sorted({v for v, m in columns})
    base_rows = [('root', v, tuple(i for i, c in enumerate(columns) if c[0] == v)) for v in roots]
    base_rows += [('conflict', (i, j), (i, j)) for i, j in cross_conflicts]
    occupied_faces = sorted({tuple(face) for row in packing['columns'] for face in row['faces']})
    for mask, base in occupied_faces:
        row = tuple(i for i, (v, m) in enumerate(columns) if v & ~mask == base and m & mask == mask)
        assert all(f & ~mask != base for f in FULL)
        base_rows.append(('face', (mask, base), row))
    labels = [[kind, arg] if kind != 'conflict' else [kind, *arg] for kind, arg, row in base_rows]
    labels = json.loads(json.dumps(labels))
    assert labels == packing['row_labels']
    for kind, arg, row in base_rows:
        assert any(set(row) <= set(clique) for clique in supplied)
    # Exact dual and primal -- no floating-point optimization or tolerance.
    dual = {}
    for idx, value in saved['nonzero_dual']:
        assert idx not in dual and 0 <= idx < len(supplied)
        dual[idx] = Fraction(value)
    assert all(x == 1 for x in dual.values()) and sum(dual.values()) == 23
    assert {supplied[i] for i in dual} == set(slots)
    assert all(sum(value for idx, value in dual.items() if j in supplied[idx]) >= weights[j]
               for j in range(len(columns)))
    primal = [Fraction(0)] * len(columns)
    seen = set()
    for idx, value in saved['exact_primal']:
        assert idx not in seen and 0 <= idx < len(columns)
        seen.add(idx)
        primal[idx] = Fraction(value)
    assert all(value >= 0 for value in primal)
    assert all(sum(primal[i] for i in row) <= 1 for row in supplied)
    assert all(sum(primal[i] for i in row) <= 1 for kind, arg, row in base_rows)
    assert sum(x * w for x, w in zip(primal, weights)) == 23
    old_dual = {}
    for idx, value in packing['dual_nonzero']:
        assert idx not in old_dual and 0 <= idx < len(base_rows)
        old_dual[idx] = Fraction(value)
    assert all(value >= 0 for value in old_dual.values()) and sum(old_dual.values()) == 27
    assert all(sum(value for idx, value in old_dual.items() if j in base_rows[idx][2]) >= weights[j]
               for j in range(len(columns)))
    origin_saved = json.loads((SRC / 'ORIGIN_CHECK.json').read_text())
    origin_rows = []
    for mask, occupied in origin_coverage.items():
        degree = mask.bit_count()
        if degree < 3:
            continue
        h = {3: 0, 4: 1, 5: 3}[degree]
        origin_rows.append({'mask': mask, 'degree': degree,
                            'block_counts': [(mask & b).bit_count() for b in BLOCKS],
                            'slots': occupied, 'H_contribution': h, 'excess': occupied - h})
    assert len(origin_rows) == 41 and origin_rows == origin_saved['rows']
    # Literal graph calibrations and low-degree deletion boundary tests.
    index = {c: i for i, c in enumerate(columns)}
    def check_graph(edges):
        assert all(0 <= a < b < 64 and (a ^ b).bit_count() == 1 for a, b in edges)
        assert not has_square(edges)
        masks = {v: 0 for v in EVEN}
        for a, b in edges:
            even = a if a in masks else b
            masks[even] |= a ^ b
        assert {v for v, m in masks.items() if m.bit_count() == 6} == set(FULL)
        selected = {index[(v, m)] for v, m in masks.items() if 4 <= m.bit_count() <= 5}
        assert all(len(selected & set(slot)) <= 1 for slot in slots)
        S = sum(comb(m.bit_count(), 3) for m in masks.values())
        L = sum(m.bit_count() <= 2 for m in masks.values())
        H = sum(weights[i] for i in selected)
        assert S + L == 89 + 3 * H <= 158
        origin_mask = masks[60]
        if origin_mask.bit_count() >= 3:
            excess = origin_coverage[origin_mask] - {3: 0, 4: 1, 5: 3}[origin_mask.bit_count()]
            assert H + excess <= 23 and S + L <= 158 - 3 * excess
        return S, L, H
    witnesses = []
    boundary_cases = 0
    for name in ('q6_code_degree_3_score21.json', 'q6_code_degree_3_score21_oppmin3.json'):
        path = OLD / name
        data = json.loads(path.read_text())
        edges = frozenset(tuple(sorted(e)) for e in data['edges'])
        assert len(edges) == len(data['edges'])
        assert check_graph(edges) == (152, 0, 21)
        witnesses.append({'path': str(path), 'sha256': sha256(path.read_bytes()).hexdigest(),
                          'edges': len(edges), 'S': 152, 'L': 0, 'H': 21})
        for v in local:
            incident = sorted(e for e in edges if v in e)
            for degree in (0, 1, 2):
                reduced = edges - set(incident[degree:])
                check_graph(reduced)
                boundary_cases += 1
        assert check_graph(fixed) == (60, 29, 0)
    result = {
        'status': 'PASS', 'method': 'independent literal-edge reconstruction and exact Fraction arithmetic; no producer import or LP/SAT',
        'even_full_triples': len(valid), 'odd_full_triples_checked_by_translation': len(valid),
        'local_masks': sum(map(len, local.values())),
        'local_maximum_histogram': dict(sorted(Counter(max(m.bit_count() for m in ms) for ms in local.values()).items())),
        'high_columns': len(columns), 'high_degree_histogram': dict(sorted(Counter(m.bit_count() for v, m in columns).items())),
        'cross_root_conflicts': len(cross_conflicts), 'all_conflicts': sum(map(len, adjacency)) // 2,
        'base_rows': len(base_rows), 'Q3_rows': len(occupied_faces), 'maximal_cliques': len(rebuilt),
        'slots': slot_labels,
        'coverage_histogram': {str(k): v for k, v in sorted(Counter((columns[i][1].bit_count(), k) for i, k in enumerate(cover)).items())},
        'exact_H_dual': 23, 'exact_H_primal': 23, 'primal_nonzero': len(seen),
        'earlier_base_dual_H_upper': 27, 'origin_corollary_masks': len(origin_rows),
        'primal_denominators': sorted({q.denominator for q in primal if q}),
        'origin_coverage_histogram': {str(k): v for k, v in sorted(Counter((m.bit_count(), k) for m, k in origin_coverage.items()).items())},
        'graph_witnesses': witnesses, 'low_degree_deletion_counterchecks': boundary_cases,
        'boundary_full_stars_only': {'S': 60, 'L': 29, 'H': 0},
        'limits': ['Fractional primal is not a graph and does not fix L.', 'L=0 bound158 is weaker than historical152.', 'No unrestricted Q8 conclusion.'],
        'source_hashes': {name: sha256((SRC / name).read_bytes()).hexdigest() for name in ('PACKING.json', 'CLIQUES.json', 'ORIGIN_CHECK.json')},
        'checker_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    (OUT / 'CHECK_RESULT.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
