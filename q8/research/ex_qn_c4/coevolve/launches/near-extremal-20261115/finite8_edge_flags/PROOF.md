# Edge flags: exact PSD redundancy and three finite-seven directions

## Outcome and scope

Edge-root PSD blocks do **not** strengthen the original five full-face PSD blocks: the exact finite-eight edge feature pulls back pointwise to those blocks. This is proved below, not inferred just from an optimization outcome. The archive's fold_old.py already contains an older partial-edge-to-full-face PSD absorption; the present derivation fixes the finite-eight collision normalization explicitly.

The complete finite-seven frequency cones are stronger than PSD alone. Three exact small kernels were found and checked: two cut the frozen818-point, and one cuts a read-only iteration10 snapshot from the degree author's eigen-cut run. That snapshot is not an accepted feasible point or graph. The third kernel is non-PSD/non-copositive and is a valid additional finite-six face direction through the pullback; independence from all existing augmented constraints is not claimed.

The primary full682 goal remains OPEN. All files outside this directory were read only.

## 1. Actual edge states and exact bridge

Orient each ambient root edge from its smaller binary endpoint u to v. Its retained state is r=0 or1. A full Q2 flag in one external direction has three bits: the connector at u, the connector at v, and the edge opposite uv. If r=1, state7 would close a C4, so states0,...,6 are legal. If r=0, all states0,...,7 are legal.

A common endpoint flip interchanges bits0/1 and preserves bit2. Average a symmetric edge kernel under this single C2 action on both arguments, obtaining Qbar_r. Do not independently quotient the flags.

An actual Q8 root edge has seven external directions, with count vector x>=0 integer, sum x=7. For u=x/7, independent draws give

    u uᵀ = (6/7)R_distinct + (1/7)diag(u).

A uniform local Q4 root edge has three external flags s_a. Define

    T_edge(K) = (1/672) Σ_(32 ambient edges e ofK)
                   [6 Σ_(3 unordered a<b) Qbar_r(s_a,s_b)
                    + Σ_(3 a) Qbar_r(s_a,s_a)].

Each global ambient edge is in35 of the1120 coordinate Q4s. Thus uniform restriction/root sampling gives uniform1024 global edges and uniform3-subsets of their seven external axes. The local cross and diagonal averages give exactly the independent-draw law, so

    E_K T_edge(K) = (1/1024) Σ_(actual ambient e) x_eᵀQbar_r x_e /49.

It is nonnegative for PSD kernels, and more generally for any kernel nonnegative on every nonnegative integer vector of total seven. This is valid on every actual C4-free Q8, without degree, parity, seed or oddness assumptions.

With denominator64512, the unaveraged coefficients are96(6cross+diagonal). Performing the C2 average gives288 per cross entry per endpoint action and48 per diagonal entry per action. edge_flags.py implements these exact upper-coordinate coefficients, using the original bottom12/top12/cross8 Q4 edge order.

## 2. Exact pointwise face pullback

Fix an actual root face F and one of its four root edges e. Let s_0 be F as a one-direction edge flag at e. Each external full-face flag g determines an edge flag s(g) at the same edge, with a common endpoint orientation. Set

    v_g = 6 e_(s(g)) + e_(s_0),
    V_(F,e) = matrix whose columns are v_g,
    P_F = (1/196) Σ_(e⊂F) V_(F,e)ᵀ Qbar_(r_e) V_(F,e).

This uses only actual bits of F and g. Changing the root frame permutes the four edges and possibly flips their endpoints. Since the edge kernels have the common C2 average, P_F is invariant under the actual canonical face stabilizer.

Use P_F in the existing finite-eight face feature, with5/6 cross and1/12 per diagonal and mean over24 root faces. Fix a local ambient edge and its three external flags s_0,s_a,s_b. The face selecting s_0 as base contributes, before1/(24·196),

    30 Q(s_a,s_b) +6 Q(s_0,s_a)+6 Q(s_0,s_b)
       +3 Q(s_a,s_a)+3 Q(s_b,s_b)+Q(s_0,s_0).

Sum the three choices of base flag. Each unordered cross has coefficient30+6+6=42 and each diagonal1+3+3=7. Since7/(24·196)=1/672,

    T_face(P)(K) = T_edge(Q)(K)

pointwise for every legal labelled Q4 K, not only after global averaging.

If Q_r is PSD, each P_F is PSD by congruence and summation. Therefore edge PSD is exactly contained in the original full-face PSD family.

If Q_r is only finite7-valid, P_F is still finite6-valid. For an arbitrary integer full-face histogram x>=0 of total6,

    V_(F,e) x = 6 z_e,
    z_e = Σ_g x_g e_(s(g)) + e_(s_0),
    sum z_e =7.

Hence xᵀP_Fx=(36/196)Σ_e z_eᵀQbar_(r_e)z_e>=0. These are directions inside the complete finite6 face-kernel cone, not a new family beyond that complete cone. They can add directions beyond a currently selected finite list of cuts.

lift.py implements this map. For already averaged integer edge kernels its return is five integer numerator matrices with denominator196. For arbitrary raw kernels it first takes the endpoint group sum and returns denominator392.

## 3. Actual normalization and identity checks

check_bridge.py verified:

