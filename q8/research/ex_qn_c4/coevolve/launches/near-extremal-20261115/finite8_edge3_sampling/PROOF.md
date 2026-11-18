# Complete three-flag edge sampling from one actual graph

This is a necessary identity for every C4-free spanning subgraph G of Q8. No maximality, density, parity equality, or graph-realization converse is assumed. Root owns this package; fresh nonauthor semantic review is a separate acceptance step. The full upper682 objective remains open.

## E3-01. Actual flags, orientation and complete row domain

An ambient edge e={u,v} has root state r=1 if retained and r=0 otherwise. Its seven other directions have flag s in {0,...,7}, with bits indicating the edges u--u+b, v--v+b and u+b--v+b. For r=1 the state7 is excluded by C4-freeness. Let y_s be the seven-count histogram. Reversing endpoints applies P(s), which interchanges bits0 and1 and fixes bit2.

Rows (r,z) consist of all nonnegative histograms z of total3 in8 labels when r=0 and7 labels when r=1. Their counts are C(10,3)=120 and C(9,3)=84, total204. The declared order is lexicographic combinations with replacement of three state labels, first r=0 then r=1. Rows related by endpoint reversal coincide as functions; 204 independent equations are not claimed.

For any histogram y of total7, define

    H_(r,z)(y) = product_s C(y_s,z_s) + product_s C((Py)_s,z_s).

The root type must match; otherwise this row is zero. Equivalently select each of the35 three-element subsets of the seven direction positions and count its histogram in both endpoint orientations. Thus H is nonnegative integral and sums to70 over all204 rows. This is a complete multivariate hypergeometric numerator, including repeated labels and zeros, with no restriction to any observed support.

For an actual legal Q4 graph K, each of its32 ambient root edges has precisely three other directions. Count its histogram in both endpoint orientations and sum over all roots. Call the resulting204-vector L(K). It is nonnegative integral and sums to64. It does not count only retained root edges. Endpoint reversal and permutations of the outside directions leave the histogram feature unchanged, so every L_z is invariant under all Q4 isometries. An actual C4-free graph supplies only the indicated legal root states.

## E3-02. One-object bijection and normalizations

Let lambda be the empirical distribution of all1120 coordinate Q4 restrictions of the SAME G. Let beta be its empirical histogram distribution over all1024 ambient edges, using the SAME7-direction observations as the existing edge frequency cone. A local occurrence is an ambient root edge, an unordered choice of three of its seven other directions, and an orientation of its endpoints. That occurrence determines a unique coordinate Q4 containing the edge; conversely every oriented root edge inside every coordinate Q4 gives exactly this occurrence. All flags and retained bits are inherited unchanged from G.

Consequently, for every row (r,z), the exact integer double count is

    sum_(all1120 K) L_(r,z)(K) = sum_(all1024 e) H_(r,z)(y_e).

Both sides enumerate71680 oriented marked objects, since1120*64=1024*70. Division by the empirical denominators gives

    1120 E_lambda L_z =1024 sum_beta H_z,
    **35 E_lambda L_z =32 sum_beta H_z**,

or equivalently E_lambda L_z/64 =sum_beta H_z/70. There is no division by the mass of either root type and no independence assumption. Lambda and beta must be measurements of the same graph.

## E3-03. Complete maps and endpoint deduplication

`edge3.py` computes L directly from literal Q4 geometry and H by all35 subsets. `export.py` regenerates the full204-by5148 H map, using every original sum7 histogram of eight or seven states, and the204-by14090 L map on the frozen actual local graph library. The full5148 source list, actual current3432 list, current1751 selected representatives and all old2788/current1751 classes are read from their real files, not guessed from old indices. Every member of each stored duplicate class has the identical H vector; the producer checks this exactly before exporting. The new maps therefore preserve these concrete existing deduplications. These checks establish safety for the pinned classes, not a theorem that an arbitrary unrelated moment compression preserves all third moments.

Current1751 columns have a separately justified maximal/leaf restriction. General graphs use the full5148 map; their raw generators are not silently deleted by the current adapter. The graph library is a pricing library and does not replace the domain of every legal Q4. Any newly priced graph uses the same literal L scorer.

The ready consumer matrices are `BETA_HYPERGEOM_FULL_204x5148.npz`, `BETA_HYPERGEOM_CURRENT_204x1751.npz`, and `LOCAL_COUNTS_204x14090.npz`, all integerCSR. `ORDER.json` pins rows, graph order, current selections and their original5148 indices. `INTERFACE.json` pins the exact sources. All204 constraints may be retained or exact duplicate rows may be removed with the mapping preserved.

## E3-04. Exact lift into the original face functional

The numerical author supplied the following additional algebraic interface. For each canonical Q2 root R and pair of full external flags i,j, and each of its four root edges e, obtain three edge-root flags: the base flag within R, and one flag from each external direction. Their nine edge bits all belong to R and the two full flags. Let A_z(i,j) count, over those four edges, the three-label histogram z in both endpoint orientations. It is symmetric in i,j and invariant under the common root stabilizer; both flags are transported by the same root action.

For an actual Q4, every edge belongs to three base Q2 faces. Therefore L_z(K)=(1/3) sum_faces A_z(i,j). Define the integer symmetric full-state kernel

    K_z(i,j)=12 A_z(i,j) - A_z(i,i) - A_z(j,j).

Its diagonal is10 A_z(i,i). The original exact finite-eight face functional for an invariant kernel is

    T_K(K4)=(1/288) sum_faces [10K(i,j)+K(i,i)+K(j,j)].

Substituting the definition cancels both diagonal corrections and gives T_(K_z)=(5/12) sum_faces A_z. Hence the pointwise identity is

    **L_z(K4)=(4/5) T_(K_z)(K4)**.

No PSD property is asserted for these kernels. The identity is a linear representation, not a nonnegative Gram decomposition. The vertex block is zero. Thus for a dual weight y on the normalized row L/64-H/70, its local lambda functional contributes exactly T_(sum_z y_z K_z)/80. The original complete integer Q4 functional maximizer can price this term after including that kernel; no extra tensor oracle is needed.

Actual construction and calibration are in `../finite8_degree_augmentation/edge3_quad_lift/`: the author compared all204 by14090 actual L values with the existing packed coefficients and obtained the exact integer identity5*64512 L=4 F K^T entrywise. Its full proof and returned kernel/order are part of the consumer evidence, with independent review still required. Root initially considered a new native tensor interface, then corrected that unsupported span assumption when this exact lift was derived. A compiled but uncalibrated abandoned extension in `../finite8_edge3_oracle/` is not used and is not accepted evidence.

## E3-05. Actual checks and precise limits

`verify_actual.py` checks ambient edges and literal common-neighbor C4-freeness, enumerates all1120 Q4 restrictions, all1024 edge roots and both orientations, and checks each of204 integer equalities directly. It passed the actual682 seed, actual576 maximal leaf calibration, actual584 same-parity-shortcut counterexample, empty graph, one-axis matching, and both parities of an8-star. Each case counts71680 objects on each side. These calibrations exercise zero/full endpoint degrees, absent root types, nonmaximal graphs and asymmetric parity; the universal result rests on E3-02's bijection.

Root's separate exact decimal-rational diagnostic on immutable master195 shows a maximum normalized row disagreement about0.0016789688135. That intermediate tuple already satisfies its older63 shared identities numerically; the new edge3 identities provide additional necessary information. It is not a Q8 graph, a completed feasible point or a whole-model infeasibility certificate. No new unrestricted bound is claimed. Complete local-domain maximization and exact global dual assembly remain requirements for any final682 proof.
