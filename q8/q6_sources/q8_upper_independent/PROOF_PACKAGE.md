# Independent proof project: $\operatorname{ex}(Q_8,C_4)=682$

## Claim and status

Original goal: **证明ex(Q_8,C_4)=682。可以参考本地的对于n=7情形304的上界证明，但是不要参考已有的n=8的进展。**

**NOT CURRENTLY JUSTIFIED.** The unrestricted upper bound $682$ is not proved.
The independent intermediate bound established below is $688$.
The subsequent refinement in `REFINEMENT_688.md` reduces its seven initial
parity profiles to four, using eighteen further checked finite certificates.
The next refinement in `REFINEMENT_K3.md`, using nine additional checked local
certificates, excludes K0 and K4 for a parity with two degree-four roots and
fixes the surviving K3 facet/box counts. It does not lower the global688 bound.
The continuation in [LOCAL_PAIR_RIGIDITY.md](LOCAL_PAIR_RIGIDITY.md) proves
that a minimum-degree-three Q6 with130 edges has at most one degree-six
vertex on either parity. Eleven more local inputs have independently rebuilt
and RUP-checked certificates. The branch now has44 such certificates and
6519933 verified additions. The global upper bound remains688.
The user-supplied lower bound is $682$. This file develops new arguments from
the allowed seven-dimensional material and does not consult old Q8 research.

## Assumptions and source boundary

The allowed theorem is that every $C_4$-free edge subset of $Q_7$ has at most
$304$ edges. Its local source is
`agents/generation/results/problem_001_304/blueprint_verified.md`, with the
Chinese expansion `proof_zh.md`. The proof below restates and derives the
star-counting facts it needs. No old Q8 upper-bound lemma is imported.

Graphs retain all cube vertices, including isolated ones. Vertices of $Q_n$
are binary vectors of length $n$ and coordinate faces fix some coordinates.
The two parity classes are denoted $P$ and $Q$.

## Dependency map

1. Full-star counting is proved directly from the prohibition of squares.
2. The degree-seven exclusion for a $304$-edge $Q_7$ follows from full stars,
   a nonnegative degree penalty, and congruences on six-dimensional faces.
3. A proposed weighted $Q_7$ inequality would imply the desired $Q_8$ upper
   bound by face summation. **That weighted inequality remains unproved.**
4. Computational searches are recorded separately. Neither a search failing
   to find an example nor a solver status `UNKNOWN` establishes a lemma.
5. A new six-dimensional star bound is supported by six independently rebuilt
   CNFs and sequential RUP-checked contradiction traces; its face sum proves
   the intermediate unrestricted $Q_8$ bound $688$.

## Lemma 1: full three-stars

In a $C_4$-free cube graph, each coordinate three-dimensional face contains
at most one full three-star rooted in a specified parity. Indeed, two distinct
vertices of that parity in $Q_3$ have Hamming distance two. If both have all
three incident face edges, their common square has all four edges.

Consequently, for a parity class $P$,

$$S_P(G):=\sum_{v\in P}\binom{d(v)}3\leq\binom n3 2^{n-3}.$$

There are $560$ coordinate $Q_3$ faces in $Q_7$ and $160$ in $Q_6$.
Define a parity hole to be a $Q_3$ containing no full star of that parity.
Then $h_P(G)=560-S_P(G)$ in dimension seven. For the fourteen $Q_6$ facets,

$$\sum_H h_P(G[H])=4h_P(G),$$

because every $Q_3$ lies in four $Q_6$ facets. Here parity in a facet always
means the restriction of the same global parity, not a newly relabelled one.

## Lemma 2: a $304$-edge $Q_7$ has no degree-seven vertex

Assume $G\subseteq Q_7$ is $C_4$-free, $|E(G)|=304$, and $v$ has degree seven.
Let $P$ be the parity containing $v$. It has $64$ vertices and degree sum
$304$. Put

$$B(d)=\binom d3-6d+20.$$

Its values for $d=0,\ldots,7$ are

$$20,14,8,3,0,0,4,13.$$

All are nonnegative, and Lemma 1 gives

$$\sum_{u\in P}B(d(u))\leq560-6\cdot304+20\cdot64=16.$$

The vertex $v$ consumes $13$ units. Thus all other vertices of $P$ have degree
four or five, except possibly one vertex $w$ of degree three. There is no
degree zero, one, two, six, or additional degree-seven vertex on $P$.

**Case A: there is no $w$.** Then

