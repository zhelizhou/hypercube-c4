# Fresh local proof-checker review: finite-eight six-block family

Verdict: **PASS for the specified local mathematical scope**, with **same-family / provisional** semantic assurance. No FATAL, CRITICAL, MAJOR or mathematical MINOR issue was found. Author PASS receipts and the restricted numerical plateau were not premises. The deterministic checks below were actually executed in this review.

This result concerns the exact sampling bridge for every actual C4-free subgraph of Q8 and the uniform obstruction for the six kernels fixed in G01. It proves neither a Q8 counterexample nor ex(Q8,C4) ≤ 682. The original goal remains **ACTIVE/OPEN**. Adding valid global degree coupling or another flag space gives a different family; this barrier cannot automatically be transferred to that augmentation.

## Identity, boundaries and source coverage

The requested route in `../REVIEWER_ROUTE.json` is codex/native, `gpt-6.1-sol`, `ultra`. This is a fresh non-author native review leaf `/root/review_finite8_flag_family`. Actual hosting model/backend/effort is not independently observable from this leaf, so the observed identity fields are null in `RECEIPT.json`. Requested identity is not represented as observed identity. Assurance is conservatively same-family/provisional.

All writes are inside this review directory. No child was spawned, no author source or shared wiki was changed, and no old goal was resumed. `recursion: false` and `max_turns: 8` are prompt conventions, not structurally attested native-host constraints. `render_html: false` was honored. No `pdflatex` is installed, so no TeX/PDF build was performed. Mathematical acceptance here does not depend on typesetting.

I read all 593 lines of `main.tex`, all of `PROOF_SKELETON.md`, the retained `FINITE8_BRIDGE_AND_OBSTRUCTION.md`, `STATEMENT.md`, `finite_flags.py`, `verify_obstruction.py`, `certify_lp_point.py`, and the actual original MathRSI `plugins/hypercube-extremal/archive/source/certificate_final_q4/verify_local.cpp`. I parsed all actual graph masks/weights, every supplied matrix entry and every rational L/D entry from `FAMILY_OBSTRUCTION.json`. I also parsed `Q8_seed682_point.json` and its actual edge source. This reads actual definitions and transport code, rather than equating dimensions with coverage.

| Source unit | main.tex lines | Result |
|---|---:|---|
| Preface and contract | 1–53 | Covered |
| G01 | 54–209 | PASS |
| G02 | 210–304 | PASS |
| G03 | 305–357 | PASS for actual transport/import interface |
| G04 | 358–509 | PASS, independently reconstructed |
| G05 | 510–552 | PASS |
| Provenance and reproduction | 553–593 | Covered; not proof premises |

Declared source-unit coverage is 7/7. It records execution of declared source units; it does not mechanically certify discovery of every mathematical obligation. `RECEIPT.json` records hashes of actual reviewed inputs, all rechecked unchanged at emission. The obstruction hash is `fdbd082699eff6d46899d6a501945881cf6f6fed48735dd3a326c5db8080aec6`.

## G01 — States, common gauge, vertex root and normalization

The original C++ implementation fixes bottom-Q3/top-Q3/crossing mask order, connector-first full-face codes, ascending legal IDs, common canonical-root transport and the same vertex axis-swap quotient. The independent reviewer checker derives square symmetries by filtering all 24 vertex permutations for adjacency preservation, rather than copying the producer's translation/swap loop. It reconstructs actual state tables, not just their dimensions.

The five canonical root masks are 0,1,3,6,7; dimensions are 240,212,190,187,170 and stabilizer orders are 8,2,2,4,2. For a nonfull root, excluding the full translated square and all four crossing squares is exactly the rooted-Q3 legality condition. The legal flag codes are labelled states in ascending order, not separately canonicalized flag orbits.

One canonicalizing root map acts on both flags. Any alternative differs by a common stabilizer action. Averaging a PSD kernel under that action preserves PSD and makes the common frame irrelevant. The inverse/permutation convention in a congruence average causes no discrepancy because the entire stabilizer is averaged. The nine vertex representatives are 0,1,3,4,5,6,7,12,13, quotienting only interchange of two directions while preserving the marked corner. Root translation would incorrectly identify different states; the attack log gives codes 1 and 8, whose correct state IDs are 1 and 3.

