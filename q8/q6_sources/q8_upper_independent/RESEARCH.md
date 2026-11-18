# Independent attempt: prove ex(Q8,C4)=682

Status: active; target unproved. Start: 2026-10-21.

## Source boundary

User permits the local proof ex(Q7,C4)<=304 and forbids consulting existing Q8
progress. This project reads the Q7 proof at
`agents/generation/results/problem_001_304/blueprint_verified.md` and its Chinese
expansion. It does not read old Q8 research, upper-bound manuscripts, reports,
memory, or the earlier construction-search project. The generic helper
`build_bhn_graphs_up_to_q7()` supplies a Q7 benchmark only.

## Target

The original statement is: 证明ex(Q_8,C_4)=682。可以参考本地的对于n=7情形304的上界证明，但是不要参考已有的n=8的进展。

The supplied lower bound is 682. The missing task is a valid upper bound of 682
for all C4-free spanning edge subsets of Q8; no odd-square or degree restriction
may be silently imposed. All larger graphs may be reduced to exactly 683 edges.

## Initial new route

Test the Q7 weighted inequality `2m+N6<=608`, where N6 counts vertices of degree
six, first on graphs with all degrees in {4,5,6}. This is a candidate, not a
known lemma. Its relevance and any failures will be recorded after checking.

## Verified progress in this goal turn

The full current mathematical argument is in `PROOF_PACKAGE.md` in this
directory. The goal remains the original equality 682; it has not been met.

1. A new hand argument excludes degree-seven vertices from every 304-edge
   C4-free Q7 graph. It uses only parity star counting and facet congruences.
2. A six-case computer-assisted lemma proves that a specified parity of a
   C4-free Q6 graph with minimum degree at least three has at most 158 full
   three-stars. All six CNFs were rebuilt independently; every contradiction
   trace was replayed sequentially by the independent RUP checker, verifying
   256403 additions in total. The manifest is
   `results/q6_star158_certificate_manifest.json`.
3. For arbitrary Q6 degrees the previous statement extends to `S<=158+2L`,
   where L counts local parity vertices of degree at most two.
4. Summing that inequality over the 112 Q6 faces of Q8 gives the unrestricted
   interim upper bound 688. For either parity P,

   `100m + sum_P w(d) <=68896`,

   with degree weights `[344,244,144,74,28,0,0,50,160]` for degrees 0..8.
   This has no minimum-degree assumption and uses no older Q8 result.
5. At m=688 these weights reduce each parity to seven degree histograms,
   recorded in `results/arithmetic_symmetry_audit.json`.

## Failed or unresolved routes, retained explicitly

- The universal weighted Q7 inequality `2m+N_{>=6}<=608` would immediately
  yield the full Q8 upper bound 682 by face summation. It is still UNPROVED.
- Four CP-SAT probes of this Q7 inequality returned UNKNOWN, including a
  minimum-degree-four case and rooted degree-six/seven cases. Two bounded
  annealing runs found no counterexample. None is evidence of nonexistence.
- An exact stacking test of 46080 automorphic pairs of one 132-edge Q6 graph
  attained weighted score 608, with no score above it. A separate 127-edge
  positive-defect Q6 seed gave maximum 600 on the analogous family. These
  restricted families do not prove the Q7 weighted inequality.
- The stronger assertion that minimum degree three in Q6 forces nonpositive
  square defect is FALSE. `results/q6_positive_defect.json` stores a checked
  127-edge counterexample with defect +1.
- A monolithic one-hole Q6 probe timed out. Its incomplete generated trace
  was discarded and its UNKNOWN status retained. Splitting the one-root case
  into its three actual hole orbits subsequently produced checked UNSAT
  certificates for all three cases. Do not cite the timed-out run as a proof.
- Small Q4/Q5 analogues of a putative simple star-deficit induction are SAT;
  witnesses are retained in `results/small_star_probes.json`.

## Revalidation and reproduction

The local generators use `/tmp/cadical-master/build/cadical` and the Python
SAT/OR-Tools packages currently installed under `/tmp/q8-683-deps`. This is
only an executable/dependency location from the environment: no old Q8
research input is read from it.

Compile `check_rup.cpp` into `/tmp/q8-independent-check-rup`, then run
`python3 q8_upper_independent/audit_rup.py`,
`python3 q8_upper_independent/audit_star_cases.py`, and
`python3 q8_upper_independent/audit_counts.py` from the repository root.
The first command audits propagation against an independent naive method;
the second rebuilds the six inputs and replays all required traces; the third
checks case-orbit coverage, hashes, and the complete degree arithmetic.

## Next work toward 682

