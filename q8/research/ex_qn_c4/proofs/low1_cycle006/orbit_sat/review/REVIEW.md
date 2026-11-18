# Cycle006 independent review: unique-degree-one Q6 theorem

Date: 2026-11-07. **PASS for the mathematical reduction, complete counterexample cover, all eleven actual CNFs, and all eleven freshly replayed final-empty RUP certificates.** There is one nonblocking **WARN** about the old checker's treatment of malformed lines, recorded precisely below. The new certificates independently pass a different, strict-parsing checker and are not dependent on that behavior.

The resulting theorem is L1: a C4-free Q6 whose specified parity has exactly one degree-one vertex and whose other 31 specified-parity vertices have degree at least three has specified-parity three-star sum at most 158. The opposite parity is unrestricted. This is now supported as a computer-assisted theorem relative to the explicit historical unique-degree-two star158 import. Its already reviewed Q8 application excludes the remaining degree-two parity profile of a hypothetical 687-edge C4-free Q8. It does not exclude degree three, prove a Q7 J bound, or prove a new unrestricted Q8 bound.

This is an independent local mathematical review from the same model family, with provisional assurance. It is not cross-model certification, a canonical whole-proof audit, Lean verification, or a fresh replay of the historical unique-degree-two certificate family.

## Read scope and execution

Read full `PROOF_DOMAIN.md` and `run_cases.py`; processed all fields of `COVER.json`, including 160 faces, 10 labelled orbit sets, 11 case records and 192 edges. Independently parsed and reconstructed all clauses of all eleven actual CNFs. Read and bound the final `RESULTS.json`, all per-case result JSON, checker stdout receipts, and actual input/proof/log hashes. Both the author's stored receipts and the reviewer's separate replay reached a final checked empty clause in every case.

Read the entire actual `audits/q7/replay/check_rup_cached.cpp` and the relevant historical `audits/q7/AUDIT.md` statements about its operation and prior scope. The latter reports two fresh historical-trace replays and nineteen historical imports; none of those twenty-one old traces was rerun for this review. Also read and exercised the ten small checker countertests and their expected outcomes. Reused the previously reviewed cycle005 hard-case reduction and unique-degree-two import at their exact scope; their sources are hash-bound in the receipt.

The reviewer's writes are confined to this `review/` directory. No SAT solver was run by the reviewer. The mathematical producer, mathematical manuscripts, original proofs, historical checker and shared records were not modified. All tools finished; no process remains running.

## Mathematical audit

### Initial reduction and hypotheses

The specified parity has 32 vertices. The exceptional root has degree one, while every other vertex on that parity has degree 3,4,5 or6. The other parity has no degree restriction. In a C4-free cube, two full three-stars of the same parity in the same Q3 force a retained square, so S<=160. Hence a violation of S<=158 is exactly S159 or S160.

If a missing edge at the degree-one root can be added while preserving C4-freeness, the resulting graph has exactly one degree-two vertex on the specified parity and all other specified-side degrees unchanged. The exceptional cubic star contribution remains zero. The historical one-sided unique-degree-two theorem gives S<=158 for this larger graph and therefore for the original graph. Consequently in a counterexample all five missing root edges are blocked. Their unique possible blockers use the root's sole retained edge; they force its neighbor to be full and the five remote square edges to be retained. A single simultaneous cube translation/direction permutation sends the exceptional root to 0 and its retained edge to 0--1, relabelling the specified parity as even if necessary. This preserves every graph and marking relevant to the argument.

### New two-edge replacement and all thirty units

For distinct i,j in {1,...,5}, delete 0--1 and add 0--2^i and 0--2^j. Since the starting graph is C4-free, every new C4 would contain a newly added edge and hence the root 0. The modified root has exactly these two edges, so the only possible new square is the coordinate i,j square through 0. It exists precisely if both remote edges from 2^i and 2^j to 2^i+2^j are retained.

If either remote edge were absent, the modified graph would be C4-free, have one degree-two even root and all other even degrees unchanged, and have the same S because binom(1,3)=binom(2,3)=0. The historical unique-degree-two theorem then contradicts S>=159. Thus both remote edges must be present in any counterexample. Varying the pair i,j forces twenty edges. The old blockers involving direction zero force the remaining ten. Together these are exactly the thirty edges between Hamming layers one and two. No degree change on an odd vertex invalidates the import because its opposite parity is unrestricted.

This does not infer that a general root switch is harmless; it identifies and checks its only possible new square. Our independent finite check examines all 427 C4-free Q3 edge subsets having the root's sole edge in direction zero. All 332 cases with at least one absent remote edge permit the replacement; the other 95 produce exactly the indicated new-square obstruction. The even star sum is unchanged in every case.

