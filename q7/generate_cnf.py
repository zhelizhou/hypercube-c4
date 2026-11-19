#!/usr/bin/env python3
"""Regenerate the 21 DIMACS inputs without invoking a SAT solver."""

import argparse
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import sys

from verify import INSTANCES, read_cases, read_json

sys.path.insert(0, str(INSTANCES))
from star_rigidity_encoding_audit import reconstruct


def degree_two_formula():
    """Reproduce the original variable numbering and clause order for A."""
    n = 6
    vertices = range(1 << n)
    even = [v for v in vertices if v.bit_count() % 2 == 0]
    edges = [
        (v, v ^ (1 << i)) for v in vertices for i in range(n) if not v & (1 << i)
    ]
    edge_ids = {pair: i for i, pair in enumerate(edges, 1)}

    def edge(v, i):
        return edge_ids[tuple(sorted((v, v ^ (1 << i))))]

    triples = list(combinations(range(n), 3))
    stars = {}
    clauses = []
    for v in even:
        for axes in triples:
            s = len(edges) + len(stars) + 1
            stars[v, axes] = s
            literals = [edge(v, i) for i in axes]
            clauses.extend([-s, x] for x in literals)
            clauses.append([s, *(-x for x in literals)])

    for i, j in combinations(range(n), 2):
        for v in vertices:
            if v & ((1 << i) | (1 << j)) == 0:
                clauses.append([-edge(v, i), -edge(v, j),
                                -edge(v ^ (1 << i), j), -edge(v ^ (1 << j), i)])

    for axes in triples:
        mask = sum(1 << i for i in axes)
        for base in vertices:
            if base & mask == 0:
                candidates = [stars[v, axes] for v in even if v & ~mask == base]
                clauses.append(candidates)
                clauses.extend([-s, -t] for s, t in combinations(candidates, 2))

    clauses.extend([edge(0, i) if i < 2 else -edge(0, i)] for i in range(n))
    for v in even[1:]:
        incident = [edge(v, i) for i in range(n)]
        clauses.extend(combinations(incident, 4))
        clauses.append([-x for x in incident])

    return len(edges) + len(stars), clauses


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path, help="new output directory")
    args = parser.parse_args()

    if args.out.exists():
        parser.error("--out must be a new directory")

    orbits = read_json(INSTANCES / "two_hole_orbits.json")
    inputs = {}
    for case, row in read_cases().items():
        stem = row["prefix"]
        if case == "A":
            variables, clauses = degree_two_formula()
        else:
            metadata = read_json(INSTANCES / (stem + ".json"))
            formula, _ = reconstruct(metadata, orbits)
            variables, clauses = formula.top, formula.cs

        header = f"p cnf {variables} {len(clauses)}\n"
        body = "".join(" ".join(map(str, clause)) + " 0\n" for clause in clauses)
        data = (header + body).encode("ascii")
        if sha256(data).hexdigest() != row["cnf_sha256"]:
            raise SystemExit(f"{stem}: regenerated CNF disagrees with the archived digest")
        inputs[stem] = data

    args.out.mkdir(parents=True)
    for stem, data in inputs.items():
        (args.out / (stem + ".cnf")).write_bytes(data)
    print(f"PASS: regenerated all {len(inputs)} CNFs with their archived byte digests.")


if __name__ == "__main__":
    main()
