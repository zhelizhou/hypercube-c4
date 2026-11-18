# Fresh bounded review of the maximal-only vertex-frequency cone

Reviewer-Model: unknown (host did not independently attest the actual model).

The parent resolved the requested route as Codex native, host-default `gpt-6.1-sol`, requested effort `ultra`. This is a completed fresh nonauthor substantive review, classified **same-family / provisional**. Requested model and effort are not actual-identity evidence. An independently attested cross-family acceptance gate is **REVIEW_UNAVAILABLE**. This identity limitation is separate from the exact finite computations below.

**Substantive verdict: PASS for the declared bounded package.** I found no FATAL, CRITICAL, MAJOR or MINOR mathematical issue and no required canonical-source repair. All 29 extracted semantic obligations close. The 25 frozen source units were read, all are accounted for, and the semantic dependency graph is acyclic. Source-unit coverage by itself does not establish mathematical completeness; the derivations and independent checks below supply the substantive assessment.

The result is a necessary restriction for every inclusion-maximal C4-free spanning subgraph of Q8, with the same actual lambda, parity alpha, and empirical vertex gamma. It includes complete finite pricing, nine RLT consequences, and exact separation of the saved normalized abstract tuple. It does not prove the main 682 upper bound, profile-list completeness, a maximal-counterexample reduction, a Q6 import, graph realization, or infeasibility of the full augmented model. Those remain outside this review.

## Inputs and independence

I read the entire canonical `PROOF.md` (MV01–MV06 and caller contract), all of the core `main.tex`, the complete `price_domain.cpp`, `price_point.py`, and `check.py`, and the actual vertex-state, normalization, and G02 sampling import in `../finite8_flags/main.tex`. I inspected the existing mask/vertex coefficient interface in `finite_flags.py`, but **the independent verifier imports none of that code**. I read and reconstructed the actual two final Q/B cuts, their saved point, their exact oracle records, all nine RLT kernels, the supplied actual edge lists, and the actual empirical gamma data. The source-unit receipt gives precise spans and hashes.

`independent_check.py` is newly written reviewer code using only the Python standard library. It uses separator-subset stars-and-bars enumeration instead of the producer's recursive group assignment, scores all 81 ordered entries using arbitrary-precision integers, and reconstructs local true moment matrices from cube geometry instead of importing folded coefficients. It rebuilt the native oracle to `review/price_domain` with C++17 and undefined-behavior sanitization. It neither imports an optimizer nor starts an LP. The parent's earlier independent result was not used as a premise, and no previous proof-audit verdict was used to close an obligation.

All files outside `review/` were read-only. The verifier hashed the frozen package before and after its work and checked equality. The original manifest matches. `INPUT_HASHES.json` preserves the whole frozen package inventory and relevant external source hashes; the audit JSON lists the declared proof/check inputs separately. No Goal, wiki, canonical proof, numerical LP, old job or prior receipt was altered. No child agents were started. No TeX, HTML or Lean work was required or claimed.

## MV01: marked states and the maximality gate

The state convention is consistent throughout. For a square rooted at v, the first two edge bits are exactly the two incident edges at v. Interchanging axes swaps bit positions 0/1 and 2/3 and preserves v. The 15 nonfull masks have the nine representatives `(0,1,3,4,5,6,7,12,13)`. Counting the incident retained bits gives the stated state-ID groups I0=(0,3,7), I1=(1,4,5,8), I2=(2,6). Therefore X0, X1 and X2 count direction pairs containing respectively zero, one and two of the d retained incident directions and equal `C(8-d,2), d(8-d), C(d,2)`.

Every hypercube C4 uses exactly two directions: in a closed walk every coordinate is flipped an even number of times, and a simple four-cycle cannot use just one direction. Fix a missing ambient edge from v in direction i. Inclusion-maximality implies that adding this edge creates a C4 containing it. Consequently some direction j supplies the other three retained square edges. At the marked root this is mask 14 if i is first, or mask 13 if i is second. Both have state ID 8.

Each state-8 square has exactly one missing root direction. Mapping the square to that direction is well defined; maximality makes the map surjective onto the `8-d` missing directions. A single square cannot cover two different missing root directions. This proves `x8 >= 8-d`; it does not assume a unique completion. Multiple squares completing the same edge are allowed.

At d=0, the I1 group has total zero and therefore x8=0, contradicting the gate. At d=1, X1=7 and the gate requires x8>=7, so x8=7 and every other I1 coordinate is zero. There is no density, edge-count or Q6 hypothesis hidden in these arguments.

