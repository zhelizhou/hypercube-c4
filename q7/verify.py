#!/usr/bin/env python3
"""Check the Q7 witness and certificate files, optionally replaying RUP proofs."""

import argparse
from hashlib import file_digest
from itertools import combinations
import json
import os
from pathlib import Path
import shutil
import subprocess
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parent
INSTANCES = ROOT / "instances"


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def check_hash(path, expected):
    if not path.is_file():
        raise SystemExit(f"Missing {path.name}. Extract the corresponding release archive first.")
    with path.open("rb") as stream:
        actual = file_digest(stream, "sha256").hexdigest()
    if actual != expected:
        raise SystemExit(f"SHA-256 mismatch: {path}")


def verify_witness():
    edge_list = read_json(ROOT / "witness-304.json")["edges"]
    edges = {tuple(sorted(edge)) for edge in edge_list}
    if len(edge_list) != 304 or len(edges) != 304:
        raise SystemExit("The witness must contain 304 distinct edges.")
    if not all(0 <= u < v < 128 and (u ^ v).bit_count() == 1 for u, v in edges):
        raise SystemExit("The witness contains an edge outside Q7.")
    checked = 0
    for a, b in combinations((1 << i for i in range(7)), 2):
        for v in range(128):
            if v & (a | b):
                continue
            u, w, x = v | a, v | b, v | a | b
            if {(v, u), (v, w), (u, x), (w, x)} <= edges:
                raise SystemExit(f"The witness contains the square at {v} in directions {a}, {b}.")
            checked += 1
    print(f"PASS: 304-edge witness, {checked} squares checked.", flush=True)


def read_cases():
    audit = read_json(INSTANCES / "local_rigidity_final_audit.json")
    cases = {"A": audit["root2_existing_report_reconfirmed"]}
    for row in audit["certificates"]:
        cases[f"{row['family']}:{row['case']}"] = row
    if len(cases) != 21:
        raise SystemExit("Expected the degree-two case and twenty orbit cases.")
    return cases


def replay(case, row, pwsh):
    root_case = case == "A"
    checker = "check_drup.ps1" if root_case else "check_drup_history_fast.ps1"
    suffix = ".checked_cs.json" if root_case else ".checked_history_cs.json"
    stem = row["prefix"]
    with TemporaryDirectory(prefix="hypercube-q7-", dir=ROOT) as temp:
        folder = Path(temp)
        for ext in (".cnf", ".drup"):
            src = INSTANCES / (stem + ext)
            dst = folder / src.name
            try:
                os.link(src, dst)
            except OSError:
                shutil.copyfile(src, dst)
        subprocess.run(
            [pwsh, "-NoProfile", "-File", str(ROOT / "tools" / checker),
             "-Prefix", str(folder / stem)],
            check=True,
        )
        report = read_json(folder / (stem + suffix))
        if not report["valid"] or report["checked_additions"] != row["checked_additions"]:
            raise SystemExit(f"Unexpected RUP checker result for {case}.")


def main():
    cases = read_cases()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--traces", action="store_true", help="also check extracted trace hashes")
    parser.add_argument("--replay", action="store_true", help="check hashes and run PowerShell RUP checkers")
    parser.add_argument("--case", choices=cases, action="append", help="limit checking to selected cases")
    parser.add_argument("--pwsh", default="pwsh", help="PowerShell 7 executable for replay")
    args = parser.parse_args()
    pwsh = shutil.which(args.pwsh) if args.replay else None
    if args.replay and not pwsh:
        parser.error("PowerShell 7 is required for --replay. Supply its path with --pwsh.")
    verify_witness()
    chosen = args.case or cases
    for case in chosen:
        row = cases[case]
        stem = row["prefix"]
        check_hash(INSTANCES / (stem + ".cnf"), row["cnf_sha256"])
        if args.traces or args.replay:
            check_hash(INSTANCES / (stem + ".drup"), row["proof_sha256"])
        if args.replay:
            replay(case, row, pwsh)
    scope = "CNF and trace" if args.traces or args.replay else "CNF"
    print(f"PASS: {len(chosen)} {scope} hash checks.")
    if args.replay:
        print(f"PASS: {len(chosen)} RUP replays.")


if __name__ == "__main__":
    main()
