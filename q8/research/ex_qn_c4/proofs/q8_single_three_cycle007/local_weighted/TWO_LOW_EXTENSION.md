# Completing two low stars and a weighted bound of 321

Cycle007, 2026-11-07. Author: /root/audit_asymptotic.
Complete candidate delta to the separately frozen one-low PROOF.md.
Independent review is still required. No sharpness claim is made.

## Statement and import

Let G be C4-free in Q6. Fix a parity P with at most two vertices of
degree below three; all other P vertices have degree at least three.
The opposite parity is unrestricted. With S and c defined as in PROOF.md,

    2S+c <=321.                                           (A)

If there are exactly two low vertices and c=4, the stronger S<=157 holds.

The one-low case is covered by the new bound 317 in PROOF.md; the
no-low case by the accepted historical bound 316. For exactly two
low vertices we use the following existing result:

> Four full P vertices and exactly two degree-two P vertices, with every
> other P degree at least three, imply S<=157. The opposite parity is
> unrestricted, and the two low positions and their directions are arbitrary.

This is Section 2 of the read-only source REFINEMENT_K3.md. The actual
historical input is results/q6_code_degree_4_score18_low2.cnf, with its
corresponding .drat. The suffix low2 means two degree-two exceptions.
The same canonical full-code argument as in PROOF.md covers every
four-full configuration.

The input fixes the four full roots, requires all other P degrees in
2,...,5 and exactly two of them to equal two, and imposes no opposite
degree restriction. For the other 26 nonfull P roots let H use weights
0,1,3 at degrees 3,4,5. Then S=80+26+3H=106+3H. Excluding H>=18 gives
S<=157. The 1612-variable, 6132-clause input has been reconstructed in
this task and its trace strictly replayed to the empty clause after
2801 additions; see TWO_LOW_CHECK.json.

## 1. The only obstruction to replacing one low star

Suppose c=4 and the two low vertices are u,v. Keep all other stars fixed.
As in PROOF.md, replacing the whole star at a low vertex u by directions
i,j is safe exactly when the opposite two edges of that root square
are not both present.

If no safe pair exists at u, translate u to zero. All thirty layer-one
to layer-two edges are retained. Every layer-three vertex can have at
most one retained downward edge, giving

    sum_{|s|=2} t_s <=20.

The full-code geometry in PROOF.md supplies at least two full layer-two
vertices, each with t_s=4. If v were not in layer two, all fifteen
layer-two vertices would be ordinary, and the lower bound would be
2*4+13=21, a contradiction. Thus v is in layer two. Its two downward
edges are forced; as a low vertex, it has degree exactly two and no
other retained edge.

Write D={i,j} for the two differing coordinates of u,v. The retained
directions at v are exactly D. This conclusion concerns the same
actual labeled graph; no independent normalizations are used.

## 2. A safe simultaneous replacement

Continue in the situation of Section 1: all thirty remote edges around
u=0 are present, v=e_i+e_j, and v has degree two in directions D={i,j}.
There is a safe pair E at v distinct from D.

Indeed, otherwise every pair except D would be blocked at v. Pick any
k outside D. The pair {j,k} at v has opposite P root e_i+e_k, so its
blockage would force that root's edges to e_i and e_i+e_j+e_k.
The pair {i,k} would similarly force the edges from e_j+e_k to e_j and
e_i+e_j+e_k. The thirty remote edges around u already force both of
these P roots to be adjacent to e_k. The four vertices

    e_i+e_k,  e_k,  e_j+e_k,  e_i+e_j+e_k

would form a retained square, a contradiction.

Choose a safe E distinct from D. Replace the stars at u and v
simultaneously by D and E, respectively, leaving every other edge
unchanged. The resulting graph is C4-free:

* A new square at u must use D and have v as its opposite P root.
  Since v's final two directions E differ from D, it lacks at least
  one of that square's required edges.
* A new square at v must use E. Since E differs from D, its opposite
  P root is not u. Its two remote edges are therefore unchanged from
  the original graph. They do not both occur, because E was safe.
* Every square avoiding u and v is unchanged.

Both low vertices now have degree two. No other P degree changes, and
the changes on the opposite parity are allowed. Both S and c are preserved.

## 3. Completing both low stars

If both low degrees are already two, no change is needed. Otherwise
choose one low root of degree zero or one. If a safe pair exists,
replace its star to give degree two. If not, Sections 1--2 complete
both low stars at once.

After a safe single replacement, apply the same argument to the other
root if its degree is below two. The four full roots and all ordinary
P degrees are still unchanged. Thus at most two such steps give a
C4-free graph with exactly two degree-two P vertices and all other
P degrees unchanged. Its S and c equal those of the original graph.

The historical four-full/two-two import applies to this graph.
Consequently every graph with exactly two low vertices and c=4 has S<=157,
even when the original exceptional degrees were zero or one.

## 4. The weighted inequality

For exactly two low vertices, the other thirty P vertices have degrees
3,4,5,6. Therefore

    S == 30+c (mod 3).

Star injection gives S<=160, and c<=4 by the elementary full-code
distance bound in PROOF.md. For c=4, Section 3 improves this to S<=157.
The largest permitted values are:

| c | bound on S | bound on 2S+c |
|---:|---:|---:|
| 0 | 159 | 318 |
| 1 | 160 | 321 |
| 2 | 158 | 318 |
| 3 | 159 | 321 |
| 4 | 157 | 318 |

This proves (A), including the no-low and one-low cases by their
separate bounds. The existing stronger historical bound with three
full roots and two degree-two vertices is not needed for (A), and
is not silently extended to other exceptional degrees here.

## Exact checks and scope

check_two_low.py reconstructs and strictly replays only the small
four-full/two-two historical input. It also checks the two local square
patterns and every final pair E in the simultaneous replacement with
explicit cube vertices, and recomputes the integer table.

These finite checks support the displayed local steps. The written
argument is responsible for the actual-domain coverage, the existence
of a safe replacement, and the unchanged specified-side degrees.
No new solver search, full Q6 graph enumeration, or sharpness assertion
is part of this delta.
