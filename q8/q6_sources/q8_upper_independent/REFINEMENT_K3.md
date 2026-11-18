# Further independent refinement: a two-degree-four parity must have K=3

The target is still the unrestricted equality ex(Q8,C4)=682. It is **not
proved**. The branch's unconditional upper bound is still688. This document
uses only the allowed Q7 proof and this independent branch's own lemmas.

The preceding turn made progress through checked local search. In this turn
the new upper-bound progress is nine independently rebuilt and RUP-checked
local certificates, which exclude the K0 and K4 families of
`REFINEMENT_688.md`. The four possible marginal parity types remain the same;
there is a stronger restriction on the type with two degree-four roots.

## 1. Sharper bounds when three or four roots have degree six

On a specified Q6 parity of minimum degree three, let c count degree-six
vertices and S the full-three-star sum. The bounds are now

| c | upper bound S |
|---|---:|
| 0 |158|
| 1 |156|
| 2 |157|
| 3 |152|
| 4 |144|

The first three follow from the preceding checked S158 lemma and congruence.
For c3 and c4, full roots have mutual distance four: distance two causes a
square; a distance-six pair cannot have a third point at distance at least
four from both. Translate the first root to0. Two weight-four supports with
intersection two give the canonical triple {0,15,51}. A fourth weight-four
support must intersect each previous support in two, hence is60. This covers
all full codes of sizes three and four, using the previously established c<=4.

For each nonfull parity vertex define H_v=0,1,3 at degrees3,4,5. Then

    S=32+19c+3H,       H=sum_nonfull H_v.

Degree thresholds z4,z5 encode H_v=z4+2z5. The CNFs exclude H>=22 for c3 and
H>=13 for c4, proving S<=152 and S<=144. Both bounds are attained by separately
verified edge lists `q6_code_degree_3_score21.json` and
`q6_code_degree_4_score12.json`; no restriction is imposed on the other parity.

## 2. Three low-degree extensions

In the following cases all unspecified roots on the specified parity have
degree at least three, and the other parity is unrestricted.

* Four full roots and exactly one degree-two root cannot have S158. In fact
  S=107+3H and the certificate excludes H>=17, so S<=155.
* Four full roots and exactly two degree-two roots cannot have S160. Here
  S=106+3H and H>=18 is excluded, giving S<=157.
* Three full roots and exactly two degree-two roots cannot have S159. Here
  S=87+3H and H>=24 is excluded, giving S<=156.

The degree-two locations and their two selected directions are not fixed:
threshold flags count the exceptions over all nonfull parity vertices.
Thus the certificates cover every position and every permitted neighborhood.

There is also a geometric extension: **two degree-two roots with the same
selected coordinate pair and agreeing on those coordinates have S<=158**.
Normalize the first root to0 and selected directions to0,1. The other root
differs in two or four of the remaining four coordinates, yielding exactly
the cases w12 and w60. Their CNFs directly exclude S>=159: each of160 Q3s
has a hole flag, and at most one hole is allowed. The full-star equivalences
and C4 exclusions make the number of holes exactly160-S. Both contradiction
traces have been checked to the empty clause.

## 3. A saturated b1 seven-facet must have 303 edges

Suppose one parity P of a hypothetical688-edge Q8 graph has exactly two
degree-four roots and all its other roots have degree five or six. The
previous package proves equality in every Q7 inequality S7<=552+b, where b
is the local number of degree-three roots, and

    3M+2c+b=916.

In a b1 facet, S7=553. All14 Q6 subfacets have S<=158: they have minimum
parity degree three or a unique degree-two root. Their sums total4*553=2212,
so every one has S158. On a minimum-degree-three subfacet, 2S+c6<=316 forces
c6=0. On the three subfacets containing the unique root with local degree2,
the congruence S=31+c6 modulo3 forces c6=1 or4. Section2 excludes4. Thus
these three subfacets each have one full root, giving c=3 in the Q7 facet.
The displayed identity then gives M303.

## 4. Excluding K=0 and K=4

Let I be the directions selected at both degree-four roots on which they
agree, K=|I|. The preceding package already gives K in {0,3,4}.

If K0, exactly eight Q7 facets have b1 and eight have b0. The former have
M303 by Section3; the old saturation table makes each latter at least300.
Their total is at least8*303+8*300=4824, while every edge belongs to seven
Q7 facets and the required total is7*688=4816. Contradiction.

