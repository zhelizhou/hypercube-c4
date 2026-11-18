from pathlib import Path
import hashlib,json,datetime,re
T=Path(__file__).resolve().parents[1]
ROOT=T.parents[3]
R=T/'review'
NOW=datetime.datetime.now(datetime.timezone.utc).isoformat()
def digest(p):return 'sha256:'+hashlib.sha256(p.read_bytes()).hexdigest()
imports=[ROOT/'proofs/q8_single_three_cycle007/GENERAL_WEIGHTED_GATE.md',ROOT/'proofs/q8_single_three_cycle007/local_weighted/PROOF.md',ROOT/'proofs/q8_single_three_cycle007/local_weighted/TWO_LOW_EXTENSION.md',ROOT/'proofs/low1_cycle006/analytic/PROOF.md',ROOT/'proofs/low1_cycle006/Q8_BRIDGE.md',Path('q6_sources/q8_upper_independent/REFINEMENT_688.md'),Path('q6_sources/q8_upper_independent/REFINEMENT_K3.md'),T.parent/'q8_equality_profiles/main.tex']
primary=[T/n for n in ['main.tex','PROOF.md','PROOF_SKELETON.md','build_inputs.py','PROFILE_COVER.json','EDGE7_GENERATORS.json','CHECK.json','REVIEWER_ROUTE.json']]
references=[T.parent/'q8_equality_profiles/PROFILES.json',ROOT/'data/q8_seed682.edges',ROOT/'proofs/q8_single_three_cycle007/local_weighted/IMPORT_CHECK.json',ROOT/'proofs/q8_single_three_cycle007/local_weighted/TWO_LOW_CHECK.json',ROOT/'coevolve/AGENTS.md']
controls=[Path('/mnt/c/users/anony/desktop/project/math-rsi/.agents/skills/proof-checker/SKILL.md'),Path('/mnt/c/users/anony/desktop/project/math-rsi/.agents/skills/shared-references/reviewer-backends.md'),Path('/mnt/c/users/anony/desktop/project/math-rsi/.agents/skills/shared-references/assurance-contract.md'),Path('/mnt/c/users/anony/desktop/project/math-rsi/.agents/skills/shared-references/integration-contract.md'),Path('/mnt/c/users/anony/desktop/project/math-rsi/base/tools/reviewer_route.py')]
files=primary+imports+references+controls
hashes={str(p.relative_to(T)) if p.is_relative_to(T) else str(p):digest(p) for p in files}
# Stable source-ordered text spans, and one JSON unit for each entire row family.
units=[]
for p in [T/'main.tex',T/'PROOF.md',T/'PROOF_SKELETON.md',T/'build_inputs.py']+imports:
    rel=str(p.relative_to(T)) if p.is_relative_to(T) else str(p)
    lines=p.read_text().splitlines()
    for start in range(1,len(lines)+1,30):
        end=min(start+29,len(lines))
        units.append({'id':f'{rel}:L{start}-L{end}','path':rel,'start_line':start,'end_line':end,'sha256':digest(p),'covered':True,'method':'full source text read and semantic inspection'})
cover=json.loads((T/'PROFILE_COVER.json').read_text())
for m,item in cover.items():
    for typ in ['all_profiles','maximal_profiles']:
        units.append({'id':f'PROFILE_COVER.json:{m}/{typ}','path':'PROFILE_COVER.json','row_count':len(item[typ]),'covered':True,'method':'all records parsed; field, integer, budget, exact-set, and duplicate checks'})
for typ,rows in json.loads((T/'EDGE7_GENERATORS.json').read_text()).items():
    units.append({'id':f'EDGE7_GENERATORS.json:{typ}','path':'EDGE7_GENERATORS.json','row_count':len(rows),'covered':True,'method':'all rows parsed; independent complete weak-composition equality and endpoint action'})
