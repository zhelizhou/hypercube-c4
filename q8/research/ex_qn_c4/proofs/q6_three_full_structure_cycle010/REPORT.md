# Cycle010 three-full analytic exploration

The completed new local result is **S+L<=158 for every C4-free Q6 graph with exactly three full roots on a specified parity**, with no minimum-degree assumption on either side. Here S is the sum of binomial(degree,3) on that parity and L counts its vertices of degree at most two. In particular three low roots give S<=155 and weighted value 2S+3<=313.

`PROOF.md` gives a self-contained 23-slot proof: 15 actual square constraints and 8 actual Q3-face constraints. Five block types cover all 29 remaining roots. This proof needs no historical UNSAT import or LP solver. The same transformation acts on all full roots and the entire graph; the specified parity is sent to the even class.

`ORIGIN_COROLLARY.md` is Root's separate refinement. If the missing fourth full root (vertex 60 in the canonical {0,15,51} coordinates) has degree at least three, its extra slot use yields S+L<=155. The full occupancy table gives further conditional bounds 152 or 149 in its stated degree-pattern cases. It does not force that vertex to be nonlow.

The bounded computation preserved the actual progression:

1. `probe.py` constructed 213 high-star columns and the initial root/pair/face relaxation. Its exact dual H<=27 was too weak; `PACKING.json` and `probe.stdout.json` retain this attempt.
2. `cliques.py` strengthened only that same 213-column domain to its 422 maximal conflict cliques. It produced the 23 coefficient-one constraints used in the proof, plus an exact rational feasible primal with H=23. All clique constraints, not only the nonzero dual rows, are saved in `CLIQUES.json`. This shows the exact optimum of the high-star clique relaxation, not a graph or sharpness of the graph theorem.
3. `check_exact.py` independently reconstructs local masks, all conflicts, all maximal cliques and the short geometric certificate without importing producer code, NumPy, SciPy or a SAT library. `EXACT_CHECK.json` and `check_exact.stdout.json` record PASS. It checks 1,206 locally permitted masks, 213 high columns, 4,320 conflict edges including same-root choices, all 422 cliques, exact dual/primal arithmetic, 480 full-root triples and 23,040 parity-preserving maps after normalization. Both named historical S152 witnesses pass direct edge and all-240-square verification.
4. `check_origin.py` checks the 41 origin direction masks of degrees 3,4,5; `ORIGIN_CHECK.json` and its stdout record PASS.

The first system-Python attempt at `probe.py` stopped because NumPy was absent. The successful producer runs used the existing workspace `.venv/bin/python`. The first clique attempt stopped because NetworkX was absent; a small explicit bitset clique enumerator replaced that dependency before the successful run. No package installation was performed. These setup failures produced no mathematical result. The independent exact check uses ordinary `python3`.

Reproduction from this directory:

```sh
python3 check_exact.py
python3 check_origin.py
```

These checks read the two named original witness files at their recorded source paths. To regenerate the exploratory LP data, run `probe.py` followed by `cliques.py` using an environment with NumPy and SciPy. The theorem itself is the explicit slot proof and its standard-library exact check.

No full-graph SAT, broad catalog search, old c3 UNSAT replay, or full integer optimization was run. All local commands are terminal; no active process or resumable handle remains. The earlier four-full packing method was read as a method source; no historical computational import is required for the new theorem. Current mission/wiki were read for scope, and no shared record was modified.

Root and the independent same-family reviewer identified a wording error in the first frozen draft: translating an initially odd specified parity to 0 exchanges parity rather than preserving it. The final draft explicitly states the correct mapping and also fixes the pre-normalization references to even/odd vertices. The theorem, slots, cases, masks and computation did not change. The separate origin check was refreshed to bind the final proof hash; the unchanged core finite computation was not rerun merely for this wording correction.

This is author evidence with an independent same-family local review requested in `review/`. It is not a canonical PROOF_AUDIT, cross-model validation, Lean verification, or a new global Q8 upper bound. The exact fractional primal blocks improvement by this clique relaxation alone; further improvement would need additional constraints or integrality, and no follow-on search is started here.
