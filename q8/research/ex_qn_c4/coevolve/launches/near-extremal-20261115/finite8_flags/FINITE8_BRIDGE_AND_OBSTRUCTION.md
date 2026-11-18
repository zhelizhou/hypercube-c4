# Exact finite-eight rooted flags and a strict six-block obstruction

## Result and precise scope

For the original five full-face flag blocks and nine-state vertex block, there is an exact finite-$n=8$ local-score-to-global-density bridge with no maximum-diagonal error. The score retains face collisions and all three vertex direction-pair overlap types. Its geometry, gauges and integer coefficients are given below.

This fixed six-block family cannot prove the requested upper bound. An explicit rational distribution on818 legal $C_4$-free $Q_4$ graphs has all six exact finite-eight moment matrices positive semidefinite and mean density

$$\boxed{\rho_* = \frac{76799371703}{113777777664}
 \approx0.6749944785333929
 >\frac{683}{1024}.}\tag{1}$$

Its strict gap is $455241445/56888888832$. Therefore every score in this family has a legal local graph with score at least $\rho_*$. This is a **lower bound on the best upper certificate available to this family**. It is not a $Q_8$ graph, a counterexample to $\operatorname{ex}(Q_8,C_4)\le682$, or a new graph-theoretic upper bound. The primary full682 goal remains OPEN.

The point, every integer probability weight, every complete nonzero moment block and every rational LDL factor are in [FAMILY_OBSTRUCTION.json](FAMILY_OBSTRUCTION.json). A standalone second geometry implementation recomputes all818 legal local graphs and all six matrices, verifies their exact LDL factors and performs a direct-root-versus-common-$Q_4$ normalization test on the actual682 $Q_8$ seed. Its result is [OBSTRUCTION_VERIFICATION.json](OBSTRUCTION_VERIFICATION.json), PASS. This is author exact verification and a second implementation, not an independent-agent or canonical proof-checker audit.

## 1. Original states actually consumed

The read-only scientific implementation is

`/mnt/c/users/anony/desktop/project/math-rsi/plugins/hypercube-extremal/archive/source/certificate_final_q4/verify_local.cpp`.

The theory guide, full-face state construction, old vertex-flag builder and geometric audits were also read. The original guide describes the asymptotic score and its coarse finite correction; its audits check the face collision identity, but neither the guide nor the inspected scorer implements the new exact finite-eight overlap score. This work does not claim the general PSD/collision identities are new.

Use the original rooted $Q_2$ vertex order $00,10,01,11$ and edge order

$$01=(0,1),\quad02=(0,2),\quad13=(1,3),\quad23=(2,3).$$

A full-face flag extends an actual root square $F$ in one external direction. Its eight-bit state consists of four connecting edges, ordered by the root's four vertices, followed by the translated square's four edges in the order above. The translated square is not full. If a root edge and its parallel translated edge are retained, the two connecting edges at their endpoints cannot both be retained. For canonical root masks $r=0,1,3,6,7$, ascending legal eight-bit codes give dimensions

$$240,212,190,187,170.$$

These are the exact original state orders. A root square of any allowed labelled edge pattern is transported to its canonical root by a $D_4$ square symmetry. Both flags are transported by the same symmetry. The matrix is then averaged under the same canonical root stabilizer:

$$\bar Q_r=\frac1{|H_r|}\sum_{h\in H_r} P_h Q_rP_h^\mathsf T,\qquad |H_r|=8,2,2,4,2.$$

This preserves PSD. Separate canonicalization of the two flags is not used.

The vertex block is not an edge-count or degree-pair flag. It is the complete four-edge $Q_2$ through a marked vertex and two directions, quotiented only by interchange of those two directions. The edge-code swap interchanges bits0/1 and2/3. The nine canonical representatives, in the original ascending order, are

$$0,1,3,4,5,6,7,12,13.$$

Write $\eta(v,A)$ for this state, where $A$ is an unordered two-direction set. The full square code15 is forbidden. Root translations are not part of this vertex quotient: the marked vertex remains its local $00$ corner.

## 2. Exact face-root sampling at finite eight

