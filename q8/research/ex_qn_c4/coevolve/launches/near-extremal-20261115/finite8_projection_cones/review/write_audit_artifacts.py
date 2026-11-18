"""Emit the review's semantic accounting and hash coverage, not a proof oracle."""
from pathlib import Path
from datetime import datetime, timezone
import json
import hashlib
import ast

HERE = Path(__file__).resolve().parent
PKG = HERE.parent
LAUNCH = PKG.parent

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write(name, obj):
    (HERE / name).write_text(json.dumps(obj, indent=2) + '\n')

def main():
    route = {'reported_by': 'Root, message to this reviewer, 2026-11-16',
             'command': 'python3 -B /mnt/c/users/anony/desktop/project/math-rsi/base/tools/reviewer_route.py --project /mnt/c/users/anony/desktop/project/research/ex_qn_c4/coevolve --host codex --tier deep --model gpt-6.1-sol --effort ultra',
             'raw_parser_output': {'backend': 'codex', 'host': 'codex', 'source': 'host-default', 'model': 'gpt-6.1-sol', 'effort': 'ultra', 'transport': 'native', 'fresh_tool': 'spawn_agent', 'continuation_tool': 'send_input'},
             'requested_model': 'gpt-6.1-sol', 'requested_reasoning_effort': 'ultra',
             'actual_model': None, 'actual_reasoning_effort': None,
             'actual_identity_attestation': None,
             'actual_identity_evidence': 'No backend-returned or independently attested model/effort identity is available.',
             'reviewer_session': '/root/review_small_projection_cones',
             'review_independence': 'same-family', 'acceptance_status': 'provisional',
             'family_relation_basis': 'Conservative Codex-native same-family classification; exact actual model identities remain unknown, and cross-family independence is not established.',
             'cross_family_acceptance': False,
             'scope_complete': True, 'review_completed': True,
             'is_mathematical_premise': False}
    write('REVIEWER_ROUTE.json', route)
    units = []
    def unit(id, path, start, end, kind, reviewed):
        units.append({'unit_id': id, 'path': str(path.resolve()), 'lines': [start, end],
                      'kind': kind, 'review_method': reviewed, 'covered': True})
    proof_spans = [('CLAIM', 1, 11), ('DEFINITIONS', 12, 19), ('SMALL_DOMAIN', 20, 33),
                   ('FULL_H_SUM', 34, 47), ('WHOLE_Q8_BRIDGE', 48, 65),
                   ('NATIVE_MOMENTS', 66, 79), ('CONCRETE_CUT', 80, 97), ('CHECKS_SCOPE', 98, 107)]
    for name, start, end in proof_spans:
        unit('PROOF:' + name, PKG / 'PROOF.md', start, end, 'canonical_proof', 'Entire source span read; obligations adjudicated below; exact data replay separately.')
    for name in ['README.md', 'price_projection_point.py', 'check_projection_point.py', 'score.py',
                 'check_full_score.py', 'check_generic_boundary.py', 'check_sparse_calibration.py']:
        p = PKG / name
        unit('PACKAGE:' + name, p, 1, len(p.read_text().splitlines()), 'interface_or_implementation',
             'Entire file read. No author checker main/LP was run; independent replay and selected pure loader/scorer calls only.')
    for name in ['finite8_flags/finite_flags.py', 'finite8_connector_frequency/membership.py']:
        p = LAUNCH / name
        unit('DEPENDENCY:' + name, p, 1, len(p.read_text().splitlines()), 'dependency_code', 'Entire source read; source definitions not used to construct reviewer geometry or histogram enumeration.')
    for name, start, end in [('G01_STATES_ACTIONS', 54, 114), ('G01_SCORE_NORMALIZATION', 133, 208), ('G02_FACE_SAMPLING', 210, 257)]:
        unit('IMPORT:' + name, LAUNCH / 'finite8_flags/main.tex', start, end, 'selected_import',
             'Actual source span read and face identities rederived. Later old PSD/barrier results are outside this audit.')
    datas = ['parallel15_master102/MAPPING.json', 'parallel15_master102/block3.EXACT_CUT.json',
             'parallel15_master102/PROJECTED_MOMENTS.json', 'parallel15_master102/DOMAIN.json',
             'parallel15_master102/INPUT_POINT.json', 'parallel15_master102/STARTED.json',
             'parallel15_master102/HISTORY.json', 'parallel15_master102/RESULT.json',
             'parallel15_master102/INDEPENDENT_CHECK.json', 'parallel15_master102/FULL_SCORE_CHECK.json',
             'parallel15_master102/NONZERO_Q8_CALIBRATION.json', 'GENERIC_BOUNDARY_CHECK.json', 'PACKAGE_MANIFEST.json']
    for name in datas:
        p = PKG / name
        method = 'JSON fully parsed. All theorem-relevant data reconstructed independently; author status fields are not premises.'
        if name.endswith('INPUT_POINT.json'):
            method = 'Every lambda graph mask/decimal weight reconstructed exactly, plus asserted scope/status metadata; unrelated alpha/beta contents parsed but their mathematical obligations are outside this audit.'
        if name.endswith(('HISTORY.json', 'RESULT.json', 'STARTED.json')):
            method = 'Full discovery/provenance metadata inspected, without repeating any LP or treating NoCut as cone membership.'
        unit('DATA:' + name, p, 1, len(p.read_text().splitlines()), 'data_or_nonpremise_receipt', method)
    extra = [LAUNCH / 'finite8_frequency_cone/generator_matrix.npz',
             LAUNCH / 'finite8_frequency_cone/histograms16_sum6.npy',
             LAUNCH / 'finite8_degree_augmentation/pool_edge3_allclass1/SCOPE_INCREMENT_004_CONNECTOR4.json',
             LAUNCH.parents[2] / 'data/q8_seed682.edges']
    for p in extra:
        unit('INPUT:' + p.name, p, None, None, 'array_or_geometry_or_provenance',
             'Full array/edge content checked; scope increment is provenance only.')
    hashes = {str(Path(u['path'])): 'sha256:' + sha(Path(u['path'])) for u in units}
    manifest = json.loads((PKG / 'PACKAGE_MANIFEST.json').read_text())
    package_hashes_ok = all(sha(PKG / name) == h for name, h in manifest['artifacts'].items())
    dep_hashes_ok = all(sha(LAUNCH / name) == h for name, h in manifest['read_only_dependencies'].items())
    assert package_hashes_ok and dep_hashes_ok
    ids = [u['unit_id'] for u in units]
    assert len(ids) == len(set(ids))
    coverage = {'planned_unit_ids': ids, 'completed_unit_ids': ids,
                'failed_unit_ids': [], 'uncovered_unit_ids': [], 'coverage_complete': True,
                'units': units, 'input_hashes': hashes,
                'package_manifest_entry_hashes_match': package_hashes_ok,
                'dependency_manifest_entry_hashes_match': dep_hashes_ok,
                'no_extraction_fanout': True,
                'sequential_inventory_note': 'This is the explicit source-unit inventory for this sequential reviewer. No extraction workers were dispatched; no claim of an unrecorded predispatch freeze is made.',
                'receipt_scope': 'Execution coverage of declared canonical proof, code, selected imports, and relevant data only. This receipt alone does not prove that all obligations were discovered or that any theorem is true.'}
    write('SOURCE_UNIT_COVERAGE.json', coverage)

    symbols = {
        'b': 'selected block index in {0,1,2,3,4}, associated root mask (0,1,3,6,7)[b]',
        'S_b': 'all increasing legal labelled full Q3 flag codes for canonical nonfull root; finite set size d_b',
        'L': 'integer in [1,16]',
        'Phi_b': 'arbitrary deterministic function S_b -> {0,...,L-1}; not assumed surjective/equivariant',
        'Q': 'symmetric integer L-by-L matrix, nonnegative only on nonnegative INTEGER total-six vectors',
        'x': 'nonnegative integer full-state vector of length d_b with total exactly six',
        'y': 'nonnegative integer L-vector aggregated from x with total exactly six',
        'B': 'integer symmetric d_b-by-d_b pullback, B_ij=Q[Phi(i),Phi(j)]',
        'H_b': 'full subgroup of the eight square graph automorphisms stabilizing canonical root mask',
        'pi_h': 'bijection S_b -> S_b induced by h on connectors and translated edges',
        'K': 'integer symmetric d_b-by-d_b FULL SUM over H_b of transformed B, not an assumed label quotient',
        's': 'positive scalar; concrete normalization max(1,max|K_ij|)=8000004',
        'G': 'arbitrary actual finite simple C4-free spanning subgraph of Q8',
        'F': 'ambient coordinate square, with root pattern read from the same G',
        'x_F': 'empirical full-state COUNT vector of G at F in one common canonical root gauge, total six',
        'u_F': 'x_F/6, NOT a conditional moment or assumed independently realizable histogram',
        'A': 'actual coordinate-Q4 restriction of G; finite uniform sample of 1120 slices',
        'T_K': 'real exact local scalar sum over 24 roots with cross coefficient 5/6 and diagonal coefficient 1/12',
        'c_bij(A)': 'integer folded UPPER full-state native coefficient; denominator 64512, off diagonal already folded',
        'D': 'positive common denominator of the stored decimal lambda weights (separate from kernel normalization s)',
        'U_b': 'integer L-by-L ORDERED projected moment numerator; denominator 129024*D',
        'lambda_actual': 'uniform restriction probability distribution of one actual G, total mass one',
        'lambda_decimal': '762 positive exact decimal weights of master102, total 999999999403515826619043431/10^27, used without renormalization',
        'J': 'all-ones L-by-L matrix; y^T J y =36 when sum y=6',
    }
    specs = [
        ('D0', 'definition', [], 'Cube geometry and full legal rooted flags', 'PROOF.md:15-17', 'All flags retain ambient coordinates; all C4 are coordinate squares.', 'Literal cube Q3 square enumeration; all 256 flags per root.'),
        ('D1', 'definition', ['D0'], 'Full-state D4 stabilizer action', 'PROOF.md:37', 'Every stabilizer element permutes the entire full-state space, with no flag quotient.', 'All square-preserving permutations, closure, legality and dimensions reconstructed.'),
        ('A0', 'assumption', [], 'Q symmetric integer and nonnegative on every small integer total-six histogram', 'PROOF.md:5-7', 'Quantified assumption of generic theorem; separately discharged for concrete Q.', 'Complete small-domain hypothesis, not PSD/copositivity.'),
        ('L1', 'lemma', [], 'Small domain cardinality and sixteen-label zero-tail filter', 'PROOF.md:33', 'All 1<=L<=16, count C(L+5,6), zero tail iff included domain.', 'Recursive integer compositions equal actual stored 54264-row set; every L filter set checked.'),
        ('L2', 'lemma', ['D0', 'A0'], 'Full-state pullback is finite-six valid', 'PROOF.md:23-31', 'For every integer x>=0 of full total six, aggregate y; x^TBx=y^TQy>=0.', 'Exact finite expansion, no realizability assumption; unused-label boundary tests.'),
        ('L3', 'lemma', ['D1', 'L2'], 'Full simultaneous H sum is invariant and finite-six valid', 'PROOF.md:37-45', 'Every permuted x remains an integer total-six count; h -> hg bijects full subgroup.', 'Permutation preservation, subgroup closure, exact full lift; all invariant matrix entries checked.'),
        ('L4', 'lemma', ['D0', 'D1', 'L3'], 'Common canonical root gauge is harmless', 'PROOF.md:51', 'All flags of one root come from the same G and use one isometry; two choices differ in H.', 'Group coset identity; literal common-frame extraction and arbitrary-map test.'),
        ('L5', 'lemma', ['L4'], 'Collision identity for six external directions', 'PROOF.md:55-59', 'Independent ordered draws: six equal ordered pairs and thirty distinct; symmetry handles unordered local pair.', 'Finite sum expansion of x^TKx/36; all diagonal terms retained.'),
        ('T1', 'theorem', ['L3', 'L4', 'L5'], 'Whole-actual-Q8 nonnegative expected feature', 'PROOF.md:61-65', 'Every actual C4-free G has 1792 roots, 1120 slices, each root in 15 slices; positive s.', 'Double count 1120*24=1792*15; local average equals root quadratic average. No PSD or root-type-mass conditioning.'),
        ('L6', 'lemma', ['L4'], 'Native folded upper coordinates match T_K', 'PROOF.md:69-73', 'K symmetric full-state invariant; DEN64512; upper off diagonal used once.', 'Native actual score coefficients read; independent literal score equals native scorer on all 762 graphs.'),
        ('L7', 'lemma', ['L6'], 'Projection moment includes distinct-state diagonal collisions', 'PROOF.md:73', 'Ordered moment has full offdiagonal in both symmetric entries; each coincident label receives both.', 'All five actual projected moments exactly rebuilt, plus non-equivariant generic moments all entries.'),
        ('L8', 'lemma', ['L3', 'L7'], 'Projected trace has exactly |H| factor for exported full sum', 'PROOF.md:75-79', 'Native full moment is invariant; projection need not be equivariant. D is exact decimal denominator.', 'Trace invariance plus actual full-kernel native score equals |H| small trace for concrete and five generic cases.'),
        ('L9', 'lemma', ['L1'], 'Exact J repair validates the stored concrete small Q', 'PROOF.md:87-89', 'Integerization candidates are discovery only; y^TJy=36; repaired exact domain minimum>=0.', 'All 38760 recursive compositions: before -8, J repair1, after minimum28.'),
        ('C1', 'corollary', ['T1', 'L9', 'L3'], 'Stored full block3/root6 kernel is a valid actual-Q8 feature', 'PROOF.md:89-97', 'Full 187-state lift equals artifact, integer symmetric Q, complete domain accepted, s>0.', 'Every exported full entry, state, permutation and normalization replayed; scale8000004.'),
        ('C2', 'calculated_claim', ['L8', 'L9'], 'Exact stored-decimal master102 separation', 'PROOF.md:83-97', '762 literal legal Q4 masks; original weights read as rational decimals without normalization.', 'Raw -15940415645124021372345799259/62500000000000000000000000; normalized /8000004, below -1e-7.'),
        ('C3', 'calculated_claim', ['D0', 'L3'], 'Full exported kernel is noncopositive and nonPSD', 'PROOF.md:105', 'Nonnegative REAL vector witness also integer total4; legal codes32,64,112.', 'Counts1,1,2 give exact quadratic -1454496. Does not contradict integer-total6 validity.'),
        ('V1', 'validation', ['C1', 'L5'], 'Actual682 and sparse nonzero Q8 bridge calibrations', 'PROOF.md:103', 'Actual682 root6 count is zero; sparse opposite-edge graph is actual and C4-free.', 'All1792 roots and1120 slices on both; sparse raw2000001/448 and normalized1/1792.'),
        ('V2', 'validation', ['L3', 'L8'], 'Generic non-equivariant producer/scorer interface', 'README.md:35-39; price_projection_point.py; score.py', 'All five maps in complete ascending state order, integer1<=L<=16; use full H sum before projection.', '14 actual loader boundary tests; maps i mod3 admit no label action in every block; 5*762 exact consumer comparisons and ordered-moment identity.'),
        ('S0', 'scope', ['C1', 'C2'], 'Local exclusion only; no theorem upper682, no family barrier', 'PROOF.md:11,97,107', 'NoCut/timeout are inconclusive, target point not a graph or exactly accepted distribution.', 'No global maximization or certificate was run; upper682 remains OPEN.'),
    ]
    nodes = []
    for id, typ, uses, statement, location, hypotheses, discharge in specs:
        nodes.append({'id': id, 'type': typ, 'depends_on': uses, 'statement': statement,
                      'location': location, 'hypotheses_and_application_conditions': hypotheses,
                      'reviewed_discharge': discharge, 'assessment': 'assumed_generic_hypothesis' if id == 'A0' else 'discharged_in_declared_scope'})
    byid = {n['id']: n for n in nodes}
    done, active, order = set(), set(), []
    def visit(id):
        assert id not in active, 'semantic dependency cycle'
        if id in done:
            return
        active.add(id)
        for dep in byid[id]['depends_on']:
            assert dep in byid
            visit(dep)
        active.remove(id)
        done.add(id)
        order.append(id)
    for id in byid:
        visit(id)
    ledger = {'symbols': symbols, 'nodes': nodes, 'acyclic': True, 'topological_order': order,
              'generic_theorem_canonical_quantifiers': 'For every b in {0,...,4}, every integer L in [1,16], every deterministic Phi:S_b->{0,...,L-1}, and every Q in Sym_L(Z) such that forall y in Z_+^L with 1^Ty=6, y^TQy>=0: K_ij=sum_{h in H_b}Q_{Phi(pi_h(i)),Phi(pi_h(j))} is symmetric H_b-invariant and forall x in Z_+^{S_b},1^Tx=6,x^TKx>=0; for every actual C4-free G subset Q8 and every positive scalar s, E_{uniform coordinate Q4 A subset Q8} T_{K/s}(G|A)=(1792*36*s)^(-1)sum_{F of type b} x_F^TKx_F>=0.',
              'quantifier_nonassumptions': ['No equivariance or induced label action', 'No surjectivity of Phi', 'No simultaneous realizability of arbitrary histograms', 'No PSD or copositivity', 'No maximality or edge-count assumption on G', 'No root-type mass one condition', 'No renormalization of the frozen decimal weights'],
              'limits_or_asymptotics': 'None. Every probability/expectation interchange is a rearrangement of a finite sum.',
              'symbol_consistency': 'b is used as a block/type label; reviewer explicitly separates its index from the corresponding root mask. D is the decimal weight denominator; s is the kernel normalization.',
              'receipt_dependency': 'SOURCE_UNIT_COVERAGE.json; all declared source units covered before this global DAG/symbol check was emitted.'}
    write('SEMANTIC_LEDGER.json', ledger)
    results = json.loads((HERE / 'INDEPENDENT_RESULTS.json').read_text())
    generic = json.loads((HERE / 'GENERIC_INTERFACE_RESULTS.json').read_text())
    audit = {'audit_skill': 'proof-checker', 'verdict': 'PASS', 'reason_code': 'all_proofs_complete',
             'summary': 'The generic arbitrary deterministic projection theorem and concrete master102 exclusion are sound in the declared local scope; independent exact replays pass. Same-family provisional review only; upper682 remains OPEN.',
             'audited_input_hashes': hashes, 'trace_path': str(HERE),
             'thread_id': '/root/review_small_projection_cones',
             'reviewer_model': None, 'reviewer_reasoning': None,
             'requested_reviewer_model': 'gpt-6.1-sol', 'requested_reviewer_reasoning': 'ultra',
             'review_independence': 'same-family', 'acceptance_status': 'provisional',
             'cross_family_acceptance': False, 'review_completed': True, 'review_scope_complete': True,
             'generated_at': datetime.now(timezone.utc).isoformat(),
             'details': {'theorems_audited': 1, 'supporting_semantic_nodes': len(nodes) - 1,
                         'issues': [], 'open_fatal': 0, 'open_critical': 0, 'open_major': 0, 'open_minor': 0,
                         'scope': 'Complete PROOF.md, generic discovery/checker/scorer interfaces, actual mapping/cut/point data, selected state/action and face-bridge imports.',
                         'source_unit_coverage': 'SOURCE_UNIT_COVERAGE.json', 'typed_acyclic_ledger': 'SEMANTIC_LEDGER.json',
                         'independent_replay': 'INDEPENDENT_RESULTS.json', 'generic_interface_replay': 'GENERIC_INTERFACE_RESULTS.json',
                         'additional_root_replay': 'ADDITIONAL_ROOT_RESULTS.json',
                         'raw_review': 'REVIEW.md', 'route_and_identity': 'REVIEWER_ROUTE.json',
                         'exact_finite6_minimum': results['finite6_minimum'],
                         'normalized_pairing': results['normalized_pairing'],
                         'full_non_copositive_witness': results['noncopositive_full_witness'],
                         'boundary_mapping_cases': len(generic['mapping_cases']),
                         'main_upper682': 'OPEN',
                         'not_claimed': ['Whole-Q4 maximum or valid-row combined certificate', 'Any full-family obstruction', 'An actual Q8 graph arising from the decimal point', 'PSD or full copositivity of emitted K', 'Cone membership from four NoCut outcomes', 'Cross-family acceptance or attested actual model identity'],
                         'review_harness_correction': 'An initial generic-interface test imported an unrelated score module after producer prepended dependency directories. The reviewer corrected its own test to load this package score.py by explicit file path; original failure is retained in GENERIC_REPLAY_ATTEMPT1.log. No author source was changed.'}}
    write('PROOF_AUDIT.json', audit)
    write('PROOF_CHECK_STATE.json', {'status': 'completed', 'rounds': 1, 'threadId': audit['thread_id'],
                                    'acceptance_gate': 'PASS_SUBSTANTIVE_SAME_FAMILY_PROVISIONAL',
                                    'fatal_fixed': 0, 'critical_fixed': 0, 'major_fixed': 0, 'minor_fixed': 0,
                                    'counterexamples_to_stated_claims_found': 0,
                                    'negative_boundary_witnesses_confirmed': 1,
                                    'actual_reviewer_model': None, 'actual_reviewer_effort': None,
                                    'timestamp': audit['generated_at'], 'main_upper682': 'OPEN'})
    md = ['# Proof skeleton and accounting', '', 'The machine-readable typed symbols, quantified theorem, hypothesis ledger and acyclic dependency graph are in `SEMANTIC_LEDGER.json`.', '',
          'Topological order: ' + ' → '.join(order) + '.', '',
          'All declared source units are covered in `SOURCE_UNIT_COVERAGE.json`. That receipt concerns execution coverage, not mathematical truth.', '',
          '| ID | Type | Obligation | Uses | Source |', '|---|---|---|---|---|']
    md += [f"| {n['id']} | {n['type']} | {n['statement']} | {', '.join(n['depends_on']) or '—'} | {n['location']} |" for n in nodes]
    md += ['', 'There are no limits, asymptotic statements, infinite sums or analytic interchanges. All constants and dimensions are fixed. All generic theorem assumptions remain explicit; the concrete artifact separately discharges the small-domain assumption.', '']
    (HERE / 'PROOF_SKELETON.md').write_text('\n'.join(md))
    print(json.dumps({'verdict': audit['verdict'], 'acceptance_status': audit['acceptance_status'], 'source_units': len(units), 'semantic_nodes': len(nodes), 'manifest_hashes_match': True}))

if __name__ == '__main__':
    main()
