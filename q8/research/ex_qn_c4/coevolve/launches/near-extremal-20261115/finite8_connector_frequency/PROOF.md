# Connector projection: two exact all-full-state finite-six cuts

## Scope and fixed input

The source is the exact frozen completed-edge-stage input

    ../finite8_vertex_degree_cone/INPUT_EDGE_STAGE_POINT.json
    SHA256223b58046502fdd7eae1847fc6fc9ab3f27dfbeca9c1f1647b14f06a54d28aa9.

INPUT_POINT.json is a byte-identical task-local copy. It has202 graph weights and status EIGEN_AND_INTEGER_CUT_ITERATION_BOUND, iteration4, with no exact acceptance or graph assertion. The stored decimal weights are interpreted as exact rationals and are not independently renormalized. Their sum is

    9999999999999698585929/10000000000000000000000.

Cone membership and the separation signs are homogeneous. This preserves the same specified lambda; it does not claim its numerical parent constraints hold exactly.

The new result is two finite-six kernels on connector labels0,...,15, lifting to ALL legal240/170 full states and strictly cutting this input. No outside-support restriction or outsideJ repair is used. The main upper682 goal remains OPEN.

## 1. Projection and actual frequency condition

Use the original ascending legal full-face eight-bit flag codes, with four connector bits at the four root vertices followed by four translated-square edge bits. For canonical root block b define

    A_b[c,i]=1 if (legal_flag_code_i &15)=c, otherwise0.

For every actual Q8 root square, six external flags have a full-state integer count vector x of total6. Its connector count vector y=A_b x is a nonnegative integer vector on all16 connector codes, also of total6. Therefore the projected root moment must lie in

    C6(16)=cone{yyᵀ : y>=0 integer, sum y=6}.

There are exactly C(21,6)=54264 complete generators. Projection commutes with the simultaneous root action: a root vertex permutation permutes connector bits, while discarded parallel bits do not affect their labels. The common root average preserves the finite histogram domain.

For any16×16 kernel Q nonnegative on every such histogram, define the entire full-state kernel

    Q_full[i,j]=Q[code_i&15,code_j&15]=A_bᵀ Q A_b.

Then xᵀQ_full x=(A_b x)ᵀQ(A_b x)>=0 for every full-state integer x of total6. Every legal full state is covered. In fact every connector code occurs with translated bits0 in every canonical root type, so the projection is onto all16 labels. This is not the old16-state support inside a larger face space.

## 2. Exact moments and PSD qualification

project.py reconstructs all five actual face moments from the202 legal labelled Q4 graphs and same decimal lambda. It projects both by grouping the upper linear coefficients and independently by grouping ordered full-moment entries; the results agree.

If D=10^22 is the common decimal denominator, the stored projected moment is U/(2·64512·D). PROJECTED_MOMENTS.json contains every exact matrix and actual integer weight.

The eligibility test was performed before a frequency LP:

- Blocks0/root mask0 and4/root mask7 have positive16×16 exact rational LDL factors.
- Blocks1/2/3 have explicit integer negative PSD directions. These are recorded as old-family violations only and were not used to advertise a new finite-frequency finding.

PSD_ELIGIBILITY.json contains the exact factors and negative directions. Thus the selected connector matrices are genuinely PSD while being tested against the stronger integer-six cone.

## 3. Complete finite-domain LPs and final exact kernels

The generic16-label generators in the previous frequency directory were reused read only. Before use, all54264 unique vectors were checked nonnegative with total6, every nonzero matrix entry was checked against x_i x_j/36, and every column support count was checked. Generic labels are connector codes0,...,15; old support state IDs are not imported.

Each selected block had one12-second-bounded primal and one explicit dual call. All finished:

| Block | Primal seconds | Dual seconds | Numeric outcome |
|---:|---:|---:|---|
|0|0.407963624|2.024280105|infeasible, explicit negative dual|
|4|1.059421020|2.447134372|infeasible, explicit negative dual|

