# DRAT-trim cross-check

The replay used [DRAT-trim at `2e3b2dc0ecf9`](https://github.com/marijnheule/drat-trim/tree/2e3b2dc0ecf938addbd779d42877b6ed69d9a985) on the archived CNFs and traces. It returned `s VERIFIED` and reported zero RAT lemmas in its backward-checking core for 21 of the 21 inputs.

For each row, set `stem` to the listed file stem and append its options to this command:

~~~bash
drat-trim "q7/instances/$stem.cnf" "q7/instances/$stem.drup" OPTIONS
~~~

The `-U` switch enables RUP-only checking. With `-p`, the checker keeps deleted clauses. The backward check verifies a refutation using the clauses it needs. The [forward replay](README.md) checks all recorded additions.

| Case | File stem | Options | Result |
| --- | --- | --- | --- |
| A | `star_q6_def0_root2_flushed` | `-p -U -t 360` | Verified |
| R0:0 | `star_rigidity_p0_b4_case0_odd_degrees_cert` | `-p -U -t 360` | Verified |
| R0:1 | `star_rigidity_p0_b4_case1_odd_degrees_cert` | `-U -w -t 3600` | Verified |
| R0:2 | `star_rigidity_p0_b4_case2_odd_degrees_cert` | `-U -w -t 3600` | Verified |
| R0:3 | `star_rigidity_p0_b4_case3_odd_degrees_cert` | `-U -w -t 3600` | Verified |
| R0:4 | `star_rigidity_p0_b4_case4_odd_degrees_cert` | `-U -w -t 3600` | Verified |
| R0:5 | `star_rigidity_p0_b4_case5_odd_degrees_cert` | `-U -w -t 3600` | Verified |
| R0:6 | `star_rigidity_p0_b4_case6_odd_degrees_cert` | `-U -w -t 3600` | Verified |
| R0:7 | `star_rigidity_p0_b4_case7_odd_degrees_cert` | `-U -w -t 3600` | Verified |
| R0:8 | `star_rigidity_p0_b4_case8_odd_degrees_cert` | `-U -w -t 3600` | Verified |
| R0:9 | `star_rigidity_p0_b4_case9_odd_degrees_cert` | `-U -w -t 3600` | Verified |
| R1:0 | `star_rigidity_p1_b8_case0_odd_degrees_cert` | `-U -w -t 120` | Verified |
| R1:1 | `star_rigidity_p1_b8_case1_odd_degrees_cert` | `-U -w -t 3600` | Verified |
| R1:2 | `star_rigidity_p1_b8_case2_odd_degrees_cert` | `-U -w -t 3600` | Verified |
| R1:3 | `star_rigidity_p1_b8_case3_odd_degrees_cert` | `-U -w -t 3600` | Verified |
| R1:4 | `star_rigidity_p1_b8_case4_odd_degrees_cert` | `-U -w -t 3600` | Verified |
| R1:5 | `star_rigidity_p1_b8_case5_odd_degrees_cert` | `-U -w -t 3600` | Verified |
| R1:6 | `star_rigidity_p1_b8_case6_odd_degrees_cert` | `-U -w -t 3600` | Verified |
| R1:7 | `star_rigidity_p1_b8_case7_odd_degrees_cert` | `-U -w -t 3600` | Verified |
| R1:8 | `star_rigidity_p1_b8_case8_odd_degrees_cert` | `-U -w -t 3600` | Verified |
| R1:9 | `star_rigidity_p1_b8_case9_odd_degrees_cert` | `-U -w -t 3600` | Verified |
