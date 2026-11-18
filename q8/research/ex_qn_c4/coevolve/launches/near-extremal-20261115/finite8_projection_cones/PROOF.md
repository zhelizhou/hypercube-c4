# Small-alphabet projections of full rooted flags

## Claim and status

**PROVABLE AS STATED.** Fix one canonical root block $b$ in root order $(0,1,3,6,7)$, with full-state dimensions $(240,212,190,187,170)$. Let $S_b$ be its entire legal labelled full-flag state space. Let $1\le L\le16$ and let $\Phi_b:S_b\to\{0,\ldots,L-1\}$ be any deterministic map. There is no equivariance hypothesis. Suppose a symmetric integer matrix $Q$ satisfies

$$y^TQy\ge0\qquad\text{for every }y\in\mathbb Z_{\ge0}^L,\quad\sum_a y_a=6.$$

Then its pullback to all full states, followed by the simultaneous full root-stabilizer sum, is a valid finite-six kernel. Its finite-eight local feature has nonnegative expectation on the uniform coordinate $Q_4$ restrictions of every actual $C_4$-free $G\subseteq Q_8$. Positive rescaling preserves this inequality. No PSD or global copositivity assumption is used.

The actual first new projection is the fifteen-label parallel-square pattern $\Phi_b(f)=f\mathbin{\texttt{>>}}4$, as distinct from the old sixteen-label connector projection $f\mathbin{\&}15$. A concrete block-3/root-6 kernel strictly separates the frozen new master102 decimal point. This is a local relaxation-point exclusion. The main upper bound $\operatorname{ex}(Q_8,C_4)\le682$ remains OPEN.

## Assumptions, notation, and dependencies

All graphs are finite simple spanning subgraphs of the stated cube. The ambient absent edges remain available as coordinates. A root square has vertices $0,1,2,3$ and edge order $(0,1),(0,2),(1,3),(2,3)$. A full flag is the eight-bit code $f=c+16p$: four connectors at these vertices, followed by the four edges in the translated square. It is legal over root mask $r$ iff $p\ne15$ and no edge $ab$ has all four of its root edge, translated edge, and two connectors retained. This is exactly the coordinate-square prohibition in that rooted $Q_3$.

The full state order is increasing legal code, without separately canonicalizing individual flags. The five state counts and root actions are those defined and proved in `../finite8_flags/main.tex`, G01. The independent checker reconstructs them from the rule above. The only imported mathematical bridge is the algebraic sampling identity in that file, G02; the proof below repeats its face part and replaces the PSD argument by the actual six-count argument. No old optimization outcome, model review, or receipt is a mathematical premise.

Dependency map: the complete small histogram test implies pullback validity; full-state permutations imply invariant-sum validity; common transport makes the local feature independent of root gauge; finite-eight sampling identifies its expectation with actual root quadratics. Exact decimal reconstruction and separate integer replay establish the concrete separation sign.

## 1. Complete small domain and full-state pullback

For a full-state integer count vector $x\in\mathbb Z_{\ge0}^{S_b}$ with $\sum_i x_i=6$, define

$$y_a=\sum_{i:\Phi_b(i)=a}x_i.$$

Every $y_a$ is a nonnegative integer and $\sum_a y_a=6$. Define the full matrix $B_{ij}=Q_{\Phi_b(i),\Phi_b(j)}$. Expanding both finite sums gives

$$x^TBx=\sum_{a,z}Q_{az}\Big(\sum_{i:\Phi_b(i)=a}x_i\Big)\Big(\sum_{j:\Phi_b(j)=z}x_j\Big)=y^TQy\ge0.$$

This includes every legal full state. Labels unused by $\Phi_b$ cause no difficulty: testing all small histograms is sufficient even when only a subset is realizable. For the concrete parallel map, all fifteen labels are present in every block, because setting all connectors to zero makes every translated pattern $p=0,\ldots,14$ legal.

There are $\binom{L+5}{6}$ nonnegative integer $L$-vectors of total six, by the stars-and-bars bijection. Reuse of the complete sixteen-label domain is exact: retain precisely the rows whose coordinates $L,\ldots,15$ vanish, then discard that zero tail. This is a bijection onto the desired domain. The actual loaded sixteen-label source checks all 54,264 distinct vectors, their signs and sums, and the packed moment columns $y_i y_j/36$. The filtered fifteen-label domain has 38,760 rows. The checker independently enumerates multisets of six labels rather than loading those arrays. `GENERIC_BOUNDARY_CHECK.json` also checks the filtered counts for every $L=1,\ldots,16$.

## 2. Full root averaging needs no label action

Let $H_b$ be the actual root stabilizer, of size $8,2,2,4,2$ in the stated block order. Its action sends legal full flags to legal full flags and therefore permutes their full-state IDs. Write $\pi_h$ for this permutation and define the integer sum