I derived matrix-entry coefficients directly from normalized G01.3–G01.4, including the symmetric trace half off-diagonal. In U = 2·64512 times the unnormalized weighted moment, each canonicalizing map contributes 2240/h to both ordered face cross entries and 448/h to each diagonal. Repeated states receive both cross contributions on their single diagonal, preserving the necessary factor two. Vertex ordered-entry weights are 720/144 for disjoint/overlap pairs and 48 for equal pairs. The packed upper-coordinate functional instead has vertex weights 720/144/24 and face weights 280/28/28 times old faceval. Density gives 2016 e(K) and 64512·683/1024 = 43029 exactly.

After independent construction, every coefficient for all 818 actual graphs was compared to unchanged `finite_flags.py` in the original state order. They all agree. No PSD assumption on an individual local matrix is introduced.

## G02 — Exact finite sampling for every actual Q8 graph

At each root square, six external flags in one common gauge yield exactly (5/6) R_distinct + (1/6) diag(u) = uuᵀ. Uniform Q4/root-face sampling makes all 1792 actual root faces and all 15 choices of two external axes uniform. Symmetric cross entries and the equally weighted two diagonal entries reproduce the exact independent-direction law. The independent attack checker explicitly obtains weight 1/36 for all 36 ordered direction pairs.

At a marked vertex, two independent pairs among 28 have probabilities 15/28,12/28,1/28 for disjoint, overlap-one and equal. Local unordered counts are 3,12,6. Global ordered counts are 420,336,28; their union sizes are 4,3,2 and four-axis completion multiplicities are 1,5,15. I independently enumerated all 70 four-axis sets and every local ordered pair and verified exact weight 1/784 on each of the 784 global ordered pairs. No overlap type or collision term is approximated.

Each global vertex belongs to 70 coordinate Q4s. Each ambient edge belongs to 35 of the 1120 restrictions, so E[e(K)/32] = e(G)/1024. The other two expected contributions are empirical PSD quadratic forms, which establishes the stated inequality direction. All flags restrict the same graph and same marked roots. All probability spaces are finite: there are no limits, measure-theoretic interchanges, probability-mode upgrades, asymptotic constants or uniformity assumptions. A strict bound below 683/1024 implies the integer edge bound 682.

## G03 — Actual symmetry and common-K coverage interface

A cube isometry permutes root faces and acts by one D4 root map on both flags. Stabilizer averaging removes the frame choice; external-direction exchange preserves a symmetric cross term and equal diagonal weights. At a marked vertex its rooted-square map can only exchange the two axis labels. Signed coordinate changes preserve the marked corner in its rooted local frame. Disjoint/overlap/equal categories remain in their own classes. Thus the full new score is invariant under Aut(Q4).

The independent checker supplements this proof with exact full-matrix equality on 21 varied legal examples under all 384 cube isometries: 8064 comparisons. Sparse and randomly greedily generated examples include root types outside the obstruction support. This is finite regression, while the analytic argument proves the universal statement.

Reading the actual original C++ confirms that common K=(A,B,S) is legal precisely when both layers are legal and S is independent in A∩B. Crossing squares correspond exactly to common retained layer edges whose two endpoint crossing edges are present. The program derives the 48 Q3 automorphisms, includes simultaneous pair transport and layer exchange, checks pair orbit coverage, enumerates independent crossing sets and computes the minimum hidden-direction pair index. New score invariance is precisely the missing prerequisite to reuse those slice transports.

The historical numerical coverage 2902/90179/8421604/13150453/3312331 is retained as an explicit computational import, not a fresh enumeration performed by this reviewer. I did not rerun the old full checker or the downstream new oracle scan. Neither the bridge nor G05 relies on those totals: their domain is the defined complete legal set, and every obstruction support graph is checked directly.

## G04 — The actual rational 818-graph object

`independent_geometry.py` was written for this fresh review. It builds all geometry and matrices without importing either author checker or extractor. Only afterward does it import `finite_flags.py` for the cross-implementation comparison. It uses no optimizer, NumPy, SciPy or precomputed LP features. `INDEPENDENT_GEOMETRY_RECEIPT.json` records the actual run.

