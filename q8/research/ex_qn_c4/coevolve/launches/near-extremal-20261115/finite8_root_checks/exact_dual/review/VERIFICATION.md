# Independent deterministic-local verification of exact scientific-row reconstruction

**Outcome.** No substantive mathematical or arithmetic defect was found in the current `reconstruct_exact_dual.py` on the actual frozen B3 and B8 inputs. Independently reconstructed scientific maps and exact coefficients agree entry by entry. B3 fails the strict sufficient criterion. B8 satisfies that criterion on the supplied B-domain interface. This report is a local verification, **not** the canonical proof-checker acceptance of a complete B-case manuscript and **not** a proof of `ex(Q8,C4) <= 682`. The original Goal remains OPEN; the m683 case and original-object/profile-cover imports are separate obligations.

This agent read and followed the deterministic-local branch of `mathrsi-verify/SKILL.md`. No proof-checker, canonical audit JSON, wiki claim, Goal change, child agent, historical research job, or source edit was made. Every write was within this `review/` directory. The requested route was `{backend:codex, host:codex, source:host-default, model:gpt-6.1-sol, effort:ultra, transport:native, fresh_tool:spawn_agent, continuation_tool:send_input}`. That is requested configuration, not an attestation of actual model identity or effort; the same-family semantic review remains provisional.

## Actual execution and independence

The independent implementation is `independent_audit.py`. It imports NumPy/SciPy from the task-local dependency directory, but imports **neither** `reconstruct_exact_dual`, `finite_flags`, `edge_flags`, nor `lift`. It reconstructs legal full flag states, common square actions, root stabilizers, vertex states, literal cube geometry, every current finite generator, all scientific integer arrays, and the rational combination directly. It reads `DUAL_EL/ER` only after scientific reconstruction for a labelled floating diagnostic. Their agreement is not the definition or validity argument.

The complete scientific arrays were compared exactly with the frozen scientific exports, not only with floating solver maps. All checks completed with exit 0:

| Scope | B3 | B8 |
|---|---:|---:|
| Actual local graph library | 15125 | 15152 |
| Packed coordinates per graph | 101801 | 101801 |
| Scientific equalities rebuilt | 356 | 356 |
| Complete finite alpha/beta columns | 645 / 1751 | 645 / 1751 |
| Nonzero exact inequality weights | 58 | 83 |
| Exact coefficient differences | 0 | 0 |

For each library, the implementation rebuilt the **entire** sparse packed F matrix from literal Q4 geometry, the entire 64-by-library edge upper moment matrix, and all five histogram coordinates. Every integer entry matched. Thus the scores of all15125/B3 and all15152/B8 graphs were independently reproduced, with integer min/max respectively `[-130544252914848,28704]` and `[-204971339704320,-37440]`.

All356 scientific equality maps were additionally materialized as exact integer matrices with common denominator36126720 in `independent_B*/independent_EL_integer.npz` and `independent_ER_integer.npz`. These matrices come from the independent scientific construction. The maximum differences from the native floating exports were at most8.89e-16 and4.45e-16, reported only as diagnostics.

`INDEPENDENT_RESULT.json` under each `independent_B*/` records every finite check, exact extrema, scalar result and scientific-input hash. `FINAL_CHECKS.json` records source/binary/query bindings and the actual command ledger. Raw stdout/stderr files are retained.

The ledger preserves commands as actually executed. For another replay choose a fresh `--output` directory (and a fresh producer output directory); the deliberate existing-output rejection protects these records.

## Exact sign and scientific row derivations

Write the actual inequalities as `g_r(x)>=0`, and their LP rows as `A_r=-g_r`. Equality rows are `Ex=b`. Parsing each decimal token as an exact rational, the independent code rounds to denominator `Dy=10^9`, choosing unrestricted `y` and `z<=0`. Hence

`a = yE + zA = yE + (-z)g`, and every actual admissible x obeys `a.x >= y.b`.

