# Maximal-only degree-conditioned vertex-frequency cone

This package proves a universal necessary restriction for every inclusion-maximal C4-free spanning subgraph of Q8, implements its complete finite histogram domain, and gives one exact cut separating a saved abstract lambda/alpha tuple. It does not prove ex(Q8,C4)≤682, realize an abstract tuple as a graph, or assert infeasibility of the full augmented model. The parent must use this package only in a maximal-graph scope. No research Goal, task wiki, parent proof, numerical solver or earlier evidence was modified here.

## MV01. The actual marked state and maximality implication

Let H⊆Q8 be C4-free and inclusion-maximal under adding ambient cube edges. Fix a vertex v. For each unordered direction pair {i,j}, preserve v as the marked local vertex 00 and encode its four square edges in order

    (00,10), (00,01), (10,11), (01,11).

Axis interchange swaps the first two bits and the last two bits. It does not translate the root. The nine nonfull canonical codes are, in state-ID order,

    0, 1, 3, 4, 5, 6, 7, 12, 13.

The groups by the number of retained incident root edges are I0={0,3,7}, I1={1,4,5,8}, and I2={2,6}. Write x_v∈Z≥0^9 for the histogram of all 28 direction pairs, and d=d_H(v). Its exact group sums are

    X0=Σ_{I0}x_i=C(8−d,2), X1=Σ_{I1}x_i=d(8−d), X2=Σ_{I2}x_i=C(d,2).

Consider any missing root edge v(v xor 2^i). Adding it creates a C4 by inclusion-maximality. Every C4 in a hypercube uses two directions, so there is a direction j≠i for which the other three edges of the {i,j} square are already retained. In particular the other incident edge at v is retained. With direction i first the code is 14, and after axis interchange it is 13; with i second the code is already 13. Thus this pair contributes to state 8.

Every state-8 square at v has exactly one missing incident root edge. Associate it with that missing direction. The association maps state-8 squares onto the 8−d missing directions: the preceding argument supplies at least one preimage for each direction. Therefore

    x_8 ≥ 8−d.                                           (MV01)

This is a surjection/counting argument, not a claim that completions are unique. Distinct missing root directions cannot share the same state-8 square, because it has a unique missing root direction. Many squares may complete one missing root edge.

If d=0, no square could supply a retained other incident edge; equivalently x8=0 from X1=0 contradicts x8≥8. Hence a maximal H has no isolated vertices. If d=1, X1=7, so MV01 forces x8=7 and all other I1 coordinates vanish. Neither statement uses an edge count, a Q6 theorem, or a density assumption.

## MV02. Complete refined domains

Let Ω_d be the original full degree-conditioned domain given by the three group sums above, and define

    Ω_d^max = {x∈Ω_d : x8≥8−d}.

This is only a necessary domain: arbitrary histograms in it need not extend to a cube graph. Ω_0^max is empty. In particular no finite minimum is assigned to it.

For 1≤d≤8, replace x8 by y8=x8−(8−d). The I1 sum becomes

    d(8−d)−(8−d)=(d−1)(8−d),

and all new coordinates remain nonnegative. This is a bijection to three independent weak-composition sets of lengths 3,4,2. Consequently

    |Ω_d^max| = C(C(8−d,2)+2,2) · C((d−1)(8−d)+3,3) · (C(d,2)+1).

The exact counts by d=0,…,8 are

| d | Original Ω_d | Refined Ω_d^max |
|---|---:|---:|
| 0 | 435 | 0 |
| 1 | 30360 | 253 |
| 2 | 123760 | 22848 |
| 3 | 215424 | 75504 |
| 4 | 189924 | 89180 |
| 5 | 89760 | 50050 |
| 6 | 21840 | 13728 |
| 7 | 2640 | 1848 |
| 8 | 29 | 29 |
| Total | 674172 | 253440 |

The native oracle enumerates these shifted weak compositions with the final coordinate in each group determined by the remainder, then adds 8−d to x8 before scoring. Each refined histogram occurs once. The Python checker independently enumerates all 674172 original histograms without shifting, filters using MV01, and confirms the 253440 refined counts. This covers all boundaries, including degree-one pure mixed-state rows and the degree-eight zero-missing-edge boundary.

## MV03. Same actual lambda, alpha and empirical gamma

We import only the already established algebraic vertex-moment identity from `../finite8_flags/main.tex`, G01–G02, with the unchanged root-preserving state order. Its vertex local score for arbitrary symmetric Q is

    T_Q(K) = (1/2688) Σ_{v∈K} [30 Σ_disjoint Q(ηA,ηB)
                                      + 6 Σ_overlap Q(ηA,ηB)
                                      + Σ_diagonal Q(ηA,ηA)].

The sums are over three unordered disjoint direction-pair pairs, twelve unordered overlap-one pairs, and six equal pairs at each Q4 vertex. For the empirical distribution lambda of all 1120 coordinate Q4 restrictions of H,

    E_lambda T_Q = tr(Q M5(lambda)),
    M5(lambda) = (1/256) Σ_{v∈Q8} x_v x_v^T / 784.        (MV03a)

