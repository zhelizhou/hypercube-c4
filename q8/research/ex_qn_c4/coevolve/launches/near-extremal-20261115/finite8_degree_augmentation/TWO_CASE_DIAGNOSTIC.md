# Exact parameter split: actual bounded diagnostics

The goal remains OPEN. Neither case is excluded, and no Q8 graph is produced.
The parent supplied the complete maximal-counterexample split in
`finite8_parameter_split/PROOF.md` and `CASES.json`. Both actual parity degree
profiles of a graph have the same integer edge count. Case A uses the 764
remaining m=683 columns; case B uses all 645 columns for m=684,...,688.
Together they cover the previous 1409-column domain. The preparer froze the
cover, profile hash, exact old indices, and all profile array slicing in each
`PARAMETER_CASE_APPLIED.json`. All 14838 lambda columns, 1751 beta columns,
356 common equalities and 8002 stored valid inequalities were inherited.
There is no fixed683 density or even-square gate.

## B: m=684,...,688

`pool_case_B684plus/RESULT.json` records a numerical library dual, not a
full-domain certificate. Four masters took about 4.8 seconds of LP time.
Lambda working columns increased 764 to 872. The finite-library numerical
margin is 0.000177356253007. The active master had 239 inequality rows;
all other valid rows have zero dual weight. Saving the full inactive-row
matrix increased total elapsed time to 60.88 seconds.

The reconstructed score matched its original LP column values to the
reported floating reconstruction tolerance. Complete Q4 enumeration then
returned the exact integer maximum 3277685310504, on graph mask 4140225459.
The positive normalization is 64512*10^9. Literal common-neighbor C4 check
and the Python original packed-feature integer score agree exactly. Thus
the local library was insufficient for this dual; the branch remains open.
Evidence is in `pool_case_B684plus/full_oracle_001/`.

A second complete traversal retained the best positive actual graph from
each coarse degree/Q2 histogram class. Its maximum and witness agree with
the first traversal. All 192 emitted graphs independently passed literal
C4 and original integer score replay. There are 171 graph masks absent
from the current 14838 library. They have not yet been feature-deduplicated
or added to a subsequent master. These are local graphs, not Q8 examples.
See `all_positive_classes/BATCH_VERIFIED.json` and `LIBRARY_MASK_OVERLAP.json`.

## A: m=683

`pool_case_A683/run001.stdout.txt` records 15 masters and 60.12 seconds.
One tuple, `point_bank/master_012.json`, passed all 8002 previously stored
inequalities, variable signs and common equalities at the controller's
stated numerical tolerances. Its six minimum eigenvalues are approximately
(-2.06e-6,-1.46e-5,-2.28e-5,-6.51e-6,-9.24e-6,+1.91e-5).
It is not a PSD-feasible point or graph. The complete maximal-vertex-domain
bounded pricer found no new exact cut; that does not establish membership.

The complete connector six-count domain pricer proposed four new valid
kernels, blocks 0,1,2,3. Independent full 54264-domain and literal-geometry
replay passed before the controller appended them as rows 8036,...,8039.
Their actual same-tuple LP pairings are approximately
(-5.73e-6,-3.32e-5,-6.75e-5,-5.11e-6).
The exact parameters and checks are in
`connector_pricing_runtime/master_012/`. All original rows remain stored.
Master 13 reactivated 58 violated inactive rows. The remaining two seconds
were insufficient for master 14, whose TimeLimit is recorded as
`IPM_EXECUTION_NO_POINT`. This is not a case infeasibility conclusion.

## Proposal-only targets and inexpensive dual snapshots

The original union master 114 was rejected because its raw residuals did
not pass the complete model predicate. `make_discovery_target.py` preserves
that raw signed vector and rejection, then explicitly records per-block
clipping/normalization in `discovery_post_parallel114/`. It is labelled
DISCOVERY_ONLY, never FULLPASS. Any proposed kernel must still receive its
independent complete-domain validity and literal score replay. The target's
feasibility is not a premise of a universal finite-frequency inequality.
The actual raw LP pairing must also be inspected before importing a cut.

The successor `*_active_dual.py` controllers save only active AL/AR rows,
their exact full-row indices and zero inactive dual weights. The complete
old row library and full-primal checks are unchanged. On the B diagnostic,
the saved AL shrank from 498530024 to 12434709 bytes and writing the active
AL/AR took 1.43 seconds. Reconstructing the floating linear combination
using all rows and using active rows differs by exactly zero. This is a
computational equivalence, not an exact-arithmetic contradiction proof.
`extract_active_dual_oracle.py` supports these snapshots while retaining
the original six-block/edge3 reconstruction check. Old scripts and logs
were preserved.

The current canonical edge3 sampling/lift claim was actually read after
these diagnostics. Its fresh review is same-family/provisional and proves
the scoped sampling/lift, not the complete 682 bound. Parallel15's current
parameter has Root exact replay and mathematical validity; the generic
projection semantic review remains separately pending as previously stated.
