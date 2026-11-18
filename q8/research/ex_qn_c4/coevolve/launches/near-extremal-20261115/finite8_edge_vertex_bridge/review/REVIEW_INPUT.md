# Bounded review request and full canonical proof input

Fresh nonauthor semantic proof review of the complete edge–vertex bridge package. The reviewed canonical source is PROOF.md, including its final §6 literal5148 root-extension claim. Full semantic, independent exact finite-domain, calibration, boundary, mutation, acyclic dependency and source-unit execution coverage checks are required. All writes are confined to review/. Other sources, MathRSI, wiki and Goal are read only. No old jobs, LP, or child agents. No TeX or HTML is required.

Requested native Codex host-default route: gpt-6.1-sol, ultra. Root resolved the route before dispatch. Actual returned model and actual effort are unattested and must remain null in the audit. Assurance is same-family/provisional.

Check the universal same-actual-lambda/beta/gamma bridge for every spanning C4-free Q8: all162 incidence identities,36 mixed retained-minus-missing balances,27 degree-group moment equations,392 constant and7/2304 packed consumer. Reconstruct all5148 generators, every old2788/current1751 stored duplicate-class member, actual source orders, current adapter versus universal map, all14090 packed vertex columns, actual682/576/584 graphs, degree0/8 and both parity/nonmaximal boundaries, and exact-decimal master050 diagnostics. Check diagonal/off-diagonal convention and synchronized root action. No author or Root PASS is a premise. Do not infer a full682 NO or row-rank63 claim.

Mandatory semantic checks: definitions and typed symbols; application hypotheses; all equality/inequality constants and directions; finite-sum interchanges; empirical probability normalizations; uniform parameter scope; degenerate/counterexample attempts; dependency consistency and semantic circularity. Report actual checked scope, input hashes, complete source-unit coverage and the obligation ledger. Root alone owns canonical/wiki integration.

## Complete canonical proof

# Same-object edge–vertex incidence and degree-group moment bridge

This package proves necessary identities for **every C4-free spanning subgraph G of Q8**. There is no maximality, degree bound, fixed edge count, regularity, parity hypothesis, or probabilistic independence assumption. These identities connect the existing edge7 beta and vertex9 moment M5 to observations of the **same actual graph**. They do not prove ex(Q8,C4)≤682, nor do they establish realizability of any relaxation tuple.

Root derived the bridge and supplied independent literal diagnostics. This author independently reconstructed its coefficient maps, proved the counting argument below, checked every original generator and duplicate class, and checked literal graphs and existing packed vertex features without importing producer flag modules. Root retains the task wiki, Goal and final review responsibility.

## 1. Vertex and edge observations

Write vertices of Q8 as eight-bit strings. A coordinate square based at a marked vertex v, with ordered axes a,b, has four edge indicators in order

`(v,v+a), (v,v+b), (v+a,v+a+b), (v+b,v+a+b)`.

Here addition means XOR of the indicated unit vector. Interchanging axes swaps bits 0↔1 and 2↔3. Take the smaller of the two resulting four-bit codes. Since G has no C4, code 15 is absent. The nine representatives and state IDs are

| state j | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| representative | 0 | 1 | 3 | 4 | 5 | 6 | 7 | 12 | 13 |
| retained edges at the marked vertex k_j | 0 | 1 | 2 | 0 | 1 | 1 | 2 | 0 | 1 |

Let d(v) be its full degree in G, and let x_vj count its 28 unordered direction pairs in state j. Then

`sum_j x_vj=28`, and `sum_j k_j x_vj=7 d(v)`.

The second identity holds because every retained edge at v belongs to seven such pairs. Define gamma_(d,x) as the fraction, among all 256 vertices, with full degree d and histogram x. Thus gamma is a probability distribution, not separate degree-normalized distributions. Put

`mu_dj = sum_x gamma_(d,x) x_j = (1/256) sum_(v:d(v)=d) x_vj`.

For an ambient undirected root edge e={u,v} of Q8, let r indicate whether e is in G. Each of the seven other directions b gives three bits: bit0 indicates {u,u+b}, bit1 indicates {v,v+b}, and bit2 indicates {u+b,v+b}. Denote that code by s. There are eight possible states for r=0 and seven for r=1, since s=7 with retained root would be a C4. Let y_s count these seven flags. Write beta_(r,y) for the fraction of the **1024 ambient edges** with this root type and histogram, in a fixed arbitrary orientation of each root.

The endpoint full degrees, recovered from this same histogram, are

`a=r+sum_s y_s bit0(s)`, `b=r+sum_s y_s bit1(s)`.

The corresponding vertex-rooted square codes are

`c_first=r+2 bit0(s)+4 bit1(s)+8 bit2(s)`,

`c_second=r+2 bit1(s)+4 bit0(s)+8 bit2(s)`.

Canonicalize each code by the vertex-preserving axis swap above. Let j_first(s),j_second(s) be the resulting state IDs. Define the integer coefficient