### Full-root restriction only in the single-hole cases

For ordinary specified-side degrees 3,4,5 the cubic binomial is 1 modulo3; for degree6 it is 2 modulo3. The exceptional root contributes zero. Therefore S is congruent to 31+c6 modulo3. At S=159 this implies c6=2 modulo3.

Distinct full even roots have Hamming distance at least four: equal roots are not distinct, and distance two would retain their common square. For r full roots, pairwise distance summation gives 4*binom(r,2)<=6*r^2/4; for r>0 this yields r<=4, also trivially true at r=0. Thus the only allowed residue is c6=2. The producer imposes it only in the S159 cases. It does not improperly impose the same count in S160.

### Ten marked hole orbits and complete cover

The root 0 and sole retained direction zero stay distinguished. Every permutation of coordinates 1,...,5 preserves these markings and all thirty forced layer units. Its action on the whole cube, not independent actions on different faces, is used.

A Q3 face is determined by its free mask and fixed base. If coordinate zero is fixed, its fixed value c is 0 or1; among the other two fixed coordinates, the number t of ones is 0,1 or2. This yields six orbit types, each of size C(5,3)C(2,t). If coordinate zero is free, the remaining three fixed coordinates have t=0,1,2,3 ones, giving four orbit types of size C(5,2)C(3,t). A permutation can map the free, fixed-one, and fixed-zero groups separately, so these statistics are sufficient for transitivity as well as invariant.

The orbit sizes, in the delivered order, are 10,20,10,10,20,10,10,30,30,10. They are disjoint and sum to160. The independent implementation checks the actual images of each representative under all120 coordinate permutations, verifies all labelled membership sets and the preserved root/layer markings, and checks that every Q3 appears exactly once.

By star injection, S159 means exactly one actual even-parity hole and S160 means no hole. In the first case one simultaneous permutation carries that hole to the representative of one of the ten orbits without losing the other constraints. In the second case no hole normalization is necessary. The full160 case plus ten single-hole cases therefore cover every counterexample. There is no omitted hole position, artificial relative-root placement, or circular use of L1 itself.

## Actual input reconstruction and semantics

The independent code in `check_inputs_fresh.py` imports no producer code. It generates edges as pairs of vertices of Hamming distance one and squares from same-parity opposite vertices, independently of the producer's coordinate-square loop. It validates the full face/indicator map and rebuilds the complete clause multiset for every case, including all duplicate multiplicities. It verifies DIMACS bounds, exact clause counts and all published CNF hashes.

All cases have 192 edge variables, 240 negative square clauses, six normalized root-edge units, thirty positive layer-one/layer-two edge units, and 31*15=465 positive four-edge clauses for specified-side degree at least three. A degree <=2 has four absent edges and violates one such clause; degree >=3 meets every four-subset. No clauses impose a minimum on the opposite parity.

There are 640 actual even three-star indicators. Each is equivalent to the AND of its three coordinate edges by three forward and one reverse implication clauses. The all-star full160 case then adds one four-star OR per face: 832 variables, 3461 clauses. For a single prescribed hole, its one OR is replaced by four negative star units, while all other faces keep their OR. These assertions express exactly the designated hole when C4-freeness supplies at most one star per face.

Each S159 case further adds 32 full-degree indicators, exactly equivalent to their six incident edges all being present. At least two is imposed by the 32 clauses each omitting one of the 32 indicators: zero true indicators violates all, one true indicator violates the clause omitting it, and at least two meets every clause. At most two is imposed by all C(32,3)=4960 negative triples. The resulting single-hole inputs have 864 variables and 8680 clauses each. All Boolean degree/AND truth tables and all 33 possible indicator cardinalities were checked independently.

Thus the input equivalences are exact where claimed, and every normalized actual counterexample extends to a satisfying auxiliary assignment of at least one delivered CNF. Coverage is the required direction for an exclusion; no realizability assumption on arbitrary Boolean auxiliary settings is used.

## Checker review and fresh certificate replay

The old checker propagates original units once, simplifies using those consequences, and validates each addition by reverse unit propagation before inserting it. Original axioms remain available. Its optional history fallback contains only original clauses and strictly earlier verified additions; restoring such consequences is logically sound. Final acceptance requires a validated empty clause. Its implementation is not formally verified, and its parsing has the local warning below. All eleven current stored receipts report zero history fallbacks.

