# Edge–vertex shared incidence bridge

Read `PROOF.md` for the universal proof and `CHECK_RESULT.json` for actual verification. Scope: necessary identities for every C4-free Q8; upper682 remains OPEN.

Current numerical consumer:

- `BALANCE_CURRENT_36x1751.npz`: integer B36, impose `B36 beta=0`.
- `MOMENT_BETA_CURRENT_27x1751.npz`: integer B27.
- `MOMENT_PACKED9_SELECTOR_TWICE_27x45.npz`: integer W, impose `2304 B27 beta=7 W F_vertex.T lambda`, where F_vertex is the existing packed9 slice of INTEGER_FEATURES.
- `MOMENT_LAMBDA_CURRENT_POOL_27x14090.npz`: optional precomputed L=196 W F_vertex.T; equivalently `B27 beta=L lambda/64512`.

Rows and columns are frozen in `ORDER.json` and `MOMENT_ORDER.json`; hashes/contracts are in `INTERFACE.json` and `MOMENT_INTERFACE.json`. CSR `.json` mirrors accompany every `.npz`. Full162×5148, separate81×5148 per root, old162×2788 and current162×1751 C maps are available. Every stored old/current duplicate class preserves C exactly.

`MASTER050_DIAGNOSTIC.json` independently records the actual frozen relaxation tuple's violations. It is not an actual graph or a whole-model exclusion. No rank63 claim is made for the63 exported rows.

Root supplied the derivations and retains wiki/Goal/review responsibility. This worker wrote only this directory. A possible later joint-gamma degree-linear oracle is not implemented in this package.