The code's comment uses this sign correctly. Arbitrary rounding of y and nonpositive z changes the candidate but never needs solver optimality, a feasible primal point, or the sign of the floating residual. Here `delta=(y0+y1)/Dy`, since only the lambda and alpha normalization rows have RHS1. Beta is an empirical probability vector on1024 ambient edges even though a separate redundant beta-normalization row was omitted in the discovery LP.

The independent rebuild uses exact Python integers/object arithmetic. Its common denominator is `551690954352885760000000000` in both cases. Every one of the101801 packed kernel numerators, five histogram numerators,645 alpha numerators and1751 beta numerators equals the producer's corresponding exact numerator, with that same denominator.

The following normalizations were derived from actual scientific source and checked against integer arrays:

1. Rows0–6: lambda/alpha mass, then degree-histogram sampling. For a128-vertex parity profile n, the numerator for local degree j is `sum_d n_d C(d,j) C(8-d,4-j)`, with denominator `128*C(8,4)=8960`. The local histogram has denominator16. All645-by-five numerators match. The lambda constant is represented exactly by adding the same `64512*y0/16` to all five histogram weights, using the universal sum16.
2. Rows7–70:64 actual edge **matrix upper entries**. Generator numerators are `x_i*x_j+x_flip(i)*x_flip(j)` with denominator98. Local U has diagonal twice the folded coefficient and off diagonal once, with denominator129024. An equality multiplier therefore corresponds to an edge symmetric kernel with diagonal `2*y`, off diagonal `y`, evaluated at half the usual packed functional. Independently expanding `V_g=6e_external+e_base` and endpoint averaging yields the face numerator over392 for that edge kernel; the extra half makes the reconstruction denominator784. This is the source of784, not an unexplained extra stabilizer factor.
3. Rows71–88:18 endpoint counts are actual integer counts of the two endpoints by root retention and full degree. RHS numerator is `(d if retained else 8-d)*n_d`, with denominator512 because alpha is half the two parity profiles while beta is normalized by1024 ambient edges. Every entry was independently reconstructed.
4. Rows89–124:36 mixed-state retained-minus-missing incidence rows. The scientific equality has zero RHS; the discovery convention divides by7, which is positive and is preserved.
5. Rows125–151:27 conditional vertex group-moment rows. Independently reconstructing the162 integer incidence counts C and the three degree-group totals gives `B27 beta=392 sum_(j in group) M5_ij`. For the actual folded packed selector W, `Wf` is twice the row-group sum, so `2304 B27 beta=7 W F_vertex^T lambda`. The actual LP convention is lambda `7 WF/129024`, beta `-B27/56`, giving original packed weights **7/2**, exactly as used. Every W and B27 entry matched; an off-diagonal is never doubled twice.
6. Rows152–355:204 edge-three-flag rows. The implementation rebuilds every full-state indicator `A_z(i,j)` from all four root-square edges and both endpoint orientations, then every packed kernel `K_z=12A_z-A_z(i,i)-A_z(j,j)`. All204-by101801 entries match exactly. The pointwise identity is `T_Kz=(5/4)L_z`, so `L_z/64=T_Kz/80`. The global common-object sampling identity is `E_lambda L_z/64=E_beta H_z/70`; both the coefficient1/80 and beta denominator70 are preserved. The independent H enumerates every triple among seven actual labels, both orientations. No general tensor oracle or separate flag canonicalization is inserted.

The scripts also check the complete current raw3432 histogram order directly:1716 maximal missing-root histograms with at least one state7, then1716 retained-root histograms. The ordinary maximal leaf condition retains1486 latter histograms. The current1751 selected classes partition exactly the allowed raw3202 histograms, and **every member** of each class preserves all rebuilt moment, endpoint, C, neighbor-capacity and three-flag maps. There is no representative-only assumption or class-size multiplier.

## Validity and actual scope of selected inequalities

