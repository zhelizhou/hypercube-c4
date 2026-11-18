# Fresh nonauthor review of the generic small-projection package

Substantive verdict: **PASS in the stated local scope**, with zero open fatal,
critical, major or minor mathematical/program issues. This is a completed
**same-family / provisional** native Codex review, not cross-family acceptance.
The requested reviewer was `gpt-6.1-sol` with `ultra` reasoning. Neither an actual
model ID nor actual effort was returned/independently attested; both remain
`null`. The route parser's requested pair is not actual identity evidence.

This file is the reviewer's full raw assessment. It is based on reading the
complete canonical `../PROOF.md`, all six implementation/checker/scorer files,
the README contract, actual mapping/cut/point data, the actual native coefficient
source and histogram loader, and the selected state/action and face-sampling
spans of `../../finite8_flags/main.tex`. No author's PASS receipt, Root replay,
old optimization result, old PSD/barrier theorem or model agreement is a premise.
All review code and results are newly written within this `review/` directory.

The main assertion `ex(Q8,C4) <= 682` is **OPEN**. No full-Q4 maximization,
combined valid-row certificate, full-family barrier, exact target PSD
qualification, or actual graph corresponding to master102 is certified here.

## Exact statement reviewed

For every selected block index b in {0,1,2,3,4}, with root mask
(0,1,3,6,7)[b], every integer 1 <= L <= 16, every deterministic map Phi from
**all** legal labelled full states S_b to {0,...,L-1}, and every symmetric
integer Q nonnegative on every nonnegative integer L-vector of total six,
define

    B[i,j] = Q[Phi(i),Phi(j)]
    K[i,j] = sum over h in H_b of B[pi_h(i),pi_h(j)].

Then K is H_b invariant and is nonnegative on every full-state nonnegative
integer count vector of total six. For every actual C4-free G subset Q8 and
every positive scale s, the local Q4 functional specified in PROOF.md:55 obeys

    E_A T_(K/s)(G|A)
      = (1792 * 36 * s)^(-1) sum over roots F of type b x_F^T K x_F >= 0.

The expectation is uniform over the 1120 coordinate Q4 restrictions of that
same G. No equivariance, surjectivity, PSD, copositivity, maximality, edge-count
condition, root-type mass normalization, or realization of arbitrary formal
histograms is assumed. The concrete stored decimal point is a separate linear
pairing calculation, not an additional hypothesis of this theorem.

## Full mathematical audit

### 1. States, legality and the actual group

The legality rule enumerates exactly the possible retained edges in one rooted
Q3: the root square is already nonfull; the translated square must be nonfull;
and each of the four side squares must have a missing edge. A cube four-cycle
is a coordinate square: a closed length-four simple walk toggles two distinct
coordinates twice each, alternating them. Thus there is no missing noncoordinate
four-cycle condition here.

My replay enumerated all 256 possible full flag codes for each root, built the
literal Q3 edges, and tested all its coordinate squares. This gave all state
codes, in increasing order, with dimensions 240/212/190/187/170. I did not use
the author's state dictionaries to generate them. The fifteen nonfull root
masks have exactly the five declared orbits.

I generated the square automorphism group as all permutations of four vertices
preserving the square's edge set. There are eight, closed under composition.
The full stabilizer sizes are 8/2/2/4/2. Each stabilizer action permutes the
entire reconstructed full-state list. The stored full-state order and all four
exported block 3 permutations agree, up to harmless order of the group elements.
These are simultaneous actions on connectors and translated edges, before Phi.

### 2. Pullback, the complete histogram domain and unused labels

For every integer full-state x with total six, the aggregation
y[a] = sum_(Phi(i)=a) x[i] is an integer nonnegative vector with total six.
Expansion of the two finite sums gives x^T B x = y^T Q y. No converse or graph
realization assertion is needed. In particular, testing a superset containing
histograms impossible for an actual graph is a sufficient condition; it causes
no logical gap. Unused labels also cause no difficulty.

The stars-and-bars count is C(L+5,6). Zero-padding to sixteen labels and deleting
the zero tail are inverse maps between the complete domains. I independently
enumerated integer compositions recursively and compared their actual sets
with the stored sixteen-label array, not merely their cardinalities. All 54,264
rows are present exactly once, and every L=1,...,16 tail filter gives exactly
the independently enumerated desired set. The fifteen-label set has 38,760 rows.

