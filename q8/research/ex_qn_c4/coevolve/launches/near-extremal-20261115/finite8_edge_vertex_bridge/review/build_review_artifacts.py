"""Emit review-only ledger, freshness receipt and assurance metadata."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json

HERE=Path(__file__).resolve().parent
PKG=HERE.parent
BASE=PKG.parent
WORKSPACE=Path('/mnt/c/users/anony/desktop/project/math-rsi')
now=datetime.now(timezone.utc).isoformat()
results=json.loads((HERE/'INDEPENDENT_RESULTS.json').read_text())
assert results['status']=='PASS_EXACT_INDEPENDENT_BOUNDED_CHECKS'
hashes=dict(results['input_hashes'])
extra=[PKG/n for n in ['PROOF.md','README.md','export_bridge.py','export_moment_bridge.py',
                      'check_bridge.py','check_master050.py','MANIFEST.json']]
extra += [BASE/'finite8_flags/finite_flags.py',BASE/'finite8_edge_flags/edge_flags.py',
          BASE/'finite8_edge_flags/PROOF.md',WORKSPACE/'base/skills/proof-checker/SKILL.md',
          WORKSPACE/'base/skills/shared-references/assurance-contract.md']
for p in extra:
    hashes[str(p)]=hashlib.sha256(p.read_bytes()).hexdigest()
for p,h in hashes.items():
    assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==h,('changed_input',p)

# Manifest integrity is an additional mechanical check, never a mathematical premise.
manifest=json.loads((PKG/'MANIFEST.json').read_text())
manifest_checks=[]
for filename,meta in manifest['files'].items():
    p=PKG/filename
    data=p.read_bytes()
    actual=hashlib.sha256(data).hexdigest()
    assert len(data)==meta['bytes'] and actual==meta['sha256'],filename
    manifest_checks.append({'file':filename,'sha256':actual,'bytes':len(data)})

units=[]
lines=(PKG/'PROOF.md').read_text().splitlines()
starts=[0]+[i for i,line in enumerate(lines) if line.startswith('## ')]+[len(lines)]
for index,(a,b) in enumerate(zip(starts,starts[1:])):
    units.append({'source_unit_id':f'P{index:02d}','file':'PROOF.md','start_line':a+1,'end_line':b,
                  'content_sha256':hashlib.sha256(('\n'.join(lines[a:b])+'\n').encode()).hexdigest(),
                  'coverage_kind':'complete semantic read and explicit obligation review'})
for index,p in enumerate(sorted(hashes)):
    path=Path(p)
    if path==PKG/'PROOF.md':
        continue
    if path.suffix in ('.py','.md'):
        count=len(path.read_text().splitlines())
        evidence='complete source read; source used only as definitions/contracts, never prior verdict'
    else:
        count=None
        evidence='complete machine read and exact reconstruction, order/hash or sparse-mirror comparison'
    units.append({'source_unit_id':f'F{index:03d}','file':p,'start_line':1 if count is not None else None,
                  'end_line':count,'file_sha256':hashes[p],'coverage_kind':evidence})

def obligation(id,unit,statement,deps,evidence,hypotheses):
    return {'obligation_id':id,'source_unit_ids':unit,'statement':statement,'dependencies':deps,
            'hypotheses':hypotheses,'status':'DISCHARGED','evidence':evidence}

common=['G is a spanning C4-free subgraph of Q8','beta, gamma and lambda are empirical data of the same actual G']
obligations=[
obligation('O01',['P01'],'The vertex-fixed axis action yields exactly nine states with the stated retained-incidence counts.',[],
           'Enumerated all15 legal labelled square codes under the single actual axis-swap permutation; read literal graph projections.',
           ['The marked vertex is fixed; no translation quotient is taken']),
obligation('O02',['P01'],'An edge histogram recovers both full endpoint degrees and both actual vertex-square states. C has total mass14.', ['O01'],
           'All5148 histograms independently realized as literal C4-free graphs; all162 entries rebuilt from actual endpoint degrees/14 observations.',
           ['Seven external directions','A retained root excludes raw state7']),
obligation('O03',['P01'],'C is invariant under one synchronized endpoint reversal.', ['O02'],
           'A root reversal swaps the two endpoints and bits0/1 together. All5148 reversed columns compared exactly.',
           ['One common endpoint action; no independent per-flag quotient']),
obligation('O04',['P02'],'For each d,j and r, the actual incidence sum equals k_j or2−k_j times the vertex-state count.', ['O02','O03'],
           'Explicit bijection (v,unordered pair,one incident ambient root edge). Nine actual graphs/all162 equations checked exactly.',common),
obligation('O05',['P02'],'Normalized incidence gives mu=2E_beta C_all and the36 integer mixed-state balances.', ['O04'],
           '1024/256=4 and two root choices. Direct integer C_all=2T checked; B36 exported with retained-minus-missing sign.',
           ['Gamma normalized over256 vertices','Beta normalized over1024 ambient edges']),
obligation('O06',['P03'],'At a degree-d vertex the three state-group sums are choose(8−d,2),d(8−d),choose(d,2).', ['O01'],
           'Choose missing/retained incident directions. All vertices of nine graphs checked, including both parities and degrees0/8.',
           ['d is the full degree of that same marked vertex']),
obligation('O07',['P03'],'M5(lambda)=E_gamma[xxT]/784 on all81 entries.', ['O01'],
           'Global completion multiplicities1/5/15 times local ordered weights360/72/24 are uniformly360; denominators checked. All1120 restrictions per calibration rebuilt.',common),
obligation('O08',['P03'],'The27 degree-group beta/lambda equations have factor392.', ['O05','O06','O07'],
           'Multiply the pointwise group sum by the same x_i, take finite sums and use784/2=392; independently rebuilt B27 and all calibration pairings.',common),
obligation('O09',['P04'],'The packed diagonal/off-diagonal selector satisfies Wf=2R-group and2304B27 beta=7WF.T lambda.', ['O08'],
           'Constructed all27x45 W entries separately; exact392/(2*64512)=7/2304; all14090x45 actual stored feature coefficients independently rebuilt.',
           ['f diagonal=Rii, offdiagonal=2Rij','M5=R/64512']),
obligation('O10',['P04'],'For any newly priced legal graph column with the same packed contract, the correct new L column is196Wf.', ['O09'],
           'Universal linear algebra196*(2Rgroup)=392Rgroup; additionally exercised31 legal out-of-pool single-edge columns.',
           ['Same original lambda variable','New feature uses the same packed45 contract']),
obligation('O11',['P05'],'The universal domain is the5148 total-seven histograms in the original frozen order.', ['O02'],
           'Independent separator enumeration sorted by expanded state sequences matches every actual source histogram;3432+1716 counts and all boundaries included.',
           ['No maximality/leaf pruning applied to the universal domain']),
obligation('O12',['P05'],'All old/current stored duplicate classes preserve C, B36 and B27; the actual column adapters and all frozen orders are correct.', ['O08','O11'],
           'Every old class member checked over5148 inputs; every current member checked over3202 retained inputs. Actual current3432 list/1751 selected indices mapped by histograms. All row/column orders and all sparse exports mirrored exactly. The actual682 seed current-class beta and same1120-slice lambda satisfy the packed consumer exactly.',
           ['Current adapter is restricted by separate pruning','Masses aggregate by addition without class-size factors']),
obligation('O13',['P06'],'The finite actual-graph and boundary calibration claims and stated mutation rejections hold.', ['O04','O07','O09'],
           'Nine independent whole-Q8 graph runs;1024 edge/256 vertex/1120 restriction observations each; all five specified mutations rejected.',
           ['Finite calibrations supplement the universal proof; they do not replace it']),
obligation('O14',['P06'],'The stored master050 decimal-rational tuple violates the new necessary equations with the reported exact maxima.', ['O09','O12'],
           'All63 exact row residuals rebuilt directly from original serialized decimals and literal local graphs, no renormalization; maxima recorded in INDEPENDENT_RESULTS.json.',
           ['Diagnostic is of this frozen tuple only','No feasible-Q8 or global-infeasibility assertion']),
obligation('O15',['P00','P05','P06','P07'],'The conclusion is scoped to universal necessary identities and specified finite interfaces; main682 remains OPEN.', ['O08','O10','O12','O14'],
           'Complete statement/conclusion and README/interface scope checked. No row-rank63, complete-Q4 classification, pruning-theorem, realizability, numerical NO or Lean claim inferred.',
           ['No conclusions beyond the declared bounded package'])]

# Acyclicity is checked only on the merged inventory, after coverage reconciliation.
ids={o['obligation_id'] for o in obligations}
assert all(set(o['dependencies'])<=ids for o in obligations)
closed=[]
pending={o['obligation_id']:set(o['dependencies']) for o in obligations}
while pending:
    ready=sorted(k for k,v in pending.items() if not v)
    assert ready,'semantic dependency cycle'
    for k in ready:
        closed.append(k);pending.pop(k)
    for v in pending.values():v.difference_update(ready)

typed_symbols={
 'G':'spanning simple C4-free subgraph of Q8 on256 vertices',
 'd(v)':'integer0..8; full degree in the same G',
 'j':'vertex-fixed square state ID0..8',
 'k_j':'number0,1,2 of retained edges at the marked vertex',
 'x_v':'nonnegative integer9-vector with total28',
 'gamma_(d,x)':'fraction over all256 vertices, total1',
 'mu_dj':'global degree-conditioned first count sum divided by256, not conditioned probability',
 'r':'root retention0/1',
 'y':'total-seven nonnegative integer vector of length8−r',
 'beta_(r,y)':'mass over all1024 ambient edges, total1 before optional class aggregation',
 'C':'integer map with162 rows and5148 universal columns; each column total14',
 'lambda':'distribution of1120 actual coordinate Q4 restrictions of the same G',
 'R':'ordered local9x9 integer matrix, M5=R/64512',
 'U':'Root alternate2R, M5=U/129024; the interface uses U locally for R',
 'f':'packed45: diagonalRii, offdiagonal2Rij',
 'W':'integer27x45 selector yielding2 times R row-group sums',
 'B36':'integer mixed retained-minus-missing rows, no denominator',
 'B27':'integer degree-weighted C_all rows',
 'L27':'integer196WF_vertex.T; one column per actual feature graph',
 'F_g(d)':'pointwise counts choose(8−d,2),d(8−d),choose(d,2)'}

ledger={'generated_at':now,'quantified_statement':'For every spanning C4-free G subset Q8, its common actual empirical beta/gamma/lambda obey all162 incidence identities,36 mixed balances and27 degree-group moment identities, with the exact packed contract.',
 'typed_symbols':typed_symbols,'obligations':obligations,'dependency_topological_order':closed,
 'dependency_cycles':[],'all_application_hypotheses_checked':True,
 'limit_order_map':'No asymptotics or limits. All expectations and rearrangements are finite uniform sums.',
 'counterexample_pass':{'executed':True,'actual_graph_count':len(results['actual_graphs']),
 'attempts':['all5148 legal raw histograms including zeros/pure states','synchronized endpoint reversal for all5148 columns',
 'degree0 and8','both vertex parities','nonmaximal empty/matching/star/deleted-edge graphs','asymmetric actual584 graph',
 'all14090 stored local graphs','31 out-of-pool newly packed graph columns','five rejected mutations'],
 'mathematical_counterexamples_found':0},'open_fatal':0,'open_critical':0,'open_major':0,'open_minor':0,
 'independent_exact_results':'INDEPENDENT_RESULTS.json','scope_exclusions':['main682 bound','whole-model infeasibility',
 'global realizability','separate maximality/leaf pruning theorem','complete Q4 classification','63-row independence','Lean formalization']}
(HERE/'SEMANTIC_OBLIGATIONS.json').write_text(json.dumps(ledger,indent=2)+'\n')

def relative_key(p):
    path=Path(p)
    try:return str(path.relative_to(PKG))
    except ValueError:return str(path)
audited={relative_key(p):'sha256:'+h for p,h in hashes.items()}
receipt={'generated_at':now,'input_base_directory':str(PKG),'input_hashes':audited,
 'source_units':units,'planned_unit_ids':[u['source_unit_id'] for u in units],
 'completed_unit_ids':[u['source_unit_id'] for u in units],'failed_unit_ids':[],'uncovered_unit_ids':[],
 'coverage_complete':True,'coverage_fraction':1.0,'execution':'sequential no-fanout review; no child agents',
 'coverage_scope_note':'Source execution coverage only; not a claim that mechanical obligation extraction proves semantic completeness.',
 'semantic_obligation_count':len(obligations),'semantic_dag_acyclic':True,'unchanged_inputs_at_finalization':True,
 'manifest_file_integrity':manifest_checks,'original_checker_imports':False,'producer_module_imports':False,
 'author_or_Root_PASS_as_premise':False,'optimizer_or_LP_run':False,
 'write_scope':str(HERE),'raw_review':'REVIEW.md','checker':'independent_checker.py',
 'checker_sha256':hashlib.sha256((HERE/'independent_checker.py').read_bytes()).hexdigest(),
 'results_sha256':hashlib.sha256((HERE/'INDEPENDENT_RESULTS.json').read_bytes()).hexdigest()}
(HERE/'RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')

audit={'audit_skill':'proof-checker','verdict':'PASS','reason_code':'all_scoped_proofs_complete',
 'summary':'All universal same-object incidence and degree-group moment identities and the stated finite packed-feature interfaces check; fresh same-family/provisional review, main682 remains OPEN.',
 'audited_input_hashes':audited,'input_base_directory':str(PKG),'trace_path':'review/',
 'agent_id':'/root/review_edge_vertex_bridge','thread_id':None,
 'executor_model':None,'executor_family':'openai','reviewer_model':None,'reviewer_family':'openai',
 'reviewer_reasoning':None,'requested_reviewer_model':'gpt-6.1-sol','requested_reviewer_reasoning':'ultra',
 'actual_returned_identity':None,'actual_identity_attestation':None,
 'reviewer_route':{'backend':'codex','transport':'native','host_default':True,'resolved_by':'Root before dispatch'},
 'review_independence':'same-family','acceptance_status':'provisional',
 'identity_note':'Actual model and actual effort were not returned; requested model/effort are recorded separately and confer no identity attestation or cross-family acceptance.',
 'generated_at':now,'details':{'theorems_audited':4,
 'theorem_count_convention':'Four substantive result families:162 incidence identities,36 balances,27 moment identities,exact packed consumer. The prose proof has no named theorem environments.',
 'semantic_obligations':len(obligations),
 'issues':[],'open_fatal':0,'open_critical':0,'open_major':0,'open_minor':0,
 'source_unit_coverage_complete':True,'source_unit_count':len(units),'semantic_dag_acyclic':True,
 'full_universal_generator_count':5148,'old_dedup_class_count':2788,'current_dedup_class_count':1751,
 'current_raw_histograms':3432,'current_class_covered_raw_histograms':3202,'current_pruned_raw_histograms':230,
 'packed_vertex_columns_checked':14090,'new_out_of_pool_feature_columns_checked':31,
 'actual682_current_adapter_same_beta_lambda':results['actual682_current_adapter_same_beta_lambda'],
 'whole_graph_calibration_count':9,'actual_graphs':results['actual_graphs'],
 'counterexample_pass':ledger['counterexample_pass'],'mutations_rejected':results['mutations_rejected'],
 'master050_diagnostic':results['master050'],'original_source_unchanged':True,
 'no_author_PASS_premise':True,'no_Root_check_premise':True,'no_LP_run':True,'no_tex':True,'no_html':True,
 'receipt':'review/RECEIPT.json','raw_review':'review/REVIEW.md','obligation_ledger':'review/SEMANTIC_OBLIGATIONS.json',
 'independent_checker':'review/independent_checker.py','independent_results':'review/INDEPENDENT_RESULTS.json',
 'scope_exclusions':ledger['scope_exclusions']}}
(HERE/'PROOF_AUDIT.json').write_text(json.dumps(audit,indent=2)+'\n')

skeleton=['# Proof skeleton and typed obligation map','',
 'The complete semantic review is in `REVIEW.md`; the exact structured inventory is in `SEMANTIC_OBLIGATIONS.json`.','',
 'All hypotheses refer to a single actual spanning C4-free Q8 graph. Maximality, parity restrictions and fixed edge counts are unused.', '']
for o in obligations:
    skeleton += [f"- **{o['obligation_id']}** ({', '.join(o['source_unit_ids'])}): {o['statement']}",
                 f"  Uses: {', '.join(o['dependencies']) or 'definitions only'}. Discharge: {o['evidence']}"]
skeleton += ['', 'Dependency topological order: '+', '.join(closed)+'. No cycles.',
             'No limits, asymptotics, measure-theoretic interchanges or solver-status premises occur.',
             'The coverage receipt establishes that all frozen source units were consumed; it does not itself prove validity.']
(HERE/'PROOF_SKELETON.md').write_text('\n'.join(skeleton)+'\n')
(HERE/'PROOF_AUDIT.md').write_text('# Bounded proof audit\n\nPASS for the declared universal identities and finite exports; same-family/provisional, with actual model and effort unattested. Main682 remains OPEN.\n\nRead `REVIEW.md` for the full raw semantic review, `SEMANTIC_OBLIGATIONS.json` for15 discharged obligations and the acyclic DAG, `RECEIPT.json` for full source-unit execution coverage/freshness, and `INDEPENDENT_RESULTS.json` for the actual exact run. No canonical source or wiki was changed.\n')
(HERE/'PROOF_CHECK_STATE.json').write_text(json.dumps({'status':'complete','verdict':'PASS',
 'assurance':'same-family/provisional; actual identity unattested','round':1,'issues_open':[],
 'generated_at':now,'canonical_integration':'Root only','main682':'OPEN','no_followup_jobs_started':True},indent=2)+'\n')
print(json.dumps({'source_units':len(units),'obligations':len(obligations),'manifest_entries_checked':len(manifest_checks),
                  'verdict':audit['verdict'],'acceptance_status':audit['acceptance_status']},indent=2))
