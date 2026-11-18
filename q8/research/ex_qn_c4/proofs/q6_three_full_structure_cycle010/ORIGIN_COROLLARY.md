# Refinement when the missing fourth full root is not low

This is a separate corollary suggested by Root after `PROOF.md` was frozen. Its premise and 23 slots are exactly those of that proof. In the symmetric coordinates of Section 2, let o=empty be the missing fourth full root; in the original {0,15,51} coordinates it is vertex 60. The same coordinate transformation is applied to the entire graph.

If d(o)>=3, then

    H <=22,       S+L<=155.

Indeed, in the slot count now include the actual star at o even if it has degree three. For its block direction counts (rA,rB,rC), its actual number of occupied slots is

    q(o) = |{D : rD=2}| + rA*rB*rC.

Its contribution to H is h(o)=0,1,3 at degrees 3,4,5 respectively. These are the only possible degrees under the premise and exactly-three-full hypothesis. The complete list up to block permutation is

| d(o) | Block direction counts | q(o) | h(o) | Excess q(o)-h(o) |
|---:|---|---:|---:|---:|
| 3 | 210 | 1 | 0 | 1 |
| 3 | 111 | 1 | 0 | 1 |
| 4 | 220 | 2 | 1 | 1 |
| 4 | 211 | 3 | 1 | 2 |
| 5 | 221 | 6 | 3 | 3 |

All other high stars retain their coverage of at least their H contribution. The 23 actual slots still have capacity one, so

    H + q(o)-h(o) <=23.

Consequently the displayed excess yields respectively S+L<=155,155,155,152,149. In particular the uniform d(o)>=3 bound follows. There is no double counting problem: multiple slots occupied by the same star are deliberately separate capacities; different stars cannot share any one slot.

Degree at most two is not included in that corollary. The original S+L<=158 remains valid there. This refinement does not assert that the missing-fourth-root vertex must have any particular degree, or that any listed upper bound is attained. `check_origin.py` checks all 41 direction masks of degrees three, four and five directly; it performs no new graph search.
