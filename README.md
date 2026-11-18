# C4-free subgraphs of hypercubes

This repository accompanies *Finite and Asymptotic Bounds for C4-Free Subgraphs of Hypercubes*. The current manuscript includes the introduction and the complete seven-dimensional proof. The dimension-eight and asymptotic proofs and replay materials are available in their own directories.

| Result | Proof and checking instructions |
| --- | --- |
| $\operatorname{ex}(Q_7,C_4)=304$ | [Manuscript](paper/hypercube-c4.pdf), [21 CNF instances, RUP checkers and a 304-edge witness](q7/) |
| $682\le\operatorname{ex}(Q_8,C_4)\le683$ | [Theorem B, exact rational certificate and four replay modes](q8/) |
| $\pi_\square(C_4)\le332729110702593/562949953421312$ | [Proof, integer inputs and full replay](asymptotic/) |

Source code, the manuscript and the smaller inputs are in the tree. The large finite proof traces and other large inputs are in [the artifact release](https://github.com/zhelizhou/hypercube-c4/releases/tag/artifacts-v0.1). Each result directory identifies which release assets it needs. The release includes a SHA-256 list for downloads.

## Compile the manuscript

From the repository root, use a local TeX Live installation, including from WSL:

~~~bash
latexmk -pdf -halt-on-error -outdir=.replay/paper paper/hypercube-c4.tex
~~~

The manuscript uses AMS-LaTeX, Latin Modern, and standard TeX Live LaTeX packages.