I also checked all actual sparse generator columns against y_i*y_j/36, including
their nonzero supports. They are stored floating representations, so this is a
representation check to 1e-12 after multiplication by 36. The accepted cut's
validity does not rest on those floating entries: its final domain minimum was
recomputed entirely with integer arithmetic and independent compositions.

### 3. Full stabilizer sum and non-equivariance

For each h, setting x_h[k] = x[pi_h^{-1}(k)] preserves nonnegativity, integrality
and total six. Therefore each transformed summand contributes a nonnegative
quadratic. Summing proves finite-six validity. Simultaneous replacement of
(i,j) by (pi_g(i),pi_g(j)) permutes the full H sum by h -> hg; closure gives
invariance. This argument never invokes or needs an action on labels.

The producer follows precisely this sequence: pull back Q through the entire
full-state map, index that full matrix by every actual stabilizer permutation,
and sum. The actual output is the full integer matrix, not a projected quotient.

For a genuinely incompatible map Phi(i) = i mod 3, I found explicit same-label
state pairs whose images have different labels under a stabilizer element in
**each** of the five blocks. For example, in block 0 the full-state IDs 3 and 0
both have label 0, but one group element sends them to labels 2 and 0. Thus an
induced label permutation does not exist. The full lifted matrices still are
invariant and pass literal actual-Q8 bridge checks. All five corresponding
full-kernel scorer and ordered-moment interfaces also pass on all 762 graphs.

### 4. Root transport, collisions and the whole-Q8 sampling identity

All six flags at an actual root are restrictions of one G and are transported
with the same square isometry. If two such isometries carry its root pattern
to the canonical pattern, their quotient stabilizes that canonical root.
The proved full-state invariance consequently preserves each K entry and the
root quadratic. Neither independent flag canonicalization nor independent
completion appears in the proof or the literal replay.

For fixed flags s_1,...,s_6,

    x^T K x / 36
      = (5/6) * (1/30) sum_(i != j) K[s_i,s_j]
        + (1/6) * (1/6) sum_i K[s_i,s_i].

This holds even when several flags have the same full-state ID. It distinguishes
equal sampled directions from equal state labels, so no collision term is lost.

Q8 has C(8,2)*2^6 = 1792 roots and C(8,4)*2^4 = 1120 coordinate Q4 slices.
Each root has C(6,2)=15 possible two-direction extensions. The identity
1120*24 = 1792*15 gives the claimed uniform root distribution. A sampled
unordered extension pair is uniform; symmetry gives the ordered-distinct cross
average, and its equally weighted two endpoint diagonals give the uniform
single-direction diagonal average. This proves exactly PROOF.md:63, without
any PSD inference or conditioning a selected root block to have mass one.

All spaces and sums are finite. There is no unproved limit interchange,
integrability assumption, asymptotic uniformity claim, or hidden parameter limit.
Positive division and a nonnegative multiplier preserve the inequality;
negative multipliers are not authorized by it.

### 5. Native upper coordinates and normalization

Native denominator 64512 is consistent with the literal local formula:
cross 2240/64512 = 10/288 and each direction's diagonal 224/64512 = 1/288.
The native coefficients already average over H. They are folded upper
coefficients, so a full symmetric entry is paired with each upper coefficient
once. Doubling upper off-diagonals again would be wrong.

Writing the ordered native moment with denominator 129024 requires twice the
native diagonal coefficient and one off-diagonal coefficient in each of the
two symmetric positions. If distinct full IDs map to one label, both positions
land on that projected diagonal. The producer's accumulation and subsequent
diagonal doubling implement this correctly. My reconstruction compared every
entry of all five concrete projected moments. It encountered 5,314 ordered
action cases with distinct states projecting to one label. The independent
generic/native comparison exercised another 9,593 folded collision cases.

For the native invariant full moment M, pairing it with the full H **sum**
gives <K,M> = |H| <B,M>. This uses invariance of M, not equivariance of Phi.
Thus the factor |H|=4 in the concrete small-trace computation is correct. The
full-kernel consumer must not insert a second group sum or a second factor 4.
It pairs the already exported invariant K directly, then divides by 8000004.
I checked both unscaled and scaled native scores for every actual point graph,
and the complete matrix-return interface with all other blocks zero. The five
generic full kernels independently satisfy the same trace-factor identity.

