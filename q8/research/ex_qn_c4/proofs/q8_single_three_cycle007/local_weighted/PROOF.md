# A weighted bound for a Q6 parity with at most one low vertex

Cycle007, 2026-11-07. Author: /root/audit_asymptotic.
Complete analytic argument with an explicitly reconstructed and strictly
replayed historical local import. Independent review is requested
separately. No optimality claim for the constant 317 is made.

## Exact statement

Let G be a C4-free subgraph of Q6, and P one of its parity classes.
Suppose at most one vertex of P has degree below three; every other
vertex of P has degree at least three. The opposite parity is unrestricted.
Set

    S = sum_{v in P} binom(d(v),3),
    c = #{v in P : d(v)=6}.

Then

    2S+c <=317.                                           (1)

When there is no low vertex the accepted historical bound is already
2S+c<=316. With exactly one low vertex, of degree zero, one, or two,
the following more detailed bounds hold:

| c | bound on S | bound on 2S+c |
|---:|---:|---:|
| 0 | 157 | 314 |
| 1 | 158 | 317 |
| 2 | 156 | 314 |
| 3 | 157 | 317 |
| 4 | 155 | 314 |

These are proved upper bounds, not assertions that every row is attainable.

## Accepted inputs and their exact scopes

1. The one-low theorem established in cycle006 says S<=158 under the
   present hypothesis. The minimum-three and unique-degree-two cases are
   historical imports; the degree-one case is the new analytic theorem
   in ../../low1_cycle006/analytic/PROOF.md, independently accepted in its
   review/REVIEW.md. The degree-zero case follows by adding one harmless
   edge, as recorded in ../../low1_cycle006/Q8_BRIDGE.md.
2. If every P vertex has degree at least three, the historical bound is
   2S+c<=316. Its exact scope is REFINEMENT_688.md, Section 2, in the
   read-only source directory identified below.
3. **Historical four-full/one-two bound:** if c=4, exactly one P vertex has
   degree two, and every other P vertex has degree at least three, then
   S<=155. No opposite-side restriction is present.

The third result is stated in Section 2 of
q6_sources/q8_upper_independent/REFINEMENT_K3.md.
Its actual input and proof are results/q6_code_degree_4_score17_low1.cnf
and the corresponding .drat in that source directory. The suffix low1
means one degree-two exception; it does not mean a degree-one root.

The producer and independent input reconstruction were read for this
task. Four full roots are fixed at 0,15,51,60. All nonfull P vertices
have degrees between two and five, with exactly one having degree two;
its position and its selected directions remain arbitrary. The opposite
parity has no degree conditions. At the 27 ordinary nonfull P vertices,
let H be the sum of weights 0,1,3 for degrees 3,4,5. Then

    S = 4*20 + 27 + 3H = 107+3H.

The 1486-variable, 5905-clause input excludes H>=17, equivalently S>=158
in this residue class. Thus H<=16 gives S<=155. Section 1 below explains
why the canonical full code covers every actual four-full configuration.

This task actually reconstructed that complete historical CNF and reran
the strict direct RUP checker on this one small trace. It reached the
empty clause after 2618 verified additions. IMPORT_CHECK.json records the
input/proof/checker hashes and the real replay output. No old solver
status or cached-checker acceptance is being used in place of this replay.
The other accepted import families were not rerun.

## 1. Four full vertices and every possible exceptional-root position

Two full vertices of the same parity cannot be at distance two: their
two common neighbors would give a C4. Five full vertices would have total
pairwise distance at least 4*C(5,2)=40, while each of six coordinates
contributes at most 6 to that distance sum. Hence c<=4.

Among three or more full vertices no pair can have distance six. After
translating one endpoint to zero, a third vertex would need weight at
least four and at most two. Therefore all pairwise distances in a
four-full code are four.

Translate one full vertex to zero. The next two weight-four supports
have intersection of size two, so a common coordinate permutation makes
them A union B and A union C, where A,B,C partition the six coordinates
into three pairs. A fourth support X has size four and intersects each
of A union B and A union C in two. Writing its three intersection sizes
as x_A,x_B,x_C gives

    x_A+x_B = x_A+x_C = 2,  x_A+x_B+x_C = 4.

