# Asymptotic upper bound

The [proof](proof.pdf) bounds the limiting edge density by 332729110702593 / 562949953421312, approximately 0.591045631464114.

The final seven-dimensional score certificate, all its integer inputs, and both compatibility searches are in this directory. [The proof and replay notes](证明与复算.txt) describe the scoring identities, coverage arguments, thresholds, and exact normalization. [receipt.json](receipt.json) records the frozen result and parameters.

Replay in a fresh working copy on little-endian Linux or WSL with Python 3 and a C++20 compiler supporting OpenMP and `__int128`:

~~~bash
mkdir -p .replay
cp -a asymptotic .replay/asymptotic
cd .replay/asymptotic
OMP_NUM_THREADS=8 python3 verify.py
~~~

The expected final line begins with `PASS upper = 332729110702593/562949953421312`. A complete replay includes a multi-hour exhaustive computation. Earlier four-, five-, and six-dimensional certificates are available as separate [release assets](https://github.com/zhelizhou/hypercube-c4/releases/tag/artifacts-v0.1). [notes/](notes/) discusses restricted configurations and related research directions.
