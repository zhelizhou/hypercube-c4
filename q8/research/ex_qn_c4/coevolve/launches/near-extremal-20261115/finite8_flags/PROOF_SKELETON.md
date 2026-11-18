# Proof skeleton for fresh verification

Canonical review target: **main.tex**. The human-readable source remains **FINITE8_BRIDGE_AND_OBSTRUCTION.md**. This adaptation creates only these two review files; the mathematical data, code, original Markdown, LP history and author receipts remain unchanged.

Do not adopt OBSTRUCTION_VERIFICATION.json or the author's conclusions as premises. Reconstruct the actual local graphs and moments from the frozen point, check the rational factor identities, and audit the analytic sampling and transport steps. This is a scoped certificate-family result. The original full ex(Q8,C4) ≤ 682 objective remains **OPEN**.

## G01 — Original state definitions and exact finite-eight score

**Statement.** Precisely the five ascending legal full-face flag spaces have dimensions240/212/190/187/170, canonical root masks0/1/3/6/7, and the original nine vertex-rooted square states. The finite-eight score is e(K)/32 + F8(K) + V8(K), with all flags read from one actual legal labelled Q4.

**Micro-obligations.**

1. Root square vertices are0/1/2/3, edges (0,1),(0,2),(1,3),(2,3). A face flag has4 connectors followed by4 translated-square edges. Excluding a full translated square and the four actual crossing C4s gives the declared legal sets and ascending IDs.
2. D4 canonicalization transports both flags by one root map. Common canonical-root stabilizer averaging preserves PSD and removes dependence on the root map; individual flags are not separately quotiented.
3. The9-state vertex flag is an actual complete Q2 rooted at its marked vertex, modulo interchange of its two axes only. Canonical codes are0,1,3,4,5,6,7,12,13.
4. Face contribution per root is (1/24)[(5/6)Qbar[s,t]+(Qbar[s,s]+Qbar[t,t])/12]. Vertex contribution is /2688 times30·3 disjoint +6·12 overlap-one +1·6 diagonal entries, summed over vertices.
5. With integer Gram factors and original faceval=8D²Qbar, denominator64512D² gives numerator coefficients density2016, face280/28/28, vertex720/144/24. The desired strict threshold is max Z < 43029D².

**Inputs.** main.tex G01; unchanged finite_flags.py; read-only MathRSI original plugins/hypercube-extremal/archive/source/certificate_final_q4/verify_local.cpp and the source theory/state definitions. The old archive score is asymptotic; its192D² normalization cannot replace the new score.

**Failure tests.** Wrong edge order, independent flag normalization, vertex-root translation, omitted diagonal/overlap terms, off-diagonal factor-two errors, or unchecked overflow after scaling.

**Return/use.** A fully defined six-PSD-kernel family and exact integer contract, consumed by G02–G05.

## G02 — Exact sampling bridge for every actual Q8

**Statement.** For every actual C4-free G⊆Q8 and every allowed kernel choice, e(G)/1024 ≤ E score8(K) for a uniform coordinate Q4 restriction. A uniform local maximum below683/1024 would imply the integer bound682.

**Micro-obligations.**

1. At each actual root square, six external flags share one gauge. Independent draws give (5/6)R_distinct+(1/6)diag(u)=uuᵀ; its PSD quadratic form is nonnegative.
2. Uniform (Q4,root Q2) sampling makes the1792 global root squares uniform, since each has15 extensions. It samples two uniform distinct external axes; the two diagonal terms give the correct marginal.
3. At a marked global vertex, two independent unordered pairs among28 direction pairs have probabilities15/28 disjoint,12/28 overlap-one and1/28 equal.
4. All overlap laws fit in the same Q4: union sizes4/3/2 have completion multiplicities1/5/15. Category counts are3/12/6. The common marked vertex and actual edges are transported together.
5. Uniform (Q4,vertex) sampling gives uniform global vertices. There are1120 Q4s and each ambient edge is in35, so E e(K)/32=e(G)/1024.
6. Add the two nonnegative expected PSD terms. No degree, parity-profile, oddness, seed-distance or independent-completion hypothesis is introduced.

**Inputs.** G01 and finite combinatorial sampling. The direct actual682-seed regression in G04 supports verification but does not replace the theorem.

**Failure tests.** Retaining only disjoint pairs, using max-diagonal errors, reversing the inequality, or requiring an individual legal K's moment matrix to be PSD.

## G03 — Aut(Q4) transport and complete common-K coverage

**Statement.** The new score is invariant under every cube isometry. The original complete common-K representation and minimum-hidden-layer-pair slice therefore remain score-complete.

**Micro-obligations.**

1. Cube isometries permute root faces, with one induced D4 map acting on both flags. Stabilizer averaging and symmetric external/diagonal coefficients preserve each contribution.
2. At marked vertices the isometry preserves the root, induces only the declared axis interchange, and permutes every disjoint/overlap/equal pair within its category.
3. Common K=(A,B,S) is legal exactly when both actual Q3 layers are C4-free and S is independent in their common retained-edge graph.
4. The unchanged finite-coverage import reconstructs2902 legal Q3s,48 symmetries,90179 disjoint layer-pair orbits covering8421604 ordered pairs,13150453 legal marked completions and3312331 minimum-hidden representatives. These are labelled coverage counts, not nonisomorphic graph counts.
5. The new invariance proof discharges the transport prerequisite; matching six matrix dimensions alone would not.

**Inputs.** G01; the original read-only geometric checker and keys.bin. Root owns task-local oracle/ and its current native run records; no new fullscan status is silently inserted in this adaptation.

