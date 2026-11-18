# Same-object edge-frequency / degree-profile bridge

## Claim and conventions

Let G be any actual C4-free spanning subgraph of Q8. Let N_d count its256 vertices of degree d, for d=0,...,8. Orient each ambient root edge by its binary endpoint order and let r=0/1 indicate absence/presence.

At that root there are seven external Q2 flags. Their three bits are the connector at the first endpoint, connector at the second endpoint, and opposite edge. For the integer histogram x, define

    a(x)=Σ_(s withbit0=1) x_s,
    b(x)=Σ_(s withbit1=1) x_s.

The actual two endpoint degrees are a(x)+r and b(x)+r: their other seven incident directions are exactly these connectors.

Let β_(r,x) be the frequency over **all1024 ambient root edges**, not a distribution conditioned on r and not a frequency over2048 oriented incidences. For each r,d define k_1(d)=d and k_0(d)=8-d. Then

    Σ_x β_(r,x)[1_(a(x)+r=d)+1_(b(x)+r=d)]
         = k_r(d) N_d/1024.                         (1)

## Proof

The left side times1024 counts incidences of an ambient edge of retained type r with a degree-d endpoint. Each degree-d vertex has exactly d retained incident edges and8-d missing ambient edges. Counting the same incidences vertex by vertex gives k_r(d)N_d. Every endpoint incidence is counted once even if both endpoints have degree d; in that case the column coefficient is2. This proves (1).

No degree bound below8, parity assumption, density threshold or graph-completion choice is used.

## Common endpoint flip and boundary cases

Endpoint flip swaps flag bits0/1, hence a and b. The sum of the two indicators is invariant. Therefore (1) is unchanged under the same C2 average used by the complete edge7 cone. No additional half factor is introduced.

Missing-edge histograms have endpoint degrees0,...,7, so row(r0,d8) is identically zero on both sides. Retained-edge histograms have endpoint degrees1,...,8, so row(r1,d0) is identically zero. All18 rows are retained in the interface; they are not18 independent nonzero constraints.

Summing over d gives2Σβ_1=Σd dN_d/1024=2e/1024, and2Σβ_0=Σd(8-d)N_d/1024=2(1024-e)/1024. This checks the all-ambient-edge normalization.

## Average parity-profile form

Suppose the parent has already established that the two actual128-vertex parity degree profiles belong to its necessary profile list. Let n(p) be a row of that list. Represent the average of the two actual parity profiles by nonnegative α with sumα=1. For one graph this is half mass at each actual profile, combined if equal. Then

    η_d=Σ_p α_p n_d(p)=N_d/2.

Equation(1) becomes

    A_endpoint β = H_profile α/512,                (2)
    H_(r,d),p = k_r(d)n_d(p).

The same α is used for both root types, and the same β is used for complete edge-moment matching and these endpoint counts. Neither a separately chosen local object nor an independent profile per root is introduced.

If the parent retains total N instead, use Aβ=D N/1024. If it retains averaged parity counts η=N/2, use Aβ=Dη/512, where D_(r,d),d=k_r(d). A projection to three Hg coordinates does not by itself retain this nine-coordinate identity; retain α or the full η in the exact profile convex hull.

This is an existence-type necessary interface: every actual graph supplies common λ,β,α. An arbitrary frequency decomposition of the same moment need not obey it; the LP must jointly choose one β satisfying both moment and degree equations. Feasible abstract data still do not imply a graph.

## Actual integer CSR contract

INTERFACE.json pins both source orders and hashes:

- A: ENDPOINT_INCIDENCE_CSR.json,18×5148, integer entries0/1/2,9450 nonzeros.
- H: PROFILE_RHS_CSR.json,18×792, integer entries,7208 nonzeros.
- D: DEGREE_VARIABLE_RHS_CSR.json,18×9,16 nonzeros.
- Row order: missingr0,d0..8; retainedr1,d0..8.
- β order: unchanged complete3432 missing-root then1716 retained-root histograms.
- α order: exact remaining-array order of pool_inventory/PROFILE_SNAPSHOT.json, source SHA452aa0e377ac002ae5687cd83268de253290e378e00a552c1f9e70840b6ce945; PROFILE_ORDER.json contains its degree vectors.
- Integer coupling:512Aβ-Hα=0. Alternatively1024Aβ-DN=0.

If the parent merges columns of the averaged edge moment generator, it must preserve these endpoint columns too. The independent checker explicitly checks every moment-column collision: all5148 columns reduce to2788 classes and every class has identical endpoint incidence.

## Actual graph calibration

build_bridge.py reconstructs every one of the actual682 seed's1024 ambient roots, reads all seven flags and checks that the decoded endpoint degrees equal degrees counted directly from the actual edge set. It checks all18 identities. The global profile is

    N_4=2, N_5=168, N_6=86, allotherN=0.

The only nonzero raw endpoint counts are

    missing: d4=8,d5=504,d6=172;
    retained: d4=8,d5=840,d6=516.

The actual two parity profiles are both(0,0,0,0,1,84,43,0,0).
These have682 edges and are **not** asserted to be members of the683-only792-row domain. The calibration verifies the general N identity and the averaging factor from actual profiles, not a false representation in that target domain.

The empty cube and a complete8-edge star with all remaining vertices isolated also pass all18 identities. They exercise degree0 and degree8 boundaries without assuming minimum degree or maximum degree7.

verify_bridge.py independently checks all exported CSR columns, reconstructs β for every actual seed root by its full histogram and source generator lookup, and verifies Aβ against direct endpoint counts and actual N. It also checks all792 RHS columns and safe2788-column moment dedup. VERIFICATION.json records the actual PASS.

## Scope and return

This package supplies a proved necessary shared interface and exact data alignment. It performs no LP, changes no earlier source/proof/point, makes no canonical claim, and proves no new edge upper bound. Root and the degree author own the joint next solve, fresh acceptance and wiki integration.
