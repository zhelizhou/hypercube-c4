# A single Q4 face does not exclude the two-low-root configuration

2026-11-07. This is a verified local counterexample to a proposed weaker
obstruction, not a Q6 counterexample and not a new search result for the
original Q8 problem. No solver was invoked in this branch.

The new Q6 obligation has two specified-parity degree-one roots at
distance two, with the same retained direction outside their difference
coordinates, all other specified-side degrees at least three, and a
putative three-star sum 160. Its full Q3 occupancy implies that every Q4
restriction has all eight Q3 faces occupied. But a Q4 containing the two
roots can satisfy that condition, even with every other specified-side
vertex of degree at least two.

## Explicit marked graph

Use Q4 bit coordinates 0,1,2,3 and the even parity. The two roots are
u=0 and v=3, with difference coordinates {0,1}. Their retained edges are
0--4 and 3--7, both in direction 2. Give the eight even vertices these
actual odd neighbors:

| Even vertex | Retained neighbors | Degree |
|---:|---|---:|
| 0 | 4 | 1 |
| 3 | 7 | 1 |
| 5 | 1,4,7,13 | 4 |
| 6 | 2,4,14 | 3 |
| 9 | 1,8,11 | 3 |
| 10 | 2,8 | 2 |
| 12 | 8,13,14 | 3 |
| 15 | 7,11,14 | 3 |

This graph has 20 edges. Its specified star sum is 4+4*1=8, and all
eight actual coordinate Q3 faces have exactly one specified-side star.
The 24 coordinate square edge-count histogram is

    {0:1, 1:1, 2:7, 3:15}.

Thus there is no retained C4. Every ordinary specified-side vertex has
degree at least two, stronger than the degree-at-least-one requirement
obtained by restricting a degree-at-least-three Q6 vertex to Q4.

Deleting 0--4 and 3--7 gives the analogous two-degree-zero-root Q4
restriction, still with all eight stars and still C4-free. Hence the
isolated Q4 necessary conditions are feasible both when the common
retained direction belongs to the Q4 and when it does not.

## What this does and does not resolve

The final Q6 problem still requires all these Q4 restrictions to come
from the same actual 192-edge cube graph, with the two additional
directions and every ordinary specified-side degree consistently
completed. This artifact supplies no such completion. It specifically
prevents the invalid inference that one Q4 with two parallel degree-one
roots must already contain a starless Q3. Any analytic exclusion through
Q4s must use their overlap or additional global constraints.

The parent owns the separate complete-domain Q6 CNF and its proof
replay. Its status is not inferred from this local example, and this
branch does not restart or extend it.

## Actual checks and files

`check_q4_witness.py` constructs the literal edge set and checks every
square and every Q3 face. It exited zero and saved `Q4_WITNESS.json` and
`check_q4_witness.stdout.txt`. Its edge list is `q4_witness.edges`.

The existing independent generic checker was also run:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 /mnt/c/Users/Anony/Desktop/project/research/ex_qn_c4/src/verify_edges.py 4 q4_witness.edges generic_verification.json
```

It exited zero, agreeing on all 24 squares and independently reporting
zero C4s by common-neighbor counting. `generic_verification.json` binds
the edge file with SHA256
`32e4849646f6873650f5cbf57d0c94b29813a67d29eeb327e1c9db0d52b77b7c`.

The constructive result is fully verified in its Q4 scope. The attempted
pure analytic Q6 exclusion did not close in this subtask. No extrapolation
from this example to a Q6 witness or to a 687-edge Q8 graph is justified.