Exclude all hypothetical edge counts 688 down through 683, or prove the
unrestricted weighted Q7 inequality. For 688 start from the seven admissible
parity degree profiles, use the new Q6 star158 lemma and the already allowed
Q7 theorem and local rigidity lemmas. A numerical profile is only necessary
data, not an actual cube graph. Retain the source boundary: do not read any
pre-existing Q8 upper-bound research, reports, or memory outside this fresh
project. This project's own newly derived evidence may be continued.

## Second goal turn: checked refinement, upper bound still688

The previous goal turn is classified as **progress**: its six-case lemma and
unrestricted 688 proof were revalidated as the starting state. This turn is
also **progress**, but the original 682 goal is still incomplete.

The complete new derivation is in `REFINEMENT_688.md`. Authoritative results:

1. Q6 specified-side degrees: exactly one degree-two root, all others at least
   three, imply S<=158. This requires one full160 case plus16 complete
   one-hole orbits. All17 inputs were independently rebuilt and all traces
   checked to the empty clause, with4122060 verified additions in total.
2. One extra checked case (204462 additions) excludes S158 with exactly three
   full Q6 roots on a minimum-degree-three parity. Together with the old
   star158 bound, it proves the sharp inequality `2S+N6<=316` on that parity.
3. The unconditional extension `2S+N6<=316+8A+4B`, for local degrees <=1
   counted by A and degree-two roots by B, gives new Q8 degree weights.
   A separate single-low-root count eliminates the degree-three profile.
   Consequently each parity in a hypothetical688 graph has only
   `(N4,N7)=(0,0),(1,0),(2,0),(0,1)`.
4. Rounded Q7 facet inequalities give exact saturation for an N4=2 parity.
   Its two degree-four roots have K=0,3,4 common selected directions on which
   their coordinate values agree. K=1,2 are excluded. When K=4 the two
   canonical positions are w48 or w240 after fixing the first root at0 and
   both selected direction sets at0,1,2,3.

New evidence: `results/low2_star158_certificate_manifest.json` and
`results/refinement_audit.json`. There are eighteen new certificates with
4326522 checked additions. Combined with the six earlier cases, the branch
has twenty-four local certificates with4582925 checked additions. This is
not a certificate of the final 682 bound.

The active/history checker restores only strictly earlier, already checked
consequences. It passed300 naive-propagation differential cases, a deletion
restoration test, and a trap rejecting the use of future clauses. The large
full160 degree-two case also passed the original historical checker with the
same407926 additions. The generated cached-checker prototype is NOT used in
the new proof manifest; it is not a mathematical premise.

Completed unresolved probes (do not restart them as if still live):

- Both K4 canonical Q8 cases returned UNKNOWN after240 seconds each. They
  remain unexcluded. Inputs use only the fresh saturation tables and the
  allowed Q7 theorem.
- The Q7 304-edge degree-six-root probe remained UNKNOWN even with the newly
  proved Q6 cuts and allowed Q6 rigidity. No global Q7 weighted theorem was
  obtained.
- The stronger local guess `S+2N6<=158` is FALSE. A checked128-edge Q6 witness
  has specified-side S157 and N6=2. It attains equality in the proved weaker
  inequality `2S+N6<=316`. A direct full-code potential test excluded some
  other root codes, but that does not rescue the false universal guess.
- Stacking this new witness against all46080 of its Q6 automorphic images
  reached Q7 weighted score606, not a counterexample to the unproved Q7
  target608 inequality.
- The candidate coupled inequality `4m+N3+3N6<=532` for minimum-degree-three
  Q6 graphs returned UNKNOWN. It is not used. Its model's m<=132 cut follows
  from the checked star158 bound: m133 would force all degrees4/5, which is
  excluded by the Q5 congruence argument in the allowed Q7 proof.

Reproduction for this turn: compile `check_rup_active.cpp` to
`/tmp/q8-independent-check-rup-active`; run `audit_history_checker.py`,
`audit_low2_star158.py`, and `audit_refinement.py`. Existing complete replay
reports are reused only after matching the current input, proof and checker
hashes. Next work should exploit the four parity types and saturation, not
assume any of the UNKNOWN families absent.

## Latest goal turn: K0 and K4 excluded for the two-degree4 parity

Classification: progress. The full682 objective is still active and unproved;
the unconditional bound remains688. See REFINEMENT_K3.md for the full new
argument and results/k3_refinement_audit.json for authoritative evidence.

Nine additional CNFs were independently reconstructed and their actual
traces checked to the empty clause, with1197754 additions. There are now33
local proof certificates and5780679 checked additions in this upper branch.
Sharp specified-parity Q6 bounds are S<=152 at c6=3, S<=144 at c6=4, each
with a verified attaining graph. Three low-degree full-code extensions and
a two-case geometric two-degree2 lemma supply the new saturation steps.

