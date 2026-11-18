# Eight-dimensional upper bound

Theorem B proves ex(Q₈, C₄) ≤ 683. Minamoto's [682-edge construction](https://arxiv.org/abs/2603.29127v5) gives the other end of the interval. An [edge list](research/ex_qn_c4/data/q8_seed682.edges) for the lower bound is included.

- [Proof of Theorem B](research/ex_qn_c4/coevolve/launches/near-extremal-20261115/finite8_degree_augmentation/pool_B684plus_enriched8/B684_EXCLUSION.md)
- [83 active constraints and their sources](research/ex_qn_c4/coevolve/launches/near-extremal-20261115/finite8_degree_augmentation/pool_B684plus_enriched8/B684_ACTIVE_83_PARAMETERS.md)
- [Six-dimensional inequality and its finite cases](research/ex_qn_c4/coevolve/launches/near-extremal-20261115/finite8_q6_import_audit/PROOF.md)
- [Four-dimensional enumeration source](research/ex_qn_c4/coevolve/launches/near-extremal-20261115/finite8_full_oracle_independent/independent_q4.cpp)
- [Exact coefficient reconstruction source](research/ex_qn_c4/coevolve/launches/near-extremal-20261115/finite8_root_checks/reconstruct_exact_dual.py)

## Reproduce

Run the commands from the repository root on Linux or WSL. The quick criterion check and complete four-dimensional enumeration use the tracked inputs. The reconstruction and six-dimensional replay also need [q8-upper683-data.tar.zst](https://github.com/zhelizhou/hypercube-c4/releases/download/artifacts-v0.1/q8-upper683-data.tar.zst), which contains the 25 DRAT traces and larger inputs listed in [release-data-files.txt](release-data-files.txt).

~~~bash
gh release download artifacts-v0.1 --pattern 'q8-upper683-data.tar.zst' --dir .artifacts
tar --zstd -xf .artifacts/q8-upper683-data.tar.zst -C q8
python3 q8/verify_bundle.py --all
~~~

Use a new output directory for each replay:

| Check | Command | Dependencies |
| --- | --- | --- |
| Re-evaluate the exact contradiction from the recorded complete transcript | `python3 q8/replay.py quick --out .replay/q8-quick` | Python 3.10+ |
| Recompile and enumerate the full four-dimensional domain | `python3 q8/replay.py q4 --out .replay/q8-q4` | Python, C++17 compiler |
| Reconstruct the rational certificate and compare the frozen coefficient files | `python3 q8/replay.py reconstruct --out .replay/q8-reconstruct` | Python, [NumPy and SciPy](requirements.txt), release data |
| Reconstruct and check the 25 finite proofs of the local six-dimensional inequality | `python3 q8/replay.py q6 --out .replay/q8-q6` | Python, Bash, C++17 compiler, release data |

The complete four-dimensional check reports 13,150,453 marked completions and raw maximum −37,440. The exact safe margin is 782808475930428709/4209067950080000000000. The six-dimensional replay checks 4,383,882 additions.

[MATERIALS_MANIFEST.json](MATERIALS_MANIFEST.json) inventories the files carried over for reproduction. The [original handoff validation](validation/HANDOFF_VALIDATION.md) records the checks performed in the larger source archive. The [Theorem B proof audit](research/ex_qn_c4/coevolve/launches/near-extremal-20261115/finite8_degree_augmentation/pool_B684plus_enriched8/PROOF_AUDIT.md) describes the scope of that review.
