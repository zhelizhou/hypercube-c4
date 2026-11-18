# Independent review: three full Q6 roots and the actual Q7 facet interface

Verdict: **PASS at the stated local scope**, after correcting the parity wording in the first draft. This is an independent same-family mathematical review and a separate exact reconstruction; semantic assurance remains same-family/provisional, not a cross-model or canonical PROOF_AUDIT acceptance. All deterministic checks below completed with exit code zero. No author source was changed by this reviewer.

The accepted statements are:

* For every C4-free spanning subgraph of Q6 and either specified parity with **exactly three** degree-six vertices, let S be its sum of binomial(degree,3), and let L count its vertices of degree at most two. Then **S+L<=158**, with no minimum-degree assumption on either side.
* Let o be the XOR of the three full vertices in common coordinates. If its degree is at least three, then **S+L<=155**. The stronger pattern-dependent bounds 152 and 149 in the separate corollary also follow as stated.
* In an actual Q6 facet of a C4-free Q7 of whole minimum degree three, with exactly three specified-side full roots, the Root caller correctly gives **h_F>=2+a_F+3*1[d_F(o)>=3]**. Its low-hole implication constrains the actual XOR point and its omitted retained edge. It does not remove any current Q7 profile by itself.

## Frozen inputs and coverage

The main proof was read in full, Sections 1–7. The separate origin corollary and Root's complete one-page Q7 caller were also read in full. Both producer programs, the author's two check programs, and the actual PACKING/CLIQUES data were inspected. The reviewer did not use the author's PASS flags as mathematical premises.

| Input | SHA256 |
|---|---|
| `../PROOF.md` | `9c7b7ceb2b11e3a07669cea8dc3b7118f6c75120e6e0136037a9522d342a23e4` |
| `../ORIGIN_COROLLARY.md` | `d6eceb810312e1ffeb9c9a529fe817e0597c434b0f0c148949ecc32aaea29584` |
| `../PACKING.json` | `b3c2a66fba337f1982693c48141e0410b72e16df2094d410e6ee8931b0f8c13d` |
| `../CLIQUES.json` | `d32b761237cd1725bfff707748511573c38a97b0b2080a1150c5a351c49a1d24` |

The receipt also binds `../../q7_three_full_gate_cycle010/PROOF.md`, all author receipt files, the actual 210-row table, and the precisely named historical comparisons and witnesses. The historical full research project and the proof of the 210-row cover were not re-audited here.

| Source unit | Obligation | Review result |
|---|---|---|
| Main §1 | Quantifiers, exactly-three premise, S and L | PASS; degree zero and one are included |
| Main §2 | One common isometry for all roots/stars and either parity | PASS after the wording correction below |
| Main §3 | Fifteen square and eight actual Q3 capacities | PASS by literal common-neighbor C4s |
| Main §4 | All five block types and every degree-four/five star | PASS by direct case analysis and all 213 columns |
| Main §5 | Exact identity S+L=89+3H | PASS for every possible specified degree |
| Main §6 | Complete finite domain, clique validity, exact dual/primal, failed earlier bound | PASS; no optimization rerun |
| Main §7 | Historical comparison and limits | PASS at the explicitly stated import scope |
| Origin corollary | Additional occupancy from the actual distinguished star | PASS, all 41 masks checked |
| Root Q7 caller | Same-facet XOR, low count, degree/omitted-edge implication | PASS; no claimed profile deletion |

## Normalization and the 23 capacities

Two same-parity full roots at distance two would create a retained square. A distance-six pair cannot have a third root at distance at least four from both, since the two distances sum to six. Thus all three pair distances equal four. After translating one root to zero, the two weight-four supports have intersection two; their intersection and two differences give one coordinate permutation to {0,15,51}. Translation by 60 then gives the three unions of two whole blocks A, B, C of size two.

