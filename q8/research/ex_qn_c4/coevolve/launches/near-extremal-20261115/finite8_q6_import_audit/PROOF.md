# Targeted Q6 premises for the finite-eight maximal-profile route

This document supplies a dependency-complete local argument for the historical
inequality used in `../finite8_maximal_route/PROOF.md`. It proves no Q8 bound of
682. The original global problem remains OPEN. The source branch's assertions
about global 687/688 exclusions are not premises here.

Every graph below is an arbitrary spanning edge subgraph of Q6, including
isolated vertices, with no retained C4. Fix either parity P of its vertices.
Write S=sum over P of binom(d(v),3), c=count of degree-six P vertices, and
L=count of P vertices of degrees zero, one, or two. No restriction is placed
on opposite-parity degrees. The result needed by the caller is

    4S+2c <= 632+5L.                                     (G)

All coordinate transformations below are single isometries of the whole
graph, including its marked vertices, directions and holes. Translating a
specified vertex to zero sends P to the even parity. It does not impose an
extra parity condition on the original graph.

The actual fresh certificate completion status is in `FRESH_REPLAYS.json` and
`VERIFICATION.md`. The mathematics here distinguishes finite cover, input
semantics, and trace correctness, rather than treating a stored UNSAT status
or manifest as a proof.

## A. Elementary facts and common encoding

There are 160 coordinate Q3 faces. Two distinct vertices of the same parity
in one Q3 have distance two. If both carry a full three-star in that face,
their common two neighbors give a retained C4. Thus at most one such star
occurs in each face, S<=160, and 160-S counts its parity holes exactly.

Distinct full P roots have distance at least four. Five full roots would
have total pairwise distance at least 4*binom(5,2)=40. Each of six coordinates
contributes at most 2*3=6, so the total is at most36. Consequently c<=4.
If at least three full roots exist, no pair has distance six: a third
root's distances to a complementary pair sum to six, and cannot both be at
least four. Three full roots therefore normalize to {0,15,51}. Four normalize
to {0,15,51,60}. For the latter claim, divide the coordinates into three pairs
A,B,C, with the second and third roots A union B and A union C. A fourth
weight-four support X must meet each in two. Writing xA,xB,xC for its block
sizes gives xA+xB=xA+xC=2 and xA+xB+xC=4, forcing xA=0,xB=xC=2.

Every even root outside this four-code is distance two from at least two
code roots. An even support either splits no pair or splits two pairs. In
the first case, an outside support uses an odd number of complete pairs;
toggling any of the three pairs reaches a codeword at distance two. In the
second case, exactly two codewords agree on the unsplit pair, giving two
distance-two roots. The independent finite check enumerates all120 actual
four-codes, with outside-distance-two histogram {2:24,3:4} for each.

The independently reconstructed CNFs index all192 cube edges as lexical
endpoint pairs. Their240 negative four-edge square clauses enforce C4-free.
At a six-edge star, all positive four-subset clauses enforce degree>=3;
all positive five-subset clauses enforce degree>=2; the negative six-edge
clause enforces degree<=5. Full roots instead have six positive units.
An exact exceptional star is imposed by one signed unit per direction.
All these clauses concern P only, except for the square clauses. There is
no hidden opposite minimum degree.

Each of640 three-star variables y is equivalent to its three edge variables
e1,e2,e3, by the four clauses (-y or ei) and (y or -e1 or -e2 or -e3).
A face OR asserts a star in that face; replacing its OR by four negative y
units makes it a hole. An unknown hole flag h is equivalent to all four y
being false, by (h or y1 or ... or y4) and (-h or -yi). A full-degree flag
has the analogous six-edge equivalence. A degree threshold zr is equivalent
to degree>=r: (-zr or OR of every (7-r)-subset of its six edges), together
with (zr or negative every r-subset). This is an equivalence for every
Boolean star assignment, including degrees0/1/2.

The compact at-most-k counter on x1,...,xn uses q(i,j), 1<=i<=n-k,
1<=j<=k. Its four clause families are

    -x_i or q(i,1);
    -q(i,j) or q(i+1,j)                  if i<n-k;
    -x_(i+j) or -q(i,j) or q(i,j+1)       if j<k;
    -x_(i+k) or -q(i,k).

An assignment with at most k true inputs extends by making q(i,j) mean at
least j true inputs among the first i+j-1 positions. Conversely the first
three families force these thresholds whenever such j true positions
exist. A (k+1)st true input at position p forces q(p-k,k), contradicting the
last family. Counts0,n,n-1 respectively use negative units, no clauses and
one all-negative clause. At-least uses at-most on negated inputs; exact
counts combine both with separate auxiliaries. Repeated inputs are allowed:
these are positions in the counted list, so repetitions contribute their
intended multiplicity. The small existential truth-table check tests every
assignment through n=6 independently of the prefix interpretation.

