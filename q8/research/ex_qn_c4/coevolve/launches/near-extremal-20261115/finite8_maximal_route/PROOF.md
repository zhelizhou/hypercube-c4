# Target-preserving maximal reduction and exact finite inputs

This is a necessary-condition reduction for the target ex(Q8,C4) <= 682. It does not prove that target and runs no LP. Every statement importing the historical Q6 bounds retains the historical proof/certificate assurance; the new arithmetic enumeration does not independently re-prove those local results.

## 1. Exact maximal counterexample domain

If a C4-free G subset Q8 has at least 683 edges, repeatedly add an ambient edge whenever C4-freeness is preserved. Finiteness ensures termination at an inclusion-maximal C4-free H containing G. Put m=|E(H)|. Then m>=683; m is not assumed equal to 683. Conversely such a maximal H is itself a counterexample. Thus exclusion of all such maximal H is equivalent to the desired upper bound.

An isolated vertex cannot occur in H: an added edge incident with it cannot complete a cycle. Hence n0=0 on both actual parity classes. This claim is used only for the new maximal domain; the historical exact-683 cover is left unchanged.

## 2. Historical import, arithmetic and the finite m range

For a C4-free coordinate Q6 face F, fix the parity induced by the SAME global class P. Let S_F=sum binom(local degree,3), c_F=count of local degree-six roots, and L_F=count of roots of local degree at most two. Import

    4 S_F + 2 c_F <= 632 + 5 L_F.

Actual sources read for this reduction:

- `../../../../proofs/q8_single_three_cycle007/GENERAL_WEIGHTED_GATE.md`, Sections 1–2;
- its `local_weighted/PROOF.md` and `local_weighted/TWO_LOW_EXTENSION.md`, including their exact imports and replacement proofs;
- `../q8_equality_profiles/main.tex`, E01–E02 and E05.

The Q6 inequality has no condition on opposite-side degrees. Its no-low case imports the historical minimum-three weighted bound 316; its one-low bound 317 imports the one-low theorem and a four-full/one-two certificate; its two-low bound 321 imports the four-full/two-two certificate after safe star replacement. The source reports strict reconstructed replays of the last two small certificates, not a new exhaustive Q6 census here. At L=3, S<=160, c<=4 and S congruent 29+c modulo3 give 2S+c<=322. At L>=4 the elementary cap324 suffices. These scopes matter: no minimum degree is imposed on restricted faces of H.

There are 112 coordinate Q6 faces. Each actual Q3 full star at a P root belongs to ten such faces; each global degree-d root is locally full in binom(d,6) faces. It is locally low in

    l_d = sum_{j=0}^2 binom(d,j) binom(8-d,6-j)
        = (28,28,28,18,6,0,0,0,0)_d

faces. Therefore summing the imported inequality gives exactly

    sum_d [40 binom(d,3)+2 binom(d,6)-5 l_d] n_d <= 70784.

Here sum n_d=128 and sum d n_d=m on either actual class. Subtract 402 sum d n_d and add 1610 sum n_d to both sides. The nine coefficients become

    2 C_d = 2(735,534,333,177,66,0,0,105,345)_d,

and the right side becomes 276864-402m. Consequently

    C(P) <= 138432-201m.

All C_d are nonnegative, so m<=floor(138432/201)=688. No external upper bound687 is used. The maximal counterexample edge count is therefore one of 683,684,685,686,687,688.

## 3. Complete parity-profile cover

For completeness, the one-parity Q3 star capacity is1792. There are binom(8,3)*2^5=1792 coordinate Q3 faces. A fixed parity of a C4-free Q3 has at most one full degree-three root: any two distinct same-parity roots have distance two and, if both were full, their common two neighbors would form a square. Double counting rooted full Q3 stars thus gives sum_P binom(d,3)<=1792.

Put b_d=binom(d,3)-10d+40, namely (40,30,20,11,4,0,0,5,16). Thus every original parity has

    b(P)=sum b_d n_d <= 6912-10m.

For each of the six m, `PROFILE_COVER.json` saves every nonnegative integer row with sum n_d=128, sum d n_d=m, C<=138432-201m, and b<=6912-10m. It also saves the subcover with n0=0, which is necessary for maximal H. These are integer relaxations, not graph classifications. No historical overlap filters or additional exclusions are silently added.

Completeness of enumeration: enumerate n_d for d in {0,1,2,3,4,7,8} in the finite ranges bounded by positive C_d. Then set

    n6 = m - sum_{d !=5,6} d n_d - 5(128-sum_{d !=5,6}n_d),
    n5 = 128-sum_{d !=5,6}n_d-n6.