These statuses discover candidates; they are not the exact acceptance argument.

The final integer matrices are in block0.EXACT_SEPARATOR.json and block4.EXACT_SEPARATOR.json. Rational recovery used denominators760 and1900, respectively, with zero diagonal repair. The kernels were summed over all actual root-stabilizer actions, giving integer invariant matrices.

Complete exact enumeration proves

    yᵀQ_b y >=0 for all54264 integer total6 connector histograms,

with minimum0 in both cases. The maximum absolute entries, used only as positive normalization scales, are12160 and7600.

Their exact raw same-lambda feature pairings are

    block0: -5650710530085758525389/15000000000000000000000,
    block4: -2909599605897848271617/3000000000000000000000.

These are strictly negative. If the projected moments had any nonnegative generator decomposition, their pairings with the corresponding finite6-valid kernel would be nonnegative, a contradiction.

Both kernels have nonnegative integer smaller-total witnesses:

    block0: y_0=1,y_15=3, total4, quadratic -2432;
    block4: y_0=1,y_12=3, total4, quadratic -760.

They are therefore non-PSD and non-copositive. This does not determine whether the target matrices are completely positive. It does establish finite-six nonmembership at matrices whose PSD qualification was exact.

## 4. Root action, full-state lift and caller

The projected moments are invariant under the induced canonical root permutations. Summing a kernel under those permutations preserves total-six validity and multiplies its negative moment pairing by the group size. The final kernels are invariant: eight root actions for block0 and two for block4.

All240 empty-root full states and all170 three-edge-root full states use their actual ascending code order. The complete lifted matrices are Q[code_i&15,code_j&15]. Their common root averages leave them unchanged; no parallel-bit state is omitted or separately completed.

For a legal local Q4 graph K define the matching face feature

    T_b(K)=(1/24)Σ_(rootfaces oftypeb)
      [(5/6)Q_full[s,t]+(Q_full[s,s]+Q_full[t,t])/12].

For every actual C4-free G⊆Q8, the exact finite-eight sampling identity gives

    E_K T_b(K)=(1/1792)Σ_(actual rootF oftypeb)
                    y_FᵀQ_b y_F/36 >=0.

The identity is algebraic and does not require PSD. Its last inequality uses the complete connector-six domain. Every flag, connector and root action comes from the same original object. The feature is invariant under cube isometries by common-root transport and symmetric outside-axis averaging, so the existing complete common-K scorer can evaluate it.

Add either normalized feature only with a nonnegative weight in the same-lambda model. A PSD-only Gram wrapper cannot establish its validity. We do not claim that all other original full-PSD constraints were satisfied by the input; blocks1/2/3 were explicitly not PSD. The new information is a strict finite-frequency violation in the separately PSD-qualified connector blocks, not a claimed feasible-point exclusion for an otherwise fully accepted model.

## 5. Consumer and verification

CONNECTOR_CUTS.json gives the compact16×16 kernels, canonical root, all full-state connector mappings, normalization, exact target pairing and finite-domain result.

- score.value_on_graph(mask,block) gives an exact normalized Fraction.
- score.full_face_kernel(block) gives the original five face-block integer matrices and the positive scale,12160 or7600.
- It uses finite_flags.local_coefficients on actual graphs. Upper off-diagonal coefficients are already combined, so no additional factor2 is inserted.

verify.py is a separate standard-library implementation with no producer, scientific package or frozen-state import. It reads the same202 graph masks/decimal weights, reconstructs connector geometry directly from Q4 edges and whole root-to-canonical cosets, and exactly matches all five projected matrices. It verifies both positive LDL factors and all three old-PSD negative directions, recursively regenerates both complete54264 histogram domains, checks root actions and the all-full-state lift, and computes both strict negative pairings. VERIFICATION.json records the actual PASS.

This bounded task performed no repetition of an old-point LP and no optional face-degree-incidence expansion. No old package, master file, wiki or running writer was changed. There is no active process. Root owns independent acceptance, any model injection and subsequent workflow.
