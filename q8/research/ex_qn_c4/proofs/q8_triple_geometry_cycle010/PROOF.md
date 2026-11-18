# Four full roots without a minimum-degree assumption

Cycle010, 2026-11-07. Analytic author: /root/audit_asymptotic.
The twelve-pair capacity argument was also derived independently by Root,
whose actual checks are in ../q6_four_full_capacity_cycle010/.
No literature novelty or new sharpness claim is made.

## Theorem

Let G be a C4-free subgraph of Q6, and fix either parity P. Suppose
exactly four vertices of P have degree six. There is no degree
restriction on any other vertex of either parity. Let

    L = #{x in P : d_G(x)<=2},
    S = sum_{x in P} binom(d_G(x),3).

Then

    S <=144-L.                                            (1)

In particular exactly three low specified-side vertices imply
S<=141 when c=4. Thus the (S,c)=(159,4) counterexample branch for a
three-low weighted bound of 319 is impossible, regardless of the
low positions and selected directions.

## 1. Complete normalization of the full code

Two full vertices in P cannot have distance two: they retain both
edges to each of their two common neighbors, making a square.
Their distance is therefore four or six.

A distance-six pair consists of complementary binary words. Every
other word has distances to that pair summing to six, so no third
full vertex could have distance at least four from both. Since
there are four full vertices, every pair has distance four.

Translate one full vertex to zero, also sending P to the even parity.
Let F1,F2 be the supports of two other full vertices. Both have
size four and their intersection has size two. The sets

    A=F1 intersect F2, B=F1 minus F2, C=F2 minus F1

partition the six directions into three pairs. The fourth full
vertex has a four-element support F3. Write a,b,c for its
intersection sizes with A,B,C. Its distance four from F1 and F2
gives a+b=a+c=2, while a+b+c=4. Hence a=0 and b=c=2.

Thus one simultaneous coordinate permutation sends the full set to

    K={0, A union B, A union C, B union C}
     ={0,15,51,60},

with A={0,1}, B={2,3}, C={4,5}. This covers every four-full input.
No low root is fixed or moved separately, and no minimum-degree
condition was used.

## 2. The four remaining block-constant vertices

Call a vertex block-constant when in each of A,B,C its two bits
are equal. There are eight such even vertices. Four are K: they
occupy an even number of whole direction pairs. The other four
occupy an odd number.

Each of these other four vertices x has exactly three full neighbors
at distance two, obtained by toggling A, B, or C. If x retained both
directions of any one of those pairs, it and the corresponding full
vertex would complete a square. Therefore x retains at most one
direction from each pair and

    d_G(x)<=3.                                           (2)

## 3. The other 24 vertices and their forced pairs

Every other even vertex has one selected bit in each of exactly two
of the blocks A,B,C, and equal bits in the third block. Indeed, the
number of blocks containing one bit must be even. There are
3*2*2*2=24 such vertices.

Let F be the third, block-constant direction pair for such a vertex x.
To reach a full vertex at distance two, one must flip one direction
in each of the two one-bit blocks, resolving both. There are four
ways to resolve them, and exactly two give an even number of occupied
whole pairs, hence a vertex of K. Thus x has exactly two full vertices
at distance two.

Let D1,D2 be their two difference pairs from x. They are disjoint:
the corresponding full vertices are at distance four, which means
their difference pairs from x have no common coordinate. Together
D1,D2 cover the two one-bit blocks; their complement is exactly F.

At x, neither D1 nor D2 may be retained in full, or a square with the
corresponding full vertex results. Consequently

    d_G(x)<=4.

Moreover, equality forces both directions in F to be retained, as
well as exactly one direction from each of D1,D2.

Define x' by flipping both bits of F. It is another of these 24
vertices, with the same two one-bit blocks and the same forced pair F.
The map x to x' is a fixed-point-free involution, giving twelve pairs.
If both x and x' had degree four, both would retain F. They would
then be adjacent to both intermediate vertices x xor e_i and
x xor e_j, for F={i,j}, making a C4. Therefore

    N4<=12,                                              (3)

where N4 is the total number of degree-four vertices in P. The
four vertices in Section 2 cannot contribute to N4.

This pairing is on actual vertices and actual forced directions.
It does not assign degree-four patterns independently or forget their
common square.

## 4. Star count and the three-low consequence

All nonfull P vertices have degree at most four by Sections 2--3.
Among their 28 vertices, L have degree at most two, N4 have degree
four, and the remaining 28-L-N4 have degree three. Hence exactly

    S=4*20+4N4+(28-L-N4)=108-L+3N4.

Apply (3) to obtain S<=144-L. This proves (1), including graphs
with degree-zero or degree-one vertices. The opposite side remains
unrestricted throughout.

For exactly three low P vertices, L=3, so S<=141. In particular
S159,c4 is impossible for the A marking, for the B marking, and
for every other three-low marking. The weighted value in this c4
case is at most 2*141+4=286.

The safe-three-star interface in SAFE_STAR_INTERFACE.md leaves only
(S,c)=(160,2) as a possible violation of 2S+c<=319 with exactly
three low roots. Its exclusion for specific A/B markings is a
separate new finite obligation owned by /root/audit_q8; this proof
does not claim to exclude every S160,c2 three-low graph.

## 5. Exact checks, provenance and acceptance boundary

Root independently enumerated all four-subsets of the 32 even
vertices whose mutual distances are at least four. There are 120.
The orbit of the canonical code under all 32 even translations and
720 coordinate permutations is exactly those 120 sets.

For the canonical code, Root's check_pairs.py enumerates all 64
possible stars at every nonfull even vertex, testing actual
retained-neighbor intersections with the four full roots.
It finds the four degree-at-most-three vertices and 24 other
vertices, each with exactly four allowable degree-four stars.
Their common forced pair gives the twelve vertex pairs above.
For every pair all sixteen cross-products of its degree-four
stars form an actual C4. These checks use no minimum-degree
assumption and were read in full alongside PAIR_CHECK.json.

The independent evidence is

    ../q6_four_full_capacity_cycle010/check_pairs.py
    ../q6_four_full_capacity_cycle010/PAIR_CHECK.json.

It also checks the historical c4 witness sides; a no-low S144
witness is retained at its original provenance. The L=0 numerical
bound 144 agrees with the old minimum-three SAT result.
The present argument explains that bound analytically and applies
without the old minimum-degree hypothesis. It does not relabel
the old result as new, replay old traces, or assert that 144-L is
attained for every L.

This analytic theorem and the A/B finite inputs receive the separate
review assigned by Root. No author verdict substitutes for that
review. The full h23 row and the unrestricted Q8 upper bound are
not changed by this theorem alone.