The first frozen draft incorrectly called the initial translation parity preserving even when the specified parity is odd. Root and this reviewer independently reported that wording issue. The final proof says that the translation sends the specified parity to the even class and also fixes its pre-normalization even/odd references. No domain, slot or mathematical case changed. In particular the odd parity is covered; it is not an extra assumption.

Each square slot has two even endpoints separated by one whole block D; occupying it means retaining both D-directions. Two such endpoint stars give all four edges of that actual square. Each Q3 slot is a face through zero choosing one direction from each block; any two of its four even roots with their three internal edges share a square. Thus each capacity one holds for the same actual graph, including if one of its occupying stars has low or degree-three total degree. Ignoring those occupations in the main proof only weakens the count.

The five block types exhaust all 29 nonfull roots: 000 once, 200 three times, 110 twelve times, 211 twelve times, and 222 once. The restrictions in the proof are exactly the forbidden direction pairs generated by the full roots. In particular, the two forbidden pairs in type 211 are disjoint, so every degree-four star there really contains the complete remaining block. The type 110 degree-five case must omit one member of its single forbidden pair and hence occupies one square plus two Q3 slots. No minimum-degree premise entered this reasoning.

For type 000 the occupations are 2 or 3 at degree four and 6 at degree five; the proof deliberately needs only 1 or 3. Every other high star has the required coverage. Consequently H=N4+3N5<=23. A nonfull root contributes 1 to S+L at either degree at most two or degree three, 4 at degree four, and 10 at degree five. Together with the three full contributions 60, this proves S+L=89+3H<=158. This proof is independent of the LP discovery and all historical UNSAT imports.

## Independent exact reconstruction

`check_fresh.py` is a new standard-library checker. It imports no author module. Local admissibility and conflicts are reconstructed from literal cube edges and all 240 four-edge squares, rather than trusting the stored neighbor lists or a solver. It constructs the 23 slots in the **translated block coordinates**, then maps them back to the saved columns. A separate iterative clique recursion compares the entire maximal-clique set.