$$S_P(G)=6\cdot304-20\cdot64+13=557,\qquad h_P(G)=3.$$

In any $Q_6$ facet containing $v$, its local degree is six. The other $31$
vertices on $P$ have local degrees three, four, or five. Since
$\binom d3\equiv1\pmod3$ for $d=3,4,5$ and
$\binom63\equiv2\pmod3$, the facet star sum is $0\pmod3$.
Its hole count $160-S_P(G[H])$ is therefore $1\pmod3$, hence at least one.

In any facet not containing $v$, all $32$ local $P$-degrees are three, four,
or five. Its star sum is $32\equiv2\pmod3$, so its hole count is
$2\pmod3$, hence at least two. There are seven facets of each type. Thus

$$\sum_H h_P(G[H])\geq7+14=21,$$

whereas Lemma 1 gives that sum as $4h_P(G)=12$, a contradiction.

**Case B: there is one degree-three vertex $w$.** Now

$$S_P(G)=557+3=560,\qquad h_P(G)=0.$$

Choose a coordinate on which $v$ and $w$ differ, and fix that coordinate to
its value at $v$. The resulting $Q_6$ facet contains $v$ and excludes $w$.
Its local parity degrees are one six and $31$ values in $\{3,4,5\}$.
The congruence calculation above makes its hole count $1\pmod3$, hence
positive. But $h_P(G)=0$ forces every facet hole count to vanish. This is
again a contradiction. Therefore $\Delta(G)\leq6$. $\square$

This is a derived structural statement about the allowed Q7 problem; it
is not a classification of all $304$-edge graphs and does not exclude degree
six.

## Lemma 3: six-dimensional parity minimum degree three gives $S\leq158$

Let $H\subseteq Q_6$ be $C_4$-free. Suppose every vertex of one specified
parity $P$ has degree at least three. There is no restriction on the other
parity. Then

$$\boxed{\sum_{v\in P}\binom{d_H(v)}3\leq158.}$$

This lemma is computer-assisted. The finite reduction and exact certificate
scope are as follows.

**Step A: all potentially violating degree patterns reduce to six cases.**
Lemma 1 bounds the sum by $160$, so only $159$ and $160$ need exclusion.
Let $c$ count the degree-six vertices of $P$, and let $b$ count its
degree-three vertices. On degrees three through six,

$$\binom d3=6d-20+3\mathbf1_{\{d=3\}}+4\mathbf1_{\{d=6\}}.$$

There are $32$ vertices on $P$ and their degree sum is $e(H)$, hence

$$S=6e(H)-640+3b+4c.$$

Two degree-six vertices in $P$ cannot have distance two: their full stars
would include all edges of their common square. Thus the degree-six vertices
form a binary code of length six with pairwise distances at least four.
There cannot be five such vertices. For any five, the total of the ten
pairwise distances would be at least $40$, but each coordinate contributes
at most $\lfloor25/4\rfloor=6$, giving total at most $36$. Thus $c\leq4$.

If $S=160$, reduction modulo three gives $c\equiv2\pmod3$, so $c=2$.
Translate one such vertex to $0$ and permute coordinates. The second can
be fixed at $15$ or $63$, according as the distance is four or six. These
give the first two CNFs.

If $S=159$, then $c\equiv1\pmod3$, so $c=1$ or $4$.
When $c=1$, fix the degree-six root at $0$. There is exactly one parity hole.
It cannot contain $0$. Under coordinate permutations fixing the root, holes
fall into three orbits: distance one, two, or three from the root. Fix their
free-coordinate mask at $7$ and external base at $8,24,$ or $56$ respectively.
Their orbit sizes are $60,60,20$, covering all $140$ three-faces not containing
the root. These are the next three CNFs.

For $c=4$, the pairwise-distance bound is tight: six pairs each have distance
four, and each coordinate splits the four vertices as two zeros and two ones.
After translating one to $0$, the zero-coordinate pairs of the other three
vertices partition the six coordinates. Thus the root set is equivalent to
$\{0,15,51,60\}$. The position of the sole hole is unrestricted in the last
CNF.

**Step B: the finite encodings cover exactly the needed counterexamples.**
Use one Boolean variable for each of the $192$ cube edges. For every square,
the disjunction of its four negative edge literals forbids a four-cycle.
There are $240$ squares. For each nonfull root in $P$, the fifteen positive
four-subset clauses impose degree at least three, and the one negative
six-subset clause imposes degree at most five. At a prescribed degree-six
root, all six incident edges are fixed present.