Let $G\subseteq Q_8$ be any actual $C_4$-free graph. Fix one actual coordinate root square $F$, including its actual embedding and one consistent root frame. There are $q=8-2=6$ external directions. Let $s_k$ be their full-face states after the common root transport, and let $u$ be their empirical probability vector. Two independent uniform external directions give

$$u u^\mathsf T=\frac56 R_{\ne}+\frac16\operatorname{diag}(u),$$

where $R_{\ne}$ is the ordered distinct-direction joint distribution. Consequently

$$\frac56\mathbb E_{k\ne\ell}\bar Q_r[s_k,s_\ell]
 +\frac16\mathbb E_k\bar Q_r[s_k,s_k]
 =u^\mathsf T\bar Q_ru\ge0.\tag{2}$$

For a coordinate $Q_4$ restriction $K$, each of its24 root squares has precisely two external directions, with actual states $s,t$. Define

$$F_8(K)=\frac1{24}\sum_{F\subset K}
 \left[\frac56\bar Q_{r(F)}[s,t]
 +\frac1{12}\bigl(\bar Q_{r(F)}[s,s]+\bar Q_{r(F)}[t,t]\bigr)\right].\tag{3}$$

Choose a uniform coordinate $Q_4$ of $Q_8$ and then a uniform root square of it. Every actual root square appears equally often, and its two external directions are a uniform distinct two-subset of the six available directions. By symmetry of $Q$, the cross entry in (3) equals the ordered distinct-pair average; the mean of its two diagonals equals the single-direction marginal. Thus

$$\mathbb E_K F_8(K)=\mathbb E_F u_F^\mathsf T\bar Q_{r(F)}u_F\ge0.$$

This uses all actual root types with their true frequencies. It neither replaces their diagonals by a maximum nor asserts that the matrix of an individual $K$ is PSD.

## 3. Exact vertex overlap sampling

Fix an actual vertex $v$ of $G$. There are $\binom82=28$ unordered direction pairs. Independently and uniformly choose $A,B$ from them and let $z$ be the empirical nine-state probability vector. Conditional on $A$, the28 choices of $B$ split into

$$15\text{ disjoint},\qquad12\text{ intersecting in one axis},\qquad1\text{ equal}.$$

Therefore

$$z^\mathsf TQ_vz
 =\frac{15}{28}R_{\mathrm{disj}}
  +\frac{12}{28}R_{\mathrm{ov1}}
  +\frac1{28}R_{\mathrm{same}}\ge0.\tag{4}$$

All terms are entries of the same symmetric PSD nine-state matrix $Q_v$. They can be read inside one actual $Q_4$:

* The six two-subsets of four axes have three unordered disjoint pairs.
* They have twelve unordered pairs intersecting in one axis.
* There are six equal pairs.

For each of the16 vertices of $K$, average the entries within the indicated category. Its finite-eight contribution is

$$\begin{aligned}
V_8(K)
&=\frac1{16}\sum_{v\in K}\left[
 \frac{15}{28}\frac13\sum_{A\sqcup B=[4]}Q_v[\eta(v,A),\eta(v,B)]\right.\\
&\hspace{35mm}\left.+\frac{12}{28}\frac1{12}\sum_{|A\cap B|=1}Q_v[\eta(v,A),\eta(v,B)]
 +\frac1{28}\frac16\sum_A Q_v[\eta(v,A),\eta(v,A)]\right]\\
&=\frac1{2688}\sum_{v\in K}
 \left[30\sum_{\mathrm{3\ disjoint}}Q_v[\eta_A,\eta_B]
 +6\sum_{\mathrm{12\ ov1}}Q_v[\eta_A,\eta_B]
 +\sum_{\mathrm{6\ same}}Q_v[\eta_A,\eta_A]\right].\tag{5}
\end{aligned}$$

Sampling a uniform four-direction set and then a category-uniform pair produces the correct global conditional law. For disjoint pairs, their union is already the four-direction set. For overlap-one pairs, each three-axis union has exactly five possible fourth axes in $Q_8$, all equally represented. For equal pairs, each two-axis union has $\binom62=15$ possible completions. Thus the extra unused directions have constant multiplicity within each category. With a uniform vertex of the restriction, the global vertex is also uniform. Equations (4)–(5) give

