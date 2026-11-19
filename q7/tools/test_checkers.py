#!/usr/bin/env python3
"""Exercise the released RUP checkers on small positive and negative traces."""

import argparse
from pathlib import Path
import shutil
import subprocess
from tempfile import TemporaryDirectory


TOOLS = Path(__file__).resolve().parent
CONFLICT = [[1], [-1]]
UNSAT_WITHOUT_UNITS = [[1, 2], [1, -2], [-1, 2], [-1, -2]]
COMMON_CASES = [
    ("unit_conflict", 1, CONFLICT, "0\n", True),
    ("false_empty", 2, [[1, 2]], "0\n", False),
    ("recover_deleted_unit", 2, UNSAT_WITHOUT_UNITS, "1 0\nd 1 0\n0\n", True),
    ("retain_axioms", 1, CONFLICT, "d 1 0\n0\n", True),
    ("missing_terminator", 1, CONFLICT, "1\n0\n", False),
    ("embedded_zero", 1, CONFLICT, "1 0 -1 0\n0\n", False),
    ("out_of_range", 1, CONFLICT, "2 0\n0\n", False),
    ("missing_empty_clause", 2, UNSAT_WITHOUT_UNITS, "1 0\n", False),
    ("tautology_then_false_empty", 2, [[1, 2]], "1 -1 0\n0\n", False),
    ("non_rup_unit", 2, [[1, 2]], "-1 0\n0\n", False),
]
HISTORY_CASES = [
    ("recover_for_nonempty", 3, UNSAT_WITHOUT_UNITS, "1 0\nd 1 0\n3 0\n0\n", True),
    ("recover_more_than_once", 4, UNSAT_WITHOUT_UNITS,
     "1 0\nd 1 0\n3 0\nd 3 0\n4 0\n0\n", True),
    ("forbid_future_clause", 3, UNSAT_WITHOUT_UNITS, "3 0\n1 0\n0\n", False),
    ("forbid_current_clause", 2, [[1, 2]], "-1 0\n0\n", False),
    ("forbid_invalid_deleted_clause", 3, UNSAT_WITHOUT_UNITS,
     "3 0\nd 3 0\n1 0\n0\n", False),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pwsh", default="pwsh", help="PowerShell 7 executable")
    args = parser.parse_args()
    pwsh = shutil.which(args.pwsh)
    if not pwsh:
        parser.error("PowerShell 7 is required. Supply its path with --pwsh.")

    batches = [
        ("check_drup.ps1", COMMON_CASES),
        ("check_drup_history_fast.ps1", COMMON_CASES + HISTORY_CASES),
    ]
    with TemporaryDirectory(prefix="q7-rup-tests-") as directory:
        for checker, cases in batches:
            for name, variables, clauses, trace, expected in cases:
                prefix = Path(directory) / name
                header = f"p cnf {variables} {len(clauses)}\n"
                body = "".join(" ".join(map(str, c)) + " 0\n" for c in clauses)
                prefix.with_suffix(".cnf").write_bytes((header + body).encode("ascii"))
                prefix.with_suffix(".drup").write_bytes(trace.encode("ascii"))
                result = subprocess.run(
                    [pwsh, "-NoProfile", "-File", str(TOOLS / checker),
                     "-Prefix", str(prefix)], capture_output=True, text=True,
                )
                if (result.returncode == 0) != expected:
                    raise SystemExit(f"{checker}: unexpected result for {name}\n{result.stderr}")
            print(f"PASS: {checker} accepted and rejected all {len(cases)} traces as expected.")


if __name__ == "__main__":
    main()
