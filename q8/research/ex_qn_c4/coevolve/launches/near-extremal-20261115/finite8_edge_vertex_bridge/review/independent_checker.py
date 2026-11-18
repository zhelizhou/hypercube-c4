"""Fresh nonauthor exact review. All writes are confined to this review directory.

No author/Root checker or producer module is imported or executed.
Run with the task venv Python. This is a bounded finite check, with no LP.
"""
from pathlib import Path
from itertools import combinations, permutations
from collections import Counter
from fractions import Fraction
from math import comb
import hashlib, json, time
import numpy as np
from scipy import sparse

OUT = Path(__file__).resolve().parent
PKG = OUT.parent
BASE = PKG.parent
CURRENT = BASE / 'finite8_degree_augmentation/pool_profile1409_working_sets'
OLD = BASE / 'finite8_degree_augmentation/pool_edge_degree_dynamic'
INPUTS = {}

def read(path):
    path = Path(path)
    data = path.read_bytes()
    INPUTS[str(path)] = hashlib.sha256(data).hexdigest()
    return data

def load(path, rational=False):
    return json.loads(read(path), parse_float=Fraction if rational else float)

def matrix(stem):
    path = PKG / (stem + '.npz')
    read(path)
    m = sparse.load_npz(path).toarray().astype(np.int64)
    j = load(PKG / (stem + '.json'))
    assert j['denominator'] == 1
    mirror = sparse.csr_matrix((j['data'], j['indices'], j['indptr']), shape=j['shape']).toarray()
    assert np.array_equal(m, mirror), stem
    return m

def edge(a, b):
    return tuple(sorted((a, b)))

def cube_edges(n):
    return [edge(v, v ^ (1 << a)) for v in range(1 << n) for a in range(n) if v < (v ^ (1 << a))]

def canonical_bits(bits):
    return min(sum(int(b) << i for i, b in enumerate(bits)),
               sum(int(bits[i]) << k for k, i in enumerate((1, 0, 3, 2))))

REP = sorted({canonical_bits([(c >> i) & 1 for i in range(4)]) for c in range(15)})
assert REP == [0, 1, 3, 4, 5, 6, 7, 12, 13]
ROOT_K = [(c & 1) + ((c >> 1) & 1) for c in REP]
GROUP = [[j for j, k in enumerate(ROOT_K) if k == g] for g in range(3)]
PAIRS4 = list(combinations(range(4), 2))
E3 = cube_edges(3)
E4 = E3 + [(a + 8, b + 8) for a, b in E3] + [(v, v + 8) for v in range(8)]
PACK = list(combinations(range(9), 2))
PACK = [(i, j) for i in range(9) for j in range(i, 9)]

def rooted_state(graph, v, a, b):
    va, vb, vab = v ^ (1 << a), v ^ (1 << b), v ^ (1 << a) ^ (1 << b)
    bits = [edge(v, va) in graph, edge(v, vb) in graph,
            edge(va, vab) in graph, edge(vb, vab) in graph]
    assert not all(bits), 'literal C4'
    return REP.index(canonical_bits(bits))

def c4free(graph):
    neighbors = {}
    for a, b in graph:
        neighbors.setdefault(a, set()).add(b)
        neighbors.setdefault(b, set()).add(a)
    common = Counter()
    for ns in neighbors.values():
        for p in combinations(sorted(ns), 2):
            common[p] += 1
            if common[p] > 1:
                return False
    return True

def compositions(total, labels):
    # Separator positions are independent of the author's multiset enumeration.
    for cuts in combinations(range(total + labels - 1), labels - 1):
        ends = (-1,) + cuts + (total + labels - 1,)
        yield tuple(ends[k + 1] - ends[k] - 1 for k in range(labels))

def build_histograms():
    ans = []
    for r in range(2):
        yy = list(compositions(7, 8-r))
        yy.sort(key=lambda y: tuple(s for s, n in enumerate(y) for _ in range(n)))
        ans += [{'root_retained': r, 'counts': list(y)} for y in yy]
    return ans

