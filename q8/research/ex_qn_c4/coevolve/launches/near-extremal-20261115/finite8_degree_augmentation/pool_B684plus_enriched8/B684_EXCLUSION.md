# Excluding 684 or more edges in a C4-free Q8

This is the complete candidate proof for branch B. The exact arithmetic and
two complete Q4 maximizations have completed. A fresh whole-proof semantic
review is a separate acceptance step. This document does not assert the
target bound 682: its conclusion is the upper bound 683. No B9 run is needed.

All paths below are relative to this directory unless explicitly stated.
The frozen numerical discovery scope has 15,152 actual local Q4 columns,
645 parity-profile columns, 1,751 ambient-edge histogram columns and 356
common equations. That finite local library is not the full Q4 domain and
is not a premise of the final maximization. Only the 83 inequalities with
nonzero rational weights are used in the proof.

## 1. Statement and maximal reduction

**Theorem B.** Every C4-free spanning edge subgraph of Q8 has at most 683
edges. In particular, there is no inclusion-maximal such graph with
684,685,686,687 or 688 edges.

Suppose instead that G has at least 684 edges. Add ambient edges while
preserving C4-freeness until an inclusion-maximal graph H containing G is
obtained. This is ordinary inclusion-maximality, with no switching or
optimization hypothesis. Write m=|E(H)|. Then m>=684. H has no isolated
vertex, since any edge incident with one could be added safely.

Here is the complete imported route to the upper endpoint of this range.
For every coordinate Q6 face F, and the parity induced by one fixed global
parity P, put S_F=sum binom(d_F(v),3), c_F=#{d_F(v)=6}, and
L_F=#{d_F(v)<=2}. The proved local theorem is

    4 S_F + 2 c_F <= 632 + 5 L_F.                         (1)

It allows arbitrary opposite-parity degrees and all degrees 0,1,2 on the
specified side. Its actual complete proof is
[Q6 import PROOF](../../finite8_q6_import_audit/PROOF.md), with the completed
[verification and 25 trace replays](../../finite8_q6_import_audit/VERIFICATION.md).
For clarity, the weighted bounds 2S+c for L=0,1,2,3 are respectively
316,317,321,322; for L>=4 the elementary bound is 324. These imply (1).
The degree-one and two-low replacements in that proof preserve the same
full code and all other specified-side degrees. Thus restricted faces are
not being assumed to have minimum degree three.

The current [import closure](../../finite8_maximal_route/IMPORT_CLOSURE.md)
and [crowded four-full sidecar](../../finite8_q6_import_audit/CROWDED_IMPORT_EXTENSION.md)
were actually read for this proof. The latter proves S+L<=144 at four full
Q6 roots, including low degrees. Historical audits retain their original
modulo-import wording; the present mathematical import is discharged by
the actual proof, reconstructed finite cover and 4,383,882 checked RUP
additions on all 25 inputs. This is ordinary targeted verification with
same-family provisional semantic assurance, rather than a retroactive new
canonical audit. The additional crowded-face downstream filters are not
used in branch B.

There are 112 Q6 faces. A rooted Q3 full star belongs to ten of them. For
a degree-d global root its number of locally low appearances is

    l_d = sum_(j=0..2) C(d,j) C(8-d,6-j)
        = (28,28,28,18,6,0,0,0,0)_d.

Summing (1), and using sum_P n_d=128 and sum_P d n_d=m, gives

    C(P) := sum_d C_d n_d <= 138432-201m,
    C_d = (735,534,333,177,66,0,0,105,345)_d.              (2)

For example before rearrangement the sum is
sum_d[40 C(d,3)+2 C(d,6)-5 l_d]n_d<=70784; subtracting
402m and adding 1610*128 gives twice (2). All C_d are nonnegative,
so m<=688. No historical global upper bound 687 is imported.