units.append({'id':'q8_seed682.edges:all-682-lines','path':str(ROOT/'data/q8_seed682.edges'),'row_count':682,'covered':True,'method':'all literal edges; all 1024 ambient edges and 1792 coordinate squares tested'})
unit_ids=[u['id'] for u in units]
coverage={'declared_units':len(units),'covered_units':len(units),'fraction':1.0,'uncovered_unit_ids':[],'coverage_scope':'execution coverage of declared source spans and complete finite families; not a claim that mechanical coverage discovers every mathematical obligation','units':units,'shards':[{'shard_id':'fresh-review-single-leaf','assigned_unit_ids':unit_ids,'covered_unit_ids':unit_ids,'status':'completed','errors':[]}], 'max_shards':8,'max_concurrency_used':1,'recursion':False,'max_turns_requested':8,'enforcement':'prompt-only; no children spawned'}
(R/'SOURCE_UNITS.json').write_text(json.dumps(coverage,indent=2)+'\n')
results=json.loads((R/'INDEPENDENT_CHECK.json').read_text())
obligations=[
{'id':'O01','statement':'For every C4-free G subset Q8 with |E(G)|>=683 there exists an inclusion-maximal C4-free H containing G; m=|E(H)|>=|E(G)|.','dependencies':[],'hypotheses':'finite simple ambient Q8; edge additions preserve C4-freeness','discharged_by':'finite monotone extension in the 1024-edge ambient graph','status':'proved'},
{'id':'O02','statement':'For every such maximal H, each actual parity degree profile has n0=0.','dependencies':['O01'],'hypotheses':'inclusion-maximality, dimension8>0','discharged_by':'an added edge at an isolated root cannot create a cycle','status':'proved'},
{'id':'I01','statement':'For every C4-free coordinate Q6 and either specified actual parity, 4S+2c<=632+5L, with no opposite-degree hypothesis.','dependencies':['I316','I317','I321'],'hypotheses':'same actual parity in every face','discharged_by':'historical GENERAL_WEIGHTED_GATE.md §§1–2; accepted only as flagged import, not independently re-proved by this finite input review','status':'explicit historical assumption'},
{'id':'I316','statement':'Every C4-free Q6 whose specified parity has all degrees>=3 satisfies 2S+c<=316.','dependencies':[],'hypotheses':'specified-side minimum degree3 only; opposite side unrestricted','discharged_by':'historical REFINEMENT_688.md §2; six-case S<=158 family plus canonical three-full CNF; no replay in this review','status':'flagged historical import'},
{'id':'I317','statement':'Every C4-free Q6 with at most one specified-side degree<3 root satisfies 2S+c<=317.','dependencies':['I316'],'hypotheses':'all other specified roots degree>=3; arbitrary opposite degrees','discharged_by':'local_weighted/PROOF.md: one-low S<=158 import, canonical four-full geometry, safe one-star replacement, four-full/one-two S<=155 certificate, residue table','status':'historical proof chain inspected; computational premises retained as assumptions'},
{'id':'I321','statement':'Every C4-free Q6 with at most two specified-side degree<3 roots satisfies 2S+c<=321.','dependencies':['I316','I317'],'hypotheses':'all other specified roots degree>=3; arbitrary opposite degrees','discharged_by':'local_weighted/TWO_LOW_EXTENSION.md: safe single/simultaneous star replacement and four-full/two-two S<=157 certificate, then residue table','status':'historical proof chain inspected; computational premises retained as assumptions'},
{'id':'O03','statement':'For either actual P of every C4-free H, summing I01 over its 112 actual coordinate Q6 faces yields sum_d[40 choose(d,3)+2 choose(d,6)-5 l_d] n_d<=70784.','dependencies':['I01'],'hypotheses':'every restricted face is C4-free; induced P is one actual local parity','discharged_by':'each actual star has10 containing faces, each degree-d root choose(d,6) full appearances and l_d low appearances; all coefficients independently checked','status':'proved modulo I01'},
{'id':'O04','statement':'For every profile in O03, C(n)<=138432-201m, and hence m<=688.','dependencies':['O03'],'hypotheses':'sum n=128; sum dn=m; n>=0','discharged_by':'nine exact identities a_d-402d+1610=2C_d; all C_d nonnegative; floor division688','status':'proved modulo I01'},
{'id':'O05','statement':'For each actual P in every C4-free Q8, sum choose(d,3)n_d<=1792 and b(n)<=6912-10m.','dependencies':[],'hypotheses':'C4-freeness on actual coordinate Q3 faces','discharged_by':'two distinct same-parity roots of Q3 are distance2; their common neighbors force a square if both stars full; inject actual full stars into1792 faces','status':'proved'},
{'id':'O06','statement':'For every m in683..688, the saved all_profiles equals every nonnegative integer n in Z^9 with degree sums, C cap and b cap; maximal_profiles is exactly its n0=0 subset.','dependencies':['O04','O05','O02'],'hypotheses':'integer necessary relaxation, not graph realization','discharged_by':'unique n5,n6 elimination in proof; independently different B-budget complete enumeration matches all1468 all rows and1428 maximal rows','status':'proved exact arithmetic'},
{'id':'O07','statement':'Every ambient C4 through an edge uv lies in its unique coordinate Q2 for one external direction.','dependencies':[],'hypotheses':'simple Q8 cube adjacency','discharged_by':'two distinct neighbors of u differ in two axes and have exactly u and their XOR corner as common neighbors; all7168 vertex/axis-pair cases independently checked','status':'proved'},
{'id':'O08','statement':'In every C4-free H, a retained edge has no state7 completion, and a missing edge is blocked exactly when its seven-flag histogram has x7>=1. Thus maximality iff every missing edge has x7>=1.','dependencies':['O07'],'hypotheses':'all state indicators from same labeled H','discharged_by':'any newly created C4 contains the added edge, and every such C4 is a coordinate square','status':'proved'},
{'id':'O09','statement':'The missing maximal local relaxation has1716 size7 eight-state histograms with x7>=1; the retained relaxation has1716 seven-state size7 histograms; both are closed under endpoint reversal.','dependencies':['O08'],'hypotheses':'nonnegative integer multiplicities, sum7','discharged_by':'stars-and-bars bijection and complete independently generated weak compositions; actual flip swaps1/2 and5/6 only','status':'proved exact arithmetic'},
{'id':'O10','statement':'For every fixed actual H at its actual m, both profiles lie in that same-m cover, and alpha is half their point masses. Then N_d=2 sum_p alpha_p n_d(p). Each actual H lies in the convex union relaxation across all m.','dependencies':['O06'],'hypotheses':'same H; normalized alpha; local lambda and beta from same actual incidences','discharged_by':'finite pushforward/averaging identity; inclusion of each exact component in its convex hull','status':'proved as necessary-only statement; endpoint equations and any LP not supplied'},
{'id':'O11','statement':'The literal seed contains682 distinct legal edges, no retained square, and all342 missing edges are closed, with closure multiplicities3/4/5/6 at frequencies41/159/120/22.','dependencies':['O07'],'hypotheses':'the exact hashed seed file','discharged_by':'independent explicit square masks and complete missing-edge closure table','status':'proved finite check'}]
# Verify dependency DAG has no cycles among recorded node IDs.
byid={x['id']:x for x in obligations}
visited=set();active=set()
def dfs(k):
    if k in visited:return
    assert k not in active
    active.add(k)
    for d in byid[k]['dependencies']:dfs(d)
    active.remove(k);visited.add(k)