def literal_column(h):
    r, counts = h['root_retained'], h['counts']
    graph = {(0, 1)} if r else set()
    axes = iter(range(1, 8))
    for s, n in enumerate(counts):
        for _ in range(n):
            a = next(axes)
            for bit, e in enumerate(((0, 1 << a), (1, 1 + (1 << a)), (1 << a, 1 + (1 << a)))):
                if s & (1 << bit):
                    graph.add(e)
    assert c4free(graph)
    deg = Counter(v for e in graph for v in e)
    ans = np.zeros((2, 9, 9), dtype=np.int64)
    # The actual fixed root is axis 0, and both actual endpoints are retained.
    for v in (0, 1):
        for a in range(1, 8):
            ans[r, deg[v], rooted_state(graph, v, 0, a)] += 1
    return ans.ravel()

def packed_local_many(codes):
    """Compute ordered 81-entry R directly by labelled square pairs, in batch."""
    codes = np.array(codes, dtype=np.uint64)
    result = np.zeros((len(codes), 9, 9), dtype=np.int64)
    row = np.arange(len(codes))
    for v in range(16):
        states = []
        for a, b in PAIRS4:
            va, vb, vab = v ^ (1 << a), v ^ (1 << b), v ^ (1 << a) ^ (1 << b)
            es = [edge(v, va), edge(v, vb), edge(va, vab), edge(vb, vab)]
            bits = [((codes >> E4.index(e)) & 1).astype(np.int64) for e in es]
            assert not np.any(np.logical_and.reduce(bits)), 'C4 Q4 graph'
            first = sum(bits[k] * (1 << k) for k in range(4))
            second = sum(bits[i] * (1 << k) for k, i in enumerate((1, 0, 3, 2)))
            states.append(np.searchsorted(REP, np.minimum(first, second)))
        for a, A in enumerate(PAIRS4):
            for b, B in enumerate(PAIRS4):
                # Completion multiplicities in Q8 are C(8-|A union B|,4-|union|).
                size = len(set(A) | set(B))
                weight = 360 // comb(8-size, 4-size)
                result[row, states[a], states[b]] += weight
    assert np.all(result.sum(axis=(1, 2)) == 64512)
    return result

def pack(R):
    return np.array([R[..., i, j] * (1 if i == j else 2) for i, j in PACK]).T

def group_counts(d):
    return [comb(8-d, 2), d*(8-d), comb(d, 2)]

def read_edges(path):
    return {edge(*map(int, line.split())) for line in read(path).decode().splitlines() if line.strip()}

def restrictions(graph):
    masks = Counter()
    for axes in combinations(range(8), 4):
        support = sum(1 << a for a in axes)
        for base in range(256):
            if base & support:
                continue
            embedding = [base | sum((1 << axes[i]) for i in range(4) if v & (1 << i)) for v in range(16)]
            mask = sum((edge(embedding[a], embedding[b]) in graph) << k for k, (a,b) in enumerate(E4))
            masks[mask] += 1
    assert sum(masks.values()) == 1120
    return masks

def actual_graph(name, graph, C, B, BM, W, lookup):
    assert all(0 <= a < b < 256 and (a ^ b).bit_count() == 1 for a, b in graph)
    assert c4free(graph)
    degree = Counter(v for e in graph for v in e)
    T = np.zeros((9, 9), dtype=np.int64)
    XX = np.zeros((9, 9), dtype=np.int64)
    beta = np.zeros(5148, dtype=np.int64)
    counts_by_parity = [Counter(), Counter()]
    for v in range(256):
        d = degree[v]
        x = np.bincount([rooted_state(graph, v, a, b) for a,b in combinations(range(8),2)], minlength=9)
        assert x.sum() == 28 and np.dot(x, ROOT_K) == 7*d
        assert [int(x[js].sum()) for js in GROUP] == group_counts(d)
        T[d] += x
        XX += np.outer(x, x)
        counts_by_parity[v.bit_count() % 2][d] += 1
    direct = np.zeros((2,9,9), dtype=np.int64)
    for u,v in cube_edges(8):
        root = int((u,v) in graph)
        a = (u ^ v).bit_length() - 1
        y = [0]*(8-root)
        for b in range(8):
            if a == b:
                continue
            flags = [edge(u,u^(1<<b)) in graph, edge(v,v^(1<<b)) in graph,
                     edge(u^(1<<b),v^(1<<b)) in graph]
            s = sum(flag << k for k,flag in enumerate(flags))
            assert s < len(y)
            y[s] += 1
            for endpoint in (u,v):
                direct[root,degree[endpoint],rooted_state(graph,endpoint,a,b)] += 1
        beta[lookup[(root,tuple(y))]] += 1
    assert beta.sum() == 1024
    assert np.array_equal(C @ beta, direct.ravel())
    for r in range(2):
        for j,k in enumerate(ROOT_K):
            assert np.array_equal(direct[r,:,j], (k if r else 2-k)*T[:,j])
    assert np.array_equal(direct.sum(axis=0), 2*T)
    assert np.array_equal(512*direct.sum(axis=0), 1024*T)
    assert not np.any(B @ beta)
    masks = restrictions(graph)
    Rs = packed_local_many(list(masks))
    totalR = sum(n*R for n,R in zip(masks.values(),Rs))
    assert np.array_equal(totalR, 360*XX)
    assert np.array_equal(784*256*totalR,1120*64512*XX)
    groupR = np.array([sum(totalR[i,j] for j in GROUP[g]) for g in range(3) for i in range(9)])
    assert np.array_equal(1120*64512*(BM @ beta),392*1024*groupR)
    assert np.array_equal(2304*1120*(BM @ beta),7*1024*(W @ pack(totalR)))
    return {'name':name,'edges':len(graph),'degree_counts_by_parity':[dict(x) for x in counts_by_parity],
            'distinct_Q4_masks':len(masks),'all162_incidence':True,'all36_balances':True,
            'all27_moments':True,'full81_second_moment':True,'gamma_first_moment':True}, beta, totalR