- All 818 masks are distinct integer 32-bit masks. Every integer weight is positive and their sum is exactly W = 11199999988800.
- Every graph's 24 actual coordinate squares is nonfull: 19632 legality checks.
- Face states, simultaneous gauges and vertex states are reconstructed from retained actual edges. Every full ordered-entry moment is rebuilt using the given integer weights.
- The complete matrices equal the supplied object, with 430 nonzero ordered entries. Blocks 0,2,3 are exactly zero. No omitted full-state coordinate is assumed zero without comparison.
- Supported block dimensions are 16,16,4 in blocks 1,4,5. I recomputed fresh rational LDL decompositions directly from the reconstructed matrices. Every pivot is strictly positive, the fresh L/D equal the supplied factors exactly, and every entry of LDLᵀ equals U. This proves PSD after zero extension to all original dimensions, including singular and zero blocks.
- The exact weighted edge sum is 241918020864450. Division by 32W = 358399999641600 gives 76799371703/113777777664; subtraction of 683/1024 gives 455241445/56888888832 > 0.

I also independently read the actual 682-edge Q8 seed and enumerated all 1120 coordinate Q4 restrictions. There are 818 distinct masks, with exactly the supplied multiplicities. Summing the newly reconstructed local matrices agrees entry by entry with independently built empirical outer products at all 1792 root faces with six external flags and all 256 marked vertices with 28 direction pairs. The mean restriction density is exactly 682/1024. This checks the complete common-graph bridge normalization; it does not realize the biased obstruction distribution as a Q8 graph.

As an additional replay, copies of the author checker, obstruction point and seed metadata were executed under `author_replay/`. The new author-code replay agrees, while its original receipt was preserved. That replay was not the premise of independent matrix or LDL acceptance.

## G05 — Uniform every-kernel barrier and dependency closure

The actual probability distribution has positive weights summing to one and legal support. Its mean score is rho* + Σ tr(Q_b M_b) by the checked coefficient convention. Both factors in every trace pairing are PSD, including singular and zero cases. Thus tr(QM) = tr(M^(1/2) Q M^(1/2)) ≥ 0, and the maximum over the complete legal domain is at least this expectation. The exact positive density gap proves the barrier for every rank and every permitted real PSD kernel choice.

The acyclic dependencies are G01 → G02/G03/G04 and G01+G04 → G05. G02 explains the target threshold. G03 supports a symmetry-reduced separator when used. Numerical convergence, Q7 density, old PASS receipts and a putative Q8 realization of p* are absent from this chain.

Hypotheses are discharged at every application: global C4-freeness gives legal restrictions; all state symmetries preserve actual legal flags; both external flags share their root map; the support and weights are checked; exact factors prove PSD; symmetric trace coordinates use the correct half off-diagonal. No degree, parity, odd-square, seed-distance or individual-local-PSD hypothesis is silently inserted. All symbols retain their stated type and finite domain; no cyclic or external theorem dependency is hidden in the final trace argument.

## Counterexample and mutation pass

The complete raw results are in `ATTACK_CHECKS.json` and its executable `attack_checks.py`.

1. Exact finite face and vertex laws check every ordered pair, detecting omitted collision or overlap categories.
2. On an actual legal support graph, a PSD rank-one test kernel has different exact traces when the off-diagonal ordered-entry factor is incorrectly doubled. The original coefficients match the correct value.
3. An actual root/flag pair exhibits different joint simultaneous canonical pairs and the incorrect pair obtained by minimizing each flag independently. The implementation uses the correct common action.
4. Vertex square codes 1 and 8 show why root translation is forbidden.
5. An explicit legal local graph has a negative 2×2 principal determinant in a moment block. Individual local PSD would therefore be false; the proof and checks do not impose it.
6. Changing the first LDL pivot by one fails its exact (0,0) identity; actual pivots match the fresh decomposition.

Zero kernels, singular blocks, equal flag states, empty/sparse graphs and all overlap categories were checked analytically or by these exact tests. No algebraically verified counterexample to G01–G05 was found.

## Required fixes and exclusions

No mathematical repair to `main.tex` is required. For standalone reading, retained Markdown §4 could repeat “C4-free” in generic actual-G sentences; preceding sections already impose it and TeX is explicit. This optional editorial restatement is not an open proof obligation.

No old full enumerator, new multi-million-object oracle, numerical optimizer, Lean or TeX build is certified by this review. Additional degree/common-Q6 constraints or flag spaces require their own valid bridge and a new check against p*. The original graph goal stays OPEN.

`RECEIPT.json` / `PROOF_AUDIT.json` contain all input hashes, source-unit coverage, requested/observed identity separation, exact scope and assurance limits. The first report-emission attempt had a relative metadata-path error before writing any audit; it was corrected without changing mathematical inputs or computations.
