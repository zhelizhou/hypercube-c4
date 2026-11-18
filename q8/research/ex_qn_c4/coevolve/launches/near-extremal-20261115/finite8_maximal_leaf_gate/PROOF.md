# A maximal leaf gate from the same actual graph

## Exact statement and proof

Let H be an inclusion-maximal C4-free spanning subgraph of Q8. Suppose v has degree one, with unique neighbor w=v xor 2^j. For every direction i different from j, the edge from v to t=v xor 2^i is missing. Maximality says that adding it creates a square. Every square containing this added edge uses another coordinate k; its other edge at v must be retained, so k=j. Consequently the other two edges

    w -- (w xor 2^i),  (w xor 2^i) -- t

are both retained. These seven forced edges at w together with vw show d(w)=8.

Use the existing edge-state convention s=a+2b+4c for the three external edges, where a is incident to the first endpoint and b to the second. On the retained root oriented (v,w), all seven a's are zero and all seven b's and c's are one. Thus every state is6. With the opposite orientation every state is5. This is stronger than merely requiring the leaf's neighbor to have degree8: it also forces all seven remote connectors.

Two distinct leaves cannot have the same neighbor. Otherwise write them v=w xor 2^j and z=w xor 2^k, j != k, and put t=w xor 2^j xor 2^k. The edge vt is missing because v is a leaf. Its only possible completed square on addition uses v's unique existing edge vw, and therefore must also use wz and zt. But zt is absent because z is a leaf adjacent only to w. This contradicts maximality. Hence mapping each leaf to its unique neighbor injects the leaves into full degree-eight vertices.

Writing N_d for the global degree counts and N_d(P) for an actual parity's degree counts gives

    N1 <= N8,
    N1(P) <= N8(opposite P).

These statements use neither the edge count nor historical Q6 inequalities. They apply to every maximal graph, including every m in683..688 from the separate maximal reduction. They do not imply the generally unjustified single-parity inequality N1(P)<=N8(P).

## Exact retained-root generator filter

For a retained-edge histogram x on states0..6 with sum x=7 define

    A=sum (s&1)x_s,   B=sum ((s>>1)&1)x_s.

The endpoint degrees are1+A and1+B. Keep the histogram exactly when

    (A !=0 or x6=7) and (B !=0 or x5=7).

This is a necessary filter on complete actual retained-root generators; it does not claim every kept histogram extends to a graph. Each endpoint-leaf condition corresponds exactly to the preceding lemma. Endpoint reversal exchanges states1/2 and5/6, swaps A/B, and exchanges the two clauses. The filter is therefore invariant under the same C2 action as the existing moment model.

Complete exact enumeration of all1716 retained-root histograms removes230 and leaves1486. The missing-root maximality inventory of1716 histograms is unchanged. `GENERATORS.json` contains every original row, its decision, connector counts, and all kept rows. No LP was run.

## Existing deduplication and model rows

The actual producer `../finite8_degree_augmentation/prepare_maximal_scope.py` deduplicates on the exact64 symmetrized quadratic-moment numerators and18 endpoint-degree numerators. For root1 the nonzero part of this key is

    (x_i*x_j + x_flip(i)*x_flip(j)) for0<=i<=j<=6,
    counts of the two endpoint degrees1+A,1+B.

All other key entries are the same zeros for every root1 generator. The new checker reconstructs this integer key directly, rather than importing the producer or running its solver. There are918 root1 classes. No class contains both a kept and a removed histogram. Thus pruning the corresponding old dedup classes is safe; rebuilding deduplication after the full-histogram filter is also safe. A representative-only filter without this check would not establish preservation of the entire old class. Root0 classes cannot mix with root1 classes because their disjoint moment blocks have nonzero total mass.

The global inequality is a row on the existing profile alpha variables. If alpha describes the average of the two actual parity profiles (or any convex combination preserving their average), then eta_d=sum alpha*n_d=N_d/2. Hence

    sum alpha*(n1-n8) <=0.

`ALPHA_GLOBAL_ROW.json` gives that integer coefficient for every maximal profile row at every m683..688, in the original per-m order. This is a coupled row on the alpha mixture; do NOT delete every individual profile with n1>n8, since the opposite parity may supply the compensating full vertices.

For completeness an equivalent retained-root beta row uses integer coefficient

    8*(1[A=0]+1[B=0]) - (1[A=7]+1[B=7]).

Summing over actual retained ambient edges gives exactly8*(N1-N8), since each degree-one vertex occurs once and each degree-eight vertex occurs eight times. Under the existing beta normalization by1024 the same expression is8*(N1-N8)/1024; its sign is unchanged. Root0 beta coefficients are zero. Each saved retained generator includes this coefficient. This beta inequality follows from the profile inequality and the complete endpoint bridge when that bridge is imposed exactly. The pure5/6 generator pruning supplies the additional remote-connector information.

## Positive calibration with genuine leaves

Begin with the15 edges01 and, for i=1..7,

    (1,1 xor 2^i), (2^i,1 xor 2^i).

The checker verifies literal C4-freeness and that every missing edge at0 already closes a square. Process all ambient edges in the deterministic order of their smaller numeric endpoint and coordinate; add an edge exactly if no square would be completed. Blocked edges stay blocked under additions, so one pass gives a maximal C4-free graph. The edge01 remains the unique edge at0 because all seven alternatives were already blocked.

The produced graph has576 edges, leaves0 and131, and their distinct full neighbors1 and3. Its global degree counts for d=0..8 are

    (0,2,14,42,70,70,42,14,2).

The two oriented leaf-root histograms are pure6 at(0,1) and pure5 at(3,131). Every retained edge passes the new filter. Every missing ambient edge closes at least one square. `CALIBRATION.edges` saves the complete actual graph; `CHECK.json` records the literal counts and SHA256. This is a positive test of the leaf-containing domain, not a dense construction claim and not a counterexample to any target.

Reproduce with `python3 check_leaf_gate.py`. It writes only this new directory, reads the older profile cover without modifying it, and starts no LP or historical job. The mathematical lemma is elementary and self-contained; exact enumeration supports only the stated finite coverage and calibration. No682 upper bound is claimed.