$$K_{ij}=\sum_{h\in H_b}B_{\pi_h(i),\pi_h(j)}.$$

For fixed $h$, grouping the counts $x_i$ according to $\pi_h(i)$ gives another nonnegative integer full-state count vector $x^{(h)}$ of total six. Consequently,

$$x^TKx=\sum_{h\in H_b}(x^{(h)})^TBx^{(h)}\ge0.$$

For $g\in H_b$, composition $h\mapsto hg$ permutes the sum's terms, so $K_{\pi_g(i),\pi_g(j)}=K_{ij}$. This proves invariance as well as validity. There need not exist a permutation of labels compatible with $\Phi_b$: the permutations in this proof act before applying $\Phi_b$, on actual full states. Averaging a projected label matrix using a nonexistent label action would not implement this proof.

The producer exports this full integer $K$ directly, its full-state order, all $\pi_h$, the unsummed small $Q$, and a positive scale $s=\max(1,\max_{ij}|K_{ij}|)$. The consumer uses $K/s$. It must not replace the exported full sum by an assumed label quotient. The explicitly non-equivariant three-label example in `check_generic_boundary.py` has no induced label action in several blocks; its full sum and literal 682-edge bridge still check exactly. This test illustrates the interface, while the finite-sum proof establishes the general statement.

## 3. Common root frame and exact finite-eight averaging

Fix one actual root square $F$ of the same original graph $G\subseteq Q_8$. Its six external directions produce six actual legal full flags. Choose one root-to-canonical square isometry and apply it to all six flags. Let $x_F$ be their full-state count vector. The preceding argument gives $x_F^TKx_F\ge0$. A different canonicalizing isometry differs by one element of $H_b$. Invariance of $K$ makes its quadratic and its paired entries independent of this choice. Both flags in a pair use this same root map. No flag-specific canonicalization, independent completion, or independently chosen source graph is used.

For a legal labelled $Q_4$ graph $A$, each of its 24 root squares has exactly two external flags $s_F,t_F$. For one selected block put

$$T_K(A)=\frac1{24}\sum_{F:\,r(F)=b}\left[\frac56K_{s_Ft_F}+\frac{K_{s_Fs_F}+K_{t_Ft_F}}{12}\right].$$

This formula explicitly includes collisions. To verify the coefficients, fix a global root with flags $s_1,\ldots,s_6$ and put $u=x_F/6$. Drawing two independent directions yields an equal-direction event of probability $1/6$, so

$$u^TKu=\frac56\,\mathbb E_{i\ne j}K_{s_i s_j}+\frac16\,\mathbb E_i K_{s_i s_i}.$$

The 1,792 coordinate root squares of $Q_8$ each belong to $\binom62=15$ coordinate $Q_4$'s. Choosing a uniform $Q_4$ and then a uniform one of its 24 roots therefore chooses a uniform global root and an unordered pair of distinct external directions. Symmetry of $K$ makes that cross term equal the ordered-distinct average. The equally weighted two diagonal terms give the single-direction average. It follows that

$$\mathbb E_A T_K(A)=\frac1{1792}\sum_{F:\,r(F)=b}\frac{x_F^TKx_F}{36}\ge0.$$

Every term comes from the same actual $G$ and its actual restrictions. The implication applies whether or not $G$ is maximal and for every edge count. Positive division by $s$ gives the exact same-lambda valid feature $\mathbb E_\lambda T_{K/s}\ge0$. A nonnegative multiplier may be used in a combined certificate. This does not assert individual local features are nonnegative.

## 4. Native upper coordinates and projection collisions

`finite_flags.local_coefficients` returns folded upper coefficients $c_{bij}(A)$ with denominator 64,512, so a full symmetric matrix is evaluated as

$$T_K(A)=\frac1{64512}\sum_{i\le j}c_{bij}(A)K_{ij}.$$

The upper off-diagonal coefficient already includes both orders; consumers insert no additional factor two. To represent a symmetric moment matrix, use twice-diagonal entries $2c_{bii}$ and off-diagonal entries $c_{bij}$ in both symmetric positions, with denominator $2\cdot64512$. When two different full-state IDs map to the same label, both symmetric entries land on one projected diagonal. The producer accordingly contributes $2c_{bij}$ whenever the two projected labels agree, even if the original IDs differ. The independent literal checker computes the ordered matrix directly and checks every entry.

Native coefficients already average over the full common root stabilizer. If $U/(2\cdot64512D)$ is the projected moment reconstructed from exact decimal weights of common denominator $D$, the pairing with the exported integer sum is

$$\mathbb E_\lambda T_K=\frac{|H_b|}{2\cdot64512D}\sum_{a,z}Q_{az}U_{za}.$$

This identity uses invariance of the native full moment, not equivariance of the projection. Alternatively the consumer can pair the exported full $K$ directly with the native folded coefficients. `score.py` implements this latter form.

