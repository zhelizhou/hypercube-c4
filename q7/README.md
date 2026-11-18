# Seven-dimensional proof

The [paper](../paper/hypercube-c4.pdf) proves ex(Q₇, C₄) = 304. Its certificate appendix identifies the single degree-two obstruction (Lemma 3.1) and the ten symmetry cases for each of R0 and R1 (Lemma 3.2).

- [instances/](instances/) contains the 21 DIMACS inputs, two-hole orbits, hashes and archived checking reports.
- [tools/](tools/) contains the original PowerShell RUP checkers.
- [witness-304.json](witness-304.json) contains a local witness. See the introduction for attribution of the previously known lower bound.

With Python 3.11 or later, check the witness and all 21 formula hashes from the repository root:

~~~bash
python3 q7/verify.py
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
