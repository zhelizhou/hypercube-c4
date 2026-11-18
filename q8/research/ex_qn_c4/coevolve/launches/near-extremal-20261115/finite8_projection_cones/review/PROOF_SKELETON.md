# Proof skeleton and accounting

The machine-readable typed symbols, quantified theorem, hypothesis ledger and acyclic dependency graph are in `SEMANTIC_LEDGER.json`.

Topological order: D0 → D1 → A0 → L1 → L2 → L3 → L4 → L5 → T1 → L6 → L7 → L8 → L9 → C1 → C2 → C3 → V1 → V2 → S0.

All declared source units are covered in `SOURCE_UNIT_COVERAGE.json`. That receipt concerns execution coverage, not mathematical truth.

| ID | Type | Obligation | Uses | Source |
|---|---|---|---|---|
| D0 | definition | Cube geometry and full legal rooted flags | — | PROOF.md:15-17 |
| D1 | definition | Full-state D4 stabilizer action | D0 | PROOF.md:37 |
| A0 | assumption | Q symmetric integer and nonnegative on every small integer total-six histogram | — | PROOF.md:5-7 |
| L1 | lemma | Small domain cardinality and sixteen-label zero-tail filter | — | PROOF.md:33 |
| L2 | lemma | Full-state pullback is finite-six valid | D0, A0 | PROOF.md:23-31 |
| L3 | lemma | Full simultaneous H sum is invariant and finite-six valid | D1, L2 | PROOF.md:37-45 |
| L4 | lemma | Common canonical root gauge is harmless | D0, D1, L3 | PROOF.md:51 |
| L5 | lemma | Collision identity for six external directions | L4 | PROOF.md:55-59 |
| T1 | theorem | Whole-actual-Q8 nonnegative expected feature | L3, L4, L5 | PROOF.md:61-65 |
| L6 | lemma | Native folded upper coordinates match T_K | L4 | PROOF.md:69-73 |
| L7 | lemma | Projection moment includes distinct-state diagonal collisions | L6 | PROOF.md:73 |
| L8 | lemma | Projected trace has exactly |H| factor for exported full sum | L3, L7 | PROOF.md:75-79 |
| L9 | lemma | Exact J repair validates the stored concrete small Q | L1 | PROOF.md:87-89 |
| C1 | corollary | Stored full block3/root6 kernel is a valid actual-Q8 feature | T1, L9, L3 | PROOF.md:89-97 |
| C2 | calculated_claim | Exact stored-decimal master102 separation | L8, L9 | PROOF.md:83-97 |
| C3 | calculated_claim | Full exported kernel is noncopositive and nonPSD | D0, L3 | PROOF.md:105 |
| V1 | validation | Actual682 and sparse nonzero Q8 bridge calibrations | C1, L5 | PROOF.md:103 |
| V2 | validation | Generic non-equivariant producer/scorer interface | L3, L8 | README.md:35-39; price_projection_point.py; score.py |
| S0 | scope | Local exclusion only; no theorem upper682, no family barrier | C1, C2 | PROOF.md:11,97,107 |

There are no limits, asymptotic statements, infinite sums or analytic interchanges. All constants and dimensions are fixed. All generic theorem assumptions remain explicit; the concrete artifact separately discharges the small-domain assumption.