At most one full same-parity three-star occurs in a Q3, so the 1,792 Q3
faces also give sum_P C(d,3)n_d<=1792. Equivalently

    sum_d b_d n_d <= 6912-10m,
    b_d=(40,30,20,11,4,0,0,5,16)_d.                       (3)

Enumerate every nonnegative integer row satisfying (2),(3), n0=0 and the
two degree sums. This is a complete necessary cover, not a classification
of graphs. Its counts for m=684,...,688 are 385,170,66,20,4, totaling 645.
Completeness follows by enumerating n_d for d=1,2,3,4,7,8 within their
positive C-budget bounds, then solving uniquely for n5,n6 from the two
degree sums. The actual row order is `PROFILE_SNAPSHOT.json`, and the
enumeration proof is [maximal-route PROOF, sections 2–3](../../finite8_maximal_route/PROOF.md).
The 19 exact-683 profile exclusions and the exact-683 even-square gate
are not used in B; all m=684,...,688 rows of this cover remain present.

## 2. Three probability measures from this same H

Let lambda be the uniform distribution of the 1,120 actual coordinate
Q4 restrictions of H, transported as whole labelled cubes. Let alpha be
the average of the two point masses at H's two actual parity profiles.
Both profiles have the same m and belong to the cover just proved. Put
eta_d=sum_p alpha_p n_d(p), so H has N_d=2 eta_d vertices of degree d.

For each ambient edge uv, with retention r, its seven other directions
give states s=a+2b+4c, where a,b are the two edges parallel to that direction
at u,v and c is the translated edge. Its histogram x has total seven.
Use both endpoint orientations simultaneously. The resulting beta is a
probability distribution over the 1,024 ambient edges, not a separately
normalized conditional distribution for r=0 or r=1.

If r=1, C4-freeness prohibits state 7. If r=0, maximality requires x7>=1,
since a newly added edge lies in a C4 exactly when one of these seven
three-edge paths is already present. If a retained edge has a leaf at u,
maximality forces all seven states to be 6; a leaf at v forces all to be 5.
The unquotiented domains therefore have 1,716 missing-root histograms and
1,486 retained-root histograms. Reversing the endpoints exchanges states
1 with 2 and 5 with 6. Taking its simultaneous histogram orbits gives the
1,751 columns in the frozen arrays. The selection and full-to-selected
maps are `GENERATOR_DEDUPLICATION.json` and `GENERATOR_HISTOGRAMS.json`.
All quantities below are invariant under this one common endpoint reversal.

Thus lambda, alpha and beta are nonnegative and each has total mass one.
No independent roots, fixed bits, direction assignments or source graphs
are chosen for different row families.

## 3. Exact common equations

The native face blocks have root masks 0,1,3,6,7, dimensions
240,212,190,187,170; the vertex block has dimension 9. For a local graph K,
let c_bij(K) be its nonnegative folded upper coefficients, with denominator
64512. Off-diagonal coefficients already include both orders. For any
symmetric kernel Q write T_Q(K)=sum_(i<=j)c_bij(K)Q_ij/64512.
The sum of all face coefficients is 64512, and the sum of vertex
coefficients is 64512. These normalizations are part of the actual
[finite-eight sampling proof](../../finite8_flags/main.tex), G01–G02.

Here are all 356 equations, in their actual zero-based row order. They
are identities for the three pushforwards of H just defined.

|Rows|Identity and frozen integer implementation|
|---|---|
|0,1|sum lambda=1; sum alpha=1|
|2–6|E_lambda h_j(K)/16=sum_p alpha_p sum_d n_d(p) C(d,j)C(8-d,4-j)/8960, j=0,...,4|
|7–70|M_edge(lambda)=(Gnum/98) beta, in true symmetric-upper entries; the local numerator is U/129024|
|71–88|EP beta=RHS alpha/512, RHS_(r,d),p=(d if r=1 else 8-d)n_d(p)|
|89–124|For each d and mixed vertex state j in {1,4,5,8}, (C_1,dj-C_0,dj) beta=0; stored row divided by 7|
|125–151|2304 B beta=7 W F_vertex^T lambda, stored after division by129024|
|152–355|E_lambda L_z/64=E_beta H_z/70 for every one of the204 edge three-flag histograms|

