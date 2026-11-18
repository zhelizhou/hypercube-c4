"""Bounded nonauthor replay. All source reads; all writes confined to this directory.

No author Python module is imported. Hypergeometric values use binomial products,
local values enumerate all 64 directed ambient roots, and face coefficients and
full-state kernels are rebuilt from cube bit geometry. This is not a Q4 scan/LP.
"""
from pathlib import Path
import hashlib, io, json, math, struct, subprocess, sys, time
from fractions import Fraction
from itertools import combinations, combinations_with_replacement, permutations
from collections import Counter

HERE = Path(__file__).resolve().parent
P = HERE.parent
B = P.parent
AUG = B / 'finite8_degree_augmentation'
SCOPE = AUG / 'pool_profile1409_vertex_priced'
LIFT = AUG / 'edge3_quad_lift'
# Bundled scientific dependencies only; no producer module is imported.
sys.path.insert(0, str(B / 'finite8_flags/deps'))
import numpy as np
from scipy import sparse

START = time.monotonic()
INPUTS = {}
def read(path):
    path = Path(path)
    data = path.read_bytes()
    h = hashlib.sha256(data).hexdigest()
    old = INPUTS.get(str(path))
    assert old is None or old['sha256'] == h, ('input changed during replay', str(path))
    INPUTS[str(path)] = {'sha256': h, 'bytes': len(data)}
    return data
def js(path, exact=False):
    return json.loads(read(path), parse_float=Fraction if exact else float)
def mat(path):
    value=sparse.load_npz(io.BytesIO(read(path)))
    assert value.format=='csr' and np.issubdtype(value.dtype,np.integer), ('expected exact integer CSR',str(path),value.format,str(value.dtype))
    return value.astype(np.int64)
def output(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2) + '\n')
def check(tag, value):
    print(tag, json.dumps(value), flush=True)
    return value
def edges(n):
    return [(v, v ^ (1 << a)) for v in range(1 << n) for a in range(n) if v < (v ^ (1 << a))]
E3 = edges(3)
ORDER = E3 + [(u + 8, v + 8) for u, v in E3] + [(v, v + 8) for v in range(8)]
EI = {e: k for k, e in enumerate(ORDER)}
def ep(u, v): return (min(u, v), max(u, v))
def flip(s): return (s & 4) + ((s & 1) << 1) + ((s & 2) >> 1)
def hist(xs, n): return tuple(Counter(xs).get(s, 0) for s in range(n))
ROWS = [(r, hist(t, 8-r)) for r in (0, 1) for t in combinations_with_replacement(range(8-r), 3)]
RI = {key:i for i, key in enumerate(ROWS)}
assert len(ROWS) == len(RI) == 204
ROW_TRIPLES = {(r, tuple(t)):RI[r, hist(t, 8-r)] for r in (0, 1) for t in combinations_with_replacement(range(8-r),3)}
ROW_REVERSE = [RI[r, tuple(z[flip(s)] for s in range(8-r))] for r,z in ROWS]
def compositions(n, k):
    if k == 1:
        yield (n,)
    else:
        for first in range(n, -1, -1):
            for tail in compositions(n-first, k-1):
                yield (first,) + tail
def H_value(r, y):
    out = np.zeros(204, dtype=np.int64)
    assert len(y) == 8-r and sum(y) == 7 and all(type(x) is int and x >= 0 for x in y)
    for j, (rr, z) in enumerate(ROWS):
        if rr == r:
            out[j] = math.prod(math.comb(y[s], z[s]) if z[s] <= y[s] else 0 for s in range(8-r)) + math.prod(math.comb(y[flip(s)], z[s]) if z[s] <= y[flip(s)] else 0 for s in range(8-r))
    assert out.sum() == 70
    return out
def literal_L(g):
    assert type(g) is int and 0 <= g < 1 << 32
    ed = {e for k,e in enumerate(ORDER) if g >> k & 1}
    # Every C4 in a hypercube is a coordinate square; check all 24 explicitly.
    for aa,bb in combinations(range(4),2):
        for v in range(16):
            if v & ((1<<aa)|(1<<bb)): continue
            assert not all(ep(x,y) in ed for x,y in [(v,v^(1<<aa)), (v,v^(1<<bb)), (v^(1<<aa),v^(1<<aa)^(1<<bb)), (v^(1<<bb),v^(1<<aa)^(1<<bb))])
    out = np.zeros(204, dtype=np.int64)
    for v in range(16):
        for aa in range(4):
            w = v ^ (1 << aa)
            r = int(ep(v,w) in ed)
            labels=[]
            for bb in range(4):
                if aa != bb:
                    x,y=v^(1<<bb),w^(1<<bb)
                    labels.append(int(ep(v,x) in ed)+2*int(ep(w,y) in ed)+4*int(ep(x,y) in ed))
            assert r == 0 or 7 not in labels
            out[ROW_TRIPLES[r,tuple(sorted(labels))]] += 1
    assert out.sum() == 64
    return out

