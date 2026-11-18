# C4-free subgraphs of hypercubes

## Current results

Here $\operatorname{ex}(Q_n,C_4)$ is the maximum edge count of a four-cycle-free subgraph of the $n$-dimensional hypercube, and $\pi_\square(C_4)$ is its limiting edge density.

| Case | Result | Proof and verification materials |
| --- | --- | --- |
| $Q_7$ | $\operatorname{ex}(Q_7,C_4)=304$ | [Manuscript](paper/hypercube-c4.pdf), [21 CNF instances, RUP checkers and a 304-edge witness](q7/) |
| $Q_8$ | $682\le\operatorname{ex}(Q_8,C_4)\le683$ | [Theorem B, exact rational certificate, 682-edge witness and replay instructions](q8/) |
| $Q_\infty$ | $\pi_\square(C_4)\le\frac{332729110702593}{562949953421312}$ (bound approximately 0.591045631464114) | [Proof, integer inputs and full replay](asymptotic/) |

The current manuscript, *Four-Cycle-Free Subgraphs of the Seven-Dimensional Hypercube*, presents the full proof of the $Q_7$ result. The $Q_8$ and asymptotic results each have a separate proof and verification materials linked above.

Source code, the manuscript and the smaller inputs are in the tree. The large finite proof traces and other large inputs are in [the artifact release](https://github.com/zhelizhou/hypercube-c4/releases/tag/artifacts-v0.1). Each result directory identifies which release assets it needs. The release includes a SHA-256 list for downloads.

## Compile the manuscript

From the repository root, use a local TeX Live installation, including from WSL:

~~~bash
latexmk -pdf -halt-on-error -outdir=.replay/paper paper/hypercube-c4.tex
~~~

The manuscript uses AMS-LaTeX, Latin Modern, and standard TeX Live LaTeX packages.
