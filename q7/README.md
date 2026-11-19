# Seven-dimensional proof

The [paper](https://github.com/zhelizhou/hypercube-c4/blob/main/paper/hypercube-c4.pdf) proves ex(Q₇, C₄) = 304. Section 4 covers the degree-two obstruction A and the ten symmetry cases for each of R0 and R1.

- [instances/](instances/) contains the 21 DIMACS inputs, two-hole orbits, hashes and archived checking reports.
- [generate_cnf.py](generate_cnf.py) regenerates the 21 inputs byte for byte using only the Python standard library.
- [tools/](tools/) contains the original PowerShell RUP checkers.
- [witness-304.json](witness-304.json) contains a local witness. See the introduction for attribution of the previously known lower bound.

With Python 3.11 or later, check the witness and all 21 formula hashes from the repository root:

~~~bash
python3 q7/verify.py
~~~

To regenerate the CNFs into a new directory:

~~~bash
python3 q7/generate_cnf.py --out .replay/cnf
~~~

To also check the trace hashes, extract the three trace archives from the [artifact release](https://github.com/zhelizhou/hypercube-c4/releases/tag/q7-artifacts-v0.1) into `q7/instances/`. These commands require authenticated GitHub CLI access and tar with Zstandard support:

~~~bash
gh release download q7-artifacts-v0.1 --pattern 'q7-*-traces.tar.zst' --dir .artifacts
for archive in .artifacts/q7-*-traces.tar.zst; do
    tar --zstd -xf "$archive" -C q7/instances
done
python3 q7/verify.py --traces
~~~

For full proof replay, with PowerShell 7 available to Python:

~~~bash
python3 q7/verify.py --replay
~~~

This checks the hashes, runs the matching checker in a temporary directory, and compares the verified addition counts. All 21 traces have 14,205,184 verified additions, including the empty clauses. Use `--case A` or `--case R0:0` to check a single refutation. The independent encoder audits in `instances/` can also run in a working copy, where they write new reports.

The [external replay record](drat-trim-replay.md) identifies the archived traces cross-checked with DRAT-trim in RUP-only mode.
The released checkers also have a small acceptance and rejection suite:

~~~bash
python3 q7/tools/test_checkers.py
~~~
