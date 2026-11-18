# An unconditional Q6 inequality and its Q8 degree gate

Root, cycle007. Analytic deduction pending separate independent review.
This consumes both newly proved local weighted bounds in
`local_weighted/PROOF.md` and `local_weighted/TWO_LOW_EXTENSION.md`.

## 1. A dimension-local inequality without any degree hypothesis

In any C4-free Q6, fix either parity and let S be its three-star sum,
c its number of degree-six vertices and L its number of vertices with
degree at most two. Then

    4S+2c <=632+5L.                                     (1)

There is no degree restriction on either parity. To prove (1), partition
by L. At L=0 the accepted minimum-three bound gives2S+c<=316. At L=1
the new one-low bound gives2S+c<=317, and at L=2 the new two-low bound
gives2S+c<=321. These are at most316+(5/2)L in each case.

At L=3 the other29 specified-side vertices have degrees3..6, so
S is congruent to29+c modulo3. With S<=160 and c<=4, its weighted upper
bounds for c=0,...,4 are316,319,322,319,322. Thus2S+c<=322, which is
at most316+(5/2)*3. At L>=4, the elementary2S+c<=324 is already at most
316+(5/2)L. These cases cover every possible specified parity, proving(1).
The coefficient5 is a proved sufficient coefficient, not a sharpness claim.

## 2. Lift to every edge count in Q8

Let G be any C4-free Q8 with m edges, and P a specified parity. There
are112 coordinate Q6 faces; every actual Q3 star lies in ten of them.
A global degree d vertex is locally of degree at most two in

    lambda(d)=sum_{k=0}^2 binom(d,k) binom(8-d,6-k)

containing faces, and is locally full in binom(d,6) faces. The exact
lambda vector for d=0,...,8 is

    (28,28,28,18,6,0,0,0,0).

Write b(d)=binom(d,3)-10d+40. Since P has128 vertices and degree sum m,
its star sum is10m-5120+sum_P b(d). Sum half of(1) over all Q6 faces
and rearrange. The result is

    200m+sum_{v in P} w(d(v)) <=137792,                  (2)
    w(d)=20b(d)+binom(d,6)-(5/2)lambda(d)
        =(730,530,330,175,65,0,1,107,348).

This is valid for arbitrary m and uses the same actual P vertices in
every restriction. All coefficients happen to be integers; no rounding
or independently assigned facet completion is involved.

## 3. The exact gate at687 and the surviving low-degree rows

At m=687, (2) gives sum n_d*w(d)<=392 on either parity. Eliminating n5
and n6 using sum n_d=128 and sum d*n_d=687 yields

    735n0+534n1+333n2+177n3+66n4+105n7+345n8 <=345.     (3)

For example n6=47+5n0+4n1+3n2+2n3+n4-2n7-3n8, and its substitution
gives47 plus the left side of(3). All coefficients are nonnegative.
Thus the new inequality directly excludes degrees0/1, two degree-three
vertices on a parity, one degree3 with three degree4 vertices, and one
degree3 with both a degree4 and a degree7 vertex. The respective last
three prohibited costs are354,375,348, all strictly above345.

The cycle006 degree-two exclusion still supplies minimum degree three;
the present gate alone permits the pure degree-two candidate and is
not a substitute for that proof. Combined with the already established
integer histogram conditions, the four remaining low-degree rows are
exactly those in `WEIGHTED_Q8_EXCLUSION.md`.

The gate provides a unified new proof of the listed necessary restrictions
and a reusable inequality for other edge counts. It does not turn the
four remaining rows into constructions, prove minimum degree four, or
prove the universal Q7 J>=73 lemma. The unrestricted upper bound remains687.

`check_general_gate.py` recomputes every binomial coefficient, the exact
degree elimination and the literal finite histogram list. Historical
imports and the two local proofs retain their own explicit verification
scope; the algebra script is not their proof.