for k in byid:dfs(k)
ledger={'typed_symbols':{
'G,H':'finite simple subgraphs of labeled Q8; H contains G and is inclusion-maximal C4-free',
'm':'integer |E(H)|; not fixed before extension; conditional range683..688',
'P':'one fixed actual global parity, 128 vertices; P intersect F is the induced local parity',
'F':'one of112 labeled coordinate Q6 faces',
'S_F,c_F,L_F':'nonnegative integers: cubic star sum, local degree-six root count, local degrees<=2 root count on P intersect F',
'n_d':'nonnegative integer number of degree-d vertices in actual P; d in0..8; depends on H,P',
'l_d,C_d,b_d':'fixed exact degree-indexed coefficients listed in PROOF.md and independently recomputed',
'x_s':'nonnegative integer multiplicity of square state s among seven external directions of one oriented actual ambient edge',
'r':'bit for whether the same ambient root edge is retained',
'lambda':'Q4 local-type pushforward weights of one H; concrete normalization/bridge equations reserved to later model',
'alpha':'probability weights on complete maximal profile cover; actual H gives half its two same-m parity point masses',
'beta':'edge7 histogram pushforward weights of the same H; concrete root-mass normalization is not certified in this note',
'N_d':'global degree-d vertex count; N_d=n_d(P_even)+n_d(P_odd)=2 sum alpha_p n_d(p)'},
'obligations':obligations,'dependency_DAG_acyclic':True,'limits_or_interchanges':[],'uniformity':'all finite statements quantified over the complete stated graph/profile domain; no asymptotic, measure-theoretic, stochastic or limiting assertion',
'open_work':['assemble explicit normalized shared Q4/profile/edge7 incidence equations and endpoint bridges','obtain and replay any exact infeasibility certificate covering the full necessary union','connect that certificate to every683+ original counterexample before asserting ex(Q8,C4)<=682']}
(R/'OBLIGATION_LEDGER.json').write_text(json.dumps(ledger,indent=2)+'\n')
receipt={'reviewer_agent_id':'/root/review_maximal_counterexample_cover','requested_reviewer':{'backend':'codex','model':'gpt-6.1-sol','effort':'ultra','source':'explicit parent invocation'},'actual_reported_reviewer_model':None,'actual_reported_reviewer_effort':None,'model_identity_evidence':'native host supplied no server-attested returned model or effort fields; requested values are not substituted for actual evidence','review_independence':'same-family','acceptance_status':'provisional','fresh_context':True,'non_author':True,'source_units':coverage,'audited_input_hashes':hashes,'generated_at':NOW,'independent_checks':{'path':'INDEPENDENT_CHECK.json','sha256':digest(R/'INDEPENDENT_CHECK.json'),'status':'PASS','checks':len(results['checks'])},'scope':'necessary maximal-counterexample reduction and exact finite input coverage modulo explicitly retained historical Q6 imports; no LP, graph classification, or full682 bound','historical_traces_rerun':False,'tex_compilation':False,'render_html':False,'math_goal_status':'ex(Q8,C4)<=682 remains open; this reviewer does not alter any Goal'}
(R/'RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
report=r'''# Fresh proof-checker review: maximal-counterexample cover

**Verdict: PASS for the stated necessary reduction, modulo the explicit historical Q6 imports. Assurance is same-family / provisional.** No FATAL, CRITICAL, MAJOR or MINOR mathematical issue was found in the submitted scope. This does not prove `ex(Q8,C4) <= 682`, run an LP, certify any shared incidence model, classify realizable graphs, or establish a new numeric record. The intermediate ceiling 688 is weaker than the recorded historical 687 ceiling.

The requested route was native Codex, GPT-6.1 Sol, ultra. No returned model/effort identity is attested by this host, so the actual fields are null. This fresh non-author leaf spawned no children. Its read-only restrictions and eight-turn cap are prompt conventions, not tool-enforced limits. All output is confined to `review/`; primary inputs were not edited. HTML and TeX compilation were explicitly disabled.

## Coverage and deterministic evidence

I read the complete `main.tex`, `PROOF.md`, `PROOF_SKELETON.md` and `build_inputs.py`, parsed every saved profile and generator row, and read the actual historical generic gate and 316/317/321 sources listed below. `SOURCE_UNITS.json` records source-ordered contiguous spans for every primary text and whole row-family units for both inventories, with no uncovered unit. This is execution coverage, not a guarantee that a mechanical partition discovers every mathematical obligation. `RECEIPT.json` hashes the declared proof, inventories, seed and import/control files.

`independent_check.py` does not import or invoke the producer. It enumerates exceptional populations in reverse degree order using the independent **b budget**, completes an initially degree-six population by degree-five corrections, and compares exact rows and their recorded C/b values. It regenerates seven-flag histograms by weak compositions, and checks the seed through explicit coordinate-square edge masks. `INDEPENDENT_CHECK.json` contains every check.

|m|C cap|b cap|all integer rows|maximal n0=0 rows|
|---:|---:|---:|---:|---:|
|683|1149|82|814|783|
|684|948|72|393|385|
|685|747|62|171|170|
|686|546|52|66|66|
|687|345|42|20|20|
|688|144|32|4|4|

Every one of 1468 all-profile records and 1428 maximal-subcover records matches. The old exact-683 artifact is used only for a read-only equality comparison of its original unfiltered 814 rows; its filters are neither imported silently nor rerun. Both 1716-row edge7 inventories match independent complete weak compositions, with no duplicates. Reversing actual endpoints swaps states 1/2 and 5/6 and fixes 0,3,4,7; both families are closed under that action.

The exact seed SHA256 is `185d2857fa64b4ff8f53314363333f5ca1ee85c3560d254027d1b2e623c56a2c`. It contains 682 distinct cube edges and zero retained coordinate squares. All 342 missing edges are blocked, and their closing-square counts have frequencies **41,159,120,22** at **3,4,5,6**. The checker also evaluates every actual Q6 face of each actual seed parity and verifies all star/full/low incidence equalities. These evaluations are compatibility checks on that one seed and do not prove any historical Q6 theorem.

## Typed quantifiers and implication audit

`OBLIGATION_LEDGER.json` contains the complete typed symbol table, explicit quantified obligations and acyclic dependency DAG. The essential quantified chain is:

1. For **every** C4-free labeled `G subset Q8` with at least 683 edges, finite monotone addition gives **some** inclusion-maximal C4-free `H` containing G. Its actual `m` can increase. Conversely any such maximal H is itself a counterexample. Excluding all of these H is therefore target-equivalent. An isolated root cannot remain in H because adding an incident edge cannot create a cycle.
2. For **either actual global parity P**, each of its **112 actual Q6 restrictions** is C4-free with induced parity `P intersect F`; no opposite-degree assumption is added. Every actual cubic star has ten containing Q6 faces. A degree-d root is locally full in `choose(d,6)` faces and locally low in `l_d=(28,28,28,18,6,0,0,0,0)`. Literal free-coordinate subset enumeration checks these counts without relying on the displayed binomial formula.
3. Summing the historical interface gives `sum [40 choose(d,3)+2 choose(d,6)-5 l_d] n_d <= 70784`. All nine identities `a_d-402d+1610=2 C_d` hold. Using `sum n=128`, `sum d n=m` gives `C(P)<=138432-201m`. Nonnegative C gives `m<=688`; `m=689` would require `C<=-57`. Thus exactly six candidate edge-count layers must be covered.
4. In a coordinate Q3, distinct same-parity roots have distance two. Full stars at both would create the square through their two common neighbors. Therefore the 1792 actual faces injectively bound the one-parity star count, and `b(P)<=1792+40*128-10m=6912-10m`. No independence across local faces is assumed.
5. The seven nonzero-cost coordinates plus the two degree equations uniquely determine n5,n6. The written C-budget loop and the independently different b-budget loop enumerate precisely the declared integer relaxation. Restricting n0 to zero is justified only after maximal extension; every layer683..688 remains included.
6. Every cube C4 is a coordinate Q2: the two neighbors of a vertex on a simple four-cycle use two distinct directions, and their only other common neighbor is the XOR corner. The checker verifies all 7168 vertex/axis-pair instances. Thus a missing edge can be added exactly when none of its seven three-edge completions is full. For C4-free H, maximality is equivalent to a state7 completion at each missing edge. A retained edge forbids state7. The stars-and-bars counts1716/1716 and unrestricted missing count3432 follow exactly.
7. Every actual H supplies its own shared Q4 weights lambda, edge-histogram weights beta and both parity rows at the same actual m. In the stated convention, alpha is **half the sum of those two point masses**, and `N_d=2 sum alpha_p n_d(p)`. They may be distinct rows. Taking a convex hull across all same-m components and then across m is a weaker necessary relaxation. It is not graph realization, an exact disjunction, or a claim that maximal extension preserves683 edges. No concrete endpoint-bridge equations or normalization constants are supplied here, and none are certified by this audit.

Every inequality direction and hypothesis application in that chain is correct. The graph, face parity and endpoint action remain the same actual labeled objects throughout. There are no asymptotic claims, stochastic mode transitions, analytic interchanges or hidden limit orders.

## Historical import ledger

The scope is deliberately conditional; the deterministic inventory checks do not upgrade the following historical theorem/certificate assurance.

- `proofs/q8_single_three_cycle007/GENERAL_WEIGHTED_GATE.md`, sections1–2, states the arbitrary-degree interface `4S+2c<=632+5L`. Its L=0/1/2 cases use bounds316/317/321. At L=3, S<=160, c<=4 and `S congruent29+c mod3` give the listed322 maximum. At L>=4, 324 suffices. No degree restriction applies to the opposite parity. All these hypotheses are discharged when applied to an actual restricted face.
- **316:** actual `q6_sources/q8_upper_independent/REFINEMENT_688.md`, section2. Specified-side minimum degree three is essential here. Its historical six-case S<=158 theorem, congruence and additional canonical three-full-root CNF imply316. The new note does not directly impose this minimum degree on arbitrary faces. This review did not reconstruct or replay those original large families.
- **317:** complete `local_weighted/PROOF.md`, including the one-low S<=158 interface, full-code normalization, all exceptional-root positions, safe replacement proof and residue table. The one-low chain was inspected in `proofs/low1_cycle006/analytic/PROOF.md` and `Q8_BRIDGE.md`: unique-degree-two is an explicit historical17-case import; degree one has the analytic replacement argument; degree zero follows by a harmless edge addition. The actual `REFINEMENT_K3.md` section2 four-full/one-two bound is S<=155 with arbitrary position/directions and unrestricted opposite parity. The historical small reconstructed replay receipt reports1486 variables,5905 clauses and2618 additions; reading it is not a new replay or an independent acceptance of all Q6 inputs.
- **321:** complete `local_weighted/TWO_LOW_EXTENSION.md`. Its single-star obstruction locates the other low root in layer two; the simultaneous replacement with a distinct safe pair preserves S,c and all ordinary specified-side degrees. The actual `REFINEMENT_K3.md` section2 four-full/two-two bound is S<=157 with arbitrary exceptional positions and unrestricted opposite parity. The historical receipt reports1612 variables,6132 clauses and2801 additions. This review did not rerun that trace. The zero/one-low cases revert to their own bounds, and the two-low congruence table gives321.
- `q8_equality_profiles/main.tex` was read in full; only E01–E02/E05 are used for the local interface and old unfiltered finite cover. Its five extra exclusions and overlap filters are not assumptions of this new cover.

The safe-star arguments preserve one actual specified parity while allowing opposite-side degrees to change; that permission is exactly present in the imported interfaces. No circular dependency on the desired Q8 bound occurs.

## Boundary and mutation attacks

The audit actively tested the following failure modes.

- Keeping only m=683 omits nonempty necessary covers at every layer684..688. Even without asserting a graph realization of those rows, deleting them would break the declared complete cover of the necessary relaxation.
- Deleting one of the four m=688 boundary rows is detected by exact-set comparison. The negative cap at689 is checked exactly, so the last allowed layer is not dropped by rounding.
- Allowing x7=0 for missing edges admits1716 extra unblocked local histograms. Allowing state7 on a retained edge admits1716 square-creating local histograms. Both mutations are rejected.
- Independent endpoint flips cannot replace the single actual endpoint reversal; the exact state permutation is checked on every generator.
- Forcing alpha to a single profile row fails the algebra for two distinct same-m candidate rows. This is an averaging/typing attack, not a claim that either candidate is a realized683-edge graph. The actual seed has matching parity profiles, so it alone cannot test the two-distinct-row case; this limitation is explicit.
- Treating local feasible marginals as a graph, or treating a convex union as an exact disjunction, would reverse the necessary implication. The submitted text expressly rejects both inferences.
- Passing the 682-edge seed through the new maximality restriction confirms that the restriction does not discard the known lower example. It supplies no exclusion of larger graphs.

The independent review script initially used the seed as a candidate for unequal parity profiles; the seed profiles are equal, so that test correctly failed to demonstrate the intended distinction. The reviewer test was corrected to an explicit two-row same-m algebra check before the final receipt. This was a test-harness correction, not a source-proof defect. All final checks pass.

## Remaining work and exact acceptance boundary

The conditional necessary reduction and exact finite covers are sound in the reviewed scope. The historical imports remain flagged assumptions with their own original assurance. The shared normalized incidence model, endpoint bridge, exact infeasibility certificate and full original-domain certificate connection remain open. No LP feasibility/infeasibility, new construction, or upper bound682 is delivered here. The active main objective remains open.

Replay this review's deterministic checks with:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 review/independent_check.py
```
'''
(R/'REVIEW.md').write_text(report)
audit={'audit_skill':'proof-checker','verdict':'PASS','reason_code':'necessary_reduction_sound_modulo_flagged_imports','summary':'The complete maximal-counterexample reduction and exact finite inventories pass in scope, modulo explicitly retained historical Q6 imports; no LP or ex(Q8,C4)<=682 proof is supplied. Same-family provisional review, actual model identity unattested.','audited_input_hashes':hashes,'trace_path':'review/','agent_id':'/root/review_maximal_counterexample_cover','thread_id':None,'executor_model':None,'executor_family':None,'reviewer_model':None,'reviewer_family':None,'requested_reviewer_model':'gpt-6.1-sol','requested_reviewer_reasoning':'ultra','reviewer_reasoning':None,'reviewer_identity_source':'native host supplied no attested actual-model return','review_independence':'same-family','acceptance_status':'provisional','generated_at':NOW,'details':{'theorems_audited':2,'issues':[],'open_fatal':0,'open_critical':0,'scope_complete':True,'source_unit_coverage':1.0,'obligation_ledger':'review/OBLIGATION_LEDGER.json','coverage_receipt':'review/SOURCE_UNITS.json','review_receipt':'review/RECEIPT.json','independent_check':'review/INDEPENDENT_CHECK.json','deterministic_checks_passed':len(results['checks']),'historical_imports_retained':True,'historical_traces_rerun':False,'tex_compilation':False,'render_html':False,'LP_run':False,'main_goal_proved':False,'main_goal_status':'active/open','new_numeric_record_claimed':False,'uncovered_unit_ids':[],'open_obligations':ledger['open_work']}}
(R/'PROOF_AUDIT.json').write_text(json.dumps(audit,indent=2)+'\n')
# Verify no declared input was mutated during audit emission.
assert all(digest(p)==hashes[str(p.relative_to(T)) if p.is_relative_to(T) else str(p)] for p in files)
print(json.dumps({'verdict':audit['verdict'],'source_units':len(units),'checks':len(results['checks']),'source_hashes':len(hashes),'outputs':[p.name for p in R.iterdir()]},indent=2))
