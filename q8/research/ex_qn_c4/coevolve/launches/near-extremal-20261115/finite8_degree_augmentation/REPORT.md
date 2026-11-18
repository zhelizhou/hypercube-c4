# Completed first genuine degree/flag augmentation

Read BRIDGE_AND_RESULT.md for the proof, exact LP model, evidence and full-Q4 oracle obligation.

- Frozen actual792-profile snapshot, SHA256452aa0e377ac002ae5687cd83268de253290e378e00a552c1f9e70840b6ce945. Later791 not substituted.
- Proved exact common root/direction sampling bridge; one lambda supplies all five hypergeometric marginals and all six finite8 moment matrices. One alpha is a convex relaxation of the actual two parity rows.
- Actually ran818 and separately1160 legal-Q4 primal pools. Both were infeasible before negative-eigenvector cuts; independently removing all PSD constraints still gives histogram-only infeasibility.
- Exact separator, checked on every pool graph and every frozen profile: local u(K)=3h4-h0-h2<=0, whereas the same coupled distribution requires E u>=3/112. No floating tolerance is an acceptance premise.
- Exact regression on all1120 restrictions of the actual682 seed verified histogram and k-star identities j,k=0,...,4.

Actual commands (cwd this directory, dependencies loaded explicitly from ../finite8_flags/deps):

```bash
PYTHONDONTWRITEBYTECODE=1 python3 coupled_lp.py
PYTHONDONTWRITEBYTECODE=1 python3 separate_marginals.py
PYTHONDONTWRITEBYTECODE=1 python3 coupled_1160_lp.py
PYTHONDONTWRITEBYTECODE=1 python3 separate_1160_marginals.py
PYTHONDONTWRITEBYTECODE=1 python3 check_bridge.py
```

All final commands exited0. The first bridge-regression assertion had an extra aggregate normalisation factor and exited1; it was corrected to the exact unnormalised double count. LP equations were already correct and unchanged. This error/correction is disclosed in BRIDGE_AND_RESULT.md.

No primal point exists on these restricted supports; no graph or full-domain NO is claimed. Root's next step is full legal-Q4 separation of u=3h4-h0-h2, adding actual violating columns if any. The requested first informative LP predicate is resolved; no stronger even-square gate or blind rerun was started. Root owns current wiki and final integration.
