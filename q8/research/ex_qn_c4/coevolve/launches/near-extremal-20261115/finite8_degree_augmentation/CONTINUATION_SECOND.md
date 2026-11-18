# Second actual full-oracle column and a profile-free new separator

Root separated the previous F=u+144*q0^T M0 q0 over its full Q4 oracle and supplied a genuine positive-score graph, mask2849669127. This13-edge graph has h4=3,h1=11,h0=1,h3=1, u=8 and q0^TM0q0=1/144, so F=9. Its literal data are frozen in pool_second_violation/SECOND_ORACLE_VIOLATOR.json. This disproves a universal F<=0 claim; no such claim was made here. The graph is not a Q8 counterexample.

All original1176 graphs and this new graph were reconstructed from literal edges. Exact columns were grouped by all five degree counts, their even-square count, and every integer coefficient in all six finite8 blocks. The1177 literal graphs give64 distinct complete feature columns. This deduplication preserves every possible convex mixture in the tested affine/PSD model. It is not an isomorphism or graph-completeness assertion. As a further check, all384 Q4 isometries of the new literal graph were individually evaluated and had identical finite8 coefficient vectors, so adding redundant isometric copies would not change this relaxation.

## Actual new LP

The new pool_second_violation scope keeps the same actual792-row snapshot and five hypergeometric equalities, one common lambda for all six finite8 matrices, and the explicitly scoped even-square lower bound57/224. Its max-margin LP was actually run. At the first affine candidate several matrices had negative eigenvalues, and24 integer eigendirections were added. The second LP had maximum margin approximately -5.789353696e-5, with a single negative-dual PSD ray active. The numerical result was not treated as exact acceptance. The following much smaller integer ray was extracted and verified independently of the floating dual.

## Exact small-integer PSD/unary separator

Define v(K)=3h0(K)+3h4(K)-h2(K). In original block2 state order (full dimension190), take q with these eight nonzero entries:

\[
q_1=q_{41}=q_{91}=q_{141}=q_{151}=-1,
\quad q_{59}=q_{109}=1,\quad q_{159}=2.
\]

All other entries are zero. The matrix qq^T is PSD. Define

\[
a(K)=q^TM_2(K)q
=\frac{\sum_i c^K_{2,i,i}q_i^2+
             \sum_{i<j}c^K_{2,i,j}q_iq_j}{64512}.
\]

The off-diagonal formula uses the original upper-coordinate functional coefficients, so no further factor of two is inserted. `extract_second_dual.py` rounded the original eigenvector to this small q, then checked exact rational coefficient intervals on all64 columns. It obtained

\[
                  v(K)+(128/3)a(K)\le0
\]

on every current column. The small-ray search took only two deterministic scales; the stated inequality, rather than the search, is the certificate. `certify_second_separator.py` then reconstructed all1177 original literal graphs, computed every exact local coefficient vector anew, and checked the equivalent integer score

\[
S(K)=1512(3h_0+h_4\cdot3-h_2)
       +\sum_i c^K_{2,i,i}q_i^2+
             \sum_{i<j}c^K_{2,i,j}q_iq_j\le0.
\]

Its exact score range on all1177 graphs is [-22176,0]. The complete result is pool_second_violation/EXACT_FINAL_CHECK.json. This verification uses integer arithmetic and does not import any floating eigenvalue or LP dual as a proof premise.

The original-domain caller is now simpler than the frozen profile relaxation. ANALYTIC_DEGREE_LOWER_BOUND.md proves from the two degree sums alone that every actual683 graph has E u>=3/112, and hence E v>=3/112. The empirical Q4 distribution of the same actual graph has M2(lambda) PSD by the parent's finite8 bridge. Therefore

\[
\mathbb E_\lambda S(K)=1512\mathbb E v(K)
                       +64512q^TM_2(\lambda)q
                      \ge1512\cdot3/112=81/2>0.
\]

Thus S<=0 on the entire legal-Q4 domain would contradict every actual683 graph, without any profile import or even-square gate in this final caller. At present it is certified only on the1177-graph current pool. The even-square gate and profile alpha remain in the preserved numerical run; their stronger assumptions are unnecessary for this exact restricted obstruction.

## Concrete next full-domain operation

Root has been given pool_second_violation/NEXT_ORACLE_SCORE.json, containing the five integer degree weights [4536,0,-1512,0,4536] and36 upper-coordinate matrix weights q_iq_j in block2. All other blocks and the density term are zero. The displayed integer S score has no remaining64512 denominator. If an oracle implementation divides its finite8 c*Q part by64512, it must multiply these listed matrix weights by64512; no off-diagonal doubling is required for the original upper-coordinate c.

The next operation is full legal-Q4 separation of S. A positive-score actual K is another new column, not a Q8 graph. A complete nonpositive oracle would still need independent coverage and same-object caller verification before asserting full upper682. No full S separation was performed by this worker. Root owns that oracle and the primary goal remains OPEN.

Executed commands, all final exit0:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 coupled_second_violation_lp.py
PYTHONDONTWRITEBYTECODE=1 python3 extract_second_dual.py
PYTHONDONTWRITEBYTECODE=1 python3 certify_second_separator.py
```

Prior818,1160 and1176 raw runs and certificates were preserved. Only this worker directory was written. No shared wiki, MathRSI, frozen accepted proof, other worker source, or original research graph was modified.