def map_checks():
    raw = js(P/'SOURCE_0_GENERATOR_HISTOGRAMS.json')
    cur = js(P/'SOURCE_1_GENERATOR_HISTOGRAMS.json')
    ded = js(P/'SOURCE_2_GENERATOR_DEDUPLICATION.json')
    old = js(P/'SOURCE_3_GENERATOR_DEDUPLICATION.json')
    graphs = js(P/'SOURCE_4_POOL_GRAPH_CODES.json')
    fullkeys = [(r,y) for r in (0,1) for y in compositions(7,8-r)]
    keys = [(g['root_retained'],tuple(g['counts'])) for g in raw]
    assert len(keys) == 5148 and len(set(keys)) == 5148 and set(keys) == set(fullkeys)
    fullindex = {k:i for i,k in enumerate(keys)}
    H = np.column_stack([H_value(*key) for key in keys])
    assert np.array_equal(H,mat(P/'BETA_HYPERGEOM_FULL_204x5148.npz').toarray())
    ckeys = [(g['root_retained'],tuple(g['counts'])) for g in cur]
    assert len(ckeys) == len(set(ckeys)) == 3432
    assert set(ckeys) == {k for k in fullkeys if k[0] == 1 or k[1][7] > 0}
    # Separate the maximal missing-root and leaf-domain adapter from full H.
    keep = []
    for i,(r,y) in enumerate(ckeys):
        a=sum((s&1)*n for s,n in enumerate(y)); b=sum(((s>>1)&1)*n for s,n in enumerate(y))
        if r == 0 or ((a != 0 or y[6] == 7) and (b != 0 or y[5] == 7)):
            keep.append(i)
    allgroups=[i for group in ded['groups'] for i in group]
    assert len(keep) == len(allgroups) == len(set(allgroups)) == 3202 and set(allgroups) == set(keep)
    cglobal = [fullindex[k] for k in ckeys]
    selected = ded['selected_original_indices']
    assert len(selected) == len(ded['groups']) == 1751
    for group,k in zip(ded['groups'],selected):
        assert k in group
        assert all(np.array_equal(H[:,cglobal[i]],H[:,cglobal[k]]) for i in group)
    oldall=[i for group in old['groups'] for i in group]
    assert len(old['groups']) == 2788 and sorted(oldall) == list(range(5148))
    for group,k in zip(old['groups'],old['selected_original_indices']):
        assert k in group and all(np.array_equal(H[:,i],H[:,k]) for i in group)
    currentH=H[:,[cglobal[i] for i in selected]]
    assert np.array_equal(currentH,mat(P/'BETA_HYPERGEOM_CURRENT_204x1751.npz').toarray())
    order=js(P/'ORDER.json')
    assert order['rows']==[dict(root_retained=r,counts=list(z)) for r,z in ROWS]
    assert order['graphs']==graphs and order['current_raw3432_to_full5148']==cglobal
    assert order['current_selected_source3432_indices']==selected
    assert order['current_selected_global5148_indices']==[cglobal[i] for i in selected]
    assert len(graphs)==len(set(graphs))==14090
    localL=np.column_stack([literal_L(g) for g in graphs])
    assert np.array_equal(localL,mat(P/'LOCAL_COUNTS_204x14090.npz').toarray())
    assert np.array_equal(localL,np.load(io.BytesIO(read(LIFT/'L_CURRENT_POOL_14090x204.npz')))['L'].T)
    # Every orientation-reversed row is the same feature, including fixed rows.
    assert np.array_equal(H,H[ROW_REVERSE]) and np.array_equal(localL,localL[ROW_REVERSE])
    return raw,cur,ded,graphs,H,currentH,localL,check('maps',dict(rows=204,root_row_counts=[120,84],full_histograms=5148,full_H_entries=204*5148,current_raw=3432,current_kept=3202,current_removed_by_leaf=230,current_classes=1751,old_classes=2788,L_columns=14090,L_entries=204*14090,all_entries_equal=True,endpoint_row_fixed=sum(i==j for i,j in enumerate(ROW_REVERSE))))

