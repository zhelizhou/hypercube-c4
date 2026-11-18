# Independent review of the analytic one-degree-one Q6 lemma

2026-11-07. Reviewer: `/root/audit_q8`, independent of the author.

**Verdict: PASS, with the historical unique-degree-two theorem as an explicit accepted import.** The new analytic argument excludes both S=160 and S=159 under its exact one-sided hypothesis. No new SAT result is needed for this argument. This review does not replay or re-prove the historical unique-degree-two certificate family.

Final reviewed source `../PROOF.md` has SHA256

`39e1f9a86971aed331185ce01711a2f507cc4dd95290e123b1bb9fc20569995d`.

The complete proof and complete `check_layers.py` were read, together with the actual source statement and certificate-domain explanation in `q6_sources/q8_upper_independent/REFINEMENT_688.md`, Section 1. All twelve author integer rows were read and independently reconstructed. The review writes only in this directory.

## 1. Exact hypothesis, historical import, and ordinary vertices

The new lemma assumes precisely one degree-one vertex u on a specified parity P of a C4-free Q6, with **all other 31 vertices of P of degree at least three**. There is no restriction on the opposite parity. All ordinary P vertices are accounted for after translating u to the empty set: fifteen two-subsets, fifteen four-subsets, and the one six-subset. Their lower degree bound is not silently dropped.

The actual unique-degree-two source has exactly the required one-sided interface: one specified-side degree-two vertex, the other 31 specified-side degrees at least three, and the opposite side unrestricted. Its stated S=160 encoding has no upper-degree-five restriction. Its S=159 domain has sixteen hole orbits, and its inventory comprises seventeen cases. This interface is read from the mathematical source, not inferred from a PASS status or transferred from a 688-edge purification statement.

The import remains a historical computational dependency. The current review verifies its use, not its millions of old proof steps.

## 2. Root-star replacement really forces the thirty layer edges

Fix any two distinct coordinate directions i,j. Replace the entire incident edge set at u by exactly these two root edges, deleting the old root edge if necessary. Every newly created C4 must use a new edge, hence contain u. Since the new root degree is two, there is only one possible such square: the i,j square. It exists exactly when both remote edges from the two-subset {i,j} to its singleton subsets are present.

If either remote edge is absent, the replacement graph is C4-free and satisfies the imported theorem. Only u changes its degree within P; every other endpoint of a changed root edge lies in the opposite parity. The other 31 specified-side degrees therefore remain at least three. The cubic contribution of u is zero both before and after the change, so the specified-side sum S is unchanged. The opposite-side degree changes are permitted by the import.

Thus in any counterexample with S>=159 both remote edges must be present for **every** pair i,j. These are precisely the thirty distinct layer-one/layer-two edges. This argument does not require the existing edge at u to be among i,j, does not assume saturation, and does not normalize different faces independently.

## 3. Star injection, layer counts, and disjoint holes

Every coordinate Q3 has at most one full P-centered three-star: two same-parity centers in a Q3 are distance two and would retain their common square. Therefore S counts occupied Q3s and h=160−S counts holes. Two full P vertices cannot be distance two. Among any five purported full vertices, the pairwise-distance lower bound is 40, whereas six coordinates contribute at most 36; hence c<=4. The residue `S≡31+c (mod 3)` is correct because ordinary degrees 3,4,5 contribute 1 modulo 3 and degree 6 contributes 2. This gives c in {0,3} at S=160 and c=2 at S=159.

A two-subset s has its two downward edges forced, so its ordinary degree lower bound gives `1<=t_s<=4`. A three-subset cannot retain two downward parents: the two parents share a singleton, whose two forced incident edges complete a C4. Hence a Q3 containing the empty set has a full P star exactly when its top three-subset has one retained parent. Summing gives `sum t_s=20−alpha`.

The fifteen two-subsets yield `z2+2z3+3z4=5−alpha`; two occurrences of t_s=4 would already cost six, proving z4<=1. Both displayed binomial-weight identities for S2 and `sum C(t_s,2)` are correct.

For each four-subset R, its four Q3 faces with singleton bases contain P vertices only at layers two and four. A two-subset with both upward edges present gives a star on exactly the two faces based at its two elements. The top R gives C(b_R,3) stars. Star injection therefore proves the exact identity

`2t_R+C(b_R,3)=4−h_R`.

The sixty faces in this sum are distinct: their singleton base and four-element top uniquely determine the face. They are disjoint from the twenty empty-base faces counted by alpha. Thus alpha+beta<=h; in particular a single hole may also be in a different layer, correctly represented by alpha=beta=0 when h=1.

For h_R=0 the only options are (b_R,t_R)=(4,0), or b_R<=2 with t_R=2. For h_R=1 the only option is (3,1). Every pair of upward edges at a two-subset determines exactly one four-subset, so summing gives `5−alpha+z3+3z4=30−2a−beta`. There is no duplicated hole or independently chosen face completion in these sums.