$$\mathbb E_K V_8(K)=\mathbb E_v z_v^\mathsf TQ_vz_v\ge0.$$

The overlap patterns use the same actual $K$ and the same marked vertex; no independently completed $Q_3$ or $Q_2$ is substituted.

## 4. Whole-domain local-score theorem

For arbitrary PSD blocks of the six specified dimensions set

$$\operatorname{score}_8(K)=\frac{e(K)}{32}+F_8(K)+V_8(K).\tag{6}$$

Every actual $G\subseteq Q_8$ has a uniform coordinate $Q_4$ restriction satisfying

$$\mathbb E_K[e(K)/32]=e(G)/1024.$$

Together with (2)–(5),

$$\frac{e(G)}{1024}\le\mathbb E_K\operatorname{score}_8(K).
$$

If every legal $C_4$-free $K\subseteq Q_4$ satisfies $\operatorname{score}_8(K)\le C$, then every actual $G\subseteq Q_8$ satisfies $e(G)/1024\le C$. In particular, the strict threshold $C<683/1024$ would prove $e(G)\le682$ by integrality. No minimum degree, parity-degree profile, odd-square hypothesis or seed restriction occurs in this theorem.

## 5. Symmetry and the old complete common-$K$ domain

The new score is invariant under $\operatorname{Aut}(Q_4)$, as required to reuse the old minimal-hidden-layer-pair representative set.

A cube isometry permutes the24 root faces. The induced frame change on each face is a single $D_4$ action on both external flags. Any two transports of that actual face to the same canonical root differ by its root stabilizer, under which $\bar Q_r$ is invariant. The two external directions can interchange; the cross term is symmetric and the two diagonal terms are averaged equally. Hence (3) is unchanged.

A cube isometry also permutes the16 marked vertices and four direction labels. At a marked vertex, its induced map on an unordered direction pair preserves the root and changes the local two-axis frame only by their interchange, exactly the quotient used for the nine states. The isometry permutes all three disjoint pairs, twelve overlap-one pairs and six diagonal pairs within their respective classes. Hence (5) is unchanged. Density is unchanged as well.

Therefore any legal $Q_4$ graph transported by a global cube isometry retains its complete new score. The old proof of common-$K$ coverage remains applicable: two valid $Q_3$ layers with an independent crossing-position set represent every legal $K$; the90179 layer-pair orbits cover all8421604 ordered layer pairs; and selecting a minimum hidden-direction layer-pair index leaves a score-complete3312331-element slice among13150453 legal marked completions. This reuse is justified by the new score's actual symmetry, not merely by keeping the same block dimensions.

The newly derived collision terms do not require a451MB coefficient-table reconstruction. Root owns the task-local native separation oracle in `oracle/`; this author used the direct geometric Python extractor below. No archive or MathRSI checker was edited.

## 6. Exact integer coefficients and interfaces

Let $Q_b=L_bL_b^\mathsf T/D^2$ with integer rectangular Gram factors in the fixed original state orders. Write $\operatorname{faceval}(r,s,t)=8\bar Q_r[s,t]D^2$, exactly the original checker's integer root-stabilizer average. The full new integer score uses denominator

$$\mathcal D=64512D^2$$

and numerator

$$\begin{aligned}
Z(K)=&\ 2016e(K)D^2\\
&+\sum_F\left[280\operatorname{faceval}(r,s,t)
 +28\operatorname{faceval}(r,s,s)+28\operatorname{faceval}(r,t,t)\right]\\
&+\sum_v\left[720\sum_{\mathrm{disj}}(L_vL_v^\mathsf T)_{\eta_A,\eta_B}
 +144\sum_{\mathrm{ov1}}(L_vL_v^\mathsf T)_{\eta_A,\eta_B}
 +24\sum_A(L_vL_v^\mathsf T)_{\eta_A,\eta_A}\right].\tag{7}
\end{aligned}$$

Every root stabilizer order divides eight, so all displayed terms are integers. A strict accepted certificate would require

