# A specified parity with one degree-one vertex has at most 158 three-stars in Q6

Author: `/root/audit_asymptotic`, cycle006, 2026-11-07.
Status: complete analytic candidate, with the finite checks in
`CHECK_RESULTS.json`; independent mathematical review is a separate obligation.
The sole non-elementary import is the already accepted unique-degree-two
lemma stated below. No new SAT exclusion is used in this proof.

## Statement and the imported interface

Let (G\subseteq Q_6) be C4-free. Fix one parity class (P), and suppose
that precisely one vertex (u\in P) has degree one, while the other 31
vertices of (P) have degree at least three. There is no hypothesis on the
degrees in the opposite parity. Then

\[
 S=\sum_{v\in P}\binom{d_G(v)}3\le158. \tag{L1}
\]

We use this accepted result, with its full one-sided interface:

> **Unique-degree-two import.** If a C4-free subgraph of Q6 has exactly one
> vertex of degree two on a specified parity and the other 31 vertices on
> that parity have degree at least three, its specified-parity three-star
> sum is at most 158. The opposite parity is unrestricted.

The source is
`q6_sources/q8_upper_independent/REFINEMENT_688.md`,
Section 1. Its 17-case certificate inventory is
`results/low2_star158_certificate_manifest.json` in the same source directory:
one S=160 case and 16 S=159 hole-orbit cases, reporting 4,122,060 checked RUP
additions. The present argument consumes that accepted import; it does not
replay its historical certificates. The precise one-sided interface was
also checked in
`../../q7_slack_cycle005/low1_probe/REDUCTION_REVIEW.md`.

## 1. Elementary star and full-vertex facts

A full three-star centered at (v) consists of its three retained edges in
one coordinate Q3. Two centers of the same parity in a Q3 are at distance
two. If both stars are full, their two common neighbors give a retained
C4. Hence every coordinate Q3 contains at most one full star centered on
(P). The 160 coordinate Q3s of Q6 give

\[
 S\le160,
 \qquad h:=160-S=\#\{\text{Q3s with no full }P\text{-star}\}. \tag{1}
\]

Call the latter Q3s holes. It suffices to exclude S=160 and S=159.

Let (c) count degree-six vertices on (P). Two such vertices cannot be
at distance two, because their common neighbors would form a C4. Thus
their pairwise distances are at least four. Five such vertices would
have total pairwise distance at least (4\binom52=40). In each of six
coordinates, a set of five binary words contributes at most
(\max_{0\le k\le5}k(5-k)=6) to that total, giving at most 36. Therefore
(c\le4). Since the 31 ordinary vertices have degrees 3,4,5,6 and cubic
weights 1,4,10,20, respectively,

\[
 S\equiv31+c\pmod3.
 \quad S=160\Rightarrow c\in\{0,3\};
 \quad S=159\Rightarrow c=2. \tag{2}
\]

## 2. Replacing the root star forces all 30 edges between layers one and two

Translate (u) to the empty subset of (Omega=\{1,\ldots,6\}); the
specified parity becomes the even subsets. For distinct directions (i,j),
delete the old edge at (u) if it is not in directions (i,j), and make
the root star consist of exactly (u\{i\}) and (u\{j\}). All edges
not incident with (u) are unchanged.

Any newly created C4 must contain (u), and, since its new degree is two,
must be the unique (i,j) square at (u). This square exists precisely
when both remote edges

\[
 \{i\}\{i,j\},\qquad \{j\}\{i,j\}
\]

are retained. If either remote edge is absent, the replacement is C4-free.
It changes no degree on (P\setminus\{u\}), and changes the root's degree
from one to two, both having cubic contribution zero. The unique-degree-two
import would then give the desired S<=158 for the original graph.

Consequently a counterexample has both remote edges for every pair
(i,j). Thus **every one of the 30 edges between Hamming layers one and
two is retained**. All subsequent reasoning concerns this same labeled
Q6 graph. No face is independently normalized.

## 3. The first two star identities

For each two-subset (s), let (t_s) count its retained edges to
three-subsets. The two edges downward are forced, so

\[
 d(s)=2+t_s,\qquad1\le t_s\le4.
\]

Every three-subset (T) has at most one retained edge to its three
two-subsets. Indeed, two such two-subsets share a singleton, and both
edges to that singleton are forced, creating a C4.

Let (alpha) be the number of holes containing the empty subset. Under
S=160 it is zero; under S=159 it is zero or one. In the Q3 on coordinates
(T), the empty subset cannot give a full star, while each two-subset
gives a full star exactly when its edge to (T) is retained. Therefore

\[
 \sum_{|s|=2}t_s=20-\alpha. \tag{3}
\]