Reject negative n5 or n6 and b violations; these are the unique values solving the two degree sums. This visits every feasible row exactly once. For the maximal cover the n0 loop consists only of zero.

|m|C cap|b cap|all rows|maximal n0=0 rows|
|---|---:|---:|---:|---:|
|683|1149|82|814|783|
|684|948|72|393|385|
|685|747|62|171|170|
|686|546|52|66|66|
|687|345|42|20|20|
|688|144|32|4|4|

The newly enumerated unfiltered683 row set is compared exactly to the existing814-row artifact; that historical enumeration is not rerun or modified.

## 4. Complete maximal edge7 generators

Fix an oriented ambient edge uv in direction i, and root value r=1 if uv is retained. For each of the other seven directions j, encode its square's three other edge indicators as

    s_j = a_j + 2 b_j + 4 c_j,

where a_j indicates u--u^ej, b_j indicates v--v^ej, and c_j indicates u^ej--v^ej. Let x_s be the number of external directions of state s. Then x is a nonnegative integer histogram with sum x_s=7.

If r=1, C4-freeness prohibits state7, so every actual retained edge gives one of all histograms on states0..6. If r=0, adding uv creates a C4 if and only if one of these seven square completions already has all three other edges. The reverse implication uses the fact that every C4 in a cube through uv is its coordinate square with some j!=i. Thus inclusion-maximality is EXACTLY the condition x7>=1 at every missing ambient edge.

The root0 generator inventory therefore consists of all eight-state histograms of size7 with x7>=1. Removing one distinguished unit of state7 bijects these with eight-state histograms of size6, giving binom(13,7)=1716. The unrestricted root0 domain had binom(14,7)=3432 histograms. The root1 inventory has binom(13,7)=1716 histograms on seven states of size7. `EDGE7_GENERATORS.json` saves all rows. Endpoint reversal exchanges states1 and2, and5 and6, and fixes0,3,4,7; both complete inventories are closed under this same actual endpoint action. No independent endpoint relabeling across overlapping flags is presumed.

## 5. Shared realization and model assembly boundary

For any fixed actual H, all Q4 types, edge7 histograms, both parity profiles, endpoint degrees, and local square counts are pushforwards of this one H. Therefore the existing local-type weights lambda and edge7 histogram weights beta must be coupled through their actual common incidences. Reusing one shared lambda across all row families is necessary: separate lambda choices for different families lose this implication. The endpoint bridge supplies further common degree equations; its own author owns those equations and scaling.

For a fixed m, the two parity profiles belong to the corresponding maximal covers above. A disjunctive model may keep m and both rows fixed, or encode an exact union. A convex union over the six m and their profile rows is weaker but remains a valid necessary relaxation: each actual parity profile maps to a row of its own fixed-m component. In the parent convention alpha is the average of these two profile point masses, beta denotes edge7 histogram weights, and N_d=2 sum_profile alpha_profile n_d(profile). Thus the actual alpha has up to two rows at that same m; it need not be one row. The convex union may additionally mix m, which is allowed only as a weaker necessary relaxation. Such mixing must not be described as an actual graph, an exact disjunction, or evidence that m stays683 after maximal extension. Every numerical normalization must use the same fixed ambient incidence convention as the lambda and alpha producers. This note makes no unsupported claim that profile inequalities alone force consistent mixed-edge-degree moments.

The next authorized mathematical obligation is to assemble those shared marginals and endpoint bridges and decide the resulting necessary model. This note supplies finite inputs and coverage only; feasibility would not produce a graph, and infeasibility would need an exact certificate and a checked connection to every input family before proving the target.

## 6. Literal seed calibration and reproducibility

`build_inputs.py` reads the actual `data/q8_seed682.edges`, checks every retained root has zero full three-edge completion, and checks every missing ambient edge has a completion. The682-edge seed is C4-free and inclusion-maximal. Its342 missing edges have exactly3,4,5,6 closing squares with frequencies41,159,120,22 respectively. The seed hash and exact counts are in `CHECK.json`. This calibrates the maximality restriction at the known lower construction; it says nothing about absence of larger graphs.

Run `python3 build_inputs.py` from any directory. It writes only this directory, compares historical683 rows read-only, enumerates complete finite histogram/profile domains, and checks literal seed edges. No solver, LP, old job or mathematical Goal is launched. Independent review and any later exact model certification remain separate.