The six-case family's unknown-single-hole encoding uses a different simple
prefix OR counter. Its clauses force at most one hole and one positive
disjunction forces at least one. These too extend every intended Boolean
counterexample. All reconstructions compare full clause multisets, including
duplicate multiplicities and variable counts, with the actual old inputs.

## B. Minimum-three star158: all six counterexample cases

Suppose all32 P roots have degree>=3. Cubic weights for degrees3,4,5,6
are1,4,10,20, so S==32+c modulo3. A violation S>=159 is therefore:

* S160 and c2: normalize one full root to0 and the second to15 or63,
  according to distance four or six. These are `q6_fullstar_d4/d6`.
* S159 and c1: normalize its full root to0. The sole hole avoids0 and falls
  under coordinate permutations into exactly three orbits, represented by
  free mask7 and bases8,24,56. Their external fixed-one counts are1,2,3;
  orbit sizes are60,60,20, partitioning all140 Q3s avoiding0. These are
  `q6_one_hole_b8/b24/b56`.
* S159 and c4: normalize all full roots to{0,15,51,60}; allow the unique
  hole anywhere. This is `q6_star159_c4`.

The nonfull roots are constrained to degrees3..5, so the full counts used
in this cover are exact. The corresponding face assertions represent
exactly S160 or S159 by star injection. Every graph violating S<=158
therefore extends to at least one of these six actual inputs. The six
fresh RUP traces, totaling256403 additions, exclude those inputs. This
proves S<=158 on arbitrary specified minimum-three parity P.

## C. Unique-degree-two star158: full case and all16 hole orbits

Suppose exactly one P root u has degree two, all other P roots have degree
at least three. Normalize u=0 and its selected direction mask to3. A
violation is again S160 or159.

For S160 the input `q6_one_low_full_r2` asserts one star in every Q3,
the exact root star0/mask3, and degree>=3 on every other P vertex. It has
no maximum-five condition on those other roots and no assumed full count.

For S159, S==31+c modulo3 forces c2, because c<=4. Every Q3 is represented
as (free mask, fixed-one base). The stabilizer S2 x S4 preserves the selected
pair{0,1}. Its48 actual coordinate maps act on the entire cube. An orbit
is determined by a=number of selected directions free, b=number of selected
directions fixed to one, and t=number of other directions fixed to one:

    0<=a<=2, 0<=b<=2-a, 0<=t<=1+a,
    size = C(2,a) C(4,3-a) C(2-a,b) C(1+a,t).

These16 disjoint possibilities total160 faces. Transitivity follows by
permuting separately the free, fixed-one and fixed-zero coordinates within
the selected pair and its complement. `COVERAGE.json` additionally computes
all labelled images of every representative under all48 maps, checks
pairwise disjointness and exact equality with all160 actual coordinate
faces; it does not rely merely on the sum of stored orbit sizes.

Each representative input has exact root star mask3, degree>=3 elsewhere
on P, its designated hole, one star in every other face, and exactly two
full flags among the other31 roots. Thus every actual S159 counterexample
normalizes to and extends one of these16 inputs. Combined with the full160
input this is a complete17-case exclusion. Its actual fresh RUP replays
contain4122060 verified additions. Hence S<=158 in this one-sided domain.

## D. A certificate-free three-full strengthening for minimum-three P

This avoids importing `q6_roots3_star158` and its204462-addition trace.
With exactly three full roots, translate by the missing fourth codeword,
so the full roots become A union B,A union C,B union C, where A,B,C are
coordinate pairs. The missing fourth root is o=empty. All other29 roots
are nonfull. Let H=N4+3N5 count the degree-four/five nonfull roots.

Construct23 actual capacity-one slots. For each block D, take the square
whose even roots are u and u union D, with u=empty or one selected coordinate
from each of the other two blocks. This gives15 slots. A root occupies a
slot when its selected directions include both of D. Also take the eight
Q3s varying one coordinate from each block, all other coordinates zero.
A root occupies one when its star contains those three varying directions.
Squares and Q3 star injection show each slot has capacity one. None of the
three full roots occupies these slots.

For every nonfull even root, count the selected directions in each block.
Up to permutation, its block support type and coverage are as follows.

* 000: degree4 has selection counts220 or211, giving at least two or three
  occupied slots. Degree5 has221, giving six.
* 200, say x=A: full roots A union B and A union C forbid selecting both
  directions of B or both of C. Degree4 selects all of A and occupies its
  square slot. Degree5 is impossible.
* 110, say x={a,b}: the full A union B root forbids the pair of their block
  mates a',b'. Degree5 therefore contains a,b and all of C, occupying its
  square slot and two Q3 slots. At degree4, if all of C is selected the
  square suffices; otherwise its three selections in A union B include
  a,b, and its selection in C supplies a Q3 slot.
