# Three full roots: a 23-slot capacity proof

Status: new author proof with exact local checks; independent external review is pending. This is a local Q6 theorem, not an unrestricted Q8 bound. All numerical certificates below concern the same explicitly defined finite relaxation; a fractional optimum is not asserted to be a graph.

## 1. Statement and definitions

Let G be any C4-free spanning subgraph of Q6, and fix one parity P. Suppose exactly three vertices of P have degree six. There is no minimum-degree assumption on either parity. Put

    L = |{v in P : d(v) <= 2}|,
    S = sum_{v in P} binom(d(v),3).

Then

    S + L <= 158.                                      (1)

In particular L=3 implies S<=155 and 2S+c6<=313, where c6=3. This applies to degrees zero, one and two without a completion argument. It does not exclude every configuration with three low roots, nor assert attainment.

## 2. One simultaneous normalization

Two full roots cannot have distance two: both common neighbors in the opposite parity would produce a square. If two full roots have distance six, no third root in the same parity has distance at least four from both, because its distances to these complementary vertices sum to six. Thus the three full roots have pairwise distance four.

Translate one full root to 0. The other two have four-element supports with intersection two. A single coordinate permutation sends their supports to {0,1,2,3} and {0,1,4,5}, giving the requested canonical triple {0,15,51}. The translation sends the specified parity P to the even parity (and preserves parity when P is initially even). The same map is applied to the entire graph and all selected directions.

For the proof make the additional single translation by 60. Split the coordinate set into three blocks A={0,1}, B={2,3}, C={4,5}. The full roots now have supports

    A union B, A union C, B union C.                    (2)

All vertices below denote subsets of these six coordinates. A star at x is its actual selected direction set M(x); its odd neighbors are x symmetric-difference {i}, for i in M(x). No stars from different coordinate gauges are combined.

## 3. Twenty-three actual capacity slots

Use the following 23 slots, each of capacity one.

* Fifteen square slots. Choose a block D. Choose u either empty or consisting of one coordinate in each of the other two blocks. There are five choices for each D. The slot is the pair of even roots u and u union D. A star occupies this slot if it is at one of these roots and contains both directions of D. If both endpoint stars occupied it, the two common odd neighbors would give a C4.
* Eight three-face slots. Choose one coordinate a in A, b in B, c in C. The slot is the actual Q3 face with varying directions {a,b,c} and all other coordinates zero. A star occupies it if its root belongs to this face and contains all three varying directions. Two distinct even roots in a Q3 have distance two, and their full stars inside this face share both intermediate odd vertices. Thus at most one such star occupies the slot.

For counting below, use only the occupations by stars of degree four or five. Ignoring lower-degree occupations preserves each capacity upper bound. No full root in (2) belongs to a slot.

## 4. Every high star receives its required coverage

For a vertex x, its block type is (|x intersect A|,|x intersect B|,|x intersect C|), allowing permutations of the three blocks. Apart from the three full vertices, all 29 even roots have one of the following types. The restrictions used are only squares with one of the actual full roots.

| Type | Number of roots | Local maximum degree | Coverage needed |
|---|---:|---:|---|
| 000 | 1 | 5, because there are exactly three full roots | degree 4: at least 1; degree 5: at least 3 |
| 200 | 3 | 4 | degree 4: at least 1 |
| 110 | 12 | 5 | degree 4: at least 1; degree 5: at least 3 |
| 211 | 12 | 4 | degree 4: at least 1 |
| 222 | 1 | 3 | no high star |

Here is the coverage proof for every type.

**Type 000.** Write the selected direction counts in the three blocks as rA,rB,rC. The star occupies one square slot for each complete selected block, and rA*rB*rC three-face slots. At degree four its count pattern is 220 or 211, so it occupies respectively 2 or 3 slots. At degree five the pattern is 221 and it occupies 2+4=6 slots. Degree six is forbidden by the exact-three-full hypothesis.

**Type 200.** Write x=A. The full roots A union B and A union C forbid selecting both directions of B or both directions of C. Hence degree four requires both directions of A, together with one direction in each other block. It occupies the square slot (empty,A). Higher degree is impossible.

**Type 110.** Write x={a,b}, with a in A and b in B; let a' and b' be their block mates. The full root A union B forbids selecting both a' and b'. The square slot ({a,b},{a,b} union C) is occupied exactly when C is contained in M. The three-face slots through x contribute

    1_{a,b in M} * |M intersect C|.