For each three-face and each of its four $P$-vertices use a star variable
$y$, defined by $y\leftrightarrow(e_1\wedge e_2\wedge e_3)$. This is encoded
by $\neg y\vee e_i$ for each $i$ and
$y\vee\neg e_1\vee\neg e_2\vee\neg e_3$. This uses $640$ star variables.
The four stars in a three-face cannot coexist in pairs by Lemma 1.

For $S=160$, require at least one star in each face. For a prescribed sole
hole, fix its four stars absent and require a star in every other face.
For the four-root case, introduce one hole indicator per face, equivalent
to all four stars being absent, and require exactly one of the $160$ holes.
The latter uses a positive disjunction and a sequential at-most-one counter.

For counter inputs $h_0,\ldots,h_{159}$, auxiliary $q_i$ represents the
disjunction of $h_0,\ldots,h_i$, for $i=0,\ldots,158$. The clauses are
$\neg h_0\vee q_0$; for $1\leq i\leq158$, the three clauses
$\neg h_i\vee q_i$, $\neg q_{i-1}\vee q_i$,
$\neg h_i\vee\neg q_{i-1}$; and $\neg h_{159}\vee\neg q_{158}$.
Assignments with at most one true input extend by the stated prefix
interpretation. If two inputs are true, the earlier one forces the prefix
before the later one, contradicting its exclusion clause. Thus the encoding
neither loses nor invents counterexamples.

**Step C: checked contradictions.** The six CNFs and their traces are in
`results/`, with prefixes

- `q6_fullstar_d4`, `q6_fullstar_d6`;
- `q6_one_hole_b8`, `q6_one_hole_b24`, `q6_one_hole_b56`;
- `q6_star159_c4`.

Every trace ends in an independently checked empty clause. The checker
`check_rup.cpp` uses unit propagation on the original clauses and strictly
earlier verified consequences, retains valid consequences after deletions,
and never calls a SAT solver. Every new clause $C$ is accepted only if
assuming all literals of $C$ false causes a propagation contradiction.
Induction therefore proves every accepted clause from the input; accepting
the empty clause proves input unsatisfiability. RAT-only additions would be
rejected rather than silently trusted.

The six traces contain respectively $3337,75440,60247,30488,58600,28291$
checked additions, totaling $256403$. `audit_star_cases.py` independently
reconstructs every CNF as a clause multiset, without importing the generator
or its cube geometry. The RUP implementation was compared with a separate
naive propagator on $300$ random cases, including valid prefixes, with $190$
positive and $110$ negative results. The exact inputs, traces, SHA-256 values,
and successful replays are recorded in
`results/q6_star158_certificate_manifest.json`.

The complete six-case cover and checked contradictions exclude both $S=159$
and $S=160$. Hence $S\leq158$. $\square$

## Lemma 4: an unconditional extension with a low-degree charge

For an arbitrary $C_4$-free $Q_6$ graph and a specified parity, let $L$ be
the number of its vertices of degree at most two. Then

$$S\leq158+2L.$$

If $L=0$, Lemma 3 applies. If $L\geq1$, the right side is at least $160$,
and Lemma 1 gives $S\leq160$. This proves the statement for every degree
sequence, without restrictions on the opposite parity. $\square$

## Intermediate theorem: the unrestricted $Q_8$ bound is at most $688$

Let $G\subseteq Q_8$ be any $C_4$-free graph, and fix one parity $P$.
It has $128$ vertices, with degree sum $m=e(G)$. Put

$$B_8(d)=\binom d3-10d+40.$$

For $d=0,\ldots,8$ its values are

$$40,30,20,11,4,0,0,5,16.$$

There are $\binom86 2^2=112$ coordinate $Q_6$ faces. A full three-star
of $G$ lies in $\binom53=10$ of them. Each vertex lies in $\binom82=28$
of them. A degree-$d$ vertex has local degree at most two in exactly

$$\ell(d)=(28,28,28,18,6,0,0,0,0)_d$$

such faces: a face drops two coordinates, and its local degree is $d$ minus
the number of selected directions dropped. For $d=3$ the number is
$28-\binom52=18$, and for $d=4$ it is $\binom42=6$; the remaining cases
follow directly from dropping at most two directions.

Apply Lemma 4 on the restriction of the same parity $P$ to each $Q_6$ face.
Then