### 6. Exact concrete acceptance and negative boundaries

The actual point/cut/mapping hashes agree with the declared artifacts. The source
master102 byte hash equals the frozen input hash. The source file's observed
mtime is strictly later than the scope increment, and the original metadata
reports 7,967 checked cuts. The scope increment separately reports 356 equalities,
14,838 library graphs and 7,894 cuts after the connector increment. These are
provenance checks, not premises proving optimization feasibility.

All 762 distinct stored Q4 masks are literal legal C4-free graphs. Their decimal
weights are positive, parsed as exact Fractions. Their exact total is

    999999999403515826619043431 / 1000000000000000000000000000,

which is not silently replaced by one. The diagnostic value is the unnormalized
linear pairing of these exact weights; no root-block mass or probability
normalization is inserted. The generic theorem still quantifies over every
actual G, independently of this diagnostic point's residuals.

The exact complete-domain minimum before the J repair is -8. Adding J shifts
every total-six quadratic by 36, giving exact minimum 28 over all 38,760 rows.
The full 187-by-187 integer kernel was rebuilt entry by entry. Its maximum
absolute entry is 8000004, which is its positive normalization. Exact raw pairing:

    -15940415645124021372345799259 / 62500000000000000000000000.

Exact normalized pairing:

    -15940415645124021372345799259 / 500000250000000000000000000000000
      = approximately -3.1880815349840365e-5 < -1e-7.

This reproduces the strict exclusion. LP success, rounding and a floating
objective were not used as acceptance evidence. The packed LP convention is
consistent: symmetric diagonal factor 2 / off-diagonal factor 1 makes the true quadratic twice
the packed linear form, preserving its sign. Exact repair, full lift and exact
target pairing close the eventual acceptance obligation.

The full-state count vector with codes 32 and 64 once each and 112 twice is legal
over root 6 and has total four. Its exact full-kernel quadratic is -1,454,496.
It proves the **actual exported full matrix**, not merely its small antecedent,
is neither copositive nor PSD. Integer-total-six nonnegativity imposes a
different discrete restriction; homogeneously rescaling this witness to total
six introduces noninteger counts, so it does not refute the theorem.

The legal individual Q4 mask 3878281676 has normalized local value
-7636349/144000072. This supplies a direct negative test against an accidental
claim of pointwise local nonnegativity. The claimed nonnegativity concerns the
whole actual-Q8 restriction expectation, which is what the proof establishes.

### 7. Actual-Q8 calibration and generic program contract

The literal 682-edge source seed has the declared hash, legal cube edges and no
C4. All 1792 global roots and all 1120 actual Q4 slices were reconstructed and
their exact averages agree. Its root counts are 301 of block 1 / root 1 and 1491 of
block 4 / root 7. Hence its block 3 / root 6 concrete value is **zero**, not a nonzero
test of the concrete cut, and this limitation remains explicit. Some other
synthetic block evaluations on that seed are also zero; a loop over five blocks
does not imply all five are sampled nontrivially by that seed.

The sparse actual graph {(0,1),(2,3)} has exactly one root of canonical type 6
and six zero flags there. The full K[0,0]=8000004. The independently reconstructed
root and slice averages are raw 2000001/448 = K[0,0]/1792 and normalized 1/1792.
An additional actual graph {(0,1),(0,2)} has one root of type 3 / block 2 and gives
a nonzero block 2 bridge value 3/448 for the generic synthetic kernel. Empty
graphs and a single-direction matching were also checked. These computations
validate edge cases of the implementation; the analytic proof supplies the
universal implication.

The generic JSON producer loader accepts five complete maps with integer labels
for L1,L3,L16 and rejects invalid L0/L17, floating or Boolean L, missing/extra
blocks, missing full states, and negative/out-of-range/Boolean/floating labels.
Both built-in modes match the reconstructed ascending full-state code lists.
Actual CLI `--help` exposes the stated modes/options without running a probe.

