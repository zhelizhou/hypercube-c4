# Crowded-face import extension: four full Q6 roots

**Local import discharged.** For any C4-free spanning edge subgraph of Q6
and either specified parity P, exactly four degree-six P roots imply

    S+L <=144,

where S=sum_P binom(d,3) and L=count_P(d<=2). Other P degrees may be0,1,2;
opposite-parity degrees are unrestricted. This supplies the additional
analytic premise in `q8_crowded_faces/main.tex`, C01. Combined with the
unchanged parent import audit, **all local mathematical imports listed in
that current C01 are closed**. This does not certify the entire crowded-face
proof, every19-profile numerical caller, or the main upper682 goal, which
remains OPEN.

This is a deterministic local verification plus same-family provisional
semantic review. The caller's route requests native Codex `gpt-6.1-sol`,
`ultra`; actual model identity is not attested (`null`). No new canonical
audit, wiki entry, Goal change, solver or large trace replay was performed.
All work is in new sidecar files. The previously consumed audit records,
including `PROOF.md`, `VERIFICATION.md`, `FRESH_REPLAYS.json` and
`ROOT_CONSUMPTION.json`, were not edited.

## Complete mathematical proof

Full roots at distance two retain their common square, so distinct full
roots have distance at least four. A complementary distance-six pair has
distances summing to six from any third root; it cannot coexist with a
third full root. Thus the four full roots have pairwise distance four.

Translate one full root to zero. For the supports X,Y of two others,
the three sets A=X intersect Y, B=X minus Y, C=Y minus X are disjoint
coordinate pairs. A fourth support Z has sizes zA,zB,zC satisfying
zA+zB=zA+zC=2 and zA+zB+zC=4. Hence Z=B union C. One coordinate
permutation therefore sends the entire graph and all of its markings to
the common full code K={0, A union B, A union C, B union C}={0,15,51,60}.
The translation sends the original specified parity to the even parity,
whether it was originally even or odd. No exceptional vertex or selected
directions are normalized independently.

Of the eight vertices made from complete blocks, four are K. Each of the
other four uses an odd number of complete blocks, and has a full root at
distance two along each block. Selecting both directions of a block would
retain a square with that full root. Its degree is therefore at most three.

Every remaining even vertex splits exactly two blocks into one selected
bit each and leaves one block D unsplit. There are24 such roots. Exactly
two full roots are distance two away: resolving the two split blocks gives
four block-constant possibilities, exactly two of which are in K. Their
two difference pairs are disjoint, because the two full roots have mutual
distance four. They cover the split blocks. The vertex cannot select a
whole difference pair without making a square with the corresponding full
root. Consequently its degree is at most four, and degree four forces
both directions of the complementary unsplit block D.

Pair each such root u with u xor D. This partner also splits the same
two blocks, has the same unsplit block D, and is a distinct root of the
same type. The map is a fixed-point-free involution, yielding12 disjoint
pairs covering all24 roots. If both ends had degree four, each would
retain both D directions, making their common actual D-square. Thus at
most one root per pair has degree four: N4<=12. No nonfull root has degree
five; the four block-constant outside roots do not contribute to N4.

The four full roots contribute80 to S. For each of the other28 roots,
degree<=2 contributes1 to S+L, degree3 contributes1, and degree4 contributes4.
Therefore

    S+L =80+28+3N4 <=108+36=144.

This proof has no minimum-degree assumption, completing all0/1/2 boundaries
without star replacement. Its pairing acts on actual roots and actual
directions in one cube, so the common-square contradiction respects the
same object rather than separately feasible star assignments.

## Fresh exact reconstruction

The original `q8_triple_geometry_cycle010/PROOF.md`, the entire
`q6_four_full_capacity_cycle010/check_pairs.py`, its full pair receipt,
and the actual crowded-face `main.tex` were read. The four-full capacity
directory has a checker and data, not a separate `PROOF.md`; the complete
analytic manuscript is the former path.

`crowded_four_full_extension/check_four_full_fresh.py` is a new independent
standard-library implementation. It imports neither the old checker nor a
producer. Its completed run exited0, producing
`crowded_four_full_extension/FRESH_FOUR_FULL_CHECK.json`:

* Rebuilt all192 actual cube edges and240 coordinate squares.
* Enumerated all120 four-root codes, matched their orbit under all23040
  even-translation/permutation isometries, and constructed one explicit
  common isometry for each code. Each map was checked on every cube edge.
* Enumerated all1792 actual stars at the28 nonfull canonical roots. Each
  permitted star was tested by adjoining its literal edges to the24 full
  root edges and checking every actual square. This includes all low
  stars, rather than assuming any minimum degree.
* Found exactly the four degree-at-most-three roots3,12,48,63, and24
  degree-at-most-four roots, each with exactly four degree-four masks.
  Their intersection directions yield12 disjoint forced pairs.
* Checked all192 cross-products of degree-four masks at those12 pairs
  against the explicit common four-edge square. Every cross-product
  contains that square. All pair memberships and local mask histograms
  match the actual old pair receipt; the old PASS field was not used as
  proof.
* Verified the exact S+L identity for every nonfull degree0..4. Independently
  recomputed all crowded C02 local cap cases for every L0..32, c0..4 and
  residue-compatible S0..160 under the stated local inputs.

Reproduce only this extension with:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 crowded_four_full_extension/check_four_full_fresh.py
```

Run from this audit directory. The script writes only next to itself;
it reads the actual old pair receipt for comparison. It runs no solver,
search, historical main routine or previous trace checker. The actual
source, checker, result, log and unchanged-parent hash bindings are in
`CROWDED_IMPORT_EXTENSION.json`.

## Consumption boundary

Current C01 imports316/317/321, general three-full S+L<=158, and four-full
S+L<=144. The first three weighted imports were discharged in the parent
audit. Its23-slot proof already establishes the **general** three-full
bound, without the missing-fourth-root degree condition; that extra
condition was only used for the stronger minimum-three S<=155 result.
The present extension closes the remaining four-full input.

Accordingly all of those local premises now apply to arbitrary actual Q6
faces with the parity inherited from one fixed global class. This statement
does not replace Root's current caller/hash binding, certify C03 or any
downstream LP/certificate, or alter historical audit verdicts. Root may
append this additional connection to the current caller while retaining
the previous reports and their original scopes unchanged.
