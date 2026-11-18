# Actual degree-score violator added; a new exact PSD obstruction

The818 and1160 raw runs and results are preserved. Root then supplied the actual legal Q4 with mask3287023647 from its full degree-score oracle:14 edges, h4=4,h1=12, u=3h4-h0-h2=12. This is a counterexample to the restricted-pool inequality u<=0, not a Q8 graph. This worker consumed its literal edge set, checked its mask and all24 non-full Q2 faces through local coefficient reconstruction, and included every384 cube isometry, yielding16 distinct new graphs. Their union with the old1160 pool has1176 graphs, frozen in pool_with_violation/POOL_GRAPH_CODES.json.

The new scope keeps the exact792-profile snapshot and the same five hypergeometric equations, six finite8 matrices and common lambda/alpha. It additionally imports the actual683 even-square>=19 gate from q8_small_defect_gate/main.tex, read in full here. Each global Q2 is in C(6,2)=15 Q4s, so the same lambda satisfies

\[
\mathbb E_\lambda[\#\text{even Q2s in }K]\ge15\cdot19/1120=57/224.
\]

The code counts all24 actual Q2 faces of each K, including zero-edge and two-edge squares. This gate is a new explicitly recorded scope, not mixed into the earlier preserved tests.

## Actual primal/eigen-cut run

`coupled_violation_lp.py` actually generated all1176 integer degree and finite8 coefficient arrays and ran the primal max-margin model. Its block support sizes are (4,30,29,0,39,8). Initially110 coordinate PSD directions were present. The first solution met all affine constraints and the new even-square gate but had genuinely negative eigenvalues in five blocks. Twenty-three integer eigendirections were added. The next LP had maximum margin -0.000372023809523814, returning a numerical restricted dual candidate. This was not accepted on tolerance: the exact certificate below independently proves the restricted obstruction using one small integer PSD direction and the exact degree equations.

The final affine candidate had alpha=1 on the all5/6 profile and mass approximately0.002232142857 on the new orbit. This floating LP candidate is not PSD and is not a graph. All numerical traces and rays are preserved in pool_with_violation/; the root EIGEN_RAYS file contains both actually used and newly generated final directions, so LP inequality dual indices refer to the prefix in force at that iteration, not necessarily all saved rays.

## Exact one-ray certificate

In the original block0 state order, let q=e_115-e_236. With the common coefficient denominator64512, define

\[
a(K)=q^TM_0(K)q
=\frac{c^K_{0,115,115}+c^K_{0,236,236}-c^K_{0,115,236}}{64512}.
\]

The original coefficients are upper-coordinate functional coefficients, so the off-diagonal minus sign above already includes the symmetric-matrix factor of two. `certify_orbit_rejection.py` first checks the saved twice-integer matrices and then reconstructs each local coefficient vector directly from every literal graph, obtaining exactly

\[
a(K)=0\quad\text{for all1160 old graphs},\qquad
a(K)=-1/12\quad\text{for each of16 new images}.
\]

Let m be the total lambda mass on the new orbit. Positive semidefiniteness of the same averaged block0 would imply

\[
0\le q^TM_0(\lambda)q=-m/12,
\]

hence m=0. But the exact degree/profile bridge already requires E u>=3/112; the old graphs have u<=0 and the orbit has u=12. Therefore

\[
12m\ge3/112,\qquad m\ge1/448>0,
\]

a contradiction. This proves restricted1176 infeasibility with exact integers/rationals, independently of LP dual tolerances. The even-square gate is not needed for this particular contradiction, and was not used as a new mathematical gain once the weaker predicate sufficed.

## New full-domain oracle interface

The preceding argument becomes the local score

\[
F(K)=u(K)+144a(K).
\]

Every1176 current K has F<=0. For an actual683 input, the same lambda would satisfy

\[
\mathbb E F\ge3/112,
\]

because the degree equations give the lower bound on E u and actual finite8 PSD gives E a>=0. Thus the next full legal-Q4 oracle must separate F, rather than merely recheck u or adjust the same restricted pool. The exact integer score is

\[
64512(3h_4-h_0-h_2)+144(c_{0,115,115}+c_{0,236,236}-c_{0,115,236}).
\]

The structured coefficients are in pool_with_violation/NEXT_ORACLE_SCORE.json. If a genuine positive-score Q4 exists, it is the next actual column; it is not a Q8 counterexample. A complete nonpositive full-domain oracle would require its own coverage and caller review before any full upper682 claim. No such full separation of F was performed here; Root owns it.

Actual final commands, both exit0:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 coupled_violation_lp.py
PYTHONDONTWRITEBYTECODE=1 python3 certify_orbit_rejection.py
```

The exact result is pool_with_violation/EXACT_ORBIT_REJECTION.json. All writes stayed within this worker directory; previous accepted proofs, shared wiki, MathRSI and other workers were unchanged. No actual683 graph or full-domain NO was found. The primary upper682 goal remains OPEN.