Root transport is also sound. An ambient cube isometry maps the marked vertex to the new marked vertex. When both local squares take their own marked vertex as 00, the induced change is only a possible exchange of axes. It is not a free local root translation. The geometric checker tested all 384 Q4 isometries on all 15 nonfull square patterns (5,760 rooted transports). As a negative check, masks 7 and 14 are equivalent after moving the marked corner but have different root-preserving state IDs; conflating them would change the incident-edge groups.

## MV02: finite domains and coverage

For d=1,...,8, subtracting `8-d` from coordinate 8 maps the refined domain bijectively to weak compositions with group totals `C(8-d,2), (d-1)(8-d), C(d,2)` and lengths 3,4,2. The inverse adds `8-d` to that coordinate. Nonnegativity, all three sums, and the gate are preserved in both directions. Each group is independent, so stars and bars proves the product formula.

The independent verifier traversed **all 674,172 original histograms**, constructing weak compositions from separator subsets, and then directly applied `x8 >= 8-d`. It obtained these refined counts, with no duplicates:

| Degree | Refined count |
|---:|---:|
| 0 | 0 |
| 1 | 253 |
| 2 | 22,848 |
| 3 | 75,504 |
| 4 | 89,180 |
| 5 | 50,050 |
| 6 | 13,728 |
| 7 | 1,848 |
| 8 | 29 |
| Total | 253,440 |

The native recursion fixes every preceding coordinate once and then determines the final coordinate from the remainder. Its three groups have distinct coordinates, and the coordinate-8 shift is removed after each score. Hence it enumerates the same product exactly once. There is no degree-zero generator or finite degree-zero minimum. The zero-degree record has count 0, minimum null, witness null. The d=1 and d=8 boundaries are both retained; no strict inequality or positivity assumption silently excludes them.

## MV03: common actual objects and normalization

The vertex part of the imported G01–G02 identity can be checked directly without any PSD premise. At a global vertex, there are 28 direction pairs. For each fixed pair A, precisely 15 choices of B are disjoint, 12 overlap in one direction, and one equals A. This gives the probabilities 15/28, 12/28 and 1/28. A pair with union of size 4,3,2 lies in exactly 1,5,15 four-axis sets respectively. The verifier checked these multiplicities for all 28² ordered pair choices.

A convenient ordered-entry proof also checks every denominator. Let U(K) be `2*64512` times the true local vertex moment matrix. At each local marked vertex, add 48 to `(etaA,etaA)` for each of the six direction pairs; for each ordered distinct pair add 720 at `(etaA,etaB)` when disjoint, or 144 when overlapping. This is exactly the stated local functional: after division by 129024, an unordered disjoint term has coefficient 30/2688, an unordered overlap term 6/2688, and an equal term 1/2688.

Fix a global marked vertex and ordered A,B. Summing U over all coordinate Q4 restrictions contributes 720 for that ordered pair in every case:

- disjoint: one completion, coefficient 720;
- overlap: five completions, each coefficient 144;
- equal: fifteen completions, each coefficient 48.

Thus, universally,

`sum_K U(K) = 720 sum_v x_v x_v^T`.

There are 1120 restrictions, and `1120*129024/720 = 256*784`. Dividing gives exactly

`M5(lambda) = (1/256) sum_v x_v x_v^T/784`.

This is an identity of symmetric matrices; pairing it with any symmetric Q is valid, including indefinite Q. PSD was used in the larger imported family for a different nonnegativity conclusion, and is not needed for this algebraic identity. The root-preserving state convention and collision terms are unchanged.

The folded/true-matrix distinction is correct. If c is the upper-coordinate coefficient with denominator 64512, then Uii=2cii and Uij=cij off diagonal. Ordered trace pairing divides by `2*64512`; it therefore equals the upper-coordinate c pairing divided by 64512. Similarly, generators paired with Q's upper triangle have diagonal `xi²/784` and off-diagonal `2xi*xj/784`. The independent pairing used true ordered matrices and detected a deliberately doubled off-diagonal interpretation.

Define gamma from the actual 256 vertices. MV01 puts each actual histogram in its correct refined domain. Partitioning the actual vertices proves nonnegative gamma, the displayed moment decomposition, and degree mass Nd/256. The two actual parity classes each have 128 vertices. Giving their degree-profile point masses weight one-half yields `sum alpha_p*n_d(p) = Nd/2`; dividing by 128 matches Nd/256. These constructions use the same actual H. There is no independent choice of lambda or alpha and no claim that an arbitrary gamma-cone point has a graph realization. Each rank-one generator is PSD, which proves only the stated necessary PSD implication.

## MV04: universal cut and exact implementation