The first marginal identity samples four of eight incident directions.
In particular it already gives 32 E_lambda |E(K)|=sum_p alpha_p m(p);
no fixed edge count 683 has been imposed.

For the edge moment identity, x/7 is the actual seven-count frequency.
On a local edge with three-count z the unbiased second-moment kernel is
(3zz^T-2diag(z))/21. Averaging over local ambient roots and applying the
common sampling law yields the displayed equation. Its pointwise lift
into the five full-face blocks is the proved `lift_to_faces` identity in
[edge-flags proof](../../finite8_edge_flags/PROOF.md): the integer lift has
denominator392. Pairing a true-upper dual y uses an edge kernel with
diagonal2y and off-diagonal y, hence denominator784 in the packed lift.
The beta generators are (xx^T+(Px)(Px)^T)/98, with the same endpoint flip P.

For EP, the endpoint degrees are a+r,b+r, where a=sum bit0(s)x_s and
b=sum bit1(s)x_s. Counting incidences at degree-d vertices gives
(8-d)N_d/1024 or dN_d/1024, proving its factor512.

For the next two families let C_r,dj count, at both endpoints of an
edge histogram, the seven vertex-rooted Q2 states with global degree d.
A mixed square has one retained and one missing root edge at that vertex,
which proves the 36 balances. Vertex states split into
I0={0,3,7}, I1={1,4,5,8}, I2={2,6}; their counts at degree d are
F0(d)=C(8-d,2), F1(d)=d(8-d), F2(d)=C(d,2). Put
B_(g,i)=sum_d Fg(d) C_all,d,i. The same-object vertex second-moment
double count is B beta=392 sum_(j in Ig)M5_ij(lambda). In folded coordinates
this is precisely 2304 B beta=7 W F_vertex^T lambda, where W has twice
diagonal and single off-diagonal entries. Full statements and proof:
[edge–vertex bridge](../../finite8_edge_vertex_bridge/PROOF.md).

Finally, H_z counts the choose-three subsets of seven directions in both
endpoint orientations (total70), while L_z counts the32 local edges in
both orientations (total64). The common double count gives35 E L=32 E H.
The exact lift is L_z=(4/5)T_Kz, where K_z=12A_z-diag(A_z)1^T-1diag(A_z)^T.
Consequently its dual enters the packed kernel as K_z/80. Proofs are
[edge3 sampling](../../finite8_edge3_sampling/PROOF.md) and
[the exact original-family lift](../edge3_quad_lift/PROOF.md).
These equations do not assert independent completion of overlapping roots.

Write them together as Ex=b. The only nonzero entries of b are b0=b1=1.

## 4. Exactly the 83 active valid rows

The full exact row list, integer parameters, normalizations, rational
weights, sources and hashes is `B684_ACTIVE_83_PARAMETERS.json`, with a
readable index in `B684_ACTIVE_83_PARAMETERS.md`. Every other one of the
8,051 stored inequality rows has weight zero and is not a premise.

* **19 PSD rows**, blocks0–3: for each integer q, T_(qq^T)(lambda)>=0.
  At a global root this is (q dot x/6)^2, averaged in the common root
  frame. It needs neither maximality nor a numerical eigenvalue claim.
* **49 integer-six rows**: for their recorded integer q,t put
  Qij=36qiqj-3(2t+1)(qi+qj)+t(t+1). For every nonnegative integer count
  x of total6, xQx=36(L-t)(L-t-1)>=0, L=q dot x an integer. The same
  sampling identity makes each expected local score nonnegative. All
  active rows have n=6; no vertex28 rounding extension is needed.