Because these new certificates are small, a different direct replay was warranted and inexpensive. `direct_rup.cpp` performs an ordinary full scan of clauses to unit-propagation closure for each candidate's negation. It uses no cached assignment, watched literal, deleted-clause state or historical fallback. It retains all original clauses and already checked additions, so ignoring deletion records is sound: all retained additions are consequences established before the current check. It rejects malformed line termination, out-of-range literals, missing terminators, and content after the terminating zero. An empty clause is accepted only after unit propagation actually reaches contradiction.

`replay_new_cases.py` binds each actual CNF and proof to the final result records and checks each of the eleven traces with this independent executable. The exact freshly checked addition counts are:

| Case | Checked additions |
|---|---:|
| full160 | 882 |
| hole159_00 | 1277 |
| hole159_01 | 1180 |
| hole159_02 | 1127 |
| hole159_03 | 933 |
| hole159_04 | 1166 |
| hole159_05 | 1201 |
| hole159_06 | 642 |
| hole159_07 | 1240 |
| hole159_08 | 868 |
| hole159_09 | 1171 |
| Total | 11687 |

Every new trace's last line is the empty clause `0`; all preceding lines were parsed, deletions were explicitly ignored, and every addition was independently checked. Every direct replay returned zero with `valid=true` and `final_empty_clause=true`. The counts match the author's checker receipts one by one. The final independent replay took about0.86 seconds in aggregate; this timing is incidental and is not a performance comparison. The initial and final runs used the same mathematical checker; the final repeat only corrected countertest summary wording so it would not call the old parser mismatch a pass.

The ten historical small fixtures were used only as countertests, not as proof imports. The new checker meets all ten declared expected outcomes; the old executable meets nine and differs on the malformed embedded-zero case below. Actual raw outputs are saved in `CHECKER_COUNTERTESTS.json`, `FRESH_REPLAY.json`, per-case `.direct.stdout/.stderr`, and `replay_new_cases.stdout.txt`. The full reconstruction result and stdout are also preserved. The old historical proof families were not rerun.

## Issue register

**C006-01 — UNDERSTATED / LOCAL / certificate-parser interface — WARN, nonblocking for this proof.**

- Exact location: `audits/q7/replay/check_rup_cached.cpp` lines64 and76; `audits/q7/replay/rup_small_tests/embedded_zero.drup` and its `cases.json` expectation.
- Statement/problem: the old checker stops parsing a clause line at its first zero and ignores subsequent tokens. The fixture contains `1 0 -1 0` on one line and is declared expected=false, but the current executable returns accepted=true.
- Why problematic: this contradicts the fixture's strict line-format rejection contract. It is not a demonstrated unsound UNSAT inference: that toy input has contradictory original units and is itself unsatisfiable. The mathematical RUP soundness for well-formed inputs is not disproved by this example.
- Counterexample: yes, to malformed-line rejection; no counterexample to the claimed theorem or a valid-input RUP inference was found.
- Downstream effects: the old checker alone must not be described as passing all ten negative/positive interface tests or strictly validating such syntax. This warning does not affect the eleven present exclusions, whose actual inputs were reconstructed and traces independently replayed with strict parsing through their terminal empty clauses.
- Minimal fix: in a separately authorized checker-maintenance change, reject additional tokens after a clause terminator and rerun the small parser fixtures. No shared checker edit was made here; independent strict replay supplies the concrete present-task remedy.

No INVALID or UNJUSTIFIED mathematical issue remains in the star replacement, orbit coverage, cardinalities, model inputs, or actual certificate chain. All local hypotheses and declared proof dependency interfaces have been covered. The historical unique-degree-two theorem remains an explicitly accepted imported leaf, not a newly replayed one.

## Established consequence and scope boundary

The complete counterexample cover and eleven checked contradictions establish L1 relative to that import. In its reviewed Q8 caller, the unique remaining degree-two parity has h8=22. Ninety-nine Q6 faces receive the old star158 bounds, twelve receive the now established L1 bound, and the last face has a nonnegative hole count. Therefore 10h8>=2*(99+12)=222 contradicts 220. This conclusion permits arbitrary allowed low degrees on the opposite parity, so it excludes degree two globally in a hypothetical 687-edge C4-free Q8. Existing degree-zero/one exclusion then gives global minimum degree at least three in that hypothetical graph.

There is no limiting argument, probability calculation, asymptotic estimate, or induction in this chain. Finite boundaries, all marked coordinate transformations, both inequality directions, and all eleven cases were checked. No claim about degree-three removal, J>=73, or a new unrestricted extremal bound is made here.