The identity is algebraic and holds for any symmetric Q; PSD is not required. It includes collisions. Two independently drawn direction pairs among the 28 have disjoint, overlap-one, and equal probabilities 15/28,12/28,1/28, which are exactly the weights used in the imported formula after uniform Q4 completion.

Define gamma_(d,x) as the fraction of the 256 actual vertices having degree d and histogram x. MV01–MV02 give

    M5(lambda)=Σ_{d=1}^8 Σ_{x∈Ω_d^max} gamma_(d,x) xx^T/784,
    gamma_(d,x)≥0,
    Σ_x gamma_(d,x)=N_d/256,                            (MV03b)
    N0=0.

If alpha is half the sum of the two actual 128-vertex parity-profile point masses, and n_d(p) is profile p's degree-d count, then

    Σ_p alpha_p n_d(p)=N_d/2,
    mass_d=Σ_x gamma_(d,x)=Σ_p alpha_p n_d(p)/128.        (MV03c)

These are the same actual lambda and alpha used by every other local and degree constraint, not separately chosen decompositions. The parent remains responsible for coverage of its profile list at the actual edge count. The identity applies at every edge count and therefore at all six m=683,…,688 in a separately justified maximal-counterexample reduction. This package does not prove that reduction or its imported Q6 bounds.

Every generator xx^T/784 is PSD. The full refined cone implies vertex PSD and carries the additional integer, degree-conditioned maximality information. No graph-realization converse follows. A missing-edge histogram marginal requiring at least one completion per edge expresses a related maximality fact; here the completions are also grouped jointly at their common actual vertex.

## MV04. Exact pricing and degree-bias inequality

For any symmetric integer 9×9 kernel Q and integer degree biases B_d satisfying

    x^T Q x + B_d ≥0   for all x∈Ω_d^max, d=1,…,8,

MV03 yields the universal maximal-only inequality

    E_lambda T_Q + Σ_p alpha_p Σ_d B_d n_d(p)/(128·784) ≥0.    (MV04)

For a fixed Q, take B_d=−min_{Ω_d^max} x^TQx for d=1,…,8. The minimum is finite on every such nonempty domain. We choose B0=0 by convention, because the actual mass at degree zero is zero. This is not a claimed minimum on an empty set; no d0 generator exists. Any positive common normalization of MV04 preserves validity.

`price_domain.cpp` accepts exactly 90 signed decimal int64 tokens: the 81 row-major entries of Q followed by nine biases. It rejects nonsymmetric Q, missing/extra tokens, malformed tokens and out-of-range integers. A missing query path requests Q=0 and B=0. Output includes all nine degree records, complete counts, exact string minima and actual integer witnesses; degree zero has count 0, minimum null, witness null. The global minimum is over the nonempty degrees 1,…,8 only. A nonzero supplied bias is included in every score.

Scoring uses signed 128-bit integers, casting Q before multiplication. Since Σx_i=28 and |Q_ij|,|B_d|≤2^63,

    |x^TQx+B_d| ≤ (784+1)·2^63 < 2^73,

and all individual multiplication and cumulative absolute sums satisfy this bound. The signed 128-bit range is more than sufficient even for INT64_MIN inputs. No floating arithmetic determines a domain minimum.

Existing local coefficients c_(5,i,j)(K) are folded: their denominator is 64512, and T_Q(K)=Σ_{i≤j} c_(5,i,j)(K) Q_ij/64512. For the true symmetric moment, U_ii=2c_(5,i,i), U_ij=c_(5,i,j) for i≠j, and M5=E_lambda U/(2·64512). Generator upper-coordinate vectors therefore use x_i²/784 on the diagonal and 2x_ix_j/784 off the diagonal when paired with Q's upper triangle. Using the folded c as a true matrix would change off-diagonal factors and invalidate the cut.

## MV05. Nine immediate all-lambda consequences

Let

    l=(-2,−1,0,−2,−1,−1,0,−2,6).

The group identities give X1+2X2=7d and X0+X1+X2=28. Hence

    l^Tx=7x8−2X0−X1=7[x8−(8−d)]≥0.

For every i=0,…,8, nonnegativity of x_i implies x_i(l^Tx)≥0. The integer symmetric kernel

    Q^(i)=e_i l^T + l e_i^T

satisfies x^TQ^(i)x=2x_i(l^Tx)≥0 throughout every refined domain. Therefore

    E_lambda T_(Q^(i))=2(M5(lambda)l)_i≥0,
    equivalently M5(lambda)l≥0 componentwise.             (MV05)

These rows need no alpha biases. `RLT_KERNELS.json` gives the exact nine matrices. They are consequences of the full refined cone, not a claimed full characterization. Root's separately saved master024 test found all nine nonnegative; this package makes no claim that those nine rows separate a current point.