Q2=[(0,1),(0,2),(1,3),(2,3)]
QEI={e:i for i,e in enumerate(Q2)}
ROOTS=[0,1,3,6,7]
DIMS=[240,212,190,187,170,9]
STARTS=[0]
for n in DIMS: STARTS.append(STARTS[-1]+n*(n+1)//2)
assert STARTS==[0,28920,51498,69643,87221,101756,101801]
def legal_states(root):
    return [f for f in range(256) if (f>>4)!=15 and not any(root>>e&1 and f>>(4+e)&1 and f>>u&1 and f>>v&1 for e,(u,v) in enumerate(Q2))]
STATES=[legal_states(r) for r in ROOTS]
assert list(map(len,STATES))==DIMS[:5]
SID=[{s:i for i,s in enumerate(st)} for st in STATES]
def make_actions():
    acts=[]
    for swap in (False,True):
        for t in range(4):
            vm=[t ^ (((v&1)<<1 | (v&2)>>1) if swap else v) for v in range(4)]
            em=[QEI[ep(vm[u],vm[v])] for u,v in Q2]
            rm=[sum((1<<em[e]) for e in range(4) if r>>e&1) for r in range(16)]
            fm=[sum((1<<vm[v]) for v in range(4) if f>>v&1) + sum((1<<(4+em[e])) for e in range(4) if f>>(4+e)&1) for f in range(256)]
            acts.append((rm,fm))
    return acts
ACTIONS=make_actions()
def A_full(root, states):
    """Independently form the eight directed-edge indicators for every ordered pair."""
    n=len(states); out=np.zeros((204,n,n),dtype=np.int16)
    pair_positions=np.arange(n*n)
    for u,v in Q2:
        for x,y in ((u,v),(v,u)):
            r=(root>>QEI[ep(x,y)])&1
            other=3^(x^y)
            base=((root>>QEI[ep(x,x^other)])&1)+2*((root>>QEI[ep(y,y^other)])&1)+4*((root>>QEI[ep(x^other,y^other)])&1)
            edge_id=QEI[ep(x,y)]
            labels=np.array([((f>>x)&1)+2*((f>>y)&1)+4*((f>>(4+edge_id))&1) for f in states])
            assert labels.max()<8-r and base<8-r
            lookup=np.array([[ROW_TRIPLES[r,tuple(sorted((base,int(a),int(b))))] for b in range(8-r)] for a in range(8-r)])
            row=lookup[labels[:,None],labels[None,:]].ravel()
            flat=out.reshape(204,-1)
            flat[row,pair_positions]+=1
    assert np.all(out.sum(axis=0)==8)
    assert np.array_equal(out,out.transpose(0,2,1))
    return out
def kernel_checks():
    given=mat(LIFT/'EDGE3_LIFT_PACKED_KERNELS.npz')
    assert given.shape==(204,101801)
    roworder=js(LIFT/'ROW_ORDER.json')
    assert roworder==[dict(root=r,histogram=list(z)) for r,z in ROWS]
    K=np.zeros((204,101801),dtype=np.int64)
    As=[]; ordered_pairs=0; root_action_tests=0; crossroot_pairs=0
    for b,(root,states) in enumerate(zip(ROOTS,STATES)):
        AA=A_full(root,states); As.append(AA)
        n=len(states); ii,jj=np.triu_indices(n); dd=AA[:,np.arange(n),np.arange(n)]
        KK=12*AA-dd[:,:,None]-dd[:,None,:]
        assert np.array_equal(KK[:,np.arange(n),np.arange(n)],10*dd)
        assert np.array_equal(10*KK+KK[:,np.arange(n),np.arange(n)][:,:,None]+KK[:,np.arange(n),np.arange(n)][:,None,:],120*AA)
        for rm,fm in ACTIONS:
            if rm[root]!=root: continue
            ids=[SID[b][fm[f]] for f in states]
            assert np.array_equal(AA,AA[:,ids,:][:,:,ids])
            assert np.array_equal(KK,KK[:,ids,:][:,:,ids])
            root_action_tests+=n*n
        K[:,STARTS[b]:STARTS[b+1]]=KK[:,ii,jj]
        ordered_pairs+=n*n
    # Check noncanonical root frames, with one simultaneous map for both flags.
    for root in range(15):
        canonical=min(rm[root] for rm,_ in ACTIONS)
        b=ROOTS.index(canonical)
        states=legal_states(root); actual=A_full(root,states)
        for rm,fm in ACTIONS:
            if rm[root]!=canonical: continue
            ids=[SID[b][fm[f]] for f in states]
            assert np.array_equal(actual,As[b][:,ids,:][:,:,ids])
            crossroot_pairs+=len(states)**2
    assert (sparse.csr_matrix(K)!=given).nnz==0
    assert np.all(K[:,:STARTS[5]].sum(axis=0)==80) and np.all(K[:,STARTS[5]:]==0)
    return K,As,check('kernels',dict(dimensions=DIMS,packed_entries=204*101801,full_ordered_pairs=ordered_pairs,simultaneous_stabilizer_ordered_pair_tests=root_action_tests,noncanonical_transport_pair_tests=crossroot_pairs,all_kernel_entries_equal=True,vertex_block_zero=True,sum_kernel_face_constant=80,min_kernel_entry=int(K.min()),max_kernel_entry=int(K.max()),diagonal_and_offdiagonal_cancellation=True))

def faces(g):
    E={e for k,e in enumerate(ORDER) if g>>k&1}
    for a,b in combinations(range(4),2):
        for x in range(16):
            if x&((1<<a)|(1<<b)): continue
            vm=[x,x^(1<<a),x^(1<<b),x^(1<<a)^(1<<b)]
            root=sum((1<<e) for e,(u,v) in enumerate(Q2) if ep(vm[u],vm[v]) in E)
            flags=[]
            for c in range(4):
                if c in (a,b):continue
                t=1<<c
                flag=sum((1<<v) for v in range(4) if ep(vm[v],vm[v]^t) in E)
                flag+=sum((1<<(4+e)) for e,(u,v) in enumerate(Q2) if ep(vm[u]^t,vm[v]^t) in E)
                flags.append(flag)
            yield root,flags
def packed_index(b,i,j):
    if i>j:i,j=j,i
    n=DIMS[b]
    return STARTS[b]+i*n-i*(i-1)//2+j-i
def feature_face(g):
    out=Counter()
    for root,(first,second) in faces(g):
        canonical=min(rm[root] for rm,_ in ACTIONS);b=ROOTS.index(canonical)
        _,initial=next(act for act in ACTIONS if act[0][root]==canonical)
        s,t=initial[first],initial[second]
        stabilizer=[fm for rm,fm in ACTIONS if rm[canonical]==canonical]
        for fm in stabilizer:
            i,j=SID[b][fm[s]],SID[b][fm[t]];scale=8//len(stabilizer)
            out[packed_index(b,i,j)]+=280*scale
            out[packed_index(b,i,i)]+=28*scale
            out[packed_index(b,j,j)]+=28*scale
    return out
def transform_graph(g,vm):
    return sum(1<<EI[ep(vm[u],vm[v])] for k,(u,v) in enumerate(ORDER) if g>>k&1)
def new_graphs(frozen):
    # Deterministic additions independent of any solver: repeatedly greedily add
    # cube edges only if no new square appears. Keep explicit fresh nonmaximal cases.
    result=[];frozen=set(frozen)
    for trial in range(16):
        seed=0x9e3779b9*(trial+1)&0xffffffff
        ranks=[]
        for e in range(32):
            seed=(1664525*seed+1013904223)&0xffffffff;ranks.append((seed,e))
        g=0
        for _,e in sorted(ranks):
            test=g|(1<<e)
            try:literal_L(test)
            except AssertionError:continue
            g=test
        for candidate in (g,g&0x55555555,g&0x0fff0fff):
            if candidate not in frozen and candidate not in result:result.append(candidate)
    assert len(result)>0
    return result
def functional_checks(graphs,localL,K):
    active_graphs=js(SCOPE/'POOL_GRAPH_CODES.json');active_F=mat(SCOPE/'INTEGER_FEATURES.npz')
    assert active_F.shape[0]==len(active_graphs) and active_F.shape[1]==101801
    active_index={g:i for i,g in enumerate(active_graphs)}
    assert len(active_index)==len(active_graphs) and set(graphs)<=set(active_graphs)
    # Independently reconstruct all face coefficients, rather than relying on
    # the author's zero residual grid or opaque producer F.
    rr=[];cc=[];vv=[]
    for row,g in enumerate(graphs):
        for k,v in feature_face(g).items():rr.append(row);cc.append(k);vv.append(v)
    ownF=sparse.csr_matrix((np.asarray(vv,dtype=np.int64),(rr,cc)),shape=(len(graphs),101801))
    stored=sparse.hstack([active_F[[active_index[g] for g in graphs],:STARTS[5]],sparse.csr_matrix((len(graphs),45),dtype=np.int64)],format='csr')
    assert (ownF!=stored).nnz==0
    # All products int64: coeff/row magnitudes are far below 2^63.
    product=ownF@sparse.csr_matrix(K).T
    assert np.array_equal(4*product.toarray(),5*64512*localL.T)
    fresh=new_graphs(graphs)
    native_graphs=[];native_expect=[]
    row_weights=np.array([((i*37)%23)-11 for i in range(204)],dtype=np.int64)
    W=row_weights@K
    for g in fresh:
        ownL=literal_L(g);fc=feature_face(g)
        value=sum(int(v)*K[:,k] for k,v in fc.items())
        assert np.array_equal(4*value,5*64512*ownL)
        assert 4*sum(int(v)*int(W[k]) for k,v in fc.items())==5*64512*int(row_weights@ownL)
        # Native --graphs keeps its documented default density numerator 2016e.
        native_graphs.append(g);native_expect.append(2016*g.bit_count()+sum(int(v)*int(W[k]) for k,v in fc.items()))
    # Every Q4 isometry on three fresh test graphs, plus asymmetric root frames.
    symtests=0
    for g in fresh[:3]:
        base=literal_L(g)
        for perm in permutations(range(4)):
            for trans in range(16):
                vm=[trans ^ sum((1<<perm[a]) for a in range(4) if v>>a&1) for v in range(16)]
                assert np.array_equal(base,literal_L(transform_graph(g,vm)))
                symtests+=1
    # Native graph mode evaluates only these fresh graphs, not a full oracle scan.
    native=B/'finite8_flags/oracle/finite8_separator'
    matrix=HERE/'NATIVE_SIGNED_KERNELS.txt';graphbin=HERE/'NATIVE_FRESH_GRAPHS.bin'
    with matrix.open('w') as f:
        f.write('1 -1 64512\n')
        for b,n in enumerate(DIMS):
            f.write(str(n)+'\n')
            for i in range(n):
                f.write(' '.join(str(int(W[packed_index(b,i,j)])) for j in range(n))+'\n')
    graphbin.write_bytes(b''.join(struct.pack('<I',g) for g in native_graphs))
    read(native);read(native.with_suffix('.cpp'));read(native.parent/'keys.bin')
    cmd=[str(native),str(matrix),'--graphs',str(graphbin)]
    run=subprocess.run(cmd,cwd=native.parent,capture_output=True,text=True)
    (HERE/'NATIVE_STDOUT.txt').write_text(run.stdout);(HERE/'NATIVE_STDERR.txt').write_text(run.stderr)
    assert run.returncode==0,run.stderr
    scores=[]
    for line in run.stdout.splitlines():
        if line.startswith('SCORE '):
            _,gs,ss,_,den=line.split();scores.append((int(gs),int(ss),int(den)))
    assert scores==[(g,int(s),64512) for g,s in zip(native_graphs,native_expect)]
    # Wrong-denominator adversaries: empty local graph makes both omitted
    # diagonal correction and omitted collision terms visibly fail.
    empty=literal_L(0);nonzero=int(np.flatnonzero(empty)[0]);assert empty[nonzero]==64
    assert Fraction(4,5)*96 != 64 and Fraction(4,5)*Fraction(24*10*80,288) != 64
    assert Fraction(1,64)*Fraction(4,5)==Fraction(1,80)
    return check('functional',dict(frozen_graphs_rebuilt=len(graphs),all_stored_face_coefficients_match=True,all204_times14090_pointwise_residuals_zero=True,active_pool_at_read=len(active_graphs),fresh_out_of_frozen_pool=len(fresh),fresh_graph_codes=fresh,isometry_tests=symtests,signed_weight_min=int(row_weights.min()),signed_weight_max=int(row_weights.max()),native_command=cmd,native_default_density_term='2016*edgecount separately included in native expectation',native_graph_mode_only=True,native_fresh_scores_match=True,wrong_denominator_adversaries_rejected=True))

def q8_checks():
    seed=B.parents[2]/'data/q8_seed682.edges'
    paths=[seed,B/'finite8_maximal_leaf_gate/CALIBRATION.edges',B/'finite8_maximal_leaf_gate/review/SAME_PARITY_COUNTEREXAMPLE.edges']
    cases=[]
    for path in paths:
        E={ep(*map(int,line.split())) for line in read(path).decode().splitlines() if line.strip()};cases.append((path.name,E))
    cases += [('empty',set()),('oneaxis_matching',{(v,v^1) for v in range(256) if v%2==0}),('even_star',{ep(0,1<<a) for a in range(8)}),('odd_star',{ep(1,1^(1<<a)) for a in range(8)})]
    results=[]
    for name,E in cases:
        assert all(0<=u<v<256 and (u^v).bit_count()==1 for u,v in E)
        adj=[set() for _ in range(256)]
        for u,v in E:adj[u].add(v);adj[v].add(u)
        assert all(len(adj[u]&adj[v])<=1 for u,v in combinations(range(256),2))
        H=np.zeros(204,dtype=np.int64);L=np.zeros(204,dtype=np.int64)
        for u,v in edges(8):
            axis=(u^v).bit_length()-1;r=int((u,v) in E);labels=[]
            for other in range(8):
                if other==axis:continue
                x,y=u^(1<<other),v^(1<<other)
                labels.append(int(ep(u,x) in E)+2*int(ep(v,y) in E)+4*int(ep(x,y) in E))
            assert r==0 or 7 not in labels
            # Use every actual ordered orientation and every triple of positions,
            # different from binomial-product export reconstruction.
            for aa in combinations(range(7),3):
                t=tuple(sorted(labels[i] for i in aa));H[ROW_TRIPLES[r,t]]+=1
                H[ROW_TRIPLES[r,tuple(sorted(flip(s) for s in t))]]+=1
        slices=0
        for axes in combinations(range(8),4):
            others=[a for a in range(8) if a not in axes]
            for fixed in range(16):
                base=sum((1<<a) for i,a in enumerate(others) if fixed>>i&1)
                vm=[base ^ sum((1<<a) for i,a in enumerate(axes) if v>>i&1) for v in range(16)]
                g=sum((1<<k) for k,(u,v) in enumerate(ORDER) if ep(vm[u],vm[v]) in E)
                L+=literal_L(g);slices+=1
        assert slices==1120 and np.array_equal(L,H) and L.sum()==H.sum()==71680
        results.append(dict(case=name,edges=len(E),Q4_slices=slices,ambient_edges=1024,total_both_sides=71680,all204_exact=True))
    assert [x['edges'] for x in results]==[682,576,584,0,128,8,8]
    return check('actual_Q8',results)

def exact_point_checks(cur,ded,currentH):
    point=js(P/'INPUT_MASTER195.json',exact=True)
    L=[Fraction(0) for _ in ROWS];H=[Fraction(0) for _ in ROWS]
    for g,w in point['lambda']:
        value=literal_L(g)
        for j,v in enumerate(value):L[j]+=w*int(v)/64
    for k,w in point['beta']:
        for j,v in enumerate(currentH[:,k]):H[j]+=w*int(v)/70
    differences=[a-b for a,b in zip(L,H)]
    diagnostic=js(P/'MASTER195_DIAGNOSTIC.json')
    for (r,z),diff,row in zip(ROWS,differences,diagnostic['rows']):
        assert row['root']==r and row['histogram']==list(z) and Fraction(row['exact_difference'])==diff
    peak=max(map(abs,differences));which=[i for i,v in enumerate(differences) if abs(v)==peak]
    # Replay the 63 older rows only as their finite decimal-point residuals.
    layout=js(SCOPE/'EXTRA_EQUALITY_LAYOUT.json')
    balance=mat(SCOPE/layout['balance_matrix']);mb=mat(SCOPE/layout['moment_beta_matrix']);sel=mat(SCOPE/layout['moment_selector_matrix'])
    beta=[Fraction(0) for _ in range(1751)]
    for k,w in point['beta']:beta[k]=w
    def exact_mv(M,vector):
        C=M.tocsr();return [sum((int(C.data[k])*vector[int(C.indices[k])] for k in range(C.indptr[i],C.indptr[i+1])),Fraction(0)) for i in range(C.shape[0])]
    oldbalance=[v/7 for v in exact_mv(balance,beta)]
    # Vertex coefficients reconstructed literally for the actual graphs used by
    # the point, avoiding active-pool positions as assumptions.
    vertex=[Fraction(0) for _ in range(45)]
    pairs=list(combinations(range(4),2))
    vreps=sorted({min(c,((c&1)<<1)|((c&2)>>1)|((c&4)<<1)|((c&8)>>1)) for c in range(15)})
    def vid(c):return vreps.index(min(c,((c&1)<<1)|((c&2)>>1)|((c&4)<<1)|((c&8)>>1)))
    for g,w in point['lambda']:
        E={e for k,e in enumerate(ORDER) if g>>k&1};coeff=Counter()
        for x in range(16):
            states=[]
            for a,b in pairs:
                vm=[x,x^(1<<a),x^(1<<b),x^(1<<a)^(1<<b)]
                c=sum((1<<e) for e,(u,v) in enumerate(Q2) if ep(vm[u],vm[v]) in E);states.append(vid(c))
            for i in range(6):
                coeff[packed_index(5,states[i],states[i])-STARTS[5]]+=24
                for j in range(i+1,6):coeff[packed_index(5,states[i],states[j])-STARTS[5]]+=720 if set(pairs[i]).isdisjoint(pairs[j]) else 144
        for k,v in coeff.items():vertex[k]+=w*v
    lm=exact_mv(sel,vertex);bm=exact_mv(mb,beta)
    oldmoment=[7*a/129024-b/56 for a,b in zip(lm,bm)]
    oldpeak=max(map(abs,oldbalance+oldmoment))
    assert oldpeak < Fraction(1,10**8)
    result=dict(lambda_columns=len(point['lambda']),beta_columns=len(point['beta']),rows=204,all_exact_strings_match=True,max_absolute_difference=str(peak),max_absolute_difference_decimal=float(peak),max_rows=which,older63_max_exact_residual=str(oldpeak),older63_max_residual_decimal=float(oldpeak),older63_only_decimal_residual_not_exact_feasibility=True,not_graph_or_infeasibility_certificate=True)
    output('MASTER195_EXACT_REPLAY.json',dict(result,rows=[dict(row=i,exact_difference=str(x)) for i,x in enumerate(differences)]))
    return check('master195',result)

def main():
    # Hash theorem-bearing sources and actual producer/consumer code before use.
    for path in [P/'PROOF.md',P/'edge3.py',P/'export.py',P/'verify_actual.py',P/'INTERFACE.json',P/'FILES_SHA256.json',LIFT/'PROOF.md',LIFT/'build_check_lift.py',B/'finite8_flags/finite_flags.py',AUG/'import_edge3_sampling.py',AUG/'vertex_priced_working_sets.py',AUG/'extract_native_dual_oracle.py',AUG/'run_local_score_oracle.py',AUG/'prepare_maximal_scope.py',B/'finite8_maximal_leaf_gate/PROOF.md']:
        read(path)
    raw,cur,ded,graphs,H,currentH,localL,maps=map_checks()
    K,As,kernels=kernel_checks()
    functional=functional_checks(graphs,localL,K)
    actual=q8_checks()
    master=exact_point_checks(cur,ded,currentH)
    result=dict(status='PASS_BOUNDED_INDEPENDENT_EXACT_REPLAY',maps=maps,kernels=kernels,functional=functional,actual_Q8=actual,master195=master,seconds=time.monotonic()-START,no_author_modules_imported=True,no_LP_or_full_Q4_scan=True,no_PSD_converse=True,upper682='OPEN',actual_model=None,requested_model='gpt-6.1-sol',requested_reasoning='ultra',acceptance='same-family/provisional; actual identity unattested')
    output('INDEPENDENT_CHECK.json',result)
    output('INPUT_RECEIPT.json',dict(files=INPUTS,scope='Declared actually read proof/code/data inputs. Source-unit coverage and semantic closure are separate artifacts.',generated_by='independent_check.py'))
    print('DONE',json.dumps({k:v for k,v in result.items() if k in ('status','seconds')}),flush=True)
if __name__=='__main__':main()