def main():
    started = time.monotonic()
    hist = build_histograms()
    assert len(hist) == 5148
    assert hist == load(BASE/'finite8_edge_flags/GENERATOR_HISTOGRAMS.json')
    lookup = {(h['root_retained'],tuple(h['counts'])):i for i,h in enumerate(hist)}
    C = np.stack([literal_column(h) for h in hist], axis=1)
    assert np.all(C.sum(axis=0) == 14)
    assert np.array_equal(C,matrix('C_FULL_162x5148'))
    assert np.array_equal(C[:81],matrix('C_MISSING_81x5148'))
    assert np.array_equal(C[81:],matrix('C_RETAINED_81x5148'))
    for col,h in enumerate(hist):
        r,y = h['root_retained'],h['counts']
        reverse = [y[(s & 4) | ((s & 1)<<1) | ((s & 2)>>1)] for s in range(len(y))]
        assert np.array_equal(C[:,col],C[:,lookup[(r,tuple(reverse))]])
    old = load(OLD/'GENERATOR_DEDUPLICATION.json')
    raw = load(CURRENT/'GENERATOR_HISTOGRAMS.json')
    current = load(CURRENT/'GENERATOR_DEDUPLICATION.json')
    raw_map = [lookup[h['root_retained'],tuple(h['counts'])] for h in raw]
    assert len(raw) == 3432 and len(set(raw_map)) == 3432
    selected = current['selected_original_indices']
    adapter = [raw_map[k] for k in selected]
    dedup_coverage = {}
    for name,dedup,mapper in [('old',old,list(range(5148))),('current',current,raw_map)]:
        covered = []
        for rep,group in zip(dedup['selected_original_indices'],dedup['groups']):
            assert rep in group
            for k in group:
                assert np.array_equal(C[:,mapper[rep]],C[:,mapper[k]])
            covered += group
        assert len(covered) == len(set(covered))
        dedup_coverage[name] = {'classes':len(dedup['groups']),'covered_raw_columns':len(covered),
                                'not_in_stored_classes':sorted(set(range(len(mapper)))-set(covered))}
    assert dedup_coverage['old']['covered_raw_columns'] == 5148
    assert len(adapter) == 1751
    order = load(PKG/'ORDER.json')
    assert order['vertex_representatives'] == REP
    assert order['C_row_order'] == [[r,d,j] for r in range(2) for d in range(9) for j in range(9)]
    balance_rows = [[d,j] for d in range(9) for j in GROUP[1]]
    assert order['balance_row_order'] == balance_rows
    assert order['current_selected_raw_indices'] == selected
    assert order['current_to_original5148_indices'] == adapter
    assert order['current_column_histograms'] == [raw[k] for k in selected]
    assert order['old_selected_original_indices'] == old['selected_original_indices']
    B = np.array([C[81+9*d+j]-C[9*d+j] for d,j in balance_rows])
    assert np.array_equal(B,matrix('BALANCE_FULL_36x5148'))
    for tag,idx in [('OLD',old['selected_original_indices']),('CURRENT',adapter)]:
        assert np.array_equal(C[:,idx],matrix(f'C_{tag}_162x{len(idx)}'))
        assert np.array_equal(B[:,idx],matrix(f'BALANCE_{tag}_36x{len(idx)}'))
    BM = np.array([sum(group_counts(d)[g]*(C[9*d+i]+C[81+9*d+i]) for d in range(9))
                   for g in range(3) for i in range(9)])
    assert np.array_equal(BM,matrix('MOMENT_BETA_FULL_27x5148'))
    assert np.array_equal(BM[:,adapter],matrix('MOMENT_BETA_CURRENT_27x1751'))
    W = np.zeros((27,45),dtype=np.int64)
    for g in range(3):
        for i in range(9):
            for j in GROUP[g]:
                W[9*g+i,PACK.index(tuple(sorted((i,j))))] += 2 if i == j else 1
    assert np.array_equal(W,matrix('MOMENT_PACKED9_SELECTOR_TWICE_27x45'))
    codes = load(CURRENT/'POOL_GRAPH_CODES.json')
    moment_order = load(PKG/'MOMENT_ORDER.json')
    assert moment_order == {'row_order':[[g,i] for g in range(3) for i in range(9)],
            'groups_by_root_retained_degree':GROUP,'packed9_order':[list(p) for p in PACK],'current_graph_order':codes}
    assert len(codes) == 14090
    info = load(BASE/'finite8_degree_augmentation/pool_inventory/LP_STARTED.json')
    feature_path = CURRENT/'INTEGER_FEATURES.npz'
    read(feature_path)
    full_features = sparse.load_npz(feature_path)
    a,b = info['packed_starts'][5:7]
    assert (a,b) == (101756,101801)
    FV = full_features[:,a:b].toarray().astype(np.int64)
    Rs = packed_local_many(codes)
    fresh = pack(Rs)
    assert np.array_equal(FV,fresh)
    assert np.array_equal(196*W @ fresh.T,matrix('MOMENT_LAMBDA_CURRENT_POOL_27x14090'))
    # Independently exercise the consumer on graph columns outside the frozen pool.
    code_set = set(codes)
    future = []
    for k in range(32):
        mask = 1 << k
        if mask not in code_set:
            future.append(mask)
    assert future
    future_R = packed_local_many(future)
    future_F = pack(future_R)
    for idx,R in enumerate(future_R):
        groups = np.array([sum(R[i,j] for j in GROUP[g]) for g in range(3) for i in range(9)])
        assert np.array_equal(W @ future_F[idx],2*groups)
        assert np.array_equal(196*(W @ future_F[idx]),392*groups)
    paths = [BASE.parents[2]/'data/q8_seed682.edges',BASE/'finite8_maximal_leaf_gate/CALIBRATION.edges',
             BASE/'finite8_maximal_leaf_gate/review/SAME_PARITY_COUNTEREXAMPLE.edges']
    graphs = [read_edges(p) for p in paths]
    assert [len(g) for g in graphs] == [682,576,584]
    cases = list(zip(['actual682','calibration576','actual584'],graphs))
    cases += [('empty',set()),('perfect_matching',{(v,v^1) for v in range(256) if v%2==0}),
              ('star_even',{(0,1<<a) for a in range(8)}),
              ('star_odd',{edge(1,1^(1<<a)) for a in range(8)}),
              ('seed_one_edge_deleted',graphs[0]-{min(graphs[0])}),
              ('seed_xor137',{edge(a^137,b^137) for a,b in graphs[0]})]
    cases_out = []
    for name,g in cases:
        row,beta,R = actual_graph(name,g,C,B,BM,W,lookup)
        cases_out.append(row)
        if name == 'actual682':
            seed_beta,seed_R = beta,R
    # Calibrate the actual same-beta/same-lambda CURRENT consumer, not only the
    # universal map. Every actual seed histogram must survive its current class.
    full_to_current = {}
    for k,group in enumerate(current['groups']):
        for raw_index in group:
            full_to_current[raw_map[raw_index]] = k
    current_beta = np.zeros(1751,dtype=np.int64)
    for raw_index in np.flatnonzero(seed_beta):
        current_beta[full_to_current[int(raw_index)]] += seed_beta[raw_index]
    assert current_beta.sum() == 1024
    assert np.array_equal(C[:,adapter] @ current_beta,C @ seed_beta)
    assert np.array_equal(B[:,adapter] @ current_beta,B @ seed_beta)
    assert np.array_equal(BM[:,adapter] @ current_beta,BM @ seed_beta)
    seed_lambda = restrictions(graphs[0])
    graph_to_pool = {int(mask):k for k,mask in enumerate(codes)}
    # POOL_GRAPH_CODES contains selected cube-frame representatives, not every
    # raw labelled restriction. Use one actual whole-Q4 automorphism, then
    # independently confirm its packed feature is unchanged.
    frame_maps,frame_names = [],[]
    for perm in permutations(range(4)):
        for translation in range(16):
            vv = [translation ^ sum(1 << perm[k] for k in range(4) if v & (1 << k)) for v in range(16)]
            frame_maps.append([1 << E4.index(edge(vv[a],vv[b])) for a,b in E4])
            frame_names.append((perm,translation))
    frame_maps = np.array(frame_maps,dtype=np.uint64)
    seed_raw_packed = pack(packed_local_many(list(seed_lambda)))
    transported_lambda = Counter()
    transport_receipt = []
    for (mask,n),raw_f in zip(seed_lambda.items(),seed_raw_packed):
        if mask in graph_to_pool:
            chosen,frame_index = mask,0
        else:
            positions = [k for k in range(32) if mask & (1 << k)]
            moved = frame_maps[:,positions].sum(axis=1)
            frame_index = next(k for k,value in enumerate(moved) if int(value) in graph_to_pool)
            chosen = int(moved[frame_index])
        assert np.array_equal(raw_f,fresh[graph_to_pool[chosen]])
        transported_lambda[chosen] += n
        perm,translation = frame_names[frame_index]
        transport_receipt.append({'raw_mask':mask,'multiplicity':n,'pool_mask':chosen,
                                  'axis_permutation':list(perm),'translation':translation})
    seed_feature_sum = sum(n*fresh[graph_to_pool[mask]] for mask,n in transported_lambda.items())
    assert np.array_equal(seed_feature_sum,pack(seed_R))
    assert np.array_equal(2304*1120*(BM[:,adapter] @ current_beta),7*1024*(W @ seed_feature_sum))
    (OUT/'SEED_CURRENT_LAMBDA_TRANSPORT.json').write_text(json.dumps({'scope':'Actual682 restrictions transported by one whole-Q4 cube-frame automorphism per restriction; all packed45 entries compared, not independent projection choices.',
        'transports':transport_receipt,'pool_lambda_integer_counts':list(transported_lambda.items()),
        'beta_current_integer_counts':[[int(k),int(current_beta[k])] for k in np.flatnonzero(current_beta)]},indent=2)+'\n')
    # All mutation rejections are detected against actual graph integer observations.
    mutations = {}
    col = int(np.flatnonzero(seed_beta)[0])
    bad = C.copy(); bad[0,col] += 1
    mutations['C_entry_plus1'] = not np.array_equal(bad @ seed_beta,C @ seed_beta)
    badB = B.copy()
    r,c = np.argwhere((B != 0) & (seed_beta[None,:] != 0))[0]
    badB[r,c] *= -1
    mutations['single_balance_sign_flip'] = bool(np.any(badB @ seed_beta))
    groupR = np.array([sum(seed_R[i,j] for j in GROUP[g]) for g in range(3) for i in range(9)])
    mutations['392_to393'] = not np.array_equal(1120*64512*(BM @ seed_beta),393*1024*groupR)
    unfactored = np.array([seed_R[i,j] for i,j in PACK])
    mutations['drop_offdiag_factor2'] = not np.array_equal(W @ unfactored,W @ pack(seed_R))
    mutations['literal_C4'] = not c4free({(0,1),(0,2),(1,3),(2,3)})
    assert all(mutations.values())
    point_path = CURRENT/'point_bank/master_050.json'
    point = load(point_path,rational=True)
    beta = [Fraction(0) for _ in adapter]
    for k,w in point['beta']:
        beta[k] += w
    def dot(M,weights):
        return [sum((int(v)*weights[j] for j,v in enumerate(row) if v),Fraction(0)) for row in M]
    residual36 = dot(B[:,adapter],beta)
    left = dot(BM[:,adapter],beta)
    right = [Fraction(0) for _ in range(27)]
    point_R = packed_local_many([int(g) for g,w in point['lambda']])
    for (_,w),R in zip(point['lambda'],point_R):
        for g in range(3):
            for i in range(9):
                right[9*g+i] += w*392*sum(int(R[i,j]) for j in GROUP[g])/64512
    residual27 = [a-b for a,b in zip(left,right)]
    diagnostic = {'arithmetic':'exact serialized decimal rational weights; no renormalization',
        'beta_mass':str(sum(beta)),'lambda_mass':str(sum(w for _,w in point['lambda'])),
        'B36_residuals':[str(x) for x in residual36],'B27_minus392M5_residuals':[str(x) for x in residual27],
        'max_B36_exact':str(max(map(abs,residual36))),'max_B27_exact':str(max(map(abs,residual27))),
        'max_B36_float':float(max(map(abs,residual36))),'max_B27_float':float(max(map(abs,residual27)))}
    assert abs(diagnostic['max_B36_float']-0.029930761918206757)<1e-17
    assert abs(diagnostic['max_B27_float']-0.10051812768628185)<1e-17
    serialized_diagnostic = load(PKG/'MASTER050_DIAGNOSTIC.json')
    assert [Fraction(row['difference']) for row in serialized_diagnostic['balance_rows']] == residual36
    assert [Fraction(row['difference']) for row in serialized_diagnostic['moment_rows']] == residual27
    assert [[row['degree'],row['state']] for row in serialized_diagnostic['balance_rows']] == balance_rows
    assert [[row['group'],row['state']] for row in serialized_diagnostic['moment_rows']] == [[g,i] for g in range(3) for i in range(9)]
    diagnostic['all63_serialized_author_residuals_match_independent_reconstruction'] = True
    # Check advertised source and mirror hashes without taking status fields as premises.
    for interface_name in ['INTERFACE.json','MOMENT_INTERFACE.json']:
        interface = load(PKG/interface_name)
        for path,h in interface.get('source_files',interface.get('sources',{})).items():
            assert hashlib.sha256(read(path)).hexdigest() == h
        for artifact in interface['artifacts'].values():
            assert hashlib.sha256(read(PKG/artifact['json'])).hexdigest() == artifact['json_sha256']
        key = 'order_sha256' if interface_name=='INTERFACE.json' else 'moment_order_sha256'
        filename = 'ORDER.json' if interface_name=='INTERFACE.json' else 'MOMENT_ORDER.json'
        assert hashlib.sha256(read(PKG/filename)).hexdigest() == interface[key]
    result = {'status':'PASS_EXACT_INDEPENDENT_BOUNDED_CHECKS','original_histogram_count':len(hist),
        'all5148_literal_root_extensions':True,'all5148_common_endpoint_reversals':True,
        'dedup':dedup_coverage,'all_exported_sparse_mirrors_exact':True,
        'all_frozen_packed45_rows':len(codes),'out_of_pool_feature_consumer_masks':future,
        'actual682_current_adapter_same_beta_lambda':{'ambient_edge_mass':int(current_beta.sum()),
            'restriction_mass':sum(seed_lambda.values()),'distinct_raw_lambda_columns':len(seed_lambda),
            'distinct_lambda_pool_columns':len(transported_lambda),
            'raw_codes_requiring_frame_transport':sum(t['raw_mask']!=t['pool_mask'] for t in transport_receipt),
            'whole_Q4_frame_transports_all_packed45_invariant':True,
            'C_and_B36_and_B27_class_aggregation':True,'all27_packed_consumer_equations':True},
        'actual_graphs':cases_out,'mutations_rejected':mutations,'master050':diagnostic,
        'input_hashes':INPUTS,'runtime_seconds':time.monotonic()-started,
        'scope':'General necessary identities and frozen finite interfaces only; no 682 upper bound or infeasibility.'}
    (OUT/'INDEPENDENT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('input_hashes','master050','dedup')},indent=2))
    print('DEDUP',json.dumps({k:{a:b for a,b in v.items() if a!='not_in_stored_classes'} for k,v in dedup_coverage.items()}))
    print('MASTER050',json.dumps({k:v for k,v in diagnostic.items() if 'residuals' not in k}))

if __name__ == '__main__':
    main()
