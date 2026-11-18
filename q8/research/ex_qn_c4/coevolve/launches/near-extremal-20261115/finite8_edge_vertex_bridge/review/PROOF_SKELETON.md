# Proof skeleton and typed obligation map

The complete semantic review is in `REVIEW.md`; the exact structured inventory is in `SEMANTIC_OBLIGATIONS.json`.

All hypotheses refer to a single actual spanning C4-free Q8 graph. Maximality, parity restrictions and fixed edge counts are unused.

- **O01** (P01): The vertex-fixed axis action yields exactly nine states with the stated retained-incidence counts.
  Uses: definitions only. Discharge: Enumerated all15 legal labelled square codes under the single actual axis-swap permutation; read literal graph projections.
- **O02** (P01): An edge histogram recovers both full endpoint degrees and both actual vertex-square states. C has total mass14.
  Uses: O01. Discharge: All5148 histograms independently realized as literal C4-free graphs; all162 entries rebuilt from actual endpoint degrees/14 observations.
- **O03** (P01): C is invariant under one synchronized endpoint reversal.
  Uses: O02. Discharge: A root reversal swaps the two endpoints and bits0/1 together. All5148 reversed columns compared exactly.
- **O04** (P02): For each d,j and r, the actual incidence sum equals k_j or2−k_j times the vertex-state count.
  Uses: O02, O03. Discharge: Explicit bijection (v,unordered pair,one incident ambient root edge). Nine actual graphs/all162 equations checked exactly.
- **O05** (P02): Normalized incidence gives mu=2E_beta C_all and the36 integer mixed-state balances.
  Uses: O04. Discharge: 1024/256=4 and two root choices. Direct integer C_all=2T checked; B36 exported with retained-minus-missing sign.
- **O06** (P03): At a degree-d vertex the three state-group sums are choose(8−d,2),d(8−d),choose(d,2).
  Uses: O01. Discharge: Choose missing/retained incident directions. All vertices of nine graphs checked, including both parities and degrees0/8.
- **O07** (P03): M5(lambda)=E_gamma[xxT]/784 on all81 entries.
  Uses: O01. Discharge: Global completion multiplicities1/5/15 times local ordered weights360/72/24 are uniformly360; denominators checked. All1120 restrictions per calibration rebuilt.
- **O08** (P03): The27 degree-group beta/lambda equations have factor392.
  Uses: O05, O06, O07. Discharge: Multiply the pointwise group sum by the same x_i, take finite sums and use784/2=392; independently rebuilt B27 and all calibration pairings.
- **O09** (P04): The packed diagonal/off-diagonal selector satisfies Wf=2R-group and2304B27 beta=7WF.T lambda.
  Uses: O08. Discharge: Constructed all27x45 W entries separately; exact392/(2*64512)=7/2304; all14090x45 actual stored feature coefficients independently rebuilt.
- **O10** (P04): For any newly priced legal graph column with the same packed contract, the correct new L column is196Wf.
  Uses: O09. Discharge: Universal linear algebra196*(2Rgroup)=392Rgroup; additionally exercised31 legal out-of-pool single-edge columns.
- **O11** (P05): The universal domain is the5148 total-seven histograms in the original frozen order.
  Uses: O02. Discharge: Independent separator enumeration sorted by expanded state sequences matches every actual source histogram;3432+1716 counts and all boundaries included.
- **O12** (P05): All old/current stored duplicate classes preserve C, B36 and B27; the actual column adapters and all frozen orders are correct.
  Uses: O08, O11. Discharge: Every old class member checked over5148 inputs; every current member checked over3202 retained inputs. Actual current3432 list/1751 selected indices mapped by histograms. All row/column orders and all sparse exports mirrored exactly. The actual682 seed current-class beta and same1120-slice lambda satisfy the packed consumer exactly.
- **O13** (P06): The finite actual-graph and boundary calibration claims and stated mutation rejections hold.
  Uses: O04, O07, O09. Discharge: Nine independent whole-Q8 graph runs;1024 edge/256 vertex/1120 restriction observations each; all five specified mutations rejected.
- **O14** (P06): The stored master050 decimal-rational tuple violates the new necessary equations with the reported exact maxima.
  Uses: O09, O12. Discharge: All63 exact row residuals rebuilt directly from original serialized decimals and literal local graphs, no renormalization; maxima recorded in INDEPENDENT_RESULTS.json.
- **O15** (P00, P05, P06, P07): The conclusion is scoped to universal necessary identities and specified finite interfaces; main682 remains OPEN.
  Uses: O08, O10, O12, O14. Discharge: Complete statement/conclusion and README/interface scope checked. No row-rank63, complete-Q4 classification, pruning-theorem, realizability, numerical NO or Lean claim inferred.

Dependency topological order: O01, O02, O06, O07, O03, O11, O04, O05, O08, O09, O12, O10, O13, O14, O15. No cycles.
No limits, asymptotics, measure-theoretic interchanges or solver-status premises occur.
The coverage receipt establishes that all frozen source units were consumed; it does not itself prove validity.