Run from this review directory:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 check_fresh.py > check.stdout.json
```

`CHECK_RESULT.json` and the matching stdout record:

| Exact check | Result |
|---|---:|
| All valid even full triples, each with an explicit simultaneous normalization | 480 |
| Corresponding odd triples checked under the parity-changing translation | 480 |
| All locally allowable nonfull direction masks | 1,206 |
| Local maximum-degree counts at 3, 4, 5 | 1, 15, 13 |
| Degree-four / degree-five columns | 183 / 30 |
| Actual cross-root C4 conflicts | 3,360 |
| Conflicts including alternative choices at the same root | 4,320 |
| Original root/conflict/face rows | 3,488 |
| Available Q3 rows | 100 |
| Complete maximal-clique catalogue | 422 |
| Certificate slots | 15 squares + 8 Q3s |
| Exact nonnegative dual value | 23 |
| Exact feasible fractional primal value | 23 |

The exact coverage histogram is (degree, occupations): (4,1):156; (4,2):3; (4,3):24; (5,3):24; (5,6):6. The 23 nonzero dual weights are all one and their rows are precisely the geometric slots. All columns are dominated with exact integer arithmetic. The saved primal has 73 nonzero entries, each with denominator 113; every clique inequality and every original base inequality holds exactly, and its objective is 23.

The producer's strengthened LP actually uses only maximal-clique rows. This is sufficient: every original root/conflict/Q3 row was independently shown to be contained in one of those cliques. Thus the saved fractional point is feasible for both descriptions of the strengthened relaxation. The earlier exact nonnegative dual of value 27 was separately checked on all original rows; no exact primal optimality is inferred for that initial weaker attempt.

Every listed clique was checked for actual same-root exclusivity or a literal retained C4, for maximality, and against the independently regenerated complete list. Mathematical validity of the upper certificate would require only the 23 valid inequalities and full column coverage; the stronger all-422 verification also supports the stated fractional-relaxation limit.

## Origin corollary and Q7 caller

In common coordinates the distinguished point is intrinsically o=f1 XOR f2 XOR f3. XOR of three vertices commutes with a common coordinate permutation and transforms by the same translation, so the point does not depend on a separately chosen gauge. It is 60 in the saved canonical coordinates and zero in the symmetric block coordinates.

Its slot occupancy is q=number of completely retained blocks plus the product of the three retained block counts. At degree three the patterns 210 and 111 each give q=1, against H-weight zero. At degree four, 220 gives q=2 and 211 gives q=3, against weight one. At degree five, 221 gives q=6, against weight three. Thus including its degree-three star when necessary gives H+(q-h(o))<=23, with excess 1, 2 or 3. The stated bounds 155, 152 and 149 follow. The reviewer's enumeration of all 41 relevant masks matches the complete author origin table. The remaining degrees zero, one and two are not assumed to satisfy the degree-at-least-three corollary.

For Root's Q7 caller, a facet loses at most one edge per vertex. Whole minimum degree three therefore makes every local degree at least two, and L equals the actual degree-two count a_F. Substituting S_F=160-h_F in the two accepted Q6 bounds gives exactly h_F>=2+a_F+3*1[d_F(o)>=3]. If h_F<5+a_F, then o has local degree two; its global degree must equal three and the omitted-direction edge must be present. The fixed facet coordinate occurs three times in the XOR, so o belongs to that same actual facet and specified parity. All caller hypotheses are discharged on that actual induced graph.

The actual 210-row table was read and its degree-count schema checked: it contains 142 rows with total N3=0, 62 with total N3=1, and 6 with total N3=2. This confirms the caller's present-cover count statement, without re-proving that cover. The local congruence is h_F+c_F-a_F=2 modulo 3, obtained from S_F=32-a_F+19c_F+3H_F. Hence the low values a_F=1,h_F=3 and a_F=2,h_F=4 have the stated XOR-low requirement; a nonlow XOR instead forces h_F>=6 or 7. At a_F=0, the older specified-minimum-three h_F>=8 bound remains stronger.

Each global specified degree-three vertex is locally degree two in precisely its three containing facets that omit a retained direction. These incidences are already the sum_a=3b budget. The new caller constrains **which actual vertex** equals the full-root XOR; it cannot charge those same incidences again or replace the common coordinates by independent labels. The caller explicitly leaves all 210 profiles and their common edge completion unresolved.

## Counterchecks and limits

The two named historical S152/c3 edge lists were independently checked for cube adjacency, duplicate-free edges, all 240 squares, the full-root set, and their computed S=152,L=0,H=21. Both have 124 edges. No broad witness search was performed. From those actual graphs, deleting edges at each nonfull root to give degree zero, one or two produces 174 further checked boundary cases; deleting every nonfull star leaves the literal three-full-star graph with S=60,L=29,H=0. These are direct calibration/counterexample attempts at omitted low-degree boundaries, not a proof by sampling. The complete block proof and local enumeration supply the universal argument.

The degree-at-least-three origin corollary and its stronger pattern bounds also hold on every applicable calibration. The exact fractional primal defeats any proposed H<23 conclusion from this clique relaxation alone, but it is **not** an actual graph, does not supply the missing degree-three/low stars, does not fix L, and does not prove graph attainment. Conversely, the theorem S+L<=158 is deliberately weaker at L=0 than the accepted historical S<=152 result. The historical c3 bound with exactly two degree-two roots has S<=156; neither historical statement was extended silently to degree zero or one.

There was no new LP solve, SAT solve, integer optimization, historical contradiction-trace replay, Lean run, or global Q7/Q8 exclusion in this review. All commands are terminal, with no live process. Shared records and author files remain unchanged. The remaining global obligation is to couple this actual XOR constraint with common full-root sets and retained directions; this review supplies no such complete exclusion.
