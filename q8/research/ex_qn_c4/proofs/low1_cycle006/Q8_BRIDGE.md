# A one-low-vertex Q6 theorem and minimum degree three at 687 edges

Root, cycle006, 2026-11-07. This deduction consumes the independently
reconstructed and replayed L1 theorem in `orbit_sat/review/REVIEW.md`.
Its historical unique-degree-two and minimum-three imports retain their
original scope; their large certificate families were not replayed here.

## 1. Uniform one-low-vertex statement

Let H be a C4-free subgraph of Q6, and fix one of its parity classes P.
Suppose at most one vertex of P has degree less than three. Then

    S_P(H) = sum_{v in P} binom(d_H(v),3) <= 158.

There is no restriction on the opposite parity. With no exceptional
vertex this is the historical minimum-three theorem. With exceptional
degree two it is the historical unique-degree-two theorem. With degree
one it is the newly established L1 theorem.

If the exceptional vertex u has degree zero, add any one of its six
ambient edges. A newly created square would contain u, which still has
degree only one, so the new graph is C4-free. Only u changes degree on P;
its cubic contribution stays zero. The new graph meets L1, proving the
same bound for H. This last case is a direct consequence, not another
solver run or an assumption on any opposite-side degree.

Equivalently every such Q6 has at least two P-holes among its 160 actual
coordinate Q3 faces. Each face has at most one full P three-star: two
same-parity full stars within a Q3 would complete a coordinate square.

## 2. Exact application to the remaining degree-two Q8 profile

Let G be any C4-free subgraph of Q8 with 687 edges. The accepted
cycle005 weighted gate already gives minimum degree at least two.
The stronger core gate and its actual-face exclusion show that a parity
containing a degree-two vertex has exactly the histogram

    n2=1, n5=77, n6=50,

with all its other degree counts zero. These facts and their historical
imports are in `../q7_slack_cycle005/low_degree/PROOF.md`, Sections1–5,
and its independent review, as recorded in `../q7_slack_cycle005/VERIFICATION.md`.

Fix such a parity and its unique degree-two vertex u. Every actual Q6
face is obtained by fixing two Q8 coordinates. All specified-side
vertices other than u have local degree at least three, since they lose
at most two of their five or six global incident edges. Thus every one
of the 112 Q6 faces satisfies Section1. For clarity the exact counts are:

| Local exceptional degree | Number of faces |
|---|---:|
| No exceptional vertex | 84 |
| Two | 15 |
| One | 12 |
| Zero | 1 |

The 28 faces containing u correspond to all omitted coordinate pairs.
They remove zero, one or two of its two retained directions, giving
binom(6,2)=15, 2*6=12, and binom(2,2)=1 respectively. No relative
position or degree hypothesis concerning the opposite parity is used.

The global specified-parity star sum and hole count are

    S_P(G) = 77*10 + 50*20 = 1770,
    h_P(G) = 1792 - 1770 = 22.

Each actual Q3 face lies in binom(5,3)=10 Q6 faces, with the same parity
stars; hence sum_F h_P(F)=10h_P(G)=220. Section1 instead gives

    sum_F h_P(F) >= 112*2 = 224 > 220,

a contradiction. Consequently **every 687-edge C4-free subgraph of Q8
has minimum degree at least three**. This strengthens the earlier
conditional 222>220 caller by also covering its single local-degree-zero
face; it does not change any earlier frozen proof or experiment.

## 3. Remaining original obligation

Removing the sole degree-two row leaves seven necessary parity
histograms containing degree-three vertices from the old eight-row
table. This does not establish minimum degree four. In the separate
minimum-degree-four Q8 domain, the already derived ceiling S8<=581 and
the sufficient universal minimum-three Q7 candidate J>=73 are unchanged.
That candidate remains unproved. Therefore the current unrestricted
bounds remain 682<=ex(Q8,C4)<=687.

All new statements above are deductions about the original actual graph,
not about a seed neighborhood or a moment-system realization. No Lean,
new canonical whole-proof audit, or fresh replay of historical imports
is claimed. The computational proof of L1 and its independent direct
RUP replay remain available independently of the new analytic draft.
