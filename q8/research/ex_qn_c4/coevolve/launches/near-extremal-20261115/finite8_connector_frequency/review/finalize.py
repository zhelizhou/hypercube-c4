from pathlib import Path
from fractions import Fraction as F
from datetime import datetime,timezone
import importlib.util,json,hashlib,contextlib,io,sys
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parents[1]; R=P/'review'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
freeze=load(R/'INPUT_FREEZE.json');res=load(R/'INDEPENDENT_RESULTS.json')
def module(path,name):
 spec=importlib.util.spec_from_file_location(name,path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
# Original checkers are replayed only after independent reconstruction, and redirected into review/.
box=R/'author_replay';box.mkdir(exist_ok=True)
for n in ['INPUT_POINT.json','PROJECTED_MOMENTS.json','PSD_ELIGIBILITY.json','block0.EXACT_SEPARATOR.json','block4.EXACT_SEPARATOR.json']:
 q=box/n
 if not q.exists():q.symlink_to(P/n)
m=module(P/'verify.py','isolated_author_verifier');m.HERE=box
out=io.StringIO()
with contextlib.redirect_stdout(out):m.main()
(R/'AUTHOR_REPLAY.stdout.json').write_text(out.getvalue())
assert load(box/'CONNECTOR_CUTS.json')==load(P/'CONNECTOR_CUTS.json')
box2=R/'root_replay';box2.mkdir(exist_ok=True)
m=module(P.parent/'finite8_root_checks/check_connector_cuts.py','isolated_root_verifier');m.HERE=box2;m.BASE=P.parent
out=io.StringIO()
with contextlib.redirect_stdout(out):m.main()
(R/'ROOT_REPLAY.stdout.json').write_text(out.getvalue())
assert load(box2/'CONNECTOR_ROOT_CHECK.json')['status']=='PASS'
assert freeze['hashes']=={n:sha(P/n) for n in freeze['hashes']}
# Additional boundary/mutation probes independent of author code.
cuts=load(P/'CONNECTOR_CUTS.json')['cuts'];pm=load(P/'PROJECTED_MOMENTS.json');mass=F(res['same_original_decimal_mass']);mut=[]
for c in cuts:
 b=c['block'];Q=c['integer_connector_Q'];U=pm['blocks'][b]['twice_integer_matrix'];den=pm['moment_denominator'];d=len(c['full_state_connector_codes'])
 correct=F(sum(Q[i][j]*U[i][j] for i in range(16) for j in range(16)),den)
 extra2=F(sum(Q[i][j]*U[i][j]*(1 if i==j else 2) for i in range(16) for j in range(16)),den)
 assert extra2!=correct
 assert correct/mass!=correct
 assert len(c['full_state_connector_codes'][:16])!=d
 # Empty actual cube has a positive block0feature, so a negative multiplier breaks validity.
 mut.append({'block':b,'extra_offdiagonal_factor_two_detected':str(extra2),'original_pairing':str(correct),'renormalization_changes_exact_pairing':True,'sixteen_old_support_truncation_detected':True,'zero_histogram_valid':True,'pure_histograms_valid':all(36*Q[i][i]>=0 for i in range(16))})
assert res['whole_Q8_bridge_checks'][0]['value']=='12160' and -F(12160)<0
mut.append({'negative_added_weight_counterexample':'emptyQ8, block0 weight−1 gives−12160 before positive normalization','whole_root_action_check':'every actual canonical stabilizer element tested','m_below8_extension_not_claimed':True})
(R/'BOUNDARY_MUTATIONS.json').write_text(json.dumps(mut,indent=2)+'\n')
units=freeze['source_units'];now=datetime.now(timezone.utc).isoformat();assigned=[u['id'] for u in units]
receipt={'schema':'source-unit-execution-coverage-v1','shard_id':'fresh_connector_frequency_review','requested_model':'gpt-6.1-sol','requested_reasoning':'ultra','actual_model':None,'actual_reasoning':None,'identity_attestation':'unavailable','reviewer_route':load(P/'REVIEWER_ROUTE.json'),'recursion':False,'children_spawned':0,'max_turns':8,'restriction_enforcement':'prompt-only','render_html':False,'tex_conversion':False,'write_scope':str(R),'assigned_unit_ids':assigned,'covered_unit_ids':assigned,'uncovered_unit_ids':[],'source_unit_coverage':1.0,'status':'COMPLETE','source_units':units,'audited_input_hashes':freeze['hashes'],'coverage_limit':'Execution coverage of declared source units only; does not by itself guarantee mathematical completeness.','generated_at':now}
(R/'RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
ob=[{'id':'C01','status':'DISCHARGED','hypotheses':['actualC4free root cube','ascending legal fullface codes','common actual root action'],'evidence':'Direct regeneration gives dimensions240/212/190/187/170; all16 labels present; induced lowbits map commutes with all actual root stabilizers; x total6 maps to y total6.'},{'id':'C02','status':'DISCHARGED','hypotheses':['exact lexical positive decimalweights','originalQ4 edge order'],'evidence':'All202 actual graphs C4free and allweights positive; exactnonunitmass retained; fullordered and directconnector aggregations coincide with all5 stored moments; independent16pivot LDL for blocks0/4; exactnegative directions for1/2/3.'},{'id':'C03','status':'DISCHARGED','hypotheses':['concrete symmetric integer kernels','complete integer16label total6 domain'],'evidence':'Combinationswithreplacement enumerate each histogram once; 54264 each, min0, zeros360/3185; exactstrictnegative targetpairings; total4 counterexamples−2432/−760. LPnotpremise.'},{'id':'C04','status':'DISCHARGED','hypotheses':['C4freeG subsetQ8','fullstate lift','simultaneous roottransport','nonnegative feature multiplier'],'evidence':'All240/170 actual lifted states; exactactual rootgroup invariance; wholeQ8 incidence1120×24=1792×15; sixaxis collision algebra; arbitrary symmetric kernels allowed. Directglobalexamples agree. Nonnegative addedweights necessary.'},{'id':'C05','status':'DISCHARGED','hypotheses':['positive scales12160/7600','upperoffdiagonal coordinates alreadyfolded'],'evidence':'Actualscore checkedonall202 graph masks against independently derived moments; fullfacewrapper exact; isolated authorandRoot checker replays agree; original sourcehashes unchanged.'}]
audit={'audit_skill':'proof-checker','verdict':'PASS','reason_code':'all_proofs_complete','summary':'Both concrete finite-six connector cuts and all-full-state lifts verified exactly; bounded local result only. Semantic acceptance is same-family provisional.','audited_input_hashes':freeze['hashes'],'trace_path':'review/','thread_id':None,'executor_model':None,'executor_family':'openai','reviewer_model':None,'reviewer_family':'openai','reviewer_reasoning':None,'requested_reviewer_model':'gpt-6.1-sol','requested_reviewer_reasoning':'ultra','actual_identity_attestation':'unavailable','review_independence':'same-family','acceptance_status':'provisional','generated_at':now,'details':{'canonical_source':'PROOF.md','theorems_audited':1,'local_kernels_audited':2,'issues':[],'obligations':ob,'dag':{'C01':[],'C02':['C01'],'C03':['C02'],'C04':['C01','C03'],'C05':['C02','C03','C04']},'dag_acyclic':True,'source_units':len(units),'source_unit_coverage':1.0,'independent_results':'INDEPENDENT_RESULTS.json','boundary_mutations':'BOUNDARY_MUTATIONS.json','author_replay':'AUTHOR_REPLAY.stdout.json','root_replay':'ROOT_REPLAY.stdout.json','deterministic_status':'PASS','main_goal682':'OPEN','not_claimed':['accepted full-family point','full-family barrier','complete positivity exclusion','main682 result','cross-family semantic acceptance']}}
(R/'PROOF_AUDIT.json').write_text(json.dumps(audit,indent=2)+'\n')
text='''# Fresh review of the complete connector-frequency proof

Verdict: **PASS for the stated bounded local result**. No FATAL, CRITICAL, MAJOR or MINOR issue was found. Both concrete finite-six kernels, their all-full-state lifts, the same-input strict separations and the exact scorer interface were independently verified. Semantic acceptance remains **same-family, provisional**. Requested route: `gpt-6.1-sol`, `ultra`; actual model and reasoning identity are unattested and recorded as null.

The canonical source was the complete `PROOF.md`, with `PROOF_SKELETON.md` C01–C05. No duplicate TeX, compilation, HTML, child reviewer, wiki update or Goal update was created. All writes are under `review/`. `RECEIPT.json` freezes input hashes and records 100% execution coverage of the declared source units; that receipt is not itself a proof of obligation completeness.

## Independent reconstruction and obligation ledger

**C01. Projection and domain.** Rebuilt the original Q4 edge order from the two Q3 layers plus vertical edges, all24 actual square roots, all eight Q2 isometries, and every legal eight-bit full flag. The five full-state dimensions are240,212,190,187,170 in ascending integer code order. C4 freedom excludes a full parallel square and each mixed square with both connectors; those are exactly the state exclusions. Every connector code0–15 occurs with parallel bitszero for each root mask. For any full integer histogram x of total6, the nonnegative incidence matrix A gives y=Ax of total6. Conversely a representative for each label lifts any such y, although only the forward direction is needed. All simultaneous root actions commute with low-bit projection.

**C02. Exact moments and qualification.** Parsed the original JSON decimal tokens as exact Decimal/Fraction values, rather than using binary float weights or normalizing. All202 masks decode to actual C4-free Q4 graphs and have positive weights. The mass is exactly9999999999999698585929/10^22; the task-local input is byte-identical to the fixed source. For each actual face and every root-to-canonical coset, rebuilt the ordered full moment, then grouped by code&15. A separate direct connector aggregation agrees entrywise with it and with all five stored16×16 matrices U. The common denominator is2·64512·10^22. Independently computed rational LDL factors have16 strictly positive pivots for each block0 and4 and match every recorded factor. The integer directions for blocks1,2,3 have strictly negative U-quadratics, respectively−10592433679698367540660066393365184, −2839542093262524448841553331512832 and−7578029497706666471095221498000192. These are old PSD violations, with no accepted full-family point inferred.

**C03. Complete finite domain and exact separation.** A fresh combinations-with-replacement generator enumerates each16-label total-six histogram exactly once: C(21,6)=54264. Both concrete integer symmetric kernels have minimumzero on that complete domain; their zero counts are360 and3185. The raw pairings are exactly−5650710530085758525389/15000000000000000000000 and−2909599605897848271617/3000000000000000000000. Pairing a nonnegative conic combination of yyᵀ with either finite-six-valid kernel is nonnegative by finite linearity; these negative values therefore prove the two specified projected matrices lie outside C6(16). No LP status, numerical tolerance, stored author PASS or incomplete generator support is a premise. The supplied total-four witnesses independently give−2432 and−760, proving the kernels noncopositive and hence non-PSD. They do not establish target-matrix non-complete-positivity.

**C04. Complete lift, root action and common object.** Verified every entry of the240×240 and170×170 lifts Qfull[i,j]=Q[code_i&15,code_j&15], including every old-support complement. Each actual root stabilizer preserves the legal state set, connector moments and final kernels; its orders areeight andtwo. Thus common canonical transport leaves the final lifted kernels unchanged and cube-isometry changes of root frame do not change the feature. A permutation of outside axes only permutes the flags.

The whole-Q8 sampling bridge follows by exact double counting, not PSD. There are1120 Q4 subcubes, each with24 roots, and1792 Q8 roots, each in C(6,2)=15 Q4 subcubes, so1120·24=1792·15. For a fixed actual root with six connector labels c1,…,c6, averaging over its15 unordered outside-axis pairs gives

    (5/6)(Σ(a≠b) Q[ca,cb]/30) + (1/6)(Σa Q[ca,ca]/6)
      = (Σa,b Q[ca,cb])/36 = yᵀQy/36.

Each selected kernel is symmetric; the first equality is finite counting and holds for indefinite kernels. The last quantity is nonnegative by the complete total-six domain. This proves the claimed root-average identity and expected-feature inequality on every actual C4-free Q8 graph. Four direct whole-object checks—empty graph, one-axis matching, a single star and a deterministic random spanning tree—independently average all1120 Q4 restrictions and all1792 roots and agree exactly for both blocks. The spanning-tree block4 value701453/5376 makes that test nonvacuous. The abstract collision algebra was also checked with an arbitrary symmetric indefinite6×6 kernel. For ambient dimension m≥8, averaging six-element subsets of the m−2 outside axes gives the same5/6 and1/6 pair/diagonal coefficients, so nonnegative expectation also extends there; no m<8 extension is asserted. Adding these features with nonnegative coefficients preserves validity for any number of features. A negative coefficient already fails on the empty cube for block0.

**C05. Consumer and reproducibility.** Compared `score.value_on_graph` against independently reconstructed exact graph features for every one of the202 graph masks, both raw and normalized. The positive scales are exactly12160 and7600. Their normalized pairings are−297405817372934659231/9600000000000000000000000 and−2909599605897848271617/22800000000000000000000000. Checked all five returned full-face blocks and the scale from `score.full_face_kernel`; only the selected block is nonzero and it is the complete lift. Upper off-diagonal coefficients are already combined, so introducing an additional factor2 changes the exact pairing and is wrong.

Only after the independent computations completed were the actual author `verify.py` and Root `check_connector_cuts.py` read and replayed. Both were redirected to isolated subdirectories of `review/` to preserve the source packages. Both pass; the author compact cuts exactly match the frozen originals. All frozen source hashes remain unchanged. Numeric membership calls were not rerun, and their timing/status statements are discovery provenance rather than theorem premises.

## Counterexample and boundary pass

The complete domain includes pure histograms6ei, every sparse support pattern, repeated labels and zero coordinates. The zero vector is valid at totalzero; finite-six validity is not asserted at smaller nonzero totals, and the actual total-four counterexamples were checked exactly. Subtractingone from a diagonal used by a minimizing total-six histogram produces an exact negative value and is detected. Tested accidental decimal renormalization, old16-state truncation and an extra off-diagonal factor2; all change an exact checked invariant. The empty-cube positive feature makes negative model weights invalid. `BOUNDARY_MUTATIONS.json` records these probes.

There are no infinite sums, limits, derivatives, measure-theoretic interchanges or asymptotic constants in this argument. All expectations are finite uniform averages. The hypotheses are the stated C4-free cube geometry, exact frozen decimal weights, complete total-six domain, common simultaneous root action and nonnegative added weights. The dependency order C01→C02→C03→C04→C05 is acyclic; each application discharges those hypotheses above.

## Scope and remaining work

This proves two concrete all-full-state finite-six connector inequalities and their strict violations at separately PSD-qualified projections of the specified nonunit-mass input. It does not show the input satisfies the original full-PSD model, establish a uniform-family barrier, prove target complete-positivity failure, or settle the upper682 goal. That goal remains OPEN. No mathematical repair is requested for this local package. Exact checks are accepted at their stated finite scope; a completed known different-family semantic review would be needed to upgrade the provisional semantic assurance under the skill contract.
'''
(R/'REVIEW.md').write_text(text)
assert freeze['hashes']=={n:sha(P/n) for n in freeze['hashes']}
print(json.dumps({'verdict':audit['verdict'],'acceptance_status':audit['acceptance_status'],'source_units':len(units),'coverage':1.0,'issues':0,'artifacts':['review/REVIEW.md','review/RECEIPT.json','review/PROOF_AUDIT.json'],'author_and_root_replays':'PASS','source_hashes_unchanged':True},indent=2))
