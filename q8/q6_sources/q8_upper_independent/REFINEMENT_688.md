# Refining the hypothetical 688-edge graph (independent branch)

The target remains ex(Q8,C4)=682. No exclusion of all 688-edge graphs is
claimed here. This document continues only this branch's newly proved 688
bound and the permitted Q7 theorem.

## 1. Unique degree-two parity root: the star158 bound survives

**Lemma.** In a C4-free Q6 graph, if one specified parity has exactly one
degree-two vertex and its other 31 vertices have degrees at least three,
its full-three-star sum S is at most158. The opposite parity is unrestricted.

Translate the exceptional root to0 and permute its selected directions to
0,1. It suffices to exclude S160 and S159. The full160 case is encoded without
any maximum-five restriction on the other vertices. Its contradiction has
407926 verified additions, independently replayed with both the historical
checker and the active/history checker, with matching counts and hashes.

In the S159 case, let c count degree-six roots on the specified parity. The
star sum is congruent to31+c modulo3, so c is2 modulo3. Distinct degree-six
roots have pairwise distances at least four, so c<=4 by the length-six
pairwise-distance bound already proved in the previous package. Hence c=2.

There is exactly one starless Q3. The stabilizer of the specified root and
its two selected directions is S2 times S4, of order48. Its16 orbits on all
160 three-faces are completely enumerated in
`results/q6_low2_hole_orbit_cover.json`. Alternatively, an orbit is determined
by a=number of selected directions among its three free directions,
b=number of fixed ones among the remaining selected directions, and
c=number of fixed ones among the remaining unselected directions. The ranges
are 0<=a<=2, 0<=b<=2-a, 0<=c<=1+a. The orbit size is

    C(2,a) C(4,3-a) C(2-a,b) C(1+a,c).

These16 disjoint types have total160. Each corresponding CNF forbids C4,
fixes the root's exact degree-two neighbourhood, imposes minimum degree three
on the other specified-side roots, defines all640 star indicators, fixes
exactly the chosen one hole, and imposes the proved necessary c=2 through
full-degree indicators. The CNFs are independently rebuilt by
`rebuild_local_cnf.py`; the cardinality counters are rebuilt from the explicit
sequential-counter specification, without importing a SAT package.

All17 cases (one full160 case and16 single-hole cases) end in independently
verified empty clauses. The manifest
`results/low2_star158_certificate_manifest.json` records 4122060 verified
additions for this lemma, including all current input/proof hashes.

## 2. A weighted star inequality on minimum-degree-three parities

**Lemma.** For a C4-free Q6 graph whose specified parity has minimum degree
at least three,

    2 S + c6 <=316,

where c6 is the number of degree-six roots on that parity.

The previous six-case lemma gives S<=158; c6<=4. Also S is2+c6 modulo3,
since all32 parity roots have degrees3,4,5 or6. The respective bounds for
c6=0,1,2,4 are S<=158,156,157,156. For c6=3, the three full roots are equivalent
to {0,15,51}. They cannot have a distance-six pair: a third root would have
distance at least four from both members, which is impossible in six
coordinates. Thus all pairwise distances are four; fixing one at0 gives the
displayed unique code up to coordinate permutation.

The additional CNF `q6_roots3_star158.cnf` excludes S158 for this triple,
with 204462 checked RUP additions. The next value in the same residue class
is155. Substitution of these five bounds proves 2S+c6<=316 in all cases.

The stronger guess S+2c6<=158 is FALSE. A separately verified witness in
`results/q6_degree_potential_2d4.json` has S157 and c6=2 on the specified
minimum-degree-three side. Its weighted value for this stronger guess is161.
It instead attains equality in the proved inequality: 2*157+2=316.

## 3. Unconditional extension and the four remaining parity types

For an arbitrary Q6 parity, let A count degrees at most one and B count
degree-two roots. The two lemmas give

    2S+c6 <=316+8A+4B.                                  (1)

If A=B=0 use Section2. If A=0,B=1 use Section1 and c6<=4. In all remaining
cases either A>=1 or B>=2; the right side is at least324, while S<=160 and
c6<=4 give the same upper bound324. Thus (1) has no hidden degree hypothesis.

Now let G be a hypothetical 688-edge C4-free Q8 graph, and P either parity.
Summing (1) over112 Q6 faces gives

    200m + sum_(v in P) w2(d(v)) <=137792,
    w2 = [576,376,236,136,56,0,1,107,348].                (2)

To check the coefficients, a global degree d vertex contributes respectively

    sum local A: [28,28,13,3,0,0,0,0,0]_d,
    sum local B: [0,0,15,15,6,0,0,0,0]_d,
    sum local c6: [0,0,0,0,0,0,1,7,28]_d.

Every global star occurs in10 Q6 faces, so substituting
S_P=10m-5120+sum B8(d) in (1), with B8 from the previous package, proves (2).

The earlier seven profiles are now reduced as follows.

* A single global degree-three root would leave every other root on P with
  degree five or six. Of its28 incident Q6 faces, three reduce its degree to
  one, fifteen reduce it to two, and ten leave it at three. On all faces
  except the three degree-one faces, S<=158 by the old lemma or Section1.
  Therefore the sum of face star counts is at most112*158+6=17702. But the
  global star sum is1771, which requires a face sum17710. Contradiction.