For every actual vertex, the priced hypothesis says `x_v^T Q x_v+B_d >= 0`. Multiply by `1/(256*784)` and sum over vertices, or equivalently multiply each histogram inequality by gamma/784. The verified bridge and parity-profile identity give MV04 with exactly the denominator `128*784`. This discharges every application hypothesis: maximality supplies domain membership, the same actual objects supply the shared moments/masses, and Q is symmetric. No averaging inequality is reversed.

Every nonempty refined domain is finite, so `B_d=-min x^TQx` is a valid integer bias for d=1,...,8. B0=0 is a convention because degree-zero actual mass is zero; it is not an invented minimum on an empty domain. Any positive common rescaling preserves the inequality.

The native score is exact for every accepted int64 Q and bias. Since xi>=0 and sum xi=28, the sum of absolute ordered quadratic terms is at most `28²*2^63`. Including bias gives at most `785*2^63 < 2^73`. The casts occur before multiplication, so both INT64_MIN and the largest positive int64 are safe in signed 128-bit arithmetic. The upper-triangle implementation doubles an off-diagonal term before multiplying xi*xj, which is also far within this bound. Conversion to decimal only encounters scores of this size and therefore does not negate the minimum signed-128 integer.

I rebuilt the oracle with `-fsanitize=undefined -fno-sanitize-recover=undefined`; all executed cases passed without sanitizer diagnostics. All 253,440 rows were independently scored for the final master050 query, the generic smoke query, the producer's dense int64 query, and a newly generated independent dense query using both int64 endpoints and arbitrary full-size entries with nonzero biases. Every degree minimum and witness matched. The repaired degree biases were submitted to the native oracle as nonzero input and yielded exactly zero minimum in every nonempty degree. Default zero input worked. Constant all-INT64_MIN and all-INT64_MAX queries with matching nonzero biases gave the analytically known score `785*entry` in every nonempty degree.

Parser checks rejected missing/extra tokens, overflow/underflow, decimal fractions, trailing characters, a bare minus, hexadecimal spelling, nan, asymmetry, an unreadable query path, and too many paths, before emitting any successful oracle output. Accepted query spelling follows the C++ decimal `from_chars` convention. These implementation checks supplement the coverage and arithmetic proof; no finite test set alone is being used to assert correctness for all Q.

## MV05: all nine RLT consequences

The stated l vector has coefficient -2 on I0, -1 on I1 except state 8, coefficient 6 on state 8, and zero on I2. Hence

`l^T x = 7x8-2X0-X1`.

Because `2X0+X1=(8-d)(7-d)+d(8-d)=7(8-d)`, this equals `7[x8-(8-d)]`, which is nonnegative on the refined domain. For every i, xi>=0 gives `x^T(e_i l^T+l e_i^T)x = 2xi*l^Tx >= 0`. Apply the universal cut with zero biases. Symmetry yields `tr(Q^(i) M5)=2(M5 l)_i`; all nine componentwise inequalities follow. Every stored matrix equals the displayed formula entry by entry. The full domain traversal checked the l identity and nonnegativity; both actual graphs satisfy every RLT row. These nine inequalities are not asserted to characterize the cone or to separate the current parent point.

## MV06: concrete cuts, actual graphs and caller

The saved master050 Q and B were reconstructed from their actual files. The fresh native output is identical to the saved final oracle output, and independent full-domain minima give precisely the repaired biases. The same checks pass for the recorded one-round generic CLI cut.

For the saved input, I parsed the actual decimal weight tokens through Decimal and Fraction, rather than using the producer's coefficient routine. All 403 distinct positive-weight local masks are legal C4-free Q4 graphs. All 1409 positive alpha rows have nonnegative integer degree counts summing to 128. The raw lambda and alpha totals are close to, but not exactly, one. I normalized each separately exactly as the stated certificate defines. The resulting degree-zero mass is exactly zero. This verifies the certificate's defined rational target; it does not claim that rounding preserves every other parent equality exactly.

Rebuilding all local ordered vertex matrices and pairing the exact weights gives the stated unnormalized value:

`-92743804234666487401677529556778857677932718514926730169 / 1045333333028001957869374093250655798339702778054401920`.

After division by positive normalization 1,000,000 this is strictly negative and approximately -0.0000887217515259. The separately recorded generic CLI cut has its own exactly negative pairing, also independently reproduced. `PAIRING_RESULT.json` retains both exact local and bias contributions, normalizations and degree masses. This separates those defined abstract maximal-scope tuples; it is not a graph counterexample or a whole-model NO certificate.

Both literal actual graphs were independently checked for ambient edges, no duplicates, C4-freeness, and a three-edge completion for every missing ambient edge. At all 256 roots their histograms satisfy the exact group sums, maximality gate and nine RLT rows. The empirical gamma files match every independently reconstructed histogram and multiplicity. All 1120 actual coordinate Q4 restrictions were rebuilt, and all 81 entries satisfy the universal integer moment identity.