## MV06. Exact cut and actual checks

`pricing_master050/INPUT_POINT.json` freezes an abstract saved point from the active 1409-alpha profile scope, with 403 positive lambda columns and 1409 positive alpha columns. Discovery only uses floating LPs to propose integer Q, never to accept a universal cut. The final query is `query_32.txt`; `query_32.oracle.json` gives complete exact degree minima over all 253440 refined histograms. The integer Q, repaired B and positive normalization are in `CONDITIONAL_VERTEX_CUT.json` in that directory.

Thirty-three bounded discovery rounds took about 1.69 seconds after local coefficient construction. Its exactly rationalized and separately normalized lambda/alpha target pairs with MV04 as

    −92743804234666487401677529556778857677932718514926730169
    /1045333333028001957869374093250655798339702778054401920.

After positive normalization 1000000 the value is approximately −0.0000887217515259. Thus that exact abstract tuple violates a valid maximal-only necessary inequality. It is not a Q8 counterexample, a general nonmaximal cut, or a whole-model NO certificate.

The independent `check.py` uses ordinary Python integers and ordered 9×9 quadratic forms, independently traverses all original histograms, and agrees with every final cut minimum. A second dense symmetric query containing both signed int64 endpoints, arbitrary full-sized entries, and nonzero biases independently agrees in all eight nonempty degrees; malformed query checks reject as documented. `DOMAIN_CHECK.json` retains these results. Root independently rebuilt the domain and literal point pairing as recorded outside this package in `../finite8_root_checks/MAXIMAL_MASTER050_VERTEX_CUT_CHECK.json`; that receipt is additional checking, not a premise of the proof.

`GRAPH_CHECK.json` records direct checks of both complete actual graphs. Each graph's edges are ambient, no two distinct vertices have two common neighbors, and every missing ambient edge has a completed square. Every actual vertex passes MV01, the exact group sums and MV05. All 1120 coordinate Q4 restrictions were scored, and their true integer vertex moment satisfies

    U_local_total = 720 Σ_v x_v x_v^T,

which is precisely MV03a after division by 1120·2·64512.

* The actual 682-edge seed has degree counts N4=2,N5=168,N6=86, eight distinct (d,x) columns, 342 missing edges, and minimum x8−(8−d)=7. Its missing-edge completion-count histogram is {3:41,4:159,5:120,6:22}.
* The actual 576-edge maximal graph from the leaf package has degree counts (0,2,14,42,70,70,42,14,2), 182 distinct (d,x) columns, and 448 missing edges. Its minimum x8−(8−d)=0, so genuine leaf boundaries are retained. Its missing-edge completion-count histogram is {1:148,2:134,3:99,4:50,5:15,6:2}.

The saved empirical gamma files retain all these actual histograms and multiplicities. These examples calibrate the interface and do not replace the universal proof.

`NONMAXIMAL_BOUNDARY.json` demonstrates why maximality cannot be dropped. The empty spanning graph is C4-free, has d=0 and x=(28,0,…,0), but x8=0<8. For i=0, MV05 gives E T_(Q^(0))=−4. The graph consisting of only edge 01 is also C4-free; at leaf 0 it has d=1 and histogram (21,7,0,…,0), violating x8≥7. Thus even absence of isolated vertices at one tested root does not remove the maximality hypothesis.

## Reproduction and adaptive caller

From this directory:

```bash
g++ -std=c++17 -O3 -Wall -Wextra price_domain.cpp -o price_domain
python3 check.py
./price_domain pricing_master050/query_32.txt
python3 price_point.py POINT_JSON NEW_RUN_DIRECTORY 80
```

`check.py` writes only this package directory and reads existing graph/flag sources. It starts no LP. `price_point.py` is the separate bounded discovery caller; it requires NumPy/SciPy available through the task's existing finite-flag environment. It consumes the existing saved-point schema with `lambda` pairs and `alpha` rows containing weight and degree histogram, and requires degree-zero mass to be exactly zero. A fresh run directory preserves its input snapshot, each exact oracle call, history and optional `CONDITIONAL_VERTEX_CUT.json`. A different input or existing history in the same directory is rejected rather than silently replacing evidence.

The discovery caller can warmstart from earlier valid refined witnesses; all proposed kernels still receive full exact pricing. It returns `CUT_FOUND` only for an exactly negative repaired rational pairing, with Q/B/scaling and explicit MAXIMAL ONLY validity. `NO_EXACT_CUT_IN_BOUNDED_PROBE` is inconclusive: it proves neither membership in the full cone nor graph feasibility. The optional round count is 1…80. `cli_smoke_master050/` records a real generic-CLI replay using saved witnesses; it found another exact valid cut in one round, about 0.46 seconds. The original stronger query32 cut remains frozen.

Fresh non-author semantic review of this new package is a separate parent-stage obligation. This package itself does not upgrade a canonical task claim or alter the open upper-bound status.