* 211, say x=A union{b,c}: the actual full roots forbid the disjoint pairs
  {b',c} and{b,c'}. At most two directions in B union C are selected, so
  degree4 requires all of A and occupies its square slot. Degree5 is
  impossible.
* 222: each full root forbids one entire pair, so degree is at most3.

Thus each degree4 star uses at least one slot and degree5 uses at least
three: H<=23. Direct cubic weights give S+L=60+29+3H=89+3H.
For the nonlow origin o, let rA,rB,rC be its selected block counts. Its
number of slots is q=number of complete selected blocks+rA*rB*rC. Its
contribution h to H is0,1,3 for degree3,4,5. Patterns210,111,220,211,221
give excess q-h respectively1,1,1,2,3. Counting the origin even at degree3
therefore yields H+1<=23, and S+L<=155 whenever d(o)>=3.

In the present minimum-three domain d(o)>=3 and L=0, so exactly three
full roots imply S<=155. All480 actual full triples, all1206 locally
allowed masks, all213 high-star columns and the23 slots were reconstructed
in the copied independent exact checker. `check_connections.py` separately
generates the symmetric slots and checks all41 nonlow origin masks and all
cross-root shared-slot conflicts, including the degree3 origin excess.
No historical contradiction trace or unproved opposite-degree hypothesis
is needed for this strengthening.

Combining B, D and S==32+c modulo3 gives the following bounds for c0..4:

    S <= (158,156,157,155,156),
    2S+c <= (316,313,316,313,316).

Consequently every minimum-three specified parity satisfies2S+c<=316.

## E. Degree-one extension, with the actual analytic proof

Suppose u is the unique degree-one P root. If replacing its incident star
by some two chosen directions i,j is safe, all other P degrees and S stay
unchanged, while u becomes degree two. C immediately gives S<=158. A new
square in such a replacement must use both final root edges, so it exists
exactly when the two remote edges of that i,j square are present.
In any counterexample S>=159 every replacement is therefore blocked.
Translate u=empty: all30 edges from singletons to two-subsets are retained.

For each two-subset s let ts count its upward edges to triples. Then
d(s)=2+ts with1<=ts<=4. Every triple has at most one retained downward
edge, because two such parents share a forced singleton neighbor. Let alpha
count the parity holes containing0, and zj=count of two-subsets with ts=j.
Then

    sum zj=15,  sum ts=20-alpha,
    z2+2z3+3z4=5-alpha,  z4<=1,
    S2=30-3alpha+3z3+10z4,
    sum binom(ts,2)=5-alpha+z3+3z4.

For a four-subset R let bR and fR count its downward/upward edges, and
tR count its two-subsets having both upward edges inside R. Among the
four Q3s with top R and singleton base, star injection gives

    2tR+binom(bR,3)=4-hR.

Put beta=sum hR and let a=count of R with bR=4. When S160, alpha=beta=0;
when S159, alpha,beta are nonnegative integers with alpha+beta<=1. Thus
there are exactly beta exceptional R with bR=3, and every other R outside
the a backward-full ones has bR<=2. Summing the tR identity gives

    5-alpha+z3+3z4 = 30-2a-beta.                         (*)

Each five-subset is adjacent to at most one backward-full R, or two such
R share a downward triple and complete a square through that five-subset.
Hence F=sum_(bR=4) fR<=6. If c4 counts full four-subsets, their backward
star sum is4a+6F+4c4<=4a+36+4c4. Write Z for the full six-subset. If
d(Z)=6 then every fR<=1, so c4=0. Always c=z4+c4+1_(d(Z)=6).
Congruence gives c0/3 at S160 and c2 at S159.

At S160, (*) and the zj equations allow only
(z1,z2,z3,z4)=(11,3,1,0), a12, or(12,2,0,1), a11. The top cannot be full:
then c=z4+1<=2, contradicting c0/3. Bounding its star by10 and other
four-subsets by4 gives respectively S<=151 and S<=154, contradictions.

At S159 with full top, c2 forces z4=1,c4=0, and each fR<=1. The total
satisfies S<=111-3alpha+3z3+3a+3beta. At(alpha,beta)=(1,0), parity in(*)
fails; at(0,0) the bound is144; at(0,1) it is147. Thus the top is not full.
For top degree<=5, c4=2-z4 and the total bound is

    S <=144-3alpha+6beta+3z3+6z4.

The possible(z3,z4) from the nonnegative zj equations and(*) are:

    alpha,beta=1,0: (0,0),(2,0), bounds141,147;
    alpha,beta=0,0: (1,0),(0,1), bounds147,150;
    alpha,beta=0,1: (0,0),(2,0),(1,1), bounds150,156,159.