**Scope.** The bridge and family obstruction range over all legal Q4s and do not require a fresh full-domain scan. Imported coverage matters for native separation of a candidate; obstruction support legality is rechecked graph by graph.

**Failure tests.** Independent root gauges, losing collision terms under transport, or reusing3312331 solely because block dimensions match.

## G04 — Actual818-graph rational point and exact PSD

**Statement.** FAMILY_OBSTRUCTION.json defines a probability distribution on818 distinct legal Q4s, with all six exact finite-eight moments PSD and mean density76799371703/113777777664.

**Frozen primary input.**

- File: FAMILY_OBSTRUCTION.json.
- SHA256: fdbd082699eff6d46899d6a501945881cf6f6fed48735dd3a326c5db8080aec6.
- Probability denominatorW=11199999988800.
- Weighted retained-edge sum241918020864450.
- All818 graph masks, positive integer weights, full nonzero matrices and rational factors are in the actual attached file.
- Matrix convention: stored U_b = 2·64512·Σ_g w_g M_b(K_g). Divide by2·64512·W for the averaged moment. Each off-diagonal upper coefficient is split between two symmetric entries.

**Micro-obligations.**

1. Check masks are distinct integers in[0,2^32), weights are positive integers and sum exactly toW.
2. Decode in the original bottom12/top12/cross8 edge order. Check every graph's24 squares are nonfull, so every support graph is legal.
3. Rebuild all flag states and six matrices directly from graph edges and weights using common root actions. Do not trust stored matrices or LP features without recomputation.
4. Confirm blocks0/2/3 are zero. Nonzero supports have sizes16/16/4 in blocks1/4/5; all omitted coordinates are zero.
5. Parse all factors as rationals; check unit lower triangularL, strictly positive diagonalD and every identity U=LDLᵀ. This establishes PSD on the full stated dimensions, including implicit zeros.
6. Recompute the exact edge density and positive gap455241445/56888888832 above683/1024.
7. Optional whole-graph regression: direct empirical outer products at the actual682 seed's1792 roots with6 flags and256 vertices with28 flags equal the1120 common-Q4 sum.

**Checker and evidence.**

- Standalone second author implementation: verify_obstruction.py.
- SHA256: bace65c9200e75b48b80178f5b7426da3b31c899f39ea7e6b88c4ce99f397841.
- It imports no finite_flags.py, NumPy, SciPy, optimizer or precomputed features.
- It reconstructs ordered entries by the complete coset of root-to-canonical maps, rather than the producer's canonical-map/stabilizer table.
- Existing author receipt: OBSTRUCTION_VERIFICATION.json; not a premise for fresh review.
- certify_lp_point.py reproduced the point byte-for-byte from working_candidate.json and Q8_seed682_point.json without optimization. Floating provenance is unnecessary to establish the final rational point.

**Fresh replay preserving original receipts.** Copy verify_obstruction.py, FAMILY_OBSTRUCTION.json and Q8_seed682_point.json into a fresh review work directory, then run PYTHONDONTWRITEBYTECODE=1 python3 verify_obstruction.py there. The seed metadata refers to its actual read-only source edges. The reviewer may instead reconstruct the point independently from graph masks and weights.

**Failure tests.** Wrong implicit support, unchecked probability/graph, trusting floating eigenvalues or authorPASS, accepting a repaired floating dual without checking the final rational object, or treating Q7 moment feasibility as automatic finite8 feasibility.

**Return/use.** Actual legal rational distribution and six PSD matrices for G05, not a Q8 graph.

## G05 — Uniform obstruction for every fixed-family kernel

**Statement.** Every real PSD choice of the six G01 kernels satisfies max_(legal K) score8(K) ≥ 76799371703/113777777664 > 683/1024.

**Micro-obligations.**

1. The G04 support lies inside the complete legal local domain.
2. Its mean score equals its density plusΣ_b tr(Q_b M_b).
3. Each trace product is nonnegative because both matrices are PSD, including singular and zero blocks.
4. A maximum is at least a probability-weighted mean. Exact density comparison gives the strict family barrier.

**Dependencies.** G01 fixes the family and moment convention; G04 supplies actual legal support and exact PSD. G02 explains why the now-unreachable threshold matters to Q8. G03 justifies a complete separator if used. Neither a new fullscan nor optimization convergence is a premise of this lower barrier.

**Limits.** The point is a biased local Q4 distribution, not necessarily restrictions of one Q8. The theorem forbids this unchanged six-block family from proving the desired threshold; it neither proves nor refutes full682. Additional valid global degree/common-Q6 conditions, free corrections or new flags make a different family requiring their own validity and a test against this point.

## Provenance excluded as mathematical premises

The actual35-round small LP used1160 distinct graphs from both280-slice Q7 families and all1120 actual682-seed slices. It produced a restricted best near0.6759921289039941. Initial Q7 points have exact negative moment witnesses. working_*, Q7_* and Q8_* files remain available for reproducibility and method history.

Neither a numerical plateau, restricted LP objective, old asymptotic certificate, an individual local matrix's PSD, a native calibration receipt nor an author's PASS establishes G05. Only the final actual legal rational point, reconstructed exact identities, density and analytic implications do.

## Current status and return

This is a complete candidate proof with exact author-run finite evidence; fresh independent proof review is pending. The reviewer should explicitly accept or reject G01–G05 and preserve original comments and fixes. This author starts neither that review nor another workflow. Existing code, frozen point, old UNKNOWN records, original Markdown and old Goal are untouched. Root owns fresh scheduling, shared wiki and any augmentation.