$$\max_K Z(K)<43029D^2,$$

because $64512\cdot683/1024=43029$. Existing large Gram denominators can exceed64-bit range after this new scaling; use a proved arithmetic bound and128-bit or arbitrary integer accumulation. An old denominator192$D^2$ or an old asymptotic-error wrapper is not the new finite scorer.

The actual `finite_flags.py` interface is:

* `local_coefficients(E) -> (r, coefficients)`, for an actual legal labelled $Q_4$ edge set. It returns $r=2016e(K)$ and an integer sparse dictionary keyed by `(block,i,j)`, $i\le j$, such that $\operatorname{score}_8(K)=r/64512+\sum c_{bij}Q_b[i,j]/64512$. Off-diagonal entries are coordinates of the symmetric matrix, with their full linear coefficient already combined.
* `q4_edges_original()` and `q4_edges_from_mask(g)` implement the source checker's bottom12/top12/crossing8 edge order. Arbitrary vertex-loop32-edge order is not interchangeable with it.
* `moment_from_graph(E,n)` takes all common coordinate $Q_4$ restrictions and returns their exact graph multiplicities and coefficient sum. It is a source of actual local distributions, not a claim that finite-eight moments of an arbitrary lower-dimensional graph are PSD.
* `dense_blocks(coefficients)` turns an upper-coordinate linear functional into twice its symmetric moment matrix. If an off-diagonal upper coefficient is $c$, the two ordered entries in this returned integer matrix each equal $c$; a diagonal upper coefficient $c$ gives diagonal entry $2c$.

The kernel state tables are reconstructed from geometry, not read from precomputed optimization features. This interface permits nontrivial single-graph score calibration, working-set generation, candidate ray pricing and exact matrix acceptance in the same state order.

## 7. Informative failed points and the actual restricted optimization

Two actual304-edge $Q_7$ graphs A/B from `proofs/q8_q7_gluing_cycle007/` were read only. Each supplies all280 common $Q_4$ restrictions and mean density $19/28>683/1024$. They do **not** supply a feasible finite-eight primal point: both have strict negative directions in face blocks1,2,4 and the vertex block. Their exact matrices, actual axes/base/mask manifests for all280 slices, and integer negative vectors with strictly negative exact quadratic forms are saved in `Q7_A_*` and `Q7_B_*`. No family obstruction is inferred from their density alone.

The actual682-edge $Q_8$ seed supplies all1120 common $Q_4$ restrictions. Its exact finite-eight moments are PSD, as the bridge predicts; its nonzero supports have dimensions16,16,4 in blocks1,4,5. Exact positive LDL factors are saved in `Q8_seed682_EXACT_MATRIX_CHECK.json`. This distribution also enforces the genuine $682/1024$ floor in any restricted search containing its1120 slices.

`working_lp.py` actually ran35 rank-one PSD column-generation rounds on the1160 distinct labelled local graphs in the union of these three complete slice families. It used68064 nonzero geometric feature entries,50 initial rays from the two actual negative Q7 moment matrices, nonnegative ray weights, and new negative-eigenvector pricing directions. Pricing sees the actual dual moment matrices; their negative eigenvalues are not assertions that any individual legal $K$ is forbidden.

The35-round run took2.150015964 seconds, within its45-second bound. Its recomputed best restricted upper candidate was approximately0.6759921289039941. The last candidate has264 rays and32 positive weights. The saved dual density is approximately0.6759921289039797, with small residual negative moment eigenvalues. It is not itself a PSD primal certificate. The run did not perform full-domain separation or integer Gram acceptance. The candidate, graph list, sparse features, all35 raw iteration records, ray provenance, active rows and weights are preserved in `working_*`. None of these restricted upper numbers is reported as a global $Q_8$ upper bound.

## 8. Rational construction of the strict family obstruction

The final restricted dual has21 nonzero probabilities, all on local graphs already in the actual682 seed's818-mask slice support. Round its probabilities to integer counts at scale $10^9$, then normalize by their exact sum $N$. Let $p$ be that rational distribution and let $q$ be the exact1120-slice probability distribution of the seed. Define