* **One leaf row**: eta8-eta1>=0. A leaf's unique neighbor is full degree8:
  each other missing edge at the leaf must close using its sole retained
  direction. Two leaves cannot have this same full neighbor, since the
  closure forced by one would give the other a second retained edge.
* **Five neighbor-capacity rows**: for a degree-t vertex, each pair of its
  retained neighbors forces a distinct missing incidence, so
  sum_(u in N(v))d(u)<=8t-C(t,2). Summing at degree t and dividing by1024
  yields J_t(beta)<= [8t-C(t,2)]eta_t/512, with exactly the beta and alpha
  of section2. The stored rows divide this nonnegative slack by16.
* **One conditional vertex row**, at
  `vertex_pricing/master_195/CONDITIONAL_VERTEX_CUT.json`: this particular
  active parameter has a simpler analytic proof than its original finite
  search. Let s be1 on{1,2,4,5,6,8} and0 on I0. Its actual matrix is
  Qij=10^6(2s_i s_j-1). For a degree-d vertex, S=sum s_i x_i=28-C(8-d,2),
  so xQx=10^6(2S^2-784). For d1,...,8 its stored B_d is exactly the
  negative of this number: (686,446,136,-184,-466,-674,-784,-784)*10^6.
  Therefore E_lambda T_Q+sum_p alpha_p sum_d B_d n_d(p)/(128*784)=0.
  Its stored B0=0 causes no problem because n0=0. Thus this active row
  uses only the degree-group identity and no isolated vertices, and does
  not require importing the stronger253440-element maximal-vertex cone.
* **Eight connector finite-six rows**: each recorded symmetric integer
  Q16 is nonnegative on all54264 nonnegative sixteen-count vectors of
  total6. For a full flag f, its connector label is f&15; pulling Q16
  back to every legal full state, with the common root averaging, preserves
  that inequality. The actual full-state label maps and all matrix entries
  are in the eight hashed source files. Their completed exact domain
  checks are linked in the parameter index. This is the complete-count
  argument of [connector proof](../../finite8_connector_frequency/PROOF.md),
  not a PSD or global-copositivity assertion about those kernels.

PSD, integer-six, connector and neighbor-capacity rows hold on every
actual C4-free graph. This specific conditional row additionally requires
no isolated vertices. The leaf and beta-domain assertions use ordinary
maximality. No parallel or
joint-projection kernel has nonzero weight in this certificate. No claim
that the discovered numerical target was a graph is used.

## 5. Rational combination and exact finite maxima

Let A=-g be the matrix of these inequalities in the convention Ax<=0.
The exact certificate rounds the stored discovery multipliers to integers
y,z with common denominator Dy=10^9, clipping z to z<=0. They are explicitly
saved in `exact_row_combination001/EXACT_COMBINATION.json`; they need not
be LP-optimal. The actual linear functional is

    a = (y/Dy)E + (z/Dy)A,
    delta = (y0+y1)/Dy = 92993/500000000.                  (4)

For the three actual measures, Ex=b and Ax<=0 imply a dot x>=delta.
The construction rebuilds every term from its integer parameter and real
denominator, rather than interpreting a rounded aggregate as PSD. Its
working common denominator is D=551690954352885760000000000. The exact
alpha and beta maxima over the complete finite covers are

    Amax = 276661617/1027604480000000000,
    Bmax = 1/250000000.                                  (5)

The lambda part has exact packed kernel numerators NW and histogram
numerators NH, so its score at any local K is

    l(K) = sum c_i(K) NW_i/(64512 D)
         + sum_(j=0..4) h_j(K) NH_j/(64512 D).             (6)

These integers and both complete finite coefficient lists are in the
same exact-combination file. The reconstruction uses the face-edge lift
denominator784, the27-moment factor7/2, and the204-edge3 factor1/80.
Its source and the frozen scientific input hashes are bound in
`exact_row_combination001/RESULT.json` and `FROZEN_CANDIDATE_INPUT_HASHES.json`.
Native floating map comparisons are useful diagnostics but are not the
reason (4) is a valid rational row combination.

