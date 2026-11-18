# Actual global degrees coupled to one finite8 Q4 distribution

This is a completed first augmentation test and exact sampling proof, not an unrestricted683 exclusion. The frozen792-profile cover and both tested legal-Q4 pools have incompatible degree marginals. An explicit exact unary separator is returned for the full Q4 oracle. No primal feasible point, Q8 graph or full-domain NO is claimed.

## A. One common actual input and frozen necessary profile cover

Let G be any actual simple C4-free683-edge subgraph of Q8. Its256 global vertex degrees have histogram N_d, d=0,...,8. Both actual parity classes have128 vertices and degree sum683. At the time of the read/copy, the current reviewed necessary cover had792 rows after22 exclusions. The exact bytes are frozen in PROFILE_SNAPSHOT.json, SHA256

`452aa0e377ac002ae5687cd83268de253290e378e00a552c1f9e70840b6ce945`.

This is a necessary integer relaxation, not a graph census. If the two actual parity profiles are rows r and s, take alpha_r=alpha_s=1/2 (or alpha_r=1 if r=s). Then

\[
N_d=2\sum_r\alpha_r n_d(r),\qquad\alpha_r\ge0,\quad\sum_r\alpha_r=1.
\]

Allowing any convex mixture alpha enlarges this actual domain. The later791-row cover is a subset; this run does not overwrite the actual792 input or relabel it791. No primal alpha exists for either restricted run below, so no discarded-row positive-weight sensitivity is hidden.

## B. Exact Q4 sampling and histogram bridge

There are C(8,4)2^4=1120 coordinate Q4 faces. Let lambda_K be the empirical distribution of their actual edge restrictions, represented with the four varying coordinates in increasing order. Repeated restrictions are aggregated; sum lambda=1. Every K is an actual legal C4-free Q4.

Sample a uniformly random coordinate Q4 face and then a uniformly random one of its16 vertices. A specified global vertex belongs to exactly C(8,4)=70 such faces. Hence the sampled root is uniform among256 global roots; conditional on that root, the four varying directions are uniform among the70 four-subsets of the eight original axes. All these samples use the same actual graph and its actual root stars. Nothing assumes independent stars or independent Q4 restrictions.

For a global degree-d root, the restricted degree is j on exactly

\[
\binom dj\binom{8-d}{4-j}
\]

of its70 containing Q4 faces. Let h_j(K) count degree-j roots of K. The exact unnormalised double count is

\[
\sum_{\text{1120 actual }K}h_j(K)
=\sum_{d=0}^8N_d\binom dj\binom{8-d}{4-j}.\tag{B1}
\]

Dividing by1120*16=256*70 and substituting the same global alpha gives

\[
\sum_K\lambda_K\frac{h_j(K)}{16}
=\sum_r\alpha_r\frac{\sum_d n_d(r)\binom dj\binom{8-d}{4-j}}{8960},\quad j=0,\ldots,4.\tag{B2}
\]

Equivalently the exact integer-coefficient coupling is

\[
560\sum_K\lambda_K h_j(K)
=\sum_r\alpha_r\sum_dn_d(r)\binom dj\binom{8-d}{4-j}.\tag{B3}
\]

For each k=0,...,4, count a global rooted k-star by its k retained directions. It occurs in C(8-k,4-k) actual Q4 faces, so

\[
\mathbb E_K\sum_{v\in K}\binom{d_K(v)}k
=\frac{\binom{8-k}{4-k}}{1120}\sum_{v\in Q_8}\binom{d_G(v)}k.\tag{B4}
\]

These are equivalent factorial moments of the same degree distribution. In particular the k=1 identity fixes E e(K)=683/32 and E rho(K)=683/1024; the density target is not imposed on another independently chosen lambda.

The exact bridge was also run on the actual682 seed, all1120 restrictions. BRIDGE_CHECK.json verifies B1 for all five j and B4 for all five k with integer arithmetic. Its local histogram totals are (2,872,6402,8512,2132), summing to17920 rooted slices, and the global histogram is N4=2,N5=168,N6=86. This is regression evidence, not an additional theorem premise. An initial regression assertion had an erroneous extra normalisation factor; it was corrected to B1. The LP equations already used the correct normalized B2 and were unchanged.

## C. Same lambda in all six finite8 matrices

The existing finite8 common-Q4 coefficient interface is imported from ../finite8_flags/finite_flags.py and the parent's finite8 sampling bridge. Each legal K returns upper-coordinate integer coefficients c^K_(b,i,j), common denominator64512. Let C_b(K) be twice the symmetric integer coefficient matrix: diagonal2c and off-diagonal c. The six moment matrices in this augmentation are exactly

\[
M_b(\lambda)=\frac1{2\cdot64512}\sum_K\lambda_K C_b(K),\quad b=0,\ldots,5.\tag{C1}
\]