| Family | B3 active | B8 active | Required input and check |
|---|---:|---:|---|
| Integer PSD rays | 11 | 19 | A positive multiple of `q q^T`; nonnegative on every real root count vector. No PSD claim is made for the aggregate kernel. |
| Integer rounding | 33 | 49 | Integer q,t; actual total6 face count or total28 vertex count. |
| Global leaf | 1 | 1 | Ordinary inclusion-maximal C4-free Q8; global alpha mixture only. |
| Retained-neighbor capacity | 5 | 5 | Every C4-free Q8; ordinary degree counts and the same empirical beta. |
| Conditional vertex | 1 | 1 | Ordinary inclusion-maximal C4-free Q8; complete refined253440 domain. |
| Connector finite6 | 6 | 8 | Any actual C4-free Q8; complete54264 total-six connector histograms and all full states. |
| Full projection finite6 | 1 | 0 | B3 parallel15 parameter; complete38760 total-six small histograms, pulled back and already summed over the root stabilizer. |

For rounding, the actual symmetric entries are

`Qij=n^2 qi qj - (n/2)(2t+1)(qi+qj) + t(t+1)`.

For **any** integer total-n x, setting `L=q.x` gives

`x^TQx=n^2 [L^2-(2t+1)L+t(t+1)]=n^2(L-t)(L-t-1)>=0`.

This derivation explicitly covers n28, as well as n6; no total6-only theorem is silently transferred. All stored rounding rows have the advertised n. All selected positive power-of-two normalizations were checked positive and retained exactly.

For the selected conditional vertex parameter, an actual marked vertex of degree d has28 direction-pair states, group sums `C(8-d,2), d(8-d), C(d,2)`, and ordinary maximality forces `x8>=8-d`: each missing incident edge has a completed square, and each state8 square belongs to a unique missing incident direction. This also rules out degree0. Independently enumerating unshifted group compositions and then filtering this condition gives counts

`[0,253,22848,75504,89180,50050,13728,1848,29]`, total253440.

For the actual source `vertex_pricing/master_195/CONDITIONAL_VERTEX_CUT.json`, the independently computed degree minima of `xQx` are

`[null,-686000000,-446000000,-136000000,184000000,466000000,674000000,784000000,784000000]`.

Each nonempty-degree minimum plus its actual B_d is exactly0. The sampling identity is `M5=E_vertex xx^T/784`. Since alpha averages two128-vertex parities, `E_alpha n_d=N_d/2`; therefore the scientific degree term is exactly `B.n/(128*784)`. The active row needs **ordinary maximality**, not switch optimality, star optimality, a fixed683 density, or an A-case profile assumption.

Each selected connector source was independently checked symmetric, invariant under the actual common root stabilizer, and mapped to the actual full-state codes `f&15`. Every one of its54264 nonnegative integer total-six histograms was tested with integer arithmetic. B8's eight minima in active-row order are `240,240,112,176,56,104,66,128`; all are positive. Five later parameters originating in A work are scientifically general-six-count connector kernels, so their transfer needs none of A's alpha domain, fixed m, dual or target tuple. All actual positive LP scales, rather than the source's different discovery scale, are used.

B3's sole parallel15 projection was separately rebuilt as the full-state matrix `sum_h smallQ[Phi(h f),Phi(h g)]`; its entire187-by187 matrix equals the source `full_Q`, and its38760 small histograms have minimum28. The full matrix is used directly. There is no second multiplication by the stabilizer size4. The finite-sum pullback proof needs no label-equivariance assumption: for every full-state integer x of total6, each h transports it to another such count vector, whose Phi grouping has total6.

For the leaf row, ordinary maximality forces the unique neighbor of a leaf to have degree8; two leaves cannot share that neighbor, since the missing edge in the square through their two directions would have no completing path. Hence `N1<=N8` and `E_alpha(n8-n1)>=0`. No invalid same-parity inequality is used.