A hypothetical688 graph with two degree4 roots on a parity must now have
K3, not K0 orK4. Its16 Q7 facets have edge counts300 nine times,302 five
times,303 twice. Ten Q6 boxes have one full root, twenty have two. The
remaining configurations normalize to nine explicit root/mask pairs.
All nine bounded CP probes terminated UNKNOWN at120 seconds each; no
family exclusion follows from those probes. All this turn's jobs are terminal.

The earlier candidate coupled inequality4m+N3+3N6<=532 is FALSE. Checked
counterexamples include m122,N3=28,N6=6, potential534. The coefficient2
variant with a proposed strictness clause is unresolved: its tested branches
are UNKNOWN. Neither conjecture is a premise of the K3 reduction.

Next: exploit a forced M300 Q7 facet with eight degree6 roots on a specified
parity, or the nine K3 patterns through stronger local rigidity; do not simply
rerun the unchanged CP models. Every other688 profile and687 through683
still needs exclusion. No old Q8 mathematical progress was imported.

## Continuation: M130 local rigidity and restricted mixed stacking

Classification: progress; the original682 objective is unproved and the
unconditional upper remains688. Full derivations and assumptions are in
LOCAL_PAIR_RIGIDITY.md. No older Q8 mathematics was read.

New checked result: a C4-free Q6 of minimum degree at least3 with130 edges
has at most one degree6 vertex on each parity. Two same-parity full roots
force the other side's histogram to (N3,N4,N5,N6)=(6,18,8,0).
The root side has either zero or one degree5 vertex. Two no-degree5 cases
and six degree5-position orbits exhaust all possibilities. Eight independent
CNF reconstructions and actual RUP checks verify96986 additions. Orbit sizes
are4,16,16,24,12 at full-pair distance4, and60 at distance6.

Three additional fixed-profile exclusions were independently reconstructed
and actually RUP-checked: M124,c=(3,3),b3=(12,12); M125,c=(3,2),b3=(10,13);
M131,c=(1,0),b3=(2,4) when the full root's neighbor degrees are3,3,3,3,5,4.
They contribute642268 additions. This turn totals11 certificates/739254
additions; branch total44 certificates/6519933 additions. Hash-bound ledger:
results/local_pair_certificate_manifest.json.

A direct Q5 hole-congruence proof establishes Q6 m<=132 with no minimum
degree restriction. With whole minimum degree3, the full-root neighbor bound
b_opposite>=3c and the checked sharp star caps imply m+N6_total<=132.
Adding the new M130 rigidity gives m+2c_P<=133 for either side. All integer
histograms for96<=m<=132 are mechanically audited; these numerical
histograms are not asserted to be realizable graphs.

Important failed stronger conjectures:
- Strict T2<532 whenever a full root occurs is FALSE. Two checked M130
  witnesses have one full root on each parity, degrees3..6, T2=532. The
  weak universal T2<=532 remains unproved. Do not reuse the strictness guess.
- Sharp c3 S152 and c4 S144 can be attained with whole minimum degree3;
  a supposed necessary opposite-side degree2 is therefore FALSE.

Forced Q7 M300/P-eight-six-root probes, all terminal UNKNOWN: normalized
root pairs at distances4/6, three paired-Q6-box patterns, two finer subcases
of the two-doubled-axis pattern, and three compact SAT encodings of the
box patterns. None is a family exclusion. A genuinely stronger next model
uses opposite minimum3, at most two degree3 roots, at most one degree7 root,
and the newly checked local cuts. Its outputs have separate names ending
lowlimit2_rigid and do not overwrite the earlier probes.

Five same-seed specified-parity stacking families each tested46080 cube
automorphisms with no parity score above304. Seven seeds, including an
independent132-edge seed and both new130-edge seeds, were then mixed in
all21 pairs:967680 automorphic pairs, no score above304. Every returned
graph was independently checked for C4-freeness, specified minimum degree4
and actual score. This is restricted-family evidence only. The universal
Q7 inequality m+N6(P)+3N7(P)<=304 is still unproved; the unrestricted
2m+N_ge6<=608 is also unproved.

Reproduction: audit_pair_rigidity.py, audit_local_density.py,
audit_histogram_profiles.py --check, audit_local_pair_summary.py.
The last ledger reuses completed actual replay results only after matching
CNF/proof/checker hashes. Compile q6_stack_parity.cpp to
/tmp/q6-stack-parity-mixed, then mixed_stack_probe.py reproduces all21
mixed stacking families and independent witness checks.

The three stronger opposite-low-limit2 box-pattern probes have now also
terminated UNKNOWN at90 seconds each. No family was excluded. The
solver-free audit_box_patterns.py checks the1001 four-facet selections,
the forced four paired boxes from weighted-star equality, and the Q5
pair geometry. All jobs of this continuation are terminal.