$$p_* =\frac9{10}p+\frac1{10}q.\tag{8}$$

For each graph mask $g$ in the seed's818-mask support, if $a_g$ is its rounded dual count and $c_g$ its seed slice multiplicity, the positive integer weight and common denominator are

$$w_g=9\cdot1120\,a_g+N c_g,\qquad W=10\cdot1120\,N.$$

This makes all probabilities rational and positive and sums them exactly to one. Its true finite-eight moment matrices, rebuilt from all818 actual legal local graphs, are PSD. The nonzero supported blocks admit exact positive LDL decompositions of dimensions16,16,4; all other block entries are zero. The full1008-state direct-sum matrix is PSD, including its implicit zero coordinates. Its density is exactly (1).

The purpose of mixing is an exact repair of the small negative residuals in the floating restricted dual, using the genuine PSD seed moment. Acceptance uses the final rational weights and their own complete matrix recomputation and LDL identities; it does not inherit floating tolerances or re-use a previous moment check.

`certify_lp_point.py` reproduces this point without running an optimizer. Its fresh output was compared byte-for-byte to the frozen `FAMILY_OBSTRUCTION.json`, with equality. The separate `verify_obstruction.py` imports neither this producer nor `finite_flags.py`, NumPy, SciPy or LP features. It independently rebuilds all local root gauges by averaging the whole coset of maps carrying the actual root to canonical form, constructs ordered-pair moment entries, checks every local square, compares all full integer matrices and verifies all rational LDL identities.

As an additional normalization regression, that verifier reads the actual682 $Q_8$ seed and directly forms empirical outer products over all1792 actual root squares with six external flags, and all256 actual vertices with28 direction-pair flags. They exactly equal the finite-eight moments summed over all1120 common $Q_4$ restrictions. This tests all three vertex overlap probabilities and the face diagonal collision terms jointly, beyond a floating single-score test.

## 9. Why the point stops this family

Let $M_b(p_*)$ be the six PSD moment matrices above. For any choice of the six PSD kernel matrices, linearity of the verified geometric score gives

$$\mathbb E_{K\sim p_*}\operatorname{score}_8(K)
 =\rho_*+\sum_b\langle Q_b,M_b(p_*)\rangle\ge\rho_*.$$

The trace product of two PSD matrices is nonnegative, because $\langle Q,M\rangle=\operatorname{tr}(M^{1/2}QM^{1/2})\ge0$. Every graph in the support is a legal local graph in the complete common-$K$ domain. Therefore

$$\max_{K\ C_4\text{-free}}\operatorname{score}_8(K)\ge\rho_*>683/1024$$

for **every** kernel choice in this fixed family, of any rank or rational/real entries. Better initialization, more ray pricing, integer rounding, full separation or additional optimization time within the same family cannot cross the threshold. The conclusion uses the actual verified primal point, not an apparent numerical optimization plateau.

The biased distribution $p_*$ is not asserted to be the distribution of restrictions of any single $Q_8$ graph. Its role is to demonstrate that legal common $Q_4$ objects plus these six exact finite-eight PSD constraints do not enforce all necessary global compatibility. A new route must add genuinely different valid information—e.g. a proved global degree/common-$Q_6$ constraint or another flag type—and then check whether this explicit point violates it. Reweighting or further tuning the same six blocks is not such an augmentation.

## 10. Reproduction and return

From this directory, the acceptance replay requires only standard Python:

```text
PYTHONDONTWRITEBYTECODE=1 python3 verify_obstruction.py
```

The exact point can be regenerated from the frozen working dual and seed slice point using a fresh filename:

```text
PYTHONDONTWRITEBYTECODE=1 python3 certify_lp_point.py --output new-point.json
```

The working optimizer uses task-local `deps/` installed and owned by Root; its35-round run is already frozen behind a started-file guard. It need not be rerun to verify the obstruction. The strict accepted mathematical scope is the fixed six-block score-family obstruction and finite-eight sampling bridge. The full682 graph upper bound is still OPEN. No new mathematical search, old Goal, archive job or same-family optimization is running from this worker. Root owns shared wiki integration, the native oracle evidence and any new augmentation.