Write (z_j=\#\{s:t_s=j\}), for (j=1,2,3,4). Then

\[
 \sum_jz_j=15,\qquad z_2+2z_3+3z_4=5-\alpha,\qquad z_4\le1. \tag{4}
\]

In particular the layer-two star sum and the number of pairs of upward
edges from layer-two roots are

\[
 S_2=30-3\alpha+3z_3+10z_4,
 \qquad \sum_{|s|=2}\binom{t_s}{2}=5-\alpha+z_3+3z_4. \tag{5}
\]

For a four-subset (R), let (b_R) count its downward retained edges to
three-subsets and (f_R) its upward retained edges to five-subsets.
Thus (0\le b_R\le4), (0\le f_R\le2), and (d(R)=b_R+f_R\ge3).
Let (t_R) count two-subsets (s\subset R) for which both upward edges
from (s) inside (R) are retained.

There are four Q3 faces with top (R) and base a singleton of (R).
A two-subset counted by (t_R) gives a star in exactly two of those
faces, the ones based at its two elements. The top (R) gives exactly
(\binom{b_R}{3}) stars there. If (h_R) counts holes among those four
faces, star injection gives the exact identity

\[
 2t_R+\binom{b_R}{3}=4-h_R. \tag{6}
\]

Let (\beta=\sum_Rh_R). These 60 faces are precisely the Q3 faces with
one fixed coordinate equal to one and all other fixed coordinates zero.
They are distinct from the 20 faces containing the empty subset. Hence
(alpha=\beta=0) when h=0, and
(alpha,\beta\in\{0,1\},\alpha+\beta\le1) when h=1.

If (h_R=0), (6) implies either (b_R=4,t_R=0), or (b_R\le2,t_R=2).
If (h_R=1), it implies (b_R=3,t_R=1). Let (a) count the four-subsets
with (b_R=4). There are exactly (\beta) exceptional four-subsets with
(b_R=3); the other (15-a-\beta) have (b_R\le2).

Each pair of upward edges from a two-subset determines one four-subset
(R), so summing (6) yields

\[
 5-\alpha+z_3+3z_4
   =\sum_Rt_R=30-2a-\beta. \tag{7}
\]

In particular

\[
 5-\alpha+z_3+3z_4\equiv\beta\pmod2. \tag{8}
\]

## 4. Upward capacity of the backward-full four-subsets

Call (R) backward-full when (b_R=4). A five-subset (W) can have a
retained edge to at most one backward-full (R\subset W). Otherwise
two such four-subsets intersect in a three-subset, and their two edges
to that intersection, together with their two edges to (W), form a C4.
There are six five-subsets, so

\[
 F:=\sum_{b_R=4} f_R\le6. \tag{9}
\]

Let (c_4) count degree-six four-subsets. These are exactly the
backward-full ones with (f_R=2). For a backward-full (R), its cubic
weight is (4+6f_R+4\mathbf1_{f_R=2}). Therefore

\[
 S_{4,\mathrm{back}}=4a+6F+4c_4\le4a+36+4c_4. \tag{10}
\]

Let (Z=Omega) be the layer-six vertex. If (d(Z)=6), every four-subset
has (f_R\le1), or its two upward edges form a C4 with (Z). In particular
then (c_4=0). In all cases the full-vertex count satisfies

\[
 c=z_4+c_4+\mathbf1_{d(Z)=6}. \tag{11}
\]

## 5. Excluding S=160

Here (alpha=\beta=0). Equations (4) and (8) give just two possibilities:

| ((z_1,z_2,z_3,z_4)) | (S_2) | (a) |
|---|---:|---:|
| ((11,3,1,0)) | 33 | 12 |
| ((12,2,0,1)) | 40 | 11 |

Indeed, (z_2+2z_3+3z_4=5), (z_4\le1), and (z_3+z_4) is odd.
The top (Z) is not full: if it were, (11) would give (c=z_4+1\le2),
contradicting (c\in\{0,3\}). Thus its contribution is at most 10.
The non-backward-full four-subsets have degree at most four, contributing
at most (4(15-a)).

In the first row (c_4\le3); in the second row (z_4=1) forces
(c=3,c_4=2). Equations (10) and (11) give, respectively,

\[
 S\le33+(48+36+12)+12+10=151,
\]
\[
 S\le40+(44+36+8)+16+10=154.
\]

Both contradict S=160.

## 6. Excluding S=159 when the top is full

Now c=2. Suppose first that (d(Z)=6). By (11), (z_4=1,c_4=0), and
every (f_R\le1). The ordinary non-backward-full four-subsets have
degree at most three; the (\beta) exceptional ones have degree at most
four. From (10),

\[
 S_4\le4a+36+(15-a-\beta)+4\beta=3a+51+3\beta.
\]

With (z_4=1), the total is therefore

\[
 S\le111-3\alpha+3z_3+3a+3\beta. \tag{12}
\]

If ((\alpha,\beta)=(1,0)), (4) forces (z_3=0,z_2=1), but (8) fails.
If ((\alpha,\beta)=(0,0)), (4) and (8) force (z_3=0,z_2=2,a=11),
and (12) gives S<=144. If ((\alpha,\beta)=(0,1)), they force
(z_3=1,z_2=0,a=10), and (12) gives S<=147. All possibilities contradict
S=159. Hence (d(Z)\le5).

## 7. The sole tight S=159 layer profile is geometrically impossible

Since the top is not full, (11) gives (c_4=2-z_4). An ordinary
non-backward-full four-subset has degree at most four; an exceptional one
has degree at most five. By (5) and (10),

\[
\begin{aligned}
 S&\le(30-3\alpha+3z_3+10z_4)
       +(4a+36+4(2-z_4))\\
  &\qquad +4(15-a-\beta)+10\beta+10\\
  &=144-3\alpha+6\beta+3z_3+6z_4. \tag{13}
\end{aligned}
\]

The small integer possibilities from (4) and (8) are as follows. Every
row shown determines (z_2=5-\alpha-2z_3-3z_4) and
(z_1=15-z_2-z_3-z_4); these are nonnegative.

| ((\alpha,\beta)) | possible ((z_3,z_4)) | upper bound in (13) |
|---|---|---|
| ((1,0)) | ((0,0),(2,0)) | 141,147 |
| ((0,0)) | ((1,0),(0,1)) | 147,150 |
| ((0,1)) | ((0,0),(2,0),(1,1)) | 150,156,159 |

Only the final possibility could attain 159. It has

\[
 (\alpha,\beta)=(0,1),\quad
 (z_1,z_2,z_3,z_4)=(13,0,1,1),\quad a=10,\quad c_4=1.
\]

Equality in (13) is now mandatory. In particular (d(Z)=5), the
backward-full vertices have F=6, the exceptional (b_R=3) vertex has
(f_R=2), and all (15-10-1=4) ordinary non-backward-full vertices have
degree four. Since those have (b_R\le2,f_R\le2), each has
(b_R=f_R=2). Along with the one full backward-full vertex, this gives
**six distinct four-subsets with (f_R=2)**.

Let (W_0) be the unique five-subset whose edge to (Z) is missing. A
four-subset with (f_R=2) cannot have both upward neighbors among the
five retained neighbors of (Z), or the corresponding square is full.
It must therefore be a neighbor of (W_0). But a five-subset has exactly
five four-subset neighbors. Six distinct such four-subsets cannot exist.
This contradiction excludes S=159, completing the proof of (L1). □

## 8. Exact original-graph consequence and scope

The previously reviewed m=687 Q8 low-degree gate leaves one possible
parity with degree counts (n_2=1,n_5=77,n_6=50), and 22 star holes.
Its 112 actual Q6 faces consist of one reducing the degree-two vertex to
zero, 12 reducing it to one, 15 keeping degree two, and 84 not containing
it. All other vertices on the specified parity retain local degree at
least three. The accepted minimum-three and unique-degree-two imports
cover 99 faces; (L1) covers the additional 12. Hence

\[
 10\cdot22=\sum_F h_F\ge2(99+12)=222>220.
\]

Thus L1 closes that degree-two Q8 branch, conditional on the already
reviewed gate and accepted imports. It does not exclude the remaining
degree-three Q8 branch and does not by itself prove ex(Q8,C4)<=686.

No novelty or current literature priority claim is made here. This is an
analytic replacement for the pending L1 obligation, not a claim that the
old UNKNOWN solver attempts proved anything. No new solver trace is
needed for Sections 1--7. The unique-degree-two import remains an explicit
historical computational dependency.

## Reproduction and finite-check scope

Run from any directory:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 /mnt/c/Users/Anony/Desktop/project/research/ex_qn_c4/proofs/low1_cycle006/analytic/check_layers.py
```

The script writes only next to itself. It checks all (4^4\cdot2^4=4096)
marked local Q4 configurations for (6): each of four triples chooses no
downward edge or one of its three two-subsets, and all four top edges are
arbitrary. It independently builds actual squares and actual stars. It
also enumerates all integer layer-count branches, using the actual cubic
weights and forward-edge counts, and verifies the final capacity for all
six labeled choices of the missing top edge. It imports no producer and
uses no SAT/CP package. These are discriminating local checks; the written
argument supplies the Q6 coverage, inequalities, and logical connection.