Put T=10^9 and round NW*T/D and NH*T/D to integers q_i,qh_j. Define
the query score

    lhat(K)=[sum c_i(K)q_i+sum h_j(K)qh_j]/(64512 T).

Nonnegativity and the two coefficient-mass identities in section3 give
a uniform bound over **every** C4-free local Q4:

    |l(K)-lhat(K)| <= eps_face+eps_vertex+16eps_hist/64512
      = 529874002317/601295421440000000000 =: eps.         (7)

Here each eps is the exact maximum absolute coefficient rounding error
in that group, divided by its exact denominator. The factor16 is the
total vertex histogram mass. This is a rational error bound against the
valid combination (4); no positivity of an approximately rounded matrix
is assumed.

Complete integer maximization of this query gives raw maximum -37440,
hence

    max_K lhat(K) = -13/22400000000 =: M.                 (8)

The independent from-scratch program enumerated all13,150,453 legal
marked completions, independently of the 15,152-column discovery pool.
Its witness is mask146532333. The previous layer-pair program also
returned -37440, with witness3889906149; literal C4/common-neighbor and
original Python integer-score replay passed. A witness is only an attained
local maximum, not a Q8 counterexample. The independent raw transcript is
[complete_oracle.stdout](../../finite8_root_checks/exact_dual/B_enriched8_candidate001/complete_oracle.stdout.txt).
The full-domain coverage proof and implementation are in
`../../finite8_full_oracle_independent/`; this program covers all ordered
Q3-layer pairs, every permitted crossing set, and the full cube-isometry
transport. The hash-bound query files are

    oracle_matrices SHA256 1a909bcc59b9ff22c679fc0d2c0ffed6e6a145e83688053793319e746feee372
    oracle_linear   SHA256 1c2c16f76a493f9b171a145d7748b7993b1e092a5716524f43f9d6ef03c02506

No hidden-direction reduction or one-representative-per-coarse-class claim
is needed by the independent maximization. Search-library deficiencies
found in preceding scopes do not weaken (8).

## 6. Contradiction and scope of the conclusion

Since each of lambda, alpha and beta has mass one, equations(5)–(8) imply

    a dot x <= M+eps+Amax+Bmax.

But exact fraction subtraction gives

    delta-(M+eps+Amax+Bmax)
      = 782808475930428709/4209067950080000000000 > 0.      (9)

This contradicts (4). Consequently no ordinary maximal H with
684<=m<=688 exists. Section1 takes every original G with at least684
edges to such an H, proving Theorem B. The argument does not assume that
a maximal extension retains its original edge count. The still separate
case m=683 is not excluded, so the main upper682 goal remains OPEN.

## 7. Minimal replay and acceptance status

No LP, working-set continuation or library reconstruction is required to
replay the certificate. With BASE the enclosing near-extremal directory,
run the following with a fresh output directory OUT:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 "$BASE/finite8_root_checks/reconstruct_exact_dual.py" \
  "$BASE/finite8_degree_augmentation/pool_B684plus_enriched8" "$OUT"
cd "$OUT"
"$BASE/finite8_full_oracle_independent/independent_q4" \
  oracle_matrices.txt --linear oracle_linear.txt > complete_oracle.stdout.txt
PYTHONDONTWRITEBYTECODE=1 python3 \
  "$BASE/finite8_degree_augmentation/check_B684_certificate.py" \
  "$OUT" complete_oracle.stdout.txt
```

The full profile/domain/bridge/active-row mathematics above must also be
audited. The current independent reconstruction has already matched every
packed, histogram, alpha and beta coefficient and rebuilt the common
equations from geometry; it independently repeated the8 complete connector
checks and the full Q4 maximization. This is substantive evidence, not a
substitute for the fresh whole-Theorem-B proof-checker still requested by
Root. Historical local audits retain their original scopes. This directory
does not alter their claims, the shared wiki, or the main Goal state.