For neighbor capacity at a degree-t vertex, start with8t available incidences at its t neighbors. For each unordered pair of retained directions, the two remote edges of their square cannot both be retained. The pairs concern disjoint remote-edge incidences; hence the sum of its neighbor degrees is at most `8t-C(t,2)`. Summing over degree-t vertices gives exactly the beta numerator CAP and alpha numerator `(8t-C(t,2))*n_t`. The actual row is `CAPAL/(512*16) - CAP/16>=0`, agreeing with both scalar normalization and sign. This argument needs only C4-freeness.

The two older `FINITE6_KERNEL` rows are zero in both exact combinations. Their generic source branch reads the actual full symmetric integer Q and its positive row normalization, just as required; this report does not claim a new exhaustive verification of all historical full-state finite6 certificates. Inactive rows are unnecessary premises of either selected combination.

## Uniform all-Q4 error bound and complete maximization

For every legal labelled Q4, each folded feature coefficient is nonnegative. Independently of any library, the five face blocks together sum to

`24*8*(280+28+28)=64512`,

and the vertex block sums to

`16*(3*720+12*144+6*24)=64512`.

The five ordinary degree-histogram coordinates sum to16. Thus rounding each exact packed entry and histogram entry to scale `T=10^9` bounds the error on **every legal Q4** by

`eps=max_face|NW/D-q/T| + max_vertex|NW/D-q/T| + (16/64512)max_hist|NH/D-qh/T|`.

Nearest integer rounding also proves `eps<=1/T+8/(64512*T)`. The implementation independently computed the actual exact eps below. It does not use a floating reconstruction tolerance, a library maximum, or a sample estimate as this universal error bound.

The independent complete-oracle source `finite8_full_oracle_independent/independent_q4.cpp` was read in full. Its coverage is elementary: every legal Q4 consists of two legal Q3 layers and a set S of vertical edges; S is permitted exactly when it is an independent vertex set of the intersection of the layer edge sets. The code generates all2902 legal Q3 masks, accounts for all8421604 ordered layer pairs under simultaneous Q3 automorphisms and layer swap, and verifies orbit-cardinality coverage before processing all90179 representatives and every permitted S. This yields13150453 marked completions. Folding with a **common** root stabilizer makes the functional invariant under that subgroup, so the representative traversal covers its maximum. The count is a check on this construction, not its sole completeness premise. The witness's direct raw edge scorer, gathered scorer and fast table scorer agree; all384 full Q4 isometries are additionally checked at the witness.

B3's independently reconstructed query bytes equal the old actual-query bytes, and the current producer replay also reproduces those exact bytes. Therefore its existing independently implemented complete-oracle result was reused by exact query/source binding, as authorized. It has raw maximum61473687284 and witness2121429215. No full B3 traversal was redundantly performed in this review.

B8's independent query bytes equal the frozen B8 query bytes. This review actually ran the existing independent binary in `independent_B8/` and, additionally, **rebuilt that source into this review directory** and ran the rebuilt binary to completion on the independent query. Both finished with raw maximum **-37440**, witness146532333,13150453 marked completions and all384 witness isometries PASS. See both raw outputs. The two local queries have SHA256:

| Query | matrices | linear |
|---|---|---|
| B3 | `cd486c2604488f61865120f2b2068194a235aafdcafa44024090e541b1a8ebcb` | `a4874747363aecc6290aaa502709e89bfd61d9487c3e7ae303c39d0d2f00cbd8` |
| B8 | `1a909bcc59b9ff22c679fc0d2c0ffed6e6a145e83688053793319e746feee372` | `1c2c16f76a493f9b171a145d7748b7993b1e092a5716524f43f9d6ef03c02506` |