For every one of the five incompatible three-label full kernels, the native
full-kernel scorer agrees with an independent literal local calculation on all
762 actual graphs. Both the generic ordered projected moment and its native
folded-coefficient projection agree entrywise. The consumer formula depends
only on the supplied full matrix and an actual legal Q4 mask, so the same
formula scores future legal columns without any invented label action or
support restriction. This is an analytic interface property plus 3,810 exact
data comparisons, not an exhaustive enumeration of every legal Q4 graph.

One initial review harness run imported a sibling `score.py` after the producer
prepended its dependency directories. I corrected my own test to load this
package's scorer by its explicit file path. The failed review harness attempt
is retained as `GENERIC_REPLAY_ATTEMPT1.log`; the successful corrected run is
`GENERIC_REPLAY.log`. It did not require any author-source change and is not
treated as a defect in the documented isolated package scorer interface.

## Mandatory A–H checklist and adversarial attempts

| Check | Result |
|---|---|
| A. Definitions/types | Full-state IDs versus labels, block index versus root mask, full H sum versus average, decimal denominator D versus scale s are distinguished. No harmful definition drift. |
| B. Hypothesis discharge | Generic small-domain hypothesis is explicit; concrete Q is integer/symmetric and has independently checked complete minimum 28. Actual G legality and common transport are sufficient for T1. No missing application hypothesis. |
| C. Inequalities | Every generic nonnegativity step is a finite-six aggregation, a sum of nonnegative terms, or positive scaling. Exact acceptance is rational with a strictly negative sign. No PSD-based step is smuggled in. |
| D. Interchanges | Finite sums only. No analytic interchange obligation. |
| E. Probability mode | Deterministic identity plus finite uniform-restriction expectation. No a.s./w.h.p. upgrade or probabilistic existence claim. |
| F. Uniformity/constants | Constants 24, 36, 1792, 1120, 64512 and the stabilizer-size factor are derived explicitly; no big-O statements. |
| G. Degenerate/adversarial cases | L1/L16, unused labels, incompatible actions, repeated states and coalesced labels, empty graph, sparse opposite/adjacent edges, single-direction matching, total-four negative witness, negative local Q4 value all checked. |
| H. Dependencies | Typed semantic graph is acyclic. Old global barriers/PSD receipts, optimization success, and calibration receipts are not proof premises. |

Attempts specifically aimed to break the result included projecting before the
full group action (ruled out by explicit non-equivariance witnesses), omitting
projected collisions (ruled out by entrywise moments), adding an extra group or
off-diagonal factor (ruled out by all literal/native score comparisons), assuming
all histograms are actual graph realizations (unnecessary in the finite pullback
argument), assuming root mass one (wrong denominator, never used), and inferring
PSD/global copositivity from the discrete test (directly contradicted by the
verified total-four witness). No counterexample to a stated claim was found.

The issue list is empty. No author-source repair or re-review round is required.

## Artifacts, coverage and remaining scope

`SOURCE_UNIT_COVERAGE.json` records 37 declared source units, their inspected
spans and exact input hashes, with no uncovered/failed units. All package and
read-only dependency hashes match the manifest. The selected old TeX imports
are explicitly scoped; this is not a new review of its later PSD/barrier theorem.
Coverage receipts describe source execution coverage, not an independent proof
that the obligation inventory is complete or the mathematics is true.

`SEMANTIC_LEDGER.json` contains 24 typed symbols, 19 dependency nodes, explicit
quantifiers and application hypotheses, discharge evidence, nonassumptions and
the checked topological order. `PROOF_SKELETON.md` is its human-readable map.
`PROOF_AUDIT.json` carries the substantive verdict separately from provisional
acceptance and unknown actual model/effort identity.

Reproduction, from this directory, without any optimizer:

    python3 -B independent_replay.py
    python3 -B generic_interface_checks.py
    python3 -B additional_root_cases.py
    python3 -B write_audit_artifacts.py

The review did not run an LP, an old job, a child agent, a whole-family search,
Lean, TeX or HTML generation. It did not write any author source, MathRSI file,
wiki, canonical claim, shared scope or Goal. Root retains canonical integration.
Four other bounded NoCut outcomes remain inconclusive. Completing the original
upper-682 objective would still require an appropriate valid-row combination
and whole-local-domain maximum argument/certificate; this package supplies
one new valid feature and a strict exclusion of one stored decimal point.
