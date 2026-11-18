# C4-free subgraphs of hypercubes

## Current results

Here ex(Qₙ, C₄) is the maximum edge count of a four-cycle-free subgraph of the n-dimensional hypercube.

| Case | Result | Repository materials |
| --- | --- | --- |
| Q₇ | ex(Q₇, C₄) = 304 | [q7/](q7/) contains 21 CNF instances, RUP checkers, a 304-edge witness, and replay instructions. |
| Q₈ | 682 ≤ ex(Q₈, C₄) ≤ 683 | [q8/](q8/) contains the upper-bound proof, exact rational certificate, 682-edge witness, and replay programs. |
| Asymptotic | Limiting edge density ≤ 332729110702593 / 562949953421312. The bound is approximately 0.591045631464114. | [asymptotic/](asymptotic/) contains the proof, integer certificate inputs, and exhaustive verification programs. |

The Q₇ manuscript, [*Four-Cycle-Free Subgraphs of the Seven-Dimensional Hypercube* (PDF)](paper/hypercube-c4.pdf), is in [paper/](paper/).

The [artifact release](https://github.com/zhelizhou/hypercube-c4/releases/tag/artifacts-v0.1) contains the large Q₇ and Q₈ proof traces, additional Q₈ inputs, and earlier asymptotic certificates. Each result directory lists the files needed for replay. The release includes SHA-256 checksums for all downloads.
