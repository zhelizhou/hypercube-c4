# Fresh review skeleton: edge flags and finite-seven kernels

Target: **main.tex**. Detailed human proof: **PROOF.md**. All previous source/point/review files remain read only. Full682 remains **OPEN**.

## E01 — States, common endpoint gauge and exact finite-eight bridge

- Missing root states0..7; retained root states0..6. Bits are first connector, second connector, opposite edge.
- Common endpoint flip swaps bits0/1 and keeps bit2; act on both flags together.
- Each actual Q8 root edge has7 external flags. Independent sampling gives(6/7)distinct+(1/7)diagonal.
- Uniform Q4/ambientedge sampling gives uniform1024 global edges and uniform3-subsets of their7 axes, since each edge lies in35 Q4s.
- Verify local coefficient /672 [6·3cross+3diag], hence /64512 coefficients288cross/48diag per endpoint action.
- No degree/parity/seed condition or PSD-only premise in the finite7 bridge.

## E02 — Exact pointwise pullback and redundancy

- At a face edge e, identify the base face as edgeflag s0 and read s(g) from the same full-face flag g with consistent endpoint orientation.
- V_e(g)=6e_s(g)+e_s0; facekernel=(1/196)Σ_e V_eᵀ Qbar_r V_e.
- Root symmetries permute face edges and possibly their endpoints; common endpoint averaging gives canonical face-stabilizer invariance.
- Expand the existing5/6 cross +1/12 diagonals. Summing3 base choices gives42 per cross and7 per diagonal; factor7/(24·196)=1/672.
- Therefore equality is pointwise on every legal labelledQ4, not just an expectation.
- PSD kernels pull back to PSD, so no newPSD block strength.
- For any integer6 histogramx, V_ex=6z with z integer total7. Finite7-valid kernels pull back to finite6-valid kernels. Do not advertise escape from the full finite6 cone.

Inputs: lift.py, original read-only fullface definitions, Root's separate EDGE_PULLBACK.md as additional derivation. The proof in main.tex is self-contained.

## E03 — Actual frozen moment and regression

- Reconstruct frozen818 graphs/weights from FAMILY_OBSTRUCTION.json, pinned hash fdbd082699eff6d46899d6a501945881cf6f6fed48735dd3a326c5db8080aec6.
- Moment convention M=U/(2·64512·W). Check off-diagonal factors and endpoint average.
- Missing support1,2,4,7; retained support0,3,5,6. Exact supported4×4 LDL positive; all omitted rows zero. These edgePSD moments survive as predicted.
- Direct actual682 seed1024-root×7flag outerproducts equal1120 localQ4 moment sum.
- BRIDGE_CHECK records882 graph identity checks and all18 face-root actions, but analytic E02 supplies full domain coverage.

## E04 — Complete finite7 domains and strict target pairings

Primary kernels: EDGE_CUTS.json and frozen_root0.RESULT.json, frozen_root1.RESULT.json, degree_snapshot_root0.RESULT.json.

- Regenerate all3432/1716/3432 integer histograms total7. Check every quadratic form; exact minimum0.
- Check symmetric C2-invariant matrices and smaller-total nonnegative witnesses giving-264/-288/-336. These certify nonPSD/noncopositive, not a seven-count contradiction.
- Reconstruct actual target matrices from graph masks and exact weights. Exact raw pairings:
  - frozen_root0: -27921397669/11851851840;
  - frozen_root1: -20810671173/3950617280;
  - degree_snapshot_root0: -34656869948258354962251/20000000000000146682828.
- These contradict finite7-cone membership by nonnegative trace pairing with every generator.
- The degree target is an exact rational normalization of the175-weight iteration10 eigen-cut intermediate, **not accepted feasible**. Preserve that scope.
- Neither floating infeasibility nor an authorPASS is a premise. verify.py independently reconstructs geometry and recursive domains without producer/scientific imports.

## E05 — Same-lambda consumer and full small-cone interface

- Add selected valid features only with nonnegative weights. Positive normalization scales1320/828/1680 do not affect validity.
- score.value_on_graph(g,name) returns an exact Fraction; score.full_face_lift gives existing5-face matrices divided by196·scale.
- Full cone: M_edge_r(λ)=Σβ_x avg_C2(xxᵀ/49), β>=0, same originalλ. All3432+1716 generators, or a separately proved complete orbit reduction.
- Use true symmetric upper matrix entries; distinguish them from full linear coefficients of off-diagonalQ entries.
- Generator ordered mass1 makesΣβ equal the ambient-root type probability automatically; no extraneous conditional mass.
- Feasible frequency/PSD data do not imply graph realization.

## Verification scope and return

The author verifier and Root's separate third checker have actual exact checks, but fresh review must read/reconstruct the kernels, data and analytic connections. No need to repeat optimization to verify the finite statements.

No old data/code/UNKNOWN was edited and no process remains. Root owns fresh review, combined optimization and wiki. The main full682 goal remains open.