If K4, select a b2 Q7 facet by dropping a direction in I. Its two degree-three
roots have identical three selected coordinates and agree on them. Each Q6
subfacet either has minimum parity degree three, or has exactly two degree-two
roots with identical selected pairs and agreement there. The geometric lemma
in Section2 makes S<=158 in the latter cases as well. Thus
4S7<=14*158=2212, contradicting the required S7=554. This excludes both formerly
UNKNOWN canonical K4 cases w48 and w240 by a local argument, not by treating
those timed-out searches as proofs.

Consequently **K=3 is necessary whenever a parity has two degree-four roots**.

## 5. K3 facets and full-root boxes are almost determined

There are three b2 facets, two b1 facets, and eleven b0 facets. In a b2 facet,
exactly two Q6 subfacets contain two degree-two roots, two contain one, and
ten contain none. S7=554 forces equality in

    4S7 <=2*160+12*158=2216.

Thus the two double-low subfacets have S160 and the rest S158. On the double-low
subfacets congruence gives c6=1 or4, with4 excluded by Section2. The single-low
subfacets likewise have c6=1; the ten others c6=0. Hence c=4 and M302 in every
b2 facet. Section3 makes the two b1 facets M303.

For a b0 facet, S7=552, so the sum over its Q6 subfacets of 158-S is4. Section1
excludes three or four full roots on any of them. For local full counts0,1,2,
the least star deficits are0,2,1 respectively, and extra deficits are multiples
of three. The old c values2,5,8 therefore yield these patterns:

* M300,c8: four boxes have two full roots; none have an odd full-root count.
* M302,c5: two boxes have two full roots and one box has one full root.
* M304,c2: either one box has two full roots, or two boxes have one full root.

Count Q7 facets as vertices of a graph, with each Q6 box joining its two
containing Q7 facets. Complementary facets do not meet, so this graph has
eight parts of size two. Label each box by its number of full roots on P.
The five special facets (three b2, two b1) have all their positive labels
equal to one, forming K5 minus the edge between the b1 facets. There are
nine such odd boxes; all their full-root counts are exhausted inside the
five facets, with no positive label to a b0 facet.

The eleven b0 edge counts sum to3304. The only old-table possibilities are
one304 plus ten300, or two302 plus nine300. The first is impossible. Its sole
304 facet would have odd-box degree0 or2, while every other b0 facet has odd
degree0; a simple graph cannot have just one vertex of positive degree2.
Thus it would have no additional odd boxes. But the total box labels sum to
the number of global degree-six P roots, namely50, while nine odd labels
and all other labels even would make that sum odd.

Therefore the exact Q7 edge-count multiset is

    nine facets M300, five facets M302, two facets M303.

The two b0 facets with M302 have one odd incident box each; their common box
has label1. In total ten Q6 boxes have label1 and twenty have label2. The
twenty label2 boxes join b0 facets only. This is necessary data, not a graph
realization and not a full exclusion of K3.

## 6. Nine canonical K3 configurations

Fix u=0 with selected mask15. If the selected masks differ, they intersect
in three agreeing coordinates, and normalize the second selected mask to23.
The other root has respectively the canonical values

    96,48,240,40,232,24,120.

If the selected masks agree, their bits differ on exactly one of the four
selected axes; the other root is24 or120, selected mask15. These nine cases
cover every K3 pattern under the subgroup preserving the first root and its
selected set. `audit_k3_refinement.py` enumerates all raw patterns to verify
the normalization. `q8_688_k3_probe.py` tests the full C4 constraints and the
new forced facet/box counts. A timeout still means UNKNOWN.
All nine bounded probes have now completed with UNKNOWN after120 seconds
each. None of the nine cases is excluded by those solver runs.

## 7. Certificate scope and a refuted route

`results/k3_refinement_audit.json` independently reconstructs every new CNF,
records current SHA-256 hashes and successful RUP reports, verifies the sharp
examples, and audits the K3 arithmetic. No SAT solver or cube helper is used
by the CNF reconstruction modules.

The candidate joint inequality 4m+N3+3N6<=532 for minimum-degree-three Q6 graphs
is **FALSE**. A checked122-edge graph with degree histogram {3:28,4:26,5:4,6:6}
has left side534 and stars146 on each parity. Other counterexamples are also
retained. The reduced-coefficient candidate 4m+N3+2N6<=532, with a possible
strictness assertion when full roots exist, is not established; the attempted
branches returned UNKNOWN. Neither candidate is a premise of Sections3–6.

The full goal remains to exclude all edge counts688 through683. This turn
does not prove an unconditional bound below688.

For continuation, the saturated Q7 case M300 with eight degree-six roots
on the specified parity is a focused new local target: nine such facets
would occur in every remaining K3 graph. Its nonexistence is only a possible
sublemma, not a result. Any full proof must also cover the other688 profiles
and all edge counts down to683.