`C^r_(d,j)(y) = sum_s y_s ([a=d][j_first(s)=j]+[b=d][j_second(s)=j])`.

Every column has total C mass 14. Root orientation reversal exchanges its endpoints and bits0,1, so C is unchanged. Consequently this map is valid with the existing endpoint-averaged beta convention. It does not require orienting endpoints independently for different projections.

## 2. Incidence identity: all 162 equations

Fix d and j. Count triples consisting of a marked vertex v of degree d, an unordered coordinate pair A giving state j at v, and a choice of one of the two edges from v along A. On the edge-root side, choosing that edge as root and the other direction as its external flag gives exactly one contribution to C. Conversely every contribution to C determines exactly this triple. All data remain in G.

For a retained root, each square state j offers k_j choices; for a missing root it offers 2−k_j. Therefore the exact integer identities are

`sum_(ambient e: r(e)=1) C^1_(d,j)(y_e) = k_j sum_(v:d(v)=d) x_vj`,

`sum_(ambient e: r(e)=0) C^0_(d,j)(y_e) = (2−k_j) sum_(v:d(v)=d) x_vj`.

Dividing by 1024 gives the normalized bridge

`sum_y beta_(1,y) C^1_(d,j)(y) = (k_j/4) mu_dj`,

`sum_y beta_(0,y) C^0_(d,j)(y) = ((2−k_j)/4) mu_dj`.

These are 2×9×9=162 identities. In particular the mixed states `I1={1,4,5,8}` have k_j=1, and hence the following 36 valid equations need no gamma variables:

`sum_y beta_(1,y) C^1_(d,j)(y) − sum_y beta_(0,y) C^0_(d,j)(y)=0`

for d=0,…,8 and j∈I1. Adding the two root-type identities gives the useful first-moment connection

`mu_dj = 2 sum_(r,y) beta_(r,y) C^r_(d,j)(y)`.

The factors 4 and 2 come from different normalizations: 1024 ambient edges versus 256 vertices, and two root choices per square at its marked vertex. There is no factor 7 or 28 to insert in this equation.

## 3. Degree groups and 27 same-lambda equations

The states split according to k_j:

`I0={0,3,7}`, `I1={1,4,5,8}`, `I2={2,6}`.

At every actual vertex of full degree d, its two chosen directions contain respectively zero, one, or two retained incident edges in exactly

`F0(d)=choose(8−d,2)`, `F1(d)=d(8−d)`, `F2(d)=choose(d,2)`

ways. Thus **pointwise**, for g=0,1,2,

`sum_(j∈Ig) x_vj=Fg(d(v))`.

Let lambda be the distribution of the 1120 actual coordinate Q4 restrictions of G. The original exact finite-eight vertex block satisfies

`M5_ij(lambda)= E_gamma[x_i x_j]/784`.

For completeness, this follows by sampling a vertex and two independent uniform direction pairs among its 28 pairs. For each first pair the second pair has 15 disjoint choices, 12 overlap-one choices and one equal choice. A uniform coordinate Q4 reproduces each category with constant completion multiplicity. Explicitly the local ordered vertex matrix has denominator 64512 and weights 360 for disjoint ordered pairs, 72 for distinct overlapping ordered pairs, and 24 for equal pairs, summed over all 16 local vertices. These weights reproduce those probabilities after averaging all coordinate Q4 restrictions. The equality uses common actual restrictions; lambda and gamma are not independently chosen distributions.

Using the first-moment bridge and the pointwise group count,

`sum_(r,y) beta_(r,y) sum_d C^r_(d,i)(y) Fg(d)`

`= (1/2) sum_d mu_di Fg(d)`

`= (1/2) E_gamma[x_i sum_(j∈Ig)x_j]`

`= 392 sum_(j∈Ig) M5_ij(lambda)`.

This proves 27 equations indexed by (g,i), g=0,1,2 and i=0,…,8. The constant is exactly `784/2=392`. The exported family of 36+27 rows is valid; it is **not claimed to consist of 63 linearly independent rows**. Zero/redundant rows may be kept for a transparent interface.

## 4. Exact packed-feature consumer

`INTEGER_FEATURES` stores the packed coefficient vector f in upper-triangle order: diagonal entries are R_ii and off-diagonal entries are 2R_ij, where true local `M5=R/64512`. Equivalently Root's integer `U=2R` has true matrix `U/129024`.

For each (g,i), the exported 27×45 selector W gives coefficient 2 at packed (i,i) if i∈Ig, coefficient 1 at packed sorted(i,j) for each j∈Ig, j≠i, and zero elsewhere. Thus

`W f = 2 sum_(j∈Ig) R_ij = sum_(j∈Ig) U_ij`.

Let B27 denote the exported integer beta rows `sum_d C_all_(d,i) Fg(d)`. The exact consumer is

**`2304 B27 beta = 7 W F_vertex^T lambda`.**

