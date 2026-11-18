# Review checker development notes

The required universal checks passed in the first independent run. An optional extra calibration then attempted to use the seed's literal Q4 restriction codes as direct frozen-pool indices. That reviewer-side assumption was false: raw mask `2330631527` is absent, and the attempt raised `KeyError: 2330631527` at the pool lookup. This was a checker adaptation error, not a counterexample to the proof or its general raw-lambda identity.

I corrected only the review checker by constructing the actual 384 Q4 cube-frame automorphisms from all axis permutations and XOR translations. The example mask reaches stored mask `126318580` under axis permutation `(2,0,1,3)` and XOR `5`. Every actual seed restriction has a stored frame representative, and every transported packed 45 column was compared entry by entry. The final successful run records all transports. No original package or numerical-author file changed.

This optional calibration checks only the vertex feature and the new incidence/moment bridge. It is not an audit of numerical-author aliases for the full six-block feature matrix, and it is not required to justify the universal proof. The literal 1120 restriction proof/calibration and frozen 14090 feature comparison remain separate required checks.