## 4. Upward capacities and all zero/one-hole branches

If two backward-full four-subsets are adjacent upward to the same five-subset, they share a three-subset and form a C4 with it. Thus the sum F of their upward degrees is at most six, without any degree condition on the six opposite-parity five-subsets. Their star weights are exactly `4+6f+4*1[f=2]`. A full top forces every four-subset to have f<=1, by the square through its two upward neighbors. The equation `c=z4+c4+1[top full]` accounts for every possible full P vertex.

At S=160, alpha=beta=0 and the parity/count equations leave exactly the two displayed z profiles. A full top would force c=z4+1<=2, inconsistent with c in {0,3}. The two nonfull-top upper bounds 151 and 154 are correct and strictly exclude S=160.

At S=159 with a full top, c=2 forces z4=1,c4=0. The three possibilities (alpha,beta)=(1,0),(0,0),(0,1) are all addressed: the first violates the parity equation, while the other two give upper bounds 144 and 147. None is omitted.

At S=159 with nonfull top, c4=2−z4 and the bound

`S<=144−3alpha+6beta+3z3+6z4`

follows by adding valid separate upper bounds on disjoint vertex groups. Its complete seven-row integer reduction agrees with the source table. The unique row that can reach 159 has alpha=0,beta=1,z=(13,0,1,1),a=10,c4=1, and top degree five.

Equality forces one f=2 backward-full vertex, the unique exceptional b=3 vertex with f=2, and all four remaining ordinary non-backward-full vertices to have b=f=2. These are **six distinct** four-subsets in disjoint categories. The degree-five top has exactly one missing five-subset neighbor W0. Every f=2 four-subset must be adjacent to W0, since otherwise its two retained upward edges and the two retained top edges form a C4. There are only C(5,4)=5 four-subsets of W0. The resulting 6>5 contradiction is valid and closes the sole equality branch.

## 5. Independent finite checks

`check_independent.py` imports none of the author's program. It performs three discriminating checks:

1. It starts from all 65,536 masks on the sixteen upper Q4 edges, then imposes the at-most-one-parent condition. Exactly 4096 remain, of which 3715 are C4-free. Actual stars in the four singleton-base Q3 faces satisfy the stated identity in every case. The near-full type counts match the author's 370 cases exactly. Root-to-singleton edges are absent in this finite check; those edges do not belong to these four tested faces, and the actual root's at-most-one retained edge cannot introduce a C4. This is the correct local identity scope.
2. It independently enumerates the integer layer equations with **actual top degree 3,4,5,6**, rather than merging degrees at most five into the degree-five upper bound. It obtains 32 rows and exactly one upper-bound survivor. Projecting to the degree-five/six upper-bound rows reproduces all twelve author rows exactly.
3. It enumerates all six labeled choices of the unique missing top edge and finds exactly five eligible four-subsets for f=2 each time. The equality branch requires six.

Results are `independent_checks.json`; all 32 rows are saved in `all_actual_top_degree_branches.json`. These checks substantiate finite identities and arithmetic. The preceding written review supplies the normalization, coverage, and import connection; finite program success is not used as a substitute for those arguments.

## 6. Original-Q8 consequence and scope

The stated caller is correct, conditional on the separately reviewed 687-edge Q8 gate. The remaining degree-two parity has histogram n2=1,n5=77,n6=50 and h8=22. Of the 28 Q6 faces containing its degree-two root, omitted-coordinate pairs give local degrees zero,one,two in counts 1,12,15 respectively. The other 84 faces do not contain the root. All other specified-side vertices stay at degree at least three because their global degree is five or six.

The historical minimum-three and unique-degree-two imports supply h_F>=2 on 84+15=99 faces; the new L1 supplies it on twelve more. The sole degree-zero face still has nonnegative hole count. Every global Q3 lies in C(5,3)=10 Q6 faces, giving

`220=10h8=sum h_F>=2*(99+12)=222`,

a contradiction. No assumption is made on opposite-side low vertices. Thus this caller excludes the degree-two branch, while the degree-three branch and the final Q8 tightening remain separate obligations.

## 7. Disposition and hashes

The only issue reported during review was a rendering defect: five occurrences of U+0008 followed by `eta` appeared where beta was intended. The author replaced those with literal LaTeX `\beta` and supplied the final hash above. No mathematical change was requested or made. The final file has no stray control characters.

No substantive mathematical defect was found. The theorem is accepted within its exact one-sided hypothesis and explicit unique-degree-two import. This is not a claim that L1 also permits another degree-one/two vertex on the specified side, or that the thirty forced edges hold in a two-low-root problem. Those would change the imported interface and require a new proof.

Reproduce only the new independent finite checks:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 check_independent.py
```

`REVIEW_RECEIPT.json` binds the final author proof, source import, complete author checks, and new review artifacts. No author source, shared record/wiki, old trace, or MathRSI file was modified by this reviewer.