Indeed `392/(2·64512)=7/2304`. Equivalently `B27 beta = L27 lambda/64512` with `L27=196 W F_vertex^T`. All forms are exported. For a newly priced graph, build its vertex packed45 feature with the identical existing contract, then apply W; the frozen 14090-column L matrix is a convenience, not a restriction to that library.

The 36 equations are simply **`B36 beta=0`**, with integer coefficients and no further denominator. Both sides must use the same beta and lambda as the existing edge7 cone, endpoint-degree equations and other model constraints.

## 5. Full domain, order and safe duplicate handling

`export_bridge.py` regenerates and compares the entire original domain: weak compositions of seven flags into eight labels for missing roots (3432), and into seven labels for retained roots (1716), in lexicographic multiset order. This gives exactly 5148 generators. These histograms form a necessary cone; arbitrary beta mixtures are not thereby shown globally realizable.

The author reads the actual original5148 histogram list, actual old2788 duplicate groups, actual current3432 raw list, and actual current1751 selected indices. It does not infer the current order from old2788 indices. The full C map is checked invariant on **every member of every old and current stored duplicate class**, not only on the selected representatives. Hence replacing an actual histogram with its existing representative preserves all new incidence and moment rows exactly. For an empirical actual beta, sum all constituent histogram masses into its class; no multiplicative class-size factor is needed.

The current1751 model also uses separately justified maximality/leaf pruning. The new identities themselves do not need those hypotheses. The current adapter preserves its retained classes; it is not asserted to represent arbitrary nonmaximal graphs. General graphs always use the full5148 map. Missing histograms pruned by the old model do not disappear from the universal proof.

`ORDER.json` freezes the full C row order `(r,d,j)`, the balance order `(d,j)` with mixed j ascending, actual current selected raw indices and their original5148 indices, actual current column histograms, and old2788 representative indices. `MOMENT_ORDER.json` freezes (g,i), packed45 order and the 14090 graph order. `INTERFACE.json` and `MOMENT_INTERFACE.json` bind source and artifact hashes.

## 6. Actual verification and its scope

The independently implemented `check_bridge.py` imports no producer flag modules. For **each of the5148 raw histogram columns**, it constructs a literal cube graph on the root edge and the fourteen endpoint connectors/opposite edges, with every other edge absent; directly recomputing the two root endpoint degrees and all fourteen rooted-square observations matches all162 exported C entries. These extensions are C4-free because squares without the root direction lack the required outer edges, and the only possible full squares containing the root are exactly the excluded retained-root/state7 combination. This independently checks the entire coefficient map, beyond the empirical graph tests. It reconstructs square states from actual graph edges, forms empirical original5148 beta and vertex histograms, and verifies all162 incidence identities, all36 balances, the gamma first moment, the full M5–gamma second moment, and all27 equations as integer identities. For each graph it enumerates all1120 coordinate Q4 restrictions.

Executed cases are the original682 graph, calibration576, the actual584 same-parity-leaf counterexample, the empty graph, a perfect matching, a full eight-edge star, the682 graph with one edge deleted, and its XOR137 translate. All passed. This includes degree0 and degree8 boundaries. The checker also independently rebuilt **all45 packed vertex coefficients of every one of the current14090 Q4 graph columns** and compared them exactly with existing features. These are local feature checks, not a complete Q4 graph-domain enumeration.

Mutation checks reject a perturbed C coefficient, a reversed signed balance coefficient,392 replaced by393, removal of the packed off-diagonal factor, and a literal C4 input. `CHECK_RESULT.json` records the actual run and input hashes. During checker development an incorrectly written intermediate unnormalized assertion was corrected from `2 C_all=T` to `C_all=2 T`; the final first-moment formula and all exports were unchanged. The final checker contains both this integer relation and its normalized gamma identity explicitly.

`check_master050.py` independently computes exact rational pairings of the serialized decimal weights of immutable master050. The largest absolute violations are approximately0.029930761918206757 for B36 and0.10051812768628185 for B27−392M5group. No renormalization was applied. This proves that this stored relaxation tuple fails the new necessary equalities; it is neither an actual Q8 graph nor a proof that the augmented global model is infeasible.

## 7. Reproduction and return

From this directory, using a Python environment with NumPy and SciPy:

```bash
python export_bridge.py
python export_moment_bridge.py
python check_bridge.py
python check_master050.py
```

This execution used `/mnt/c/users/anony/desktop/project/research/ex_qn_c4/.venv/bin/python`. All writes were confined to this package. Existing task, producer, numerical-author and wiki files were read only.

The numerical author has received the ready B36/B27/W paths and is responsible for actually adding the same-beta/same-lambda equations, pricing any new lambda columns with the new vertex directions, and validating its own solve/full-domain result. Root will independently review the proof and interfaces and decide canonical wiki status. No numerical infeasibility, final dual certificate, Lean theorem, or complete682 proof is claimed here.
