# A low-hole Q7 facet must put its missing full-code point at a low root

Root, cycle010. This is an actual-geometry consequence of the new Q6
three-full proof and ORIGIN_COROLLARY.md in
../q6_three_full_structure_cycle010/. Acceptance requires their separate
independent review; this note introduces no numerical search or new
unrestricted extremal bound.

Let G be a C4-free spanning subgraph of Q7 of minimum degree at least three.
Fix a parity P and an actual Q6 coordinate facet F. Suppose F has exactly
three full vertices f1,f2,f3 on its induced specified parity. Define

    r_F = f1 xor f2 xor f3,
    a_F = number of specified vertices of local degree two,
    h_F = 160 - sum_{v in P intersect F} binomial(d_F(v),3).

The XOR uses the common global binary coordinates. The fixed coordinate
of F has the same bit at all three vertices, so r_F is in F. Its parity
equals their parity. Under a coordinate permutation XOR commutes with the
permutation; under a translation by t, XOR of three translated vertices
is the original XOR translated by t. Thus r_F is the distinguished missing
fourth full-code point in the simultaneous Q6 normalization. In canonical
coordinates it is0 xor15 xor51=60, or0 after the final translation by60.
It is different from all three full vertices. It is not asserted to be full.

Every vertex of F loses at most one edge from G, so it has degree at least
two. Consequently the local count L in the new theorem equals a_F exactly.
The general three-full bound and its origin refinement give

    h_F >= 2+a_F+3*1_{d_F(r_F)>=3}.                       (1)

In particular, if h_F<5+a_F, then d_F(r_F)=2. Its global degree is at least
three and at most its local degree plus one, so its global degree is exactly
three and its edge in the omitted coordinate is retained.

This is a constraint on the same three actual full vertices, their actual
XOR point and an actual retained edge of G. It cannot be represented merely
by freely assigning each face an independent low-root label. If G has only
one specified-side degree-three vertex x, every facet satisfying the strict
hole premise must have r_F=x and must omit a retained direction at x.
If there are two such vertices, r_F must be one of those two actual vertices.

For the current210-profile Q7 cover there are at most two global degree-three
vertices in total, so a_F is0,1 or2. When a_F=0, the older specified-minimum-
three import h_F>=8 is stronger than (1). For a_F=1 the old low value h_F=3
requires r_F low, while r_F nonlow forces h_F>=6. For a_F=2, h_F=4 requires
r_F low, while r_F nonlow forces h_F>=7. The low values also follow from the
existing congruence h_F+c_F-a_F=2 mod3 with c_F=3.

Every global degree-three root is locally degree two in exactly the three
containing facets that omit a retained direction. These incidences were
already counted in the scalar sum_a=3b. The NEW content is the identity of
that root with the XOR of the three full vertices, not an extra independent
budget that could be added a second time. No current profile is removed by
this note and no common edge completion is supplied.

The next finite obligation is to consume (1) together with the actual common
full-root sets and retained directions of the current Q7 profiles. Repeating
the scalar14-facet DP without those positions would miss precisely this
new information. The whole-minimum-three premise remains separate from
the unresolved low-degree Q8 rows and is not applied to them implicitly.