A degree-five star must omit a' or b', so it contains a,b and all of C and occupies 1+2=3 slots. For degree four, if C is selected completely the square slot suffices. Otherwise at most one direction is selected in C. Four selected directions then require exactly one in C and three in A union B. The forbidden pair a',b' forces those three to include a and b, so a three-face slot is occupied. The case of no selected direction in C would require selecting both a' and b' and is impossible.

**Type 211.** Write x=A union {b,c}, with b in B and c in C, and let b',c' be their block mates. The full roots A union B and A union C respectively forbid the pairs {b',c} and {b,c'}. These disjoint forbidden pairs partition B union C, so at most two directions are selected there. Degree four therefore requires all of A and occupies the square slot ({b,c},A union {b,c}). Higher degree is impossible.

**Type 222.** Each full root in (2) differs from x in exactly one entire block. Consequently no block can be selected completely, and the degree is at most three.

Thus each actual degree-four star occupies at least one slot and each actual degree-five star at least three. If N4,N5 count these degrees on P, summing the 23 capacity-one inequalities gives

    H := N4 + 3 N5 <= 23.                              (3)

This is a necessary capacity count on one actual graph. It requires no assertion that an arbitrary collection of compatible high stars can be completed to the required low or degree-three stars.

## 5. Converting capacity to S

The three full roots contribute 3*20=60 to S. Every other root contributes to S+L an amount 1,1,4,10 at degrees <=2,3,4,5 respectively. There are 29 nonfull roots. Therefore the exact identity is

    S+L = 60+29+3N4+9N5 = 89+3H.

Combining with (3) proves (1). This calculation also checks all degree-zero and degree-one boundaries; no induction, limiting argument, probability or asymptotics occurs.

## 6. Finite checks and the earlier weaker attempt

All stored columns use the original canonical full roots {0,15,51}, before the extra translation by 60. `PACKING.json` records all locally permitted masks and all 213 degree-four/five columns: 183 degree-four and 30 degree-five. Local compatibility with a full root is tested by intersecting actual odd-neighbor sets. There is no restriction on the opposite parity. The local maximum-degree histogram is one root at most three, fifteen at most four, and thirteen at most five.

The initial `probe.py` used per-root constraints, 3,360 conflicts between distinct roots, and 100 available Q3 face capacities. Its exact nonnegative dual gave H<=27, or S+L<=170. This weaker bound is retained as the actual unsuccessful first layer. Its numeric primal is not used to assert exact optimality of that first relaxation.

`cliques.py` then enumerated all 422 maximal cliques of the 213-column conflict graph, where columns conflict if they choose different stars at the same root or their actual odd-neighbor sets share at least two vertices. The LP returned an integral dual consisting of the 23 slots above, each with coefficient one. `CLIQUES.json` preserves every clique, all nonzero dual entries and an exact rational feasible primal of value 23. Fractions have been checked exactly, not only within a solver tolerance.

The independent `check_exact.py` imports neither producer and uses only Python's standard library. It reconstructs all stars and conflicts, independently enumerates all maximal cliques, regenerates the 15 square and 8 face slots, verifies their capacity by literal conflicts, checks coverage for every high star, and checks the matching rational primal. Its coverage histogram (degree, slots occupied) is

    (4,1):156, (4,2):3, (4,3):24, (5,3):24, (5,6):6.

It also compares every valid three-full-root set with the orbit under all 32 even translations and 720 coordinate permutations. The analytic normalization in Section 2 is the proof; the orbit calculation is a direct cross-check.

The exact feasible fractional primal proves that this complete high-star clique relaxation cannot yield H<23. It is not a graph, does not specify degree-three or low-star completion, does not fix L=3, and does not prove sharpness of (1). A stronger theorem could require integrality or a constraint coupling the remaining actual stars.

## 7. Historical imports and scope

The only historical mathematical comparison read here is `q6_sources/q8_upper_independent/REFINEMENT_K3.md`. Its c3 bound S<=152 requires minimum degree three on the specified parity. Its c3 bound S<=156 allows exactly two degree-two roots and requires all other specified-parity roots to have degree at least three. Neither statement is silently extended to arbitrary L, degree zero, or degree one. No historical contradiction trace was replayed in this exploration, and neither bound is a premise of the new proof.

Only the two named c3 examples `q6_code_degree_3_score21.json` and `q6_code_degree_3_score21_oppmin3.json` were inspected. The fresh checker validates each literal edge list and all 240 Q6 squares, recomputing S=152, L=0 and exactly the three specified full roots. These examples do not attain the new bound and do not establish sharpness. There was no broad witness catalog scan.

No full-graph SAT or integer optimization was run. The proof and exact finite checks are author evidence from the same model family; an independent review is a separate obligation. No Lean, PDF, canonical proof-checker or global extremal claim is made.