* The profile with three global degree-four roots has51 degree-six roots.
  Its penalty in (2) is3*56+51=219, exceeding the allowance192 at m688.
* The profile with one degree-seven and one degree-four root has47
  degree-six roots. Its penalty is107+56+47=210>192.

Consequently the only remaining exceptional-degree patterns per parity are

    (N4,N7) = (0,0), (1,0), (2,0), (0,1).               (3)

There are no degree-three roots. The remaining counts are uniquely determined:

    N6=48+N4-2N7,    N5=80-2N4+N7.

These are necessary patterns, not witnessed cube graphs.

## 4. A rounded seven-dimensional inequality

**Lemma.** For a C4-free Q7 graph whose specified parity has degrees at
least three, at most two degree-three roots b, and at most one degree-seven
root f,

    S7 + f <=552+b.                                    (4)

For b=0, all Q6 parity restrictions have minimum degree at least three, so
4S7<=14*158=2212 and S7<=553. The parity of S7 is b+f modulo2. If f=0 this
gives S7<=552. If f=1, summing Section2 on the Q6 facets gives
8S7+c6+7f<=4424, hence S7<=552; its odd parity improves this to551.

For b=1, every Q6 parity either has minimum degree three or has a unique
degree-two root. Thus again S7<=553. Its parity gives S7<=553 for f0 and
S7<=552 for f1. For b=2, each degree-three root produces a local degree-two
root in three facets; at most three facets can contain two of them. Thus
4S7<=11*158+3*160=2218, so S7<=554. Its parity gives554 for f0 and553 for f1.
These exhaust b=0,1,2 and f=0,1 and prove (4).

In Q8 with (3), every Q7 restriction meets (4). Every star belongs to five
Q7 facets, each global degree-four root produces four local degree-three
roots, and each global degree-seven root produces one local degree-seven
root. Hence

    5S_P+N7 <=16*552+4N4.

At m688, S_P=1760+4N4+5N7, so this yields

    16N4+26N7<=32.                                     (5)

The surviving four types all satisfy (5), and N4=2 forces equality in all
sixteen instances of (4).

## 5. Saturation data when a parity has two degree-four roots

Assume N4=2,N7=0 on P in a hypothetical688 graph. In any Q7 facet let b be
its local count of degree-three P-roots, c its local degree-six count, and
M its edge count. All sixteen facets have

    S=552+b,    3M+2c+b=916.

Section3 on Q6 subfacets gives c<=8+4b. Together with c=2+b modulo3 and the
permitted Q7 upper bound M<=304, the possible (M,c) pairs are

    b0: (304,2),(302,5),(300,8);
    b1: (303,3),(301,6),(299,9),(297,12);
    b2: (304,1),(302,4),(300,7),(298,10),(296,13),(294,16).

Let the two global degree-four roots be u,w with selected direction sets
T(u),T(w). Let I be the directions selected at both roots on which u,w have
the same bit, and K=|I|. Facets containing two local degree-three roots are
exactly the K facets indexed by I. Within one of these facets, the number
of Q6 subfacets with two local degree-two roots is K-1. Its S7=554 requires
4*554<=14*158+2*(K-1), so K>=3 whenever K>0. Therefore

    K is one of 0,3,4.

For K4 the two selected direction sets coincide and the roots agree on
all four selected coordinates. They differ in two or four of the remaining
coordinates. These give two canonical cases after fixing u=0 and its
selected directions0,1,2,3: w=48 or w=240, with the same selected directions.

None of these remaining families has been excluded yet. The full objective
682 remains active; the intermediate upper bound is still688.

## 6. Cardinality extension and checker details

For signed inputs x1,...,xn and 0<k<n-1, the compact at-most-k counter uses
q(i,j), 1<=i<=n-k, 1<=j<=k. Its clauses are

    not x_i or q(i,1);
    not q(i,j) or q(i+1,j)                    (i<n-k);
    not x_(i+j) or not q(i,j) or q(i,j+1)      (j<k);
    not x_(i+k) or not q(i,k).

Interpret q(i,j) as at least j true inputs among the first i+j-1 inputs.
Every assignment with at most k true inputs extends by this interpretation.
Conversely the first three clause families force each such prefix threshold;
if a (k+1)st true input occurs at position p, q(p-k,k) is forced and conflicts
with the last clause at that input. Boundary counts0,n,n-1 are respectively
negative units, no clauses, and one all-negative clause. At-least-k is
at-most-(n-k) on negated inputs; exact-k uses both counters with separate
auxiliaries. This is the specification independently reconstructed here.

The active/history checker first tries propagation with original axioms and
the active verified prefix. If it fails, it tries the complete STRICTLY
EARLIER verified history, then restores only earlier propagation reasons.
The current clause is added to neither store until it has passed. Deletions
cannot invalidate previously proved consequences, so both propagation paths
are sound. The checker rejects a test that tries to use future clauses to
justify an earlier empty clause. Differential checks against naive
propagation passed300 cases, including170 positive and130 negative targets,
and a separate deleted-reason restoration test passed.
