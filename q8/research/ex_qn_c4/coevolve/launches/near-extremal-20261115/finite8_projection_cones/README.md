# Generic small-alphabet finite-six projection kernels

`PROOF.md` proves the arbitrary deterministic projection interface, including non-equivariant maps, full-state root-stabilizer averaging, common root transport, exact diagonal collisions, and the whole-actual-Q8 finite-eight bridge. The concrete new projection is `parallel15`, the translated-square edge pattern `flag >> 4`; the older `connector16` means `flag & 15`.

A new cut was found and separately replayed at **post-connector4 master102**, with 7,967 stored cuts checked. See `parallel15_master102/block3.EXACT_CUT.json`, `INDEPENDENT_CHECK.json`, and `FULL_SCORE_CHECK.json`. Its full 187-state invariant kernel has scale 8,000,004 and exact normalized pairing approximately −0.00003188081534984. The four other bounded probes are inconclusive. The upper682 goal remains OPEN.

## Ready consumer interface

Read the emitted cut JSON. Use `full_Q` in `block=3`, exactly in `full_state_codes` order, with all other blocks zero; divide the feature by `positive_normalization=8000004`. The integer full matrix **already is the stabilizer sum**, so no extra stabilizer factor or label action is needed. The existing native coefficient scorer's root averaging leaves this invariant matrix unchanged. Upper off-diagonal coefficients are already folded; do not multiply them again.

```python
from pathlib import Path
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path('finite8_projection_cones').resolve()))
from score import full_face_kernel, value_on_graph
cut = Path('finite8_projection_cones/parallel15_master102/block3.EXACT_CUT.json')
matrices, positive_scale = full_face_kernel(cut)
exact_feature = value_on_graph(actual_q4_mask, cut)
```

`full_face_kernel` returns five full integer face matrices and the positive denominator. `value_on_graph` returns an exact Fraction, including the scale by default; set `normalize=False` to obtain the raw integer-kernel feature. It evaluates the full matrix against the actual unchanged `finite_flags.local_coefficients`. A nonnegative coefficient on this same-lambda feature is valid for every actual C4-free Q8, with no maximality or PSD assumption. It does not establish an inequality separately on every Q4.

## Generic discovery and checking commands

Run from the launch directory. Use a new output directory and an immutable point that reports at least 7,894 full stored cuts checked and actually postdates `SCOPE_INCREMENT_004_CONNECTOR4.json`.

```bash
python3 -B finite8_projection_cones/price_projection_point.py \
  finite8_degree_augmentation/pool_edge3_allclass1/point_bank/NEW_POINT.json \
  finite8_projection_cones/NEW_OUTPUT --mapping-mode parallel15 --seconds 8
python3 -B finite8_projection_cones/check_projection_point.py \
  finite8_projection_cones/NEW_OUTPUT
```

Mapping modes are `parallel15`, `connector16`, and `json`. For `json`, add `--mapping-json MAP.json`; its format is `{"labels": L, "full_state_to_label": [map0,map1,map2,map3,map4]}`. Each map lists integer labels in ascending legal full-state-code order, with dimensions 240/212/190/187/170; `1 <= L <= 16`. The producer freezes the actual resolved mapping and full-state code lists in `MAPPING.json`. Generic maps require no label action, since the exported full matrix sums the actual full-state root permutations.

The LP discovers bounded packed duals, then integerizes with diagonal2/offdiagonal1 convention. Exact complete histogram minima determine a nonnegative J repair. Only an exact repaired full-kernel normalized pairing below −1e−7 is emitted. NoCut and timeout are inconclusive. They do not prove cone membership or whole-family failure.

Reproduce the completed independent checks without repeating any LP:

```bash
python3 -B finite8_projection_cones/check_projection_point.py \
  finite8_projection_cones/parallel15_master102
python3 -B finite8_projection_cones/check_full_score.py
python3 -B finite8_projection_cones/check_generic_boundary.py
python3 -B finite8_projection_cones/check_sparse_calibration.py
```

The main checker uses only the standard library. It rebuilds actual literal Q4 geometry, all full states/actions, exact projected moments, complete multiset histograms and the actual682 seed bridge. The separate full-score check compares all 762 frozen-point full-kernel scores with the native consumer scorer, including the exact negative pairing, and evaluates a legal root6 graph nontrivially. The actual682 seed has no root6 squares; the cut's zero seed calibration is explicitly retained. The separate sparse actual-Q8 test uses two opposite retained edges and verifies a nonzero exact normalized bridge value 1/1792 from both all 1,792 roots and all 1,120 slices. Its receipt is `NONZERO_Q8_CALIBRATION.json`. Synthetic signed kernels check the other blocks, and the generic boundary script checks all 1..16 filtered domain counts and an actual non-equivariant mapping on the true seed.

## Files and dependencies

- `parallel15_master102/STARTED.json`: original source, point hash, increment hash, 7,967 checked rows, producer hash and time bound.
- `INPUT_POINT.json`, `MAPPING.json`, `PROJECTED_MOMENTS.json`: frozen decimal point, frozen map, exact integer projected matrices and denominator.
- `DOMAIN.json`: original complete sixteen-label array hashes and actual 38,760 filtered domain.
- `HISTORY.json`, `RESULT.json`: all five bounded discovery outcomes.
- `block3.EXACT_CUT.json`: small Q, exported full integer kernel, full state mapping/permutations, positive scale, exact repair/minimum/pairing.
- `INDEPENDENT_CHECK.json`, `FULL_SCORE_CHECK.json`, `GENERIC_BOUNDARY_CHECK.json`: actual independent replays and precise scope.

Dependencies are reused read-only: `finite8_flags/deps` (numpy/scipy), `finite8_flags/finite_flags.py`, `finite8_connector_frequency/membership.py`, and the complete generator arrays in `finite8_frequency_cone/`. No installation, global LP, original job, wiki, Goal, shared numerical scope or old file was modified. This scoped mathematical package is returned to Root for final integration and any canonical review.