| Graph | Degree counts N0,...,N8 | Gamma columns | Missing edges | Minimum gate slack |
|---|---|---:|---:|---:|
| 682-edge seed | (0,0,0,0,2,168,86,0,0) | 8 | 342 | 7 |
| 576-edge maximal graph | (0,2,14,42,70,70,42,14,2) | 182 | 448 | 0 |

The missing-edge completion-count histograms also agree exactly with the proof. The second graph has actual leaves and attains equality, so it directly tests the non-strict degree-one boundary.

The empty spanning graph gives x=28e0 and violates `x8>=8`; its Q^(0) expectation is exactly -4. At root 0 of the single-edge graph {(0,1)}, d=1 and x=(21,7,0,...,0), violating x8>=7. Both are actual C4-free nonmaximal graphs. These are confirmed counterexamples to dropping the maximality hypothesis, not counterexamples to the stated theorem.

I inspected the complete generic caller. The generator upper-coordinate normalization agrees with the target's folded upper-coordinate normalization. Proposed integer Q is fully priced; biases are repaired from exact minima; only the resulting exact rational negative pairing causes CUT_FOUND. Warmstart rows can affect search proposals, but never bypass complete final pricing. A no-cut outcome is correctly reported as inconclusive. The recorded 33-round history and all 33 query/oracle file pairs are present; the one-round CLI replay uses the same frozen point and its accepted cut is independently validated. I did not rerun the discovery LP, reprice every intermediate history row, or validate elapsed-time measurements as portable performance claims; none is a premise of the universal cut or final separation.

`cli_contract_check.py` additionally exercised five early rejection paths without starting an LP: round count 0, round count 81, existing history, a changed existing input snapshot, and positive degree-zero target mass. All rejected with the documented diagnostic and wrote no query or accepted cut. The caller's schema is the stated existing saved-point schema; no stronger general-purpose input-validation claim is needed.

## Mandatory global and adversarial checks

- **Definitions and typed symbols:** Root-preserving state order, actual/abstract weights, folded c, true U, M5, degree masses, and the empty domain are consistent. No symbol drift affecting a result was found.
- **Hypothesis discharge:** Every substantive application is listed in `OBLIGATION_LEDGER.json`. Maximality is retained for the gate and all cuts. The actual-object construction retains common lambda/alpha/gamma. Parent profile coverage and edge-count reduction remain explicitly outside the theorem.
- **Inequalities:** The maximality surjection, weighted nonnegative sum, PSD outer products, positive normalization and RLT implications all have the correct direction. Negative rational separation is established by exact arithmetic.
- **Interchanges and probability modes:** Every expectation is an average over a finite explicitly counted set. Only finite sums are rearranged. No limit, derivative, integration, convergence-mode or measurability issue occurs.
- **Uniformity and constants:** There are no asymptotic statements. The int128 bound is uniform over the complete int64 input range and every domain row. The 8-dimensional cube is fixed.
- **Boundary and counterexample pass:** d=0 empty, d=1 pure mixed-state boundary, d=8 zero-missing-edge boundary, zero kernels, indefinite kernels, full-range signed inputs, nonzero biases, empty/nonmaximal actual graphs, and genuine maximal leaves were covered. No counterexample within the declared maximal scope was found.
- **Dependency and global closure:** The source-to-obligation ledger has no cycle. Statement and conclusion agree. The TeX core restates the canonical restrictions faithfully. The final proof requires no author's PASS receipt, floating LP convergence, graph-realization converse, or parent goal completion.

Mutation checks deliberately changed a degree minimum, supplied an invalid witness, assigned a fake finite degree-zero minimum, doubled true off-diagonal entries, removed collision contributions, and conflated marked-root positions. Each produced a detected inconsistency or an explicit geometric contradiction. These confirm that the independent checks respond to the principal failure modes rather than only reading producer PASS labels.

## Artifacts and disposition

`PROOF_AUDIT.json` is the machine-readable substantive PASS with explicit provisional/identity-unattested fields. `RECEIPT.json` accounts for all source units. `OBLIGATION_LEDGER.json` and `PROOF_SKELETON.md` give the semantic DAG, hypotheses, typed symbols and discharges. The newly written `independent_check.py` and `cli_contract_check.py` retain reproducible checks; their result files preserve exact finite outputs. `REVIEWER_IDENTITY.json` records the route limits. No canonical repair is requested. Root alone may integrate this scoped result and decide how to represent the provisional review in canonical task records. The main 682 objective remains OPEN.
