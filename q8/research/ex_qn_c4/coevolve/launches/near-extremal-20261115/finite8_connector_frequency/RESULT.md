# Return: two all-full-state connector-frequency cuts

Same input:202-weight completed-edge-stage point, SHA223b58046502fdd7eae1847fc6fc9ab3f27dfbeca9c1f1647b14f06a54d28aa9. Its exact decimal lambda was preserved, not renormalized or replaced.

Five connector projections were rebuilt. Blocks0/4 are exact16×16 positive-LDL matrices; blocks1/2/3 have old-PSD negative directions and were not used as new frequency findings.

The two PSD-qualified blocks both fail complete C6(16). Their final integer kernels pass all54264 histograms, minimum0, and have exact negative target pairings. Both lift to every legal240/170 full state via flagcode&15, with no outside-support or outsideJ repair. Explicit smaller-total negative vectors show the kernels are non-PSD/non-copositive.

**CONNECTOR_CUTS.json** and **score.py** are the compact consumer interface. Positive scales are12160/7600. Use nonnegative feature weights in the same-lambda model; the PSD-only Gram validity rule is insufficient.

**PROOF.md** gives the whole-Q8 caller. **verify.py** independently rebuilt all projected geometry, exact PSD eligibility, complete histogram domains, full-state lifts and strict pairings; **VERIFICATION.json** records PASS.

No optional degree-incidence extension, extra LP, old-file edit or upper682 claim. The source point was not an accepted feasible point or graph. No process remains.