Only the last could attain159; equality forces z=(13,0,1,1), a10,c4=1,
d(Z)=5, one exceptional bR=3,fR=2 root, and four ordinary bR=fR=2 roots.
Together with the single full R, six distinct R have fR=2. Each must be
adjacent to the unique five-subset whose edge to Z is missing, else its
two upward neighbors and Z complete a square. That five-subset has only
five four-subset neighbors, a contradiction. This proves S<=158.

The isolated copy of `check_layers.py` checks all4096 marked local Q4
configurations for the identity, all integer branches above and all six
choices of the absent top edge. It writes only under this audit. The
eleven alternate degree-one SAT certificates are not needed or replayed:
the analytic proof just given uses exactly C and these elementary counts.
For a unique isolated P root, add an arbitrary incident edge: it cannot
make a C4 and changes no other P degree or S. The degree-one result applies.
Together with B/C, every P with at most one low root has S<=158.

## F. Four-full low-degree certificates and safe completions

The two small historical inputs fix precisely the canonical four full
roots, require all other P degrees in2..5, count exactly one or exactly two
degree-two roots using their threshold flags, and leave every such root
position and its selected directions free. No opposite restrictions occur.

At one degree-two exception the other27 nonfull roots have weights
1,4,10, giving S=107+3H. Excluding H>=17 proves S<=155. The actual input
`q6_code_degree_4_score17_low1` has1486 variables and5905 clauses. At two
degree-two exceptions the other26 nonfull roots give S=106+3H. Excluding
H>=18 proves S<=157; `q6_code_degree_4_score18_low2` has1612 variables and
6132 clauses. Their fresh strict direct full-scan RUP replays have2618 and
2801 additions. The suffixes low1/low2 mean counts of degree-two roots,
not a degree-one root.

These lemmas extend to original exceptional degrees0/1 as follows. A
replacement of the whole star at u by a pair is safe unless both remote
edges of that square are present. If no pair is safe, translate u=0:
all30 singleton/two-subset edges are retained and the triple downward
capacity gives sum ts<=20. The four-code geometry in A provides at least
two full two-subsets, each with ts4. With only one low root, every other
two-subset has ts>=1, giving sum ts>=2*4+13=21, impossible. Thus a unique
low root can always be completed safely to degree two, preserving S,c and
all other P degrees.

With two low roots u,v, if u has no safe pair then v must itself be a
two-subset, or the same lower bound21 applies. Its two downward edges are
forced and its low degree makes its star exactly that pair D. There must
be a safe pair E at v different from D: if every pair except D were
blocked, for each k outside D={i,j}, the blockages of{j,k} and{i,k} at v,
together with the30 forced edges around u, retain the square

    {i,k}, {k}, {j,k}, {i,j,k}.

This is impossible. Simultaneously replace the stars at u by D and at v by
such E. The only new u-square would have v as opposite root, but E!=D
omits a required v-edge. The only new v-square uses E and has opposite
root different from u; its remote edges are unchanged, and E was safe.
All other squares are unchanged. Both exceptional roots now have degree
two, with S,c and all other P degrees unchanged.

If an initially0/1 low root does have a safe pair, replace it alone and
repeat for the other low root if necessary. The argument applies after
each step to the same full code. Hence both low roots can always be
completed, one at a time or simultaneously, and the two certificate bounds
apply at their intended unrestricted opposite-side scope.

## G. Weighted tables and the universal gate

At exactly one low root, S==31+c modulo3. By E, S<=158, improved to155
at c4 by F. The resulting S bounds are(157,158,156,157,155), so2S+c is
at most(314,317,314,317,314). For L0 use D. Thus L<=1 implies2S+c<=317.

At exactly two low roots, S==30+c modulo3. Using S<=160 and c<=4,
improved to S<=157 at c4 by F, gives S bounds(159,160,158,159,157),
weighted bounds(318,321,318,321,318). Thus L<=2 implies2S+c<=321.

For L3, S==29+c modulo3 and S<=160 gives weighted bounds
(316,319,322,319,322), all<=322. For L>=4, the elementary bound2S+c<=324
suffices. The four cases give respectively

    4S+2c <=632,634,642,644        for L=0,1,2,3,

all at most632+5L. At L>=4, 4S+2c<=648<=632+5L. This proves(G) on
every specified parity, including arbitrary degrees0/1/2 on either side.

The caller may therefore sum this same one-sided theorem on the112 actual
coordinate Q6 faces induced from one fixed global parity. No result about
global687/688 graphs, no exact edge count on a restricted face, and no
opposite minimum degree is needed. That closes these imported local
premises only; it supplies no exclusion of the caller's remaining Q8
profiles and no proof of682.