The parent's finite8 interface states that the empirical distribution of any actual Q8 makes all these matrices PSD. This augmentation adds B2 to that same lambda, with one alpha representing the actual two parity profiles. It does not assert that separately feasible moment matrices and degree profiles arise from a graph. The full coefficient arrays, histograms and profile hypergeometric numerators used by each run are saved in COUPLED_COEFFICIENTS.npz, respectively pool1160/COUPLED_COEFFICIENTS.npz.

The primal LP uses lambda>=0, alpha>=0, both masses1, the five equalities B2, and a scalar margin s. For any integer vector q on a block's actual pool support, the valid rank-one constraint is

\[
q^TM_b(\lambda)q\ge s\,q^Tq.
\]

At s=0 these are necessary PSD cuts. The implementation initially inserts all coordinate directions; a negative eigenvalue relative to s would be quantized to an integer q and evaluated with the actual integer C coefficients before adding a valid rational cut. No eigenvalue tolerance would constitute exact acceptance. For the two runs here the marginals were already incompatible, so no negative-eigenvector cuts were needed and no floating PSD point was accepted.

## D. Actual first runs and exact separating certificate

The first pool is exactly the818 legal Q4 codes in FAMILY_OBSTRUCTION.json. Its nonzero block-support sizes are (0,16,0,0,16,4). The second, separate scope uses all1160 legal codes frozen from working_graphs.json, adding the actual Q7 A/B slices; its support sizes are (0,30,27,0,38,7). Each local coefficient reconstruction checks every Q2 face is non-full, hence every K is C4-free. These are restricted supports, not all C4-free Q4s.

Both initial primal LPs returned infeasible. A separate histogram-only LP, with no PSD or margin constraints, also returned infeasible in both scopes. More decisively, separate_marginals.py and separate_1160_marginals.py recovered and exactly checked this integer histogram score:

\[
c=(-2,-1,-2,-1,2),\qquad u(K)=3h_4(K)-h_0(K)-h_2(K).
\]

Since sum h_j=16,

\[
\sum_jc_jh_j(K)=-16+u(K).
\]

For every818 and every1160 pool graph, the exact integer score satisfies

\[
\sum_jc_jh_j(K)\le-16,\quad\text{equivalently }u(K)\le0.\tag{D1}
\]

Every one of the792 frozen profiles, separately checked with integer arithmetic, has the hypergeometric coefficient score at least -8945. Dividing by8960 gives

\[
\sum_K\lambda_K\frac{\sum_jc_jh_j(K)}{16}
\ge-\frac{1789}{1792}>-1,\tag{D2}
\]

with strict gap3/1792 from D1. The unique minimizing profile is (0,0,0,0,0,85,43,0,0), which remains in the later791 cover. Thus the restricted infeasibility does not depend on the newly discarded row.

For a smaller full-domain oracle interface, put

\[
w=(-70,-35,-30,-35,-34,-15,30,105,210).
\]

The entry w_d is exactly

\[
\sum_{j=0}^4\binom dj\binom{8-d}{4-j}
       (3\mathbf1_{j=4}-\mathbf1_{j=0}-\mathbf1_{j=2}).
\]

The792 profile scores n(r)·w range from15 to467, all exactly checked. From B2,

\[
\mathbb E_\lambda u(K)=\frac{\sum_r\alpha_r n(r)\cdot w}{560}
                         \ge\frac3{112}>0.\tag{D3}
\]

Equations D1 and D3 are the exact certificate that no coupled lambda/alpha exists on either restricted pool. This reasoning is independent of numerical LP tolerances and independent of the PSD constraints. The integer coefficient arrays and both MARGINAL_SEPARATOR.json files reproduce every local and profile check.

## E. Actual next mathematical obligation and limits

The exact full-domain Q4 oracle task returned to Root is:

> Enumerate/cover every legal C4-free Q4 and maximize u(K)=3h4(K)-h0(K)-h2(K). If the maximum is positive, return an actual violating K and add its full flag coefficients and degree histogram to the same primal support. If a complete verified oracle proves maximum<=0, D3 gives a full683 contradiction, subject to the existing profile/import bridges.

Neither oracle outcome is presumed. The818 and1160 restricted failures cannot be called full-domain NO. No universal local inequality D1 is claimed before that complete oracle. If violations exist, their actual graph codes are the next column inputs, rather than more tuning of the fixed six-block family or an unchanged LP retry.

The additionally offered global even-square>=19 gate was deliberately not inserted into either preserved scope: their weaker marginal predicate already resolved them. Its exact same-distribution lift, for a later distinct scope, is E_lambda[even_Q2(K)]>=15*19/1120=57/224, since every global Q2 lies in C(6,2)=15 coordinate Q4s. Any future use must keep its own explicit import and scope.

The parent owns full-domain separation, independent review and final theorem acceptance. All writes remained in this directory. No original683 graph, full upper682 proof, global canonical claim, Lean, or historical trace replay is asserted.