## 5. Actual new input, discovery, and exact acceptance

The frozen input is the byte copy `parallel15_master102/INPUT_POINT.json`, SHA256 `edb7e4aeff257229fe93c1b0c2c944d9ec7397329990b8563ce2b0962e08220d`. It is master102 of the current 356-equality, 14,838-library-graph scope, and explicitly reports 7,967 full stored cuts checked. Its original file postdates `SCOPE_INCREMENT_004_CONNECTOR4.json`, which introduced rows through 7,893 (7,894 total). Thus this probe uses a new post-four-connector point, rather than the already excluded old master048. The input has 762 nonzero graph weights. Its original status is `FULL_STORED_SCOPE_FLOAT_POINT_NONPSD`, with `exact_acceptance_done=false`, `is_graph=false`, and `primary_goal=OPEN`.

Decimal weights are read as exact rational numbers without renormalization. The moment file records their actual sum. The mathematical validity of a kernel is independent of any numerical equality or PSD residual in this diagnostic point; the exact negative pairing pertains precisely to these stored decimals.

Each of five blocks received one bounded eight-second dual LP over the complete fifteen-label domain. LP variables are packed upper coefficients: a recovered packed diagonal variable contributes twice to the symmetric integer diagonal, while an off-diagonal contributes once to each symmetric off-diagonal. All LPs finished in about 0.53–1.09 seconds; their statuses only discover candidate matrices. Integerization used scale $10^6$. If the exact minimum is $m<0$, adding $rJ$ with $r=\lceil -m/36\rceil$ repairs every total-six quadratic, because $y^TJy=36$. This repair is nonnegative and uses the exact minimum over the complete domain.

Block 3 (root mask 6) produced one strict cut. Before repair its minimum was $-8$; $r=1$ gives exact complete-domain minimum 28. Its stabilizer has size four. The full 187-by-187 invariant integer kernel has positive scale 8,000,004. Its exact raw same-lambda pairing is

$$-\frac{15940415645124021372345799259}{62500000000000000000000000},$$

and its normalized pairing is

$$-\frac{15940415645124021372345799259}{500000250000000000000000000000000}\approx-3.188081534984\cdot10^{-5}.$$

This is strictly below the declared $-10^{-7}$ threshold. The emitted cut's SHA256 is `7dbfa0d60749c220a88a3e3b462c9a24b70acfc23405337e7454238fd595573f`. All other blocks returned no meaningful separator in this bounded call. That is inconclusive: no exact primal decomposition or cone membership is asserted, and no unchanged old-point LP was repeated.

## 6. Checks and remaining scope

`check_projection_point.py` uses the standard library only and imports neither the producer, the native state/action definitions, nor the histogram arrays. It reconstructs full flag legality, all square isometries, root stabilizers, actual point Q4 geometry, ordered projected moments, and all 38,760 multiset six-count vectors. It regenerates the exported full kernel and checks invariance, exact normalization, exact target pairings and hashes. Its result is `parallel15_master102/INDEPENDENT_CHECK.json`.

On the actual 682-edge seed (SHA256 `185d2857fa64b4ff8f53314363333f5ca1ee85c3560d254027d1b2e623c56a2c`), the checker verifies ambient edge legality and absence of C4, then compares all 1,792 global root quadratics with all 1,120 coordinate Q4 local features. Signed synthetic finite-six kernels exercise the other four blocks when there is no emitted cut there. This seed has no root-mask-6 squares, so the concrete cut contributes zero in this calibration; this fact is retained rather than presented as a nonzero block-3 test. Additional literal local tests check the concrete block-3 functional independently on all 762 frozen-point graphs and explicit root-6 graphs. A nonvacuous actual-Q8 calibration uses exactly the two edges $\{(0,1),(2,3)\}$. It has one root of type 6, with all six external full flags zero. Here $K_{00}=8{,}000{,}004$, and both the 1,792-root and 1,120-slice averages are exactly $K_{00}/1792=2000001/448$ before scaling, and $1/1792$ after scaling. See `NONZERO_Q8_CALIBRATION.json`.

The full exported kernel also has an exact smaller-total witness: full-state codes 32 and 64 each occur once and code 112 occurs twice. These are legal over root 6, and the resulting total-four quadratic is $-1{,}454{,}496$. Thus the actual exported full kernel is non-PSD and non-copositive while remaining valid on every full-state count vector of total six. This is recorded in `FULL_SCORE_CHECK.json`; no exact PSD qualification is asserted for the target projection.

This is an ordinary local proof/data/check package returned to Root for integration. It creates no canonical claim or wiki entity, changes no shared code or numerical scope, runs no old search/global LP, and does not replace the final whole-domain certificate obligation. Exact full-Q4 maximization and a strict valid-row combination would still be needed to prove the original upper682 goal.