$$10S_P(G)\leq112\cdot158+2\sum_{v\in P}\ell(d(v)).$$

Since $S_P(G)=10m-5120+\sum_{v\in P}B_8(d(v))$, rearrangement yields

$$\boxed{100m+\sum_{v\in P}w(d(v))\leq68896,}$$

where

$$w(d)=10B_8(d)-2\ell(d)
       =(344,244,144,74,28,0,0,50,160)_d.$$

All entries are nonnegative. Therefore

$$m\leq\lfloor68896/100\rfloor=688.$$

This covers all cube edge subsets with no $C_4$, including graphs with low
degrees, degree-eight vertices, empty faces, and even face-edge counts. It
does not assume any unproved purity or odd-square property. $\square$

For a hypothetical $688$-edge graph, each parity has total $w$-penalty at
most $96$. Consequently all global degrees lie in $\{3,4,5,6,7\}$; on
each parity the exceptional-degree counts $(N_3,N_4,N_7)$ must be one of

$$\boxed{(0,j,0)\ (0\leq j\leq3),\quad(1,0,0),\quad(0,j,1)\ (0\leq j\leq1).}$$

These are the seven initial marginal profiles, not proved graph realizations.
The continuation `REFINEMENT_688.md` eliminates three of them and gives
additional saturation constraints on the four remaining types. Eliminating
the remaining $688$ families, followed by $687$ through $683$, remains part
of the full original task.

## Conditional reduction: a weighted $Q_7$ theorem would suffice

Consider the proposed inequality

$$\tag{W7}
2e(H)+\#\{v\in V(H):d_H(v)\geq6\}\leq608
$$

for **every** $C_4$-free $H\subseteq Q_7$. No minimum degree restriction is
allowed in (W7). The inequality is currently a conjectured sufficient lemma.

Assume (W7) temporarily, and let $G\subseteq Q_8$ be $C_4$-free with $m$ edges.
Sum (W7) over its sixteen $Q_7$ facets. Every edge occurs in seven facets.
A vertex $v$ of global degree $d$ belongs to eight facets: in $d$ of them
its degree is $d-1$, and in the other $8-d$ it is $d$. Its contribution to
the high-degree term is

$$t(d)=d\,\mathbf1_{\{d-1\geq6\}}+(8-d)\,\mathbf1_{\{d\geq6\}}.$$

For $d=0,\ldots,8$, the values of $t(d)$ are

$$0,0,0,0,0,0,2,8,8.$$

Each satisfies $t(d)\geq2d-10$. Therefore

$$9728=16\cdot608\geq14m+\sum_vt(d(v))
\geq14m+2\sum_vd(v)-10\cdot256=18m-2560.$$

It follows that

$$m\leq\left\lfloor\frac{12288}{18}\right\rfloor=682.$$

This reduction covers all degree sequences, including isolated vertices and
degree-eight vertices. It would prove the full upper bound if (W7) were
established. The ordinary $Q_7$ bound $e(H)\leq304$ alone does **not** imply
(W7): its additional degree term is the unresolved stability assertion.

## Testing an overstrong intermediate idea

For a $C_4$-free $Q_6$ graph with all degrees in $\{3,4,5\}$, put
$D=N_0-N_{2,\mathrm{opposite}}$. Square/adjacent-pair counting gives

$$\sum_vd(v)^2=12m-480+2D.$$

Subtracting $7\sum_vd(v)-12\cdot64$ gives

$$2N_5=288-2m+2D,\qquad D=m+N_5-144.$$

The tempting claim that minimum degree three forces $D\leq0$ is **false**.
`results/q6_positive_defect.json` records a checked $127$-edge example with
degrees $3^{20}4^{26}5^{18}$, two empty squares, and one opposite-edge square.
Thus $D=1$. This counterexample is retained to keep that false assertion out
of later arguments.

## Completion obligations

- Prove (W7), or replace it by another fully established argument proving the
  original unrestricted upper bound. A restricted-family computation is not
  sufficient.
- Verify any new finite certificate at the scope actually used.
- Combine the upper bound with a valid $682$-edge lower-bound witness.
- Audit the full original claim before marking the goal complete.

## Main theorem (UNPROVED)

**证明ex(Q_8,C_4)=682。可以参考本地的对于n=7情形304的上界证明，但是不要参考已有的n=8的进展。**

Proof status: the weighted reduction above has an unproved premise (W7).
The independently established intermediate upper bound is $688$. This file
is a research package, not a completed proof of the main theorem.