- Direct outer products at all1024 actual ambient edges of the true682 Q8 seed, each with seven flags, equal the edge moment coefficients summed over all1120 common Q4 restrictions.
- A nontrivial arbitrary symmetric integer kernel pair has exactly equal direct edge and lifted face scores on all818 frozen support graphs and64 general C4-free Q4 samples; maximum exact error is0.
- All18 canonical face-root stabilizer actions preserve the lifted kernels.

BRIDGE_CHECK.json records these actual checks. No complete-Q4 census is inferred from samples; the pointwise identity is proved analytically in §2.

## 4. Frozen point: PSD survives, integer-seven frequency does not

FROZEN_EDGE_MOMENTS.json reconstructs both exact matrices from the actual818 graph masks and rational weights in the frozen FAMILY_OBSTRUCTION.json. Its source hash is pinned. The moment denominator is2·64512·W, W=11199999988800.

The missing-root moment has support1,2,4,7; the retained-root moment has support0,3,5,6. Both4×4 supported matrices have exact positive LDL factors, with zero other rows/columns. Thus both full edge moments are PSD, consistent with the pointwise PSD redundancy theorem.

For each small state space, all integer total7 histograms were tested:

| Target | Root state | Dimension | Complete histograms | Minimum kernel value |
|---|---:|---:|---:|---:|
|frozen818|missing0|8|C(14,7)=3432|0|
|frozen818|retained1|7|C(13,7)=1716|0|
|degree iteration10 snapshot|missing0|8|3432|0|

The actual LP discovery runs were bounded at10seconds per primal/dual call and completed. The accepted statements use exact integer kernels and full enumeration, independent of numerical infeasibility.

Their raw exact moment pairings are

    frozen_root0: -27921397669/11851851840,
    frozen_root1: -20810671173/3950617280,
    degree_snapshot_root0:
      -34656869948258354962251/20000000000000146682828.

These strict negative pairings prove nonmembership in the full finite-seven cones. A conic combination of total7 outer products would pair nonnegatively with a finite7-valid kernel.

Every accepted kernel is symmetric and common-endpoint invariant. Nonnegative smaller-total integer witnesses prove they are genuinely non-PSD and non-copositive:

    frozen_root0: (0,1,1,0,0,0,0,3), total5, value-264;
    frozen_root1: (2,0,0,4,0,0,0), total6, value-288;
    degree_snapshot_root0: (2,0,0,2,1,0,0,0), total5, value-336.

This does not decide complete positivity of the target moments. The validity condition is the exact integer total7 domain, rather than all nonnegative real vectors.

## 5. Accurate degree-snapshot scope

degree_snapshot.json is a frozen read-only copy of the degree author's iteration10 FLOAT_CANDIDATE.json, with status EIGEN_CUT_ITERATION_BOUND and175 nonzero graph weights. It was explicitly not an accepted PSD/degree feasible point.

For reproducibility, its JSON decimal weights were interpreted as exact rationals and renormalized to sum one. DEGREE_SNAPSHOT_EDGE_MOMENTS.json contains those actual rational numerators and rebuilt edge matrices. This defines a precise local probability distribution, not a graph and not a claimed feasible augmented point.

The kernel degree_snapshot_root0 strictly cuts this actual snapshot and is valid globally by finite7 enumeration. In particular it is not merely a PSD pricing direction: its explicit nonnegative integer witness gives a negative quadratic form. The old frozen_root0 kernel, by contrast, has positive mean on this snapshot. The new direction therefore has concrete exploratory information for that numerical state, without proving independence from every other valid augmented constraint.

No later running point was silently substituted for this frozen snapshot.

## 6. Compact consumer interface

EDGE_CUTS.json contains the complete8×8 or7×7 integer kernels, raw state order, endpoint action, exact finite-domain minima, strict target pairing, witness and recommended positive scale:

    frozen_root0: scale1320;
    frozen_root1: scale828;
    degree_snapshot_root0: scale1680.

Use score.value_on_graph(original_order_mask, cut_name) for an exact normalized Fraction edge feature. It uses only the matching root state and the unchanged /64512 coefficient contract. Add such a feature with a nonnegative weight.

Alternatively score.full_face_lift(cut_name) returns the existing five face-block integer numerator matrices and denominator196·scale. This permits an unchanged full-face native score oracle; validity is the finite7-to-finite6 proof, not a fictitious Gram factor.

FEATURE_CHECK.json verifies direct point means and lift consistency. All three kernels have nonnegative means on the actual682 seed. The snapshot cut's mean on that seed is1/3840, and its exact normalized snapshot mean is

    -11552289982752784987417/11200000000000082142383680.

The legal16-edge oracle graph1774744440 has snapshot-cut feature11/120. No single-graph exclusion follows.

## 7. Independent verification and return

verify.py imports no producer, optimizer, scientific package, edge_flags module or frozen state module. It independently reconstructs all local edge geometry and exact moments, checks both frozen PSD factors, enumerates histograms recursively rather than by multisets, verifies every complete finite7 domain, endpoint action, negative witness and exact pairing, and rechecks the actual682 whole-graph regression.

VERIFICATION.json records PASS_EXACT_GEOMETRY_PSD_AND_FINITE7_CUTS. Root also ran its separate third implementation, finite8_root_checks/check_edge7.py and EDGE7_ROOT_CHECK.json; those files are Root-owned and are not altered or assumed as premises here.

This bounded task returns a proved PSD redundancy, actual finite7 separators, exact compact interfaces and precise snapshot scope. It starts no further LP or workflow, modifies no old files, makes no canonical claim, and does not close the original upper682 goal.