Consequently x_A=0 and x_B=x_C=2. Thus the full code is exactly

    C = {empty, A union B, A union C, B union C}.             (2)

This is the canonical code {0,15,51,60}, after one simultaneous cube
isometry. No exceptional-root marking is independently normalized.

Every even vertex u outside this code has at least two code vertices
at distance two. To see this, count the selected coordinates of u in
each of the pairs A,B,C. Because u is even, either no pair or exactly
two pairs have a single selected coordinate.

* If no pair is split, u is a union of complete pairs. Being outside (2),
  it selects an odd number of the three pairs. Toggling any one entire
  pair gives one of three distinct code vertices, each at distance two.
* If two pairs are split, each contributes one disagreement from every
  code vertex. Exactly two code vertices agree with u on the remaining
  complete pair, so those two vertices are at distance two.

This covers all possible positions of u. The exact independent check
also enumerates all 120 four-element full codes in the even Q6 parity,
without taking a quotient. Each has 24 outside points at distance two
from exactly two roots, and four outside points at distance two from
exactly three roots.

## 2. Completing the unique low root to degree two when c=4

Suppose c=4 and u is the unique P vertex of degree below three.
If its degree is two the historical import applies directly.
Otherwise replace its entire incident star by two chosen directions i,j.
All other edges remain unchanged.

The replacement changes no degree on P except u. A newly created C4
would have to use u's two final edges, so the only possible new square
is the i,j square at u. It is absent if at least one of the two remote
edges from u+e_i+e_j to u+e_i,u+e_j is absent.

Assume, for a contradiction, that no two directions give a safe
replacement. Translate u to the empty subset. Every one of the 30 edges
between layers one and two is then retained. For each two-subset s,
let t_s count its retained edges to layer three. All fifteen such s
have degree at least three, so t_s>=1. Every full two-subset has t_s=4.
By Section 1 there are at least two such full two-subsets.

Each three-subset has at most one retained edge downward to a two-subset:
two downward parents share a singleton, and their two forced edges to
it would create a C4. Thus

    sum_{|s|=2} t_s <=20.

The two full two-subsets and the remaining thirteen ordinary two-subsets
instead give

    sum_{|s|=2} t_s >=2*4+13=21,

a contradiction. Therefore a safe two-edge replacement always exists.

The replacement preserves S because both the old low degree and degree
two contribute zero. It also preserves c and all 31 other P degrees.
Changes to opposite-side degrees are permitted. The replacement graph
satisfies the historical four-full/one-two theorem, proving S<=155
for every unique-low case with c=4, including original degree zero or one.
This argument does not require S to be near 160.

## 3. Congruence closes the weighted bound

If there is exactly one low vertex, its cubic contribution is zero.
The other 31 P vertices have degrees 3,4,5,6 and weights 1,4,10,20.
Hence

    S == 31+c (mod 3).

The accepted one-low theorem gives S<=158, and Section 2 improves the
c=4 case to S<=155. Taking the largest permitted integer in each residue
class yields exactly the five rows of the displayed table. Its maximum
weighted value is 317. If there is no low vertex, the separate historical
minimum-three weighted bound gives 316, which also implies (1).

This proves the theorem with its full specified-side hypothesis. It
does not transfer the minimum-three bound 316 to a graph with a low
vertex, nor does it prove that 317 is attained.

## Verification and remaining precision

Run check_import.py with PYTHONDONTWRITEBYTECODE=1. It only writes in this
directory. It reconstructs and strictly replays the one historical
certificate described above, checks all four-full-code positions, and
recomputes the five integer bounds.

A read-only scan of the 13 historical JSON files in the source results
directory that contain actual Q6 edge lists found 26 eligible parity
sides. Twenty-four have minimum degree at least three; two have a unique
degree-two vertex, with (S,c)=(142,0) and (118,0). The largest weighted
value was 316, at q6_degree_potential_2d4.json on its even parity.
WITNESS_SCAN.json records every observed side. This limited scan supplies
no single-low equality example and does not establish global sharpness.
An initial draft incorrectly described all 26 sides as minimum-three;
the full scan's assertion caught this, and the corrected rows are explicit.
No new solver search was used for this proof.

The original-Q8 caller is owned and reviewed separately by the parent.
This note delivers only the exact local theorem and its proof dependencies.
