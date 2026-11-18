# Independent complete legal-Q4 maximizer

The exact maximum of the supplied signed integer functional over **every C4-free spanning subgraph of Q4** is

```
4,924,508,303,670
```

An independently found maximizing mask is `3001496046`. The parent comparison mask `3923956094` is also legal and has exactly this raw score. This is a complete finite separation result for the supplied matrices and explicit linear coefficients. It does not prove the original 682/683 research objective or a full combined dual certificate.

The final-source run processed 90,179 layer-pair orbits and all 13,150,453 legal marked completions, without the minimum-hidden-direction restriction. Its wall time was 4.34 seconds. The complete unabridged stdout is [full.stdout.txt](full.stdout.txt), with empty [full.stderr.txt](full.stderr.txt). Actual commands, source hashes, exit codes, and timing are in [RUNS.json](RUNS.json).

## Independence and frozen inputs

The implementation was constructed from the parent's abstract contract and the actual numeric inputs. No original `verify_local.cpp`, Root `finite8_flags/oracle/*.cpp`, producer geometry modules, or `keys.bin` was read, before or after implementation. No precomputed orbit keys or producer feature tables are used. The value `4924508303670` and parent witness appear only in final comparison checks, and never affect enumeration, maximization, or pruning.

Only `OWN_ORACLE_RUN.json` was read to locate the matrix and explicit linear input files. Their numeric bytes were copied unchanged into this new directory. [INPUT_MANIFEST.json](INPUT_MANIFEST.json) records their source paths, byte counts, and hashes. All writes for this task were confined to this directory; no child agent or historical job was started.

The final source is [independent_q4.cpp](independent_q4.cpp), SHA-256:

```
df2cc05dd8f96ef7d9497d57ee01106e8cb4eed10dff173749a16f48f2b53211
```

The actual matrix and linear hashes are respectively:

```
d76afe3322661041d1f1b2d39b2e5a43ddf116add57e5ecc4b701398bb35a116
9220e518ddc448986d40b12a2495b78f5cc5735a924da524715f2fe250e53713
```

The parser requires symmetric integer matrices of dimensions `240,212,190,187,170,9`, six explicit linear coefficients, and no trailing input tokens. It does not test or assume PSD. The matrix header is `1 -1 64512`; its `D` and target fields are metadata for this raw functional and do not scale the integers. The independent certified quantity here is the raw integer S. If the parent-provided external scale is `1e9`, the normalized value is

```
4924508303670 / (64512 * 1000000000)
= 164150276789 / 2150400000000
= 0.076334764131789434523809523809523809...
```

The header itself does not encode `1e9`; the external scale's metadata is separately the parent's responsibility unless supplied for direct reading. This distinction has no effect on the raw maximum or its positivity.

## Complete domain construction

Q3 vertices are the integers 0 through 7. Its edge order is independently constructed by `x=0,...,7`, then axis `a=0,1,2`, retaining the edge `(x,x xor 2^a)` exactly when bit a of x is zero. Q4 has these twelve edges on the bottom layer, the corresponding twelve edges shifted by 8 on the top layer, and eight cross edges `(x,x+8)` in increasing x order. A 32-bit mask therefore has bottom A in bits 0--11, top B in bits 12--23, and cross subset S in bits 24--31.

A four-cycle in a hypercube uses precisely two axes, each twice, and is therefore a coordinate square. The program constructs all six Q3 squares by choosing two axes and fixing the remaining coordinate. It tests every one of the 4,096 Q3 edge masks against these six squares. Exactly **2,902** pass. This derives the legal list; the expected count is checked only afterward.

Every Q4 graph has a unique ordered decomposition `(A,B,S)` along the fixed last axis. It is legal exactly when A and B are legal Q3 graphs and S is an independent vertex set in the graph with edge set `A intersect B`. Indeed, every square internal to one layer is already tested in A or B. A square crossing the layers consists of one Q3 edge in both A and B, together with the cross edges at its two endpoints. Thus all crossing squares are absent exactly when no edge in `A intersect B` has both endpoints in S.