The separately implemented primary oracle's actual B8 output was also read at `pool_B684plus_enriched8/exact_primary_oracle001.stdout.txt` and `exact_row_combination001/own_oracle.stdout.txt`. Its input matrices/linear files have exactly the same bytes and hashes above; its completed13150453 traversal reports the same maximum-37440, with tied representative3889906149. `finalize_receipt.py` independently reconstructs the literal geometric score and C4 legality of **both**146532333 and3889906149; each score is exactly-37440. Thus the two distinct oracle implementations agree on the final exact query, rather than confusing the earlier floating-derived query's15371 maximum with this one. The second execution of a recompiled independent binary is a source/binary reproducibility check, not itself a second algorithm. This review consumed the primary oracle's actual completed result; its original complete-source/proof audit is a separate imported check.

## Exact finite extrema and sufficient criterion

| Quantity | B3 | B8 |
|---|---|---|
| delta | `18877/100000000` | `92993/500000000` |
| alpha maximum | `-75705877/293601280000000000` | `276661617/1027604480000000000` |
| alpha maximizing index | 119 | 373 |
| beta maximum | `141/490000000000` | `1/250000000` |
| beta maximizing index | 1730 | 1688 |
| eps | `12301/16384000000000` | `529874002317/601295421440000000000` |
| complete integer-query maximum M | 61473687284 | -37440 |
| `delta-Amax-Bmax-eps-M/(64512*T)` | `-2826818780018833/3699376128000000000` | `782808475930428709/4209067950080000000000` |

All finite maxima were computed from independently reconstructed **complete**645 alpha and1751 beta arrays with exact integers. Positive tiny finite maxima are correctly allowed: their separate maxima are added, rather than incorrectly requiring each residual nonpositive. The B8 margin is strictly positive. B3's negative margin is a failed sufficient criterion; its local maximizer is not a Q8 graph or a counterexample to the target.

## Current producer replay, issues and remaining obligation

This review actually ran the **current** Root script, SHA256 `fe6d93d9b0519a5039e657398bf23e6e65dc7bf46a7133a607775c21f5f28f80`, into `producer_replay/` on frozen B3. `EXACT_COMBINATION.json`, `LOCAL_PRICE_SCORE.json`, `oracle_matrices.txt` and `oracle_linear.txt` are byte-identical to the old actual B3 run. Only `RESULT.parameter_source_hashes` and runtime seconds differ. The revised source therefore has an actual replay; this report does not retroactively claim the newer hash-binding code was the version used in the original run.

No substantive source bug was found or fixed. The current exact interface's rational sign, n28 identity, scientific denominators, uniform all-domain rounding bound and failed-B3 interpretation are supported by this audit. The producer correctly labels its mechanical reconstruction as insufficient to establish universal validity of arbitrary future row parameters; new parameters still require their actual finite-domain checks and mathematical caller.

For B8 the returned result is an exact, independently reproduced strict local certificate **conditional on the supplied scientific original-object interfaces and the complete B profile cover**. This audit consumed the relevant sampling and ordinary-maximality manuscripts and rederived the normalization/selected-row implications above. It did not re-audit every historical Q6 imported theorem, profile exclusion or SAT trace. Parent verification must connect those allowed imports to both actual parity profiles and the frozen645 list, and formally review the assembled B684 exclusion manuscript. The m683 branch remains separate. No whole682 theorem, full model graph realization, accepted primal point, or generic full-family NO claim follows merely from this local report.

Relevant read imports include `finite8_flags/FINITE8_BRIDGE_AND_OBSTRUCTION.md`, `finite8_edge_flags/{lift.py,edge_flags.py,export_cones.py}`, `finite8_root_checks/{EDGE_PULLBACK.md,FINAL_CERTIFICATE_INTERFACE.md}`, `finite8_edge_vertex_bridge/PROOF.md`, `finite8_maximal_vertex_cone/PROOF.md`, `finite8_connector_frequency/PROOF.md`, `finite8_projection_cones/PROOF.md`, `pool_native_leaf_connector/LEAF_PROOF.md`, the actual B3/B8 row controllers/layouts/parameters, and the edge3 pointwise lift proof. These are ordinary/local theorem imports, not a claim of rerunning their prior canonical audits. The exact import hashes consumed for reporting are in `FINAL_CHECKS.json`.
