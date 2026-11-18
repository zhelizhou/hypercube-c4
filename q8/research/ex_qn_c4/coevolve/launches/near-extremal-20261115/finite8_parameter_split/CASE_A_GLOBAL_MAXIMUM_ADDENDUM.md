# Stronger representative for the remaining A683 research branch

This addendum changes the representative used in a new A research model; it
does not retroactively change an old frozen model or assert that a bounded
NoCut proves anything. Main upper682 remains OPEN. The existing B proof uses
only ordinary inclusion-maximality and is independently valid with that scope.

Suppose there is any C4-free Q8 graph with at least683 edges. Among all
C4-free spanning subgraphs of this finite cube, choose H with maximum edge
count. Then e(H) is at least the original counterexample's edge count. H need
not contain that original graph; containment is unnecessary for a universal
upper-bound contradiction. H is inclusion-maximal, has no isolated vertex,
and obeys every previously established general or ordinary-maximal interface.
The original universal Q6 argument still gives683<=e(H)<=688.

If e(H)>=684 the unchanged branch-B argument applies. If e(H)=683 its parity
profiles belong to the same764-profile A cover, including only the already
proved exact683 exclusions. Its actual lambda, alpha and beta are defined
exactly as before. Thus ruling out A under the **global edge maximum** premise
and B under ordinary maximality is a target-preserving case cover. Once the
whole-B theorem upper683 is accepted, any683-edge graph is itself a global
edge maximum, giving the same conclusion directly. No P2 tie optimization is
required for the Hall-triple rows below.

For a vertex v, build the conflict graph T on its eight ambient directions.
Directions i,j conflict exactly when both remote edges of their actual
rooted Q2 are retained. The retained incident direction set S is independent
in T, since retaining both incident edges of a conflicting pair makes a C4.
Conversely, replace all edges at v by any independent direction set S' of T.
All C4s not containing v are unchanged; a C4 containing v is exactly one of
these direction-pair squares and is excluded by independence of S'. Hence
global edge maximality makes S a maximum independent set of T.

If I is an independent set of three missing incident directions, then

    |N_T(I) intersect S| >=3.

Otherwise `(S minus N_T(I)) union I` is independent and strictly larger.
This simultaneous replacement concerns one actual star and its same remote
edges. It does not assume compatible separate completions from marginal
histograms.

An actual marked Q3 face rooted at v specifies its three missing incident
directions I and their three conflict tests. Conditional on any fixed rooted
Q3 pattern with those properties, its five outside axes contribute one
Boolean witness U each, exactly indicating membership in N_T(I) intersect S.
For each of the40 classes under the common S3 permutation of I, the resulting
local Q4 feature is h_c/64: sum over the64 marked Q3 corners of a Q4, adding
`5U-3` when that Q3 belongs to class c. The common sampling count is

    14336 actual marked Q3 corners *5 extensions
      =1120 coordinate Q4s *64 local marked Q3 corners.

Thus E_lambda h_c/64 equals the actual marked-Q3 average of
`1_class (sum_five U-3)`, and is nonnegative for the selected H. This is a new
global-maximum-only family. It is not valid for arbitrary C4-free graphs or
asserted for every inclusion-maximal graph.

The independent producer/definition/checks are in
`../finite8_star_optimal_vertex/hall_triples/`. Root's original diagnostic
scripts are in `../finite8_root_checks/`. They find strict violations of24
class rows at frozen A103. The necessary inequality's proof, program and
new full-domain scoring interface still require their accurately scoped
acceptance before use in a final682 certificate. This addendum itself is not
that acceptance and does not move any previous canonical audit boundary.