The code independently builds all 48 Q3 isometries as six coordinate permutations times eight translations. Each map is an explicit vertex permutation and hence an explicit edge permutation. Every image of every legal Q3 mask is checked to remain in the generated legal list.

It traverses **all 2,902 squared = 8,421,604 ordered pairs** `(A,B)` in increasing mask-index order. For each unseen pair it selects that pair as a representative and marks all images under a common Q3 isometry, both with and without exchanging the layers. It does not canonicalize A and B independently. The sum of newly marked orbit cardinalities is checked to equal 8,421,604, and every pair's visited byte is checked at the end. This derives **90,179** pair representatives. Their independently obtained orbit-size histogram is:

| Orbit size | Number of pair orbits |
|---:|---:|
| 1 | 1 |
| 3 | 1 |
| 4 | 2 |
| 6 | 8 |
| 8 | 9 |
| 12 | 46 |
| 16 | 15 |
| 24 | 355 |
| 32 | 11 |
| 48 | 4,216 |
| 96 | 85,515 |

For every representative the code tries **all 256** cross subsets and keeps exactly those independent in `A intersect B`. There is no further quotient of S and no hidden-direction pruning. Summing the kept subsets derives **13,150,453** legal marked completions. This number counts marked representatives and may include isomorphic Q4 graphs; it is not asserted to count nonisomorphic graphs.

To see why this covers every legal Q4, transport its pair `(A,B)` to the selected pair representative using the common cube isometry and possible layer exchange that marked it. The same transport carries its cross set to another subset of the eight cross positions. Independence in the intersection is preserved. This transported subset is among all 256 tested for that representative, so a graph isometric to the original legal Q4 is evaluated.

## The exact functional and its invariance

All 24 root Q2 faces are constructed by choosing two of four axes and fixing the other two coordinates. In the chosen face coordinates their vertices are `0,1,2,3`, with edges `01,02,13,23`. For each outer direction the flag consists of the four connectors followed by the four parallel edges in this order.

All eight square isometries are generated directly from two axis orders and four translations. The canonical root is the minimum image of the four-bit root edge mask. Its possible representatives are `0,1,3,6,7`. The ascending legal flag list is constructed from codes `0,...,239`, excluding exactly a cross square whose root edge, parallel edge, and two endpoint connectors are all present. The five list sizes are independently derived as **240,212,190,187,170**.

For a face, one chosen root-canonicalizing map is applied to both flags. The code then sums the corresponding matrix entry over the stabilizer of the canonical root and multiplies by `8 / |stabilizer|`, obtaining the integer `8*Qbar`. The face contribution is exactly

```
280 * faceval(s,t) + 28 * faceval(s,s) + 28 * faceval(t,t).
```

The stabilizer average removes the choice of canonicalizing map: any two such maps differ by a canonical-root stabilizer element, which only permutes the averaging sum. Simultaneous transportation preserves the relative placement of the two flags. Exchanging the outer directions preserves the result because the input matrices are symmetric and the diagonal coefficients are equal.

At a vertex, each of six direction pairs supplies a Q2 with that same marked root vertex. Its four-bit code is `01,02,13,23`. The only quotient swaps the two axes, giving representatives `0,1,3,4,5,6,7,12,13`; the root is never moved to another square vertex. Among unordered pairs of the six direction pairs, including equal pairs, the code derives 3 disjoint pairs, 12 pairs with one common direction, and 6 diagonal pairs. Their weights are 720, 144, and 24 respectively.

A Q4 isometry permutes its faces and vertices; local root frames change by precisely the synchronized square actions above. Vertex direction-pair intersections are preserved. Edge count and degree histogram are also preserved. Consequently **the entire signed functional is Q4-isometry invariant for arbitrary symmetric input matrices**, independently of any PSD condition. This makes the layer-pair orbit reduction valid.

For speed, the program precomputes exact face contributions and the 65,536 possible marked-vertex neighborhood contributions, and constructs byte-gather tables from its own endpoint geometry. These are mechanical accelerations of the preceding definitions; they do not remove graphs from the domain.

## Witness checks independent of the fast score tables

The maximizing mask found by this enumeration is `3001496046`, with 19 edges:

```
0-2 0-4 1-3 2-3 2-6 3-7 4-5
8-9 8-10 9-13 10-11 10-14 12-14 13-15 14-15
1-9 4-12 5-13 7-15
```

The fast score is checked against both a direct bit-gather replay and a separate raw literal scorer. The raw scorer asks for each edge by its vertex endpoints, rebuilds every face and vertex state, performs the canonicalizing/stabilizer matrix contraction directly from the original integer entries, and does not use the fast gather geometry or score tables.

A separate literal C4 check enumerates every pair of vertices and counts common neighbors; every pair has at most one. The same literal legality and raw score checks are then performed on all **384** Q4 isometry images of the witness. Every score is exactly `4924508303670`. The parent comparison mask `3923956094` is checked by the same literal common-neighbor criterion and raw scorer and has the same exact score.

There are five maximizing marked completions in this chosen enumeration. This does not assert that they are five different isomorphism classes.

## Arithmetic safety

Let `M_F` and `M_v` be the largest absolute entries among the five face matrices and the vertex matrix. Each face value has absolute value at most `8*M_F`, so all 24 face contributions have absolute value at most

```
24 * (280 + 28 + 28) * 8 * M_F = 64512 * M_F.
```

All sixteen vertex terms have absolute value at most

```
16 * (3*720 + 12*144 + 6*24) * M_v = 64512 * M_v.
```

Every graph has at most 32 edges and 16 vertices. Therefore a rigorous bound on the absolute raw score is

```
32*abs(eCoeff) + 16*max_d(abs(hCoeff[d])) + 64512*(M_F + M_v).
```

For the actual supplied input, `M_F=1334997068`, `M_v=0`, and this bound is **124395477268976**, already below signed 64-bit capacity. The implementation nevertheless accumulates matrix contractions, linear terms, scores, maxima, and bounds in signed **128-bit integers**. Every narrowing into a signed 64-bit lookup-table entry is explicitly checked. The computed bound is also required to be below `2^120`, leaving ample 128-bit headroom. There is no floating arithmetic in the score, comparison, legality, or coverage logic.

## One nonconstant calibration

Because the actual input's vertex matrix is zero, one additional complete calibration exercises the vertex state and weighting path. Let `f(i)` be 1 precisely when the Q2 state has both root-incident edges, and let

```
Qv(i,j) = f(i) + f(j),
eCoeff = 0,
hCoeff[d] = -1344 * binom(d,2),
all face matrices = 0.
```

For any one of the six direction pairs, its f-value appears once in a disjoint pair, four times in a one-overlap pair, and twice in its diagonal contraction. The coefficient is `720 + 4*144 + 2*24 = 1344`. At vertex v the sum of f over its six pairs is exactly `binom(deg(v),2)`. The total functional therefore vanishes identically on every legal graph.

The calibration actually evaluates the same **13,150,453** complete legal marked domain. Its maximum is exactly zero, and its maximizing-completion count is exactly **13,150,453**, verifying that every evaluated score is zero. The raw literal scorer also returns zero on the real-input comparison witness. Full output and inputs are [calibration.stdout.txt](calibration.stdout.txt), [calibration_matrices.txt](calibration_matrices.txt), and [calibration_linear.txt](calibration_linear.txt). This was the only additional calibration.

## Reproduction and scope

From this directory:

```sh
g++ -O3 -std=c++17 -Wall -Wextra -Wconversion -o independent_q4 independent_q4.cpp
./independent_q4 oracle_matrices.txt --linear oracle_linear.txt
./independent_q4 calibration_matrices.txt --linear calibration_linear.txt
```

Compilation produced no warnings or errors. Both final-source complete runs exited zero. An earlier 1,000-pair real-input cost probe is retained as `cost_probe.stdout.txt`; it predates removal of unused constructor code and addition of the separate raw literal witness scorer, so it is not claimed as a final-source hashed run. The final source was rerun completely after those changes.

The established mathematical result is the complete finite maximum of this actual integer functional, including its positive maximizing witness. It independently confirms the parent's reported raw maximum and local violation. No PSD property, the full combined-certificate assembly, its high-dimensional averaging connection, or the original 682/683 nonexistence goal is established by this check.
