"""Emit the bounded review accounting; does not edit author/canonical inputs."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json

R=Path(__file__).resolve().parent;P=R.parent;B=P.parent;A=B/'finite8_degree_augmentation';L=A/'edge3_quad_lift'
def load(name):return json.loads((R/name).read_text())
def out(name,x):(R/name).write_text(json.dumps(x,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
check=load('INDEPENDENT_CHECK.json');extra=load('CONSUMER_ADVERSARIES.json')
assert check['status']=='PASS_BOUNDED_INDEPENDENT_EXACT_REPLAY' and extra['status']=='PASS_BOUND_CONSUMER_AND_ADVERSARIES'

# The source-unit receipt inventories execution coverage only. Its fields do
# not assert obligation completeness or mathematical validity.
units=[]
proof=P/'PROOF.md';lines=proof.read_text().splitlines();starts=[i+1 for i,line in enumerate(lines) if line.startswith('## E3-')]
anchors=[1]+starts;names=['E3-INTRO','E3-01','E3-02','E3-03','E3-04','E3-05']
for i,(name,start) in enumerate(zip(names,anchors)):
    units.append(dict(unit_id=name,path=str(proof),start_line=start,end_line=anchors[i+1]-1 if i+1<len(anchors) else len(lines),kind='proof-source-span',sha256=sha(proof)))
for uid,path in [('LIFT-FULL',L/'PROOF.md'),('DEF-CODE',P/'edge3.py'),('EXPORT-CODE',P/'export.py'),('ACTUAL-CODE',P/'verify_actual.py'),('LIFT-CODE',L/'build_check_lift.py'),('ORIGINAL-FUNCTIONAL',B/'finite8_flags/finite_flags.py'),('IMPORT-CONSUMER',A/'import_edge3_sampling.py'),('DUAL-CONSUMER',A/'extract_native_dual_oracle.py'),('NATIVE-FUNCTIONAL',B/'finite8_flags/oracle/finite8_separator.cpp'),('MAXIMAL-DOMAIN-CONTEXT',A/'prepare_maximal_scope.py'),('LEAF-DOMAIN-CONTEXT',B/'finite8_maximal_leaf_gate/PROOF.md')]:
    units.append(dict(unit_id=uid,path=str(path),start_line=1,end_line=len(path.read_text().splitlines()),kind='proof-or-code-source-span',sha256=sha(path)))
path=A/'vertex_priced_working_sets.py'
units.append(dict(unit_id='EQUALITY-CONSUMER',path=str(path),start_line=38,end_line=43,kind='bounded-code-source-span',sha256=sha(path)))
for path in sorted(P.glob('SOURCE_*.json')):
    units.append(dict(unit_id='DATA-'+path.stem,path=str(path),kind='complete-structured-data',sha256=sha(path)))
for name in ['ORDER.json','INTERFACE.json','INPUT_MASTER195.json','MASTER195_DIAGNOSTIC.json','BETA_HYPERGEOM_FULL_204x5148.npz','BETA_HYPERGEOM_CURRENT_204x1751.npz','LOCAL_COUNTS_204x14090.npz']:
    path=P/name;units.append(dict(unit_id='DATA-'+path.stem,path=str(path),kind='complete-structured-data',sha256=sha(path)))
for name in ['ROW_ORDER.json','EDGE3_LIFT_PACKED_KERNELS.npz','L_CURRENT_POOL_14090x204.npz']:
    path=L/name;units.append(dict(unit_id='LIFT-DATA-'+path.stem,path=str(path),kind='complete-structured-data',sha256=sha(path)))
ids=[u['unit_id'] for u in units];assert len(ids)==len(set(ids))
receipt=dict(frozen_source_units=units,planned_unit_ids=ids,completed_unit_ids=ids,failed_unit_ids=[],uncovered_unit_ids=[],coverage_complete=True,extraction_mode='single fresh nonauthor reviewer, sequential; no child agents',meaning='This is source-unit execution coverage only. It does not imply that all relevant obligations were discovered or semantically closed.')
out('SOURCE_UNITS.json',receipt)

symbols={
 'G':'finite simple C4-free spanning subgraph of Q8, with actual retained bits',
 'r':'root retention bit in {0,1}; absent roots included',
 'z':'nonnegative integer vector in N^(8-r), sum(z)=3',
 'y_hist':'nonnegative integer vector in N^(8-r), sum(y_hist)=7',
 'P_endpoint':'involution on labels swapping bits 0 and 1, preserving bit 2',
 'lambda':'empirical probability measure on the 1120 coordinate Q4 restrictions of G',
 'beta_full':'empirical probability measure on 1024 ambient-edge histograms of the same G; full domain 5148',
 'beta_current':'1751 selected representatives of 3202 kept maximal/leaf raw histograms; not general-graph domain',
 'H':'nonnegative integer 204-vector, total 70 for each full histogram; full map 204x5148',
 'L':'isometry-invariant nonnegative integer 204-vector on each legal actual Q4, total 64',
 'A_z^R':'integer symmetric function of a pair of full outside flags on canonical Q2 root R; both arguments share one frame; all individual-state pairs allowed',
 'K_z':'signed symmetric full-state kernel, five face blocks of dimensions (240,212,190,187,170), zero 9-state vertex block',
 'c(g)':'original folded upper-entry integer feature row; denominator 64512, off-diagonal folding already in coefficients',
 'T_Q(g)':'signed real linear functional c(g) dot Q /64512, no PSD premise',
 'dual_y':'arbitrary real vector in R^204; may have negative coordinates',
 'master195':'fixed finite decimal tuple parsed as exact rational numbers; not asserted feasible or realized by a graph'
}
nodes=[]
def node(i,statement,depends,rule,assumptions,source,evidence):
    nodes.append(dict(id=i,canonical_statement=statement,depends_on=depends,rule=rule,usage_minimal_assumptions=assumptions,claimed_discharge=source,reviewed_discharge=evidence,status='proved_in_bounded_scope'))
node('O01','Every actual retained-root external state is in 0..6, and endpoint reversal is P.',[], 'a retained root with state7 is exactly a coordinate C4; swap connectors',['actual cube geometry','C4-freeness'], 'E3-01:7','literal geometry, all actual graph checks')
node('O02','The complete row domain has 120 root0 and 84 root1 rows, in declared order.',['O01'],'stars-and-bars / multisets',['sum(z)=3'],'E3-01:9','independent ROWS/order and reversal reconstruction')
node('O03','For every full (r,y), H_z equals the two binomial products and all 204 entries sum to70.',['O02'],'35 subsets of seven distinct positions, twice for endpoints',['sum(y)=7','no independence assumption'],'E3-01:11-15','all 5148 complete histograms, exact binomial reconstruction; repeated/zero labels included')
node('O04','For every legal Q4, L counts all64 directed ambient roots and is Q4-isometry invariant.',['O01','O02'],'literal histogram of its three other directions; unoriented multiset with both endpoint orientations',['actual C4-free Q4'],'E3-01:17','independent 64-root scorer; 14090 frozen graphs and 1152 isometry tests; general action proof')
node('O05','For every actual C4-free G in Q8 and every row, sum1120 L = sum1024 H.',['O03','O04'],'bijection (ambient edge, 3 other axes, endpoint orientation) with (coordinate Q4, oriented ambient root)',['same actual G for lambda and beta'],'E3-02:21-25','inverse fixes the three other axes and all remaining coordinates; actual bits inherited unchanged')
node('O06','For every such G,row: 35 E_lambda L =32 E_beta H, equivalently E_lambda L/64=E_beta H/70.',['O05'],'1120=70*16, 1024=8*128, both total71680; divide by fixed empirical denominators',['lambda and beta are empirical probabilities on same G'],'E3-02:27-32','exact denominator derivation and seven actual Q8 calibrations')
node('O07','All frozen full/current H maps and frozen L map equal literal definitions entrywise.',['O03','O04'],'complete finite reconstruction, no observed-support shortcut',['five frozen SOURCE snapshots and declared order'],'E3-03:36-40','1050192 full-H entries, 357204 current-H entries, 2874360 L entries match; integer CSR verified')
node('O08','Each pinned old2788 and current1751 duplicate class preserves H; current coverage is exactly3202 retained raw generators.',['O07'],'exact member-wise equality, separate full/current domains',['stored classes only; current maximal/leaf restriction'],'E3-03:36-38','full partition5148; current3432 raw minus230 leaf-forbidden =3202, selected1751; no arbitrary-compression theorem')
node('O09','Every A_z(i,j) uses only the root square and two full flags; A is symmetric and invariant under a simultaneous root stabilizer.',['O01','O02'],'eight directed root-edge summands; shared action permutes edges and reverses endpoint orientations',['full flag encoding; same root action on both arguments'],'E3-04:44; LIFT-FULL definition','all202513 ordered canonical-state pairs; 820564 stabilizer-pair and 1620104 frame-transport tests; direct invariant proof')
node('O10','For every legal actual Q4,row: L_z=(1/3) sum24faces A_z.',['O04','O09'],'each of32 edges lies in exactly3 root faces, each observes the same three labels',['actual Q4 geometry'],'E3-04:46; LIFT-FULL (1)','24*4=3*32, endpoint counts remain doubled')
node('O11','For every invariant symmetric Q with zero vertex block, T_Q=(1/288) sumfaces(10Qij+Qii+Qjj).',['O09'],'original coefficients are 280*8 Qij plus28*8 diagonal terms; 64512=224*288',['synchronized stabilizer averaging; folded upper-entry convention'],'E3-04:50-52; LIFT-FULL (2)','all stored face coefficient entries independently reconstructed; existing native scorer fresh-graph calibration')
node('O12','K_z=12A_z-A_z(ii)-A_z(jj) is symmetric invariant; diag K=10diag A and 10Kij+Kii+Kjj=120Aij.',['O09'],'exact pointwise algebra over every individual full-state pair',['diagonal A defined by same repeated-observation formula'],'E3-04:48-54; LIFT-FULL collision calculation','20767404 packed entries match; full ordered pair cancellation exact; no PSD premise')
node('O13','For every legal Q4,row: L_z=(4/5)T_(K_z); equivalently 5*64512L_z=4 c(g)dot K_z.',['O10','O11','O12'],'T=(120/288)sum A=(5/12)sum A=(5/4)L',['same actual Q4 in L and c(g)'],'E3-04:54-56; LIFT-FULL (3)','independent full coefficient rebuild on frozen14090 plus48 fresh graphs; universal proof does not use library completeness')
node('O14','For every real dual_y, dual_y dot L/64=T_(sum_z dual_y_z K_z)/80; beta contribution is -dual_y dot H/70.',['O06','O13'],'linearity and (4/5)/64=1/80',['real weights arbitrary, including negative'],'E3-04:58; LIFT-FULL normalized equation','actual consumer K/H all entries match, equality starts152, source consumers use exact factors; native signed-weight fresh graphs')
node('O15','The sum of204 K_z is constant80 on each face block and zero on vertex block; hence sum L=64.',['O09','O12','O13'],'sum A=8 for every pair; 12*8-8-8=80',['complete row domain'],'LIFT-FULL normalization paragraph','all packed coordinates checked and face functional mass1 from64512 normalization')
node('O16','All seven declared actual Q8 calibrations obey all204 integer identities.',['O05','O07'],'direct literal graph validation and independent local/global enumeration',['the three saved edge lists plus four explicit degenerate constructions'],'E3-05:64','each checks1120 slices,1024 roots,71680 objects; edgecounts682,576,584,0,128,8,8')
node('O17','Master195 has the stated exact new-row discrepancy; older63 decimal residuals are only numerical smallness.',['O03','O04','O07'],'parse every finite decimal as Fraction and perform rational dot products',['immutable INPUT_MASTER195; frozen selected beta order'],'E3-05:66','new maximum47011126778443172104731/28000000000000000000000000; old63 maximum1868969814443/672000000000000000000000000')
node('O18','These necessary identities and signed linear lifts establish no unrestricted682 upper bound, PSD converse, or graph-realization converse.',['O06','O08','O13','O14','O17'],'logical scope of equalities and finite library checks',['no completed exact global dual or unrestricted maximization imported'],'E3-INTRO:3; E3-04:58-60; E3-05:66','explicit retained OPEN scope; exact nonPSD2x2 determinant -64; current adapter excluded for general graphs')
lookup={n['id']:n for n in nodes};temporary=set();permanent=set();topo=[]
def visit(k):
    assert k not in temporary,('cycle',k)
    if k in permanent:return
    temporary.add(k)
    for d in lookup[k]['depends_on']:assert d in lookup;visit(d)
    temporary.remove(k);permanent.add(k);topo.append(k)
for k in lookup:visit(k)
ledger=dict(typed_symbols=symbols,obligations=nodes,dependencies_acyclic=True,topological_order=topo,open_obligations_in_bounded_package=[],limit_order_map='No asymptotic or limiting statements. All sums are finite; no analytic interchange theorem is required.',source_unit_coverage_receipt='SOURCE_UNITS.json',source_unit_execution_is_not_semantic_closure=True,excluded_obligations=['original upper682 theorem','unrestricted full-domain local maximum for a final dual','exact global Farkas/dual assembly','old maximal/profile or leaf theorems beyond current adapter context','independent full audit of native oracle classification coverage','arbitrary-moment compression preserving H'])
out('OBLIGATION_LEDGER.json',ledger)

files={}
for name in ['INPUT_RECEIPT.json','CONSUMER_INPUT_RECEIPT.json']:
    for path,entry in load(name)['files'].items():
        assert path not in files or files[path]['sha256']==entry['sha256'];files[path]=entry
out('RECEIPT.json',dict(audited_inputs=files,reviewer_artifact_hashes={p.name:sha(p) for p in R.iterdir() if p.is_file() and p.name not in ['RECEIPT.json','PROOF_AUDIT.json']},immutable_frozen_export_inputs=[str(p) for p in sorted(P.glob('SOURCE_*.json'))],active_pool_policy='The active numerical pool/F may grow. Their hashes bind only the bytes used for this replay; they are not required immutable and do not define the universal Q4 domain.',source_coverage='SOURCE_UNITS.json',semantic_ledger='OBLIGATION_LEDGER.json'))
audited={str(proof):'sha256:'+sha(proof),str(L/'PROOF.md'):'sha256:'+sha(L/'PROOF.md')}
audit=dict(audit_skill='proof-checker',verdict='PASS',reason_code='all_proofs_complete',summary='All obligations in the bounded E3-01..05 sampling package and exact full-state lift close; acceptance is same-family/provisional with actual model identity unattested. Upper682 remains OPEN.',audited_input_hashes=audited,trace_path=str(R),thread_id='/root/review_edge3_sampling',reviewer_model=None,reviewer_reasoning=None,requested_reviewer_model='gpt-6.1-sol',requested_reviewer_reasoning='ultra',actual_model_identity_attested=False,reviewer_route='native Codex host-default; requested identity supplied by parent; returned actual identity unavailable',acceptance_classification='same-family/provisional',generated_at=datetime.now(timezone.utc).isoformat(),details=dict(theorems_audited=5,essential_lift_audited=True,issues=[],zero_open_fatal_or_critical=True,bounded_scope='Universal same-actual-G edge-three sampling identity, pointwise universal signed full-state quadratic lift, frozen maps/dedup/order and bounded consumer/calibration/diagnostic replay.',excluded_scope=ledger['excluded_obligations'],semantic_obligation_count=len(nodes),source_unit_count=len(units),source_unit_coverage_complete=True,semantic_ledger='OBLIGATION_LEDGER.json',source_units='SOURCE_UNITS.json',independent_checker='independent_check.py',independent_result='INDEPENDENT_CHECK.json',consumer_adversaries='CONSUMER_ADVERSARIES.json',actual_model=None,requested_model='gpt-6.1-sol',requested_reasoning='ultra',bounded_acceptance=True,original_upper682='OPEN',no_LP_or_full_Q4_scan=True,no_author_inputs_modified=True,reviewer_harness_correction='ATTEMPT1 logs retain a reviewer-native comparison failure: --graphs includes default2016*edgecount. Fixed the independent expected score to include that documented baseline; no author proof/input correction. Final exact replay passes.'))
out('PROOF_AUDIT.json',audit)
out('PROOF_CHECK_STATE.json',dict(status='COMPLETE_BOUNDED_REVIEW',verdict='PASS',round=1,issues=[],reviewer_model=None,requested_model='gpt-6.1-sol',requested_reasoning='ultra',next='Return artifacts to Root for canonical integration; no next sibling workflow started.'))
print(json.dumps(dict(verdict=audit['verdict'],source_units=len(units),obligations=len(nodes),actual_model=None,acceptance=audit['acceptance_classification'])))
