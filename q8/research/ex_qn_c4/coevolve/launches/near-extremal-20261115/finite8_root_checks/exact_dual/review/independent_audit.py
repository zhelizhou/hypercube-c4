"""Fresh deterministic-local audit; does not import the producer or flag/lift code.

All write destinations are this review directory. Scientific maps are derived
from cube geometry, integer histograms, and cut parameters, never from DUAL_*.
"""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
from fractions import Fraction as Q
from itertools import combinations, combinations_with_replacement
from collections import Counter
from math import comb, lcm
import json, hashlib, time, argparse

HERE = Path(__file__).resolve().parent
BASE = HERE.parents[2]
ap=argparse.ArgumentParser()
ap.add_argument('--scope',default='pool_B684plus_enriched3')
ap.add_argument('--reference',default='B_enriched3_replay001')
ap.add_argument('--output',default='independent_B3')
args=ap.parse_args()
SCOPE = BASE/'finite8_degree_augmentation'/args.scope
OUT=HERE/args.output
assert OUT.parent==HERE and not OUT.exists()
OUT.mkdir()
REFERENCE=HERE.parent/args.reference
sys.path.insert(0, str(BASE/'finite8_flags/deps'))
import numpy as np
from scipy import sparse

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
used = {}
def read(p):
    p = Path(p); used[str(p)] = sha(p)
    return json.loads(p.read_text())
def scientific(name): return read(SCOPE/name)
def saved(name):
    p=SCOPE/name;used[str(p)]=sha(p)
    return sparse.load_npz(p).tocsr()
def same_matrix(a,b,label):
    a=sparse.csr_matrix(a);b=sparse.csr_matrix(b)
    d=a-b;d.eliminate_zeros()
    assert a.shape==b.shape and d.nnz==0,(label,a.shape,b.shape,d.nnz)
    checks.append(dict(name=label,shape=list(a.shape),exact_nonzero_differences=0))
def nearest(q):
    # Integer floor, with the same unambiguous positive tie convention.
    return q.numerator//q.denominator + int(q-q.numerator//q.denominator >= Q(1,2))
def flip(s):return (s&4)|((s&1)<<1)|((s&2)>>1)
def canon_vertex(c):return min(c,((c&1)<<1)|((c&2)>>1)|((c&4)<<1)|((c&8)>>1))
SQ=[(0,1),(0,2),(1,3),(2,3)]
ROOTS=[0,1,3,6,7]
VREPS=sorted({canon_vertex(c) for c in range(15)})
VINDEX={c:VREPS.index(canon_vertex(c)) for c in range(15)}
DIM=[240,212,190,187,170,9]
START=[0]
for n in DIM:START.append(START[-1]+n*(n+1)//2)
PACK=[list(combinations_with_replacement(range(n),2)) for n in DIM]
PINDEX=[{ij:k for k,ij in enumerate(v)} for v in PACK]
GROUP=[]
for swap in range(2):
    for shift in range(4):
        vm=[shift ^ ((((x&1)<<1)|((x&2)>>1)) if swap else x) for x in range(4)]
        em=[SQ.index(tuple(sorted((vm[a],vm[b])))) for a,b in SQ]
        GROUP.append((vm,em))
def root_action(r,h):return sum(((r>>k)&1)<<h[1][k] for k in range(4))
def flag_action(f,h):
    return sum(((f>>k)&1)<<h[0][k] for k in range(4))+sum(((f>>(4+k))&1)<<(4+h[1][k]) for k in range(4))
def legal_flag(r,f):
    return f<240 and not any((r>>k&1) and (f>>(4+k)&1) and (f>>a&1) and (f>>b&1) for k,(a,b) in enumerate(SQ))
STATES=[[f for f in range(240) if legal_flag(r,f)] for r in ROOTS]
assert list(map(len,STATES))==DIM[:5]
IDS=[{f:i for i,f in enumerate(codes)} for codes in STATES]
STAB=[[h for h in GROUP if root_action(r,h)==r] for r in ROOTS]
EDGES3=[(v,v^(1<<a)) for v in range(8) for a in range(3) if not v&(1<<a)]
EDGES=EDGES3+[(u+8,v+8) for u,v in EDGES3]+[(v,v+8) for v in range(8)]
EI={tuple(sorted(e)):i for i,e in enumerate(EDGES)}
def edge_bit(m,u,v):return (m>>EI[tuple(sorted((u,v)))])&1
def triple_index(r,values):
    z=[0]*(8-r)
    for s in values:z[s]+=1
    return TIDX[r,tuple(z)]

checks=[];t0=time.monotonic()
result=read(SCOPE/'RESULT.json'); exact_source=read(REFERENCE/'EXACT_COMBINATION.json')
Dy=10**9;T=10**9
# Read the decimal token exactly, independently from the producer's JSON parser.
decimal=json.loads((SCOPE/'RESULT.json').read_text(),parse_float=Q)
y=[nearest(v*Dy) for v in decimal['equality_duals']]
z=[min(0,nearest(v*Dy)) for v in decimal['inequality_duals']]
meta=scientific('CUT_ROW_METADATA.json')
active=[(i,row,-z[i]) for i,row in enumerate(meta) if z[i]]
assert len(y)==356 and len(z)==len(meta)
assert all(v>=0 for _,_,v in active)
assert y==exact_source['y'] and z==exact_source['z']
assert all(row.get('n',28 if row.get('block')==5 else 6)==(28 if row.get('block')==5 else 6) for row in meta if row['kind']=='INTEGER_ROUNDING')
scales=[int(row.get('positive_power2_normalization',1)) for _,row,_ in active]
assert all(s>0 and (s&(s-1))==0 for s in scales)
D=Dy*lcm(8960,784,98,512,7,56,80,16,8192,*(s*128*784 for s in scales))
assert D==int(exact_source['common_denominator'])
NW=np.zeros(START[-1],dtype=object)
profiles=scientific('PROFILE_SNAPSHOT.json')['remaining'];assert len(profiles)==645
assert Counter(p['m'] for p in profiles)=={684:385,685:170,686:66,687:20,688:4}
for p in profiles:
    assert sum(p['degrees'])==128 and sum(i*n for i,n in enumerate(p['degrees']))==p['m'] and p['degrees'][0]==0
rawhist=scientific('GENERATOR_HISTOGRAMS.json');de=scientific('GENERATOR_DEDUPLICATION.json')
sel=de['selected_original_indices'];assert len(sel)==1751 and len(rawhist)==3432
expected=[]
for r in (0,1):
    for xs in combinations_with_replacement(range(8-r),7):
        xx=[xs.count(i) for i in range(8-r)]
        if r==0 and xx[7]==0:continue
        expected.append(dict(root_retained=r,counts=xx))
assert rawhist==expected
allowed=[]
for h in rawhist:
    r=h['root_retained'];x=h['counts']
    a=r+sum((s&1)*n for s,n in enumerate(x));b=r+sum((s>>1&1)*n for s,n in enumerate(x))
    allowed.append(r==0 or ((a!=1 or x[6]==7) and (b!=1 or x[5]==7)))
covered=[i for g in de['groups'] for i in g]
assert len(covered)==len(set(covered)) and set(covered)=={i for i,ok in enumerate(allowed) if ok}
assert all(k in g for k,g in zip(sel,de['groups']))

# Rebuild all finite scientific RHS maps on every raw histogram, then the pinned
# current order. Equality moment entries are actual upper matrix entries.
EROW=[(r,i,j) for r,n in enumerate((8,7)) for i in range(n) for j in range(i,n)]
G=np.zeros((64,len(rawhist)),dtype=np.int64);EP=np.zeros((18,len(rawhist)),dtype=np.int64)
C=np.zeros((162,len(rawhist)),dtype=np.int64);CAP=np.zeros((9,len(rawhist)),dtype=np.int64)
TROWS=[(r,tuple(xs.count(s) for s in range(8-r))) for r in (0,1) for xs in combinations_with_replacement(range(8-r),3)]
TIDX={v:i for i,v in enumerate(TROWS)};assert len(TROWS)==204
H3=np.zeros((204,len(rawhist)),dtype=np.int64)
for k,h in enumerate(rawhist):
    r=h['root_retained'];x=h['counts'];a=r+sum((s&1)*n for s,n in enumerate(x));b=r+sum((s>>1&1)*n for s,n in enumerate(x))
    EP[9*r+a,k]+=1;EP[9*r+b,k]+=1
    for row,(rr,i,j) in enumerate(EROW):
        if rr==r:G[row,k]=x[i]*x[j]+x[flip(i)]*x[flip(j)]
    for s,n in enumerate(x):
        for side,d in [(0,a),(1,b)]:
            code=r+2*(s>>side&1)+4*(s>>(1-side)&1)+8*(s>>2&1)
            C[81*r+9*d+VINDEX[code],k]+=n
    if r:
        CAP[a,k]+=b;CAP[b,k]+=a
    xs=[s for s,n in enumerate(x) for _ in range(n)]
    for positions in combinations(range(7),3):
        ss=[xs[i] for i in positions]
        H3[triple_index(r,ss),k]+=1;H3[triple_index(r,[flip(s) for s in ss]),k]+=1
assert np.all(C.sum(axis=0)==14) and np.all(H3.sum(axis=0)==70)
for a in (G,EP,C,CAP,H3):
    for k,group in zip(sel,de['groups']):
        assert np.all(a[:,group]==a[:,k,None])
G=G[:,sel];EP=EP[:,sel];C=C[:,sel];CAP=CAP[:,sel];H3=H3[:,sel]
same_matrix(G,saved('EDGE_GENERATOR_DEDUP_NUMERATOR.npz'),'64 edge second-moment numerators')
same_matrix(EP,saved('EDGE_ENDPOINT_DEDUP.npz'),'18 endpoint counts')
SDEG=np.array([p['degrees'] for p in profiles],dtype=np.int64)
RHS=np.array([[(d if r else 8-d)*p['degrees'][d] for p in profiles] for r in (0,1) for d in range(9)],dtype=np.int64)
same_matrix(RHS,saved('EDGE_DEGREE_PROFILE_RHS_NUMERATOR.npz'),'18 degree incidence RHS')
B=np.array([[sum(p['degrees'][d]*comb(d,j)*comb(8-d,4-j) for d in range(9) if j<=d and 4-j<=8-d) for j in range(5)] for p in profiles],dtype=np.int64)
features_path=SCOPE/'MARGINAL_FEATURES.npz';used[str(features_path)]=sha(features_path);marg=np.load(features_path)
assert np.array_equal(B,marg['profile_hypergeom'])
checks.append(dict(name='645 by five degree hypergeometric numerators',exact_nonzero_differences=0))
MIX=[1,4,5,8];VG=[[0,3,7],[1,4,5,8],[2,6]]
BAL=np.array([C[81+9*d+j]-C[9*d+j] for d in range(9) for j in MIX])
MB=np.array([sum([comb(8-d,2),d*(8-d),comb(d,2)][g]*(C[9*d+i]+C[81+9*d+i]) for d in range(9)) for g in range(3) for i in range(9)])
W=np.zeros((27,45),dtype=np.int64)
for g,group in enumerate(VG):
    for i in range(9):
        for j in group:W[9*g+i,PINDEX[5][min(i,j),max(i,j)]]+=2 if i==j else 1
layout=scientific('EXTRA_EQUALITY_LAYOUT.json');e3=scientific('EXTRA_EDGE3_LAYOUT.json')
same_matrix(BAL,saved(layout['balance_matrix']),'36 retained-minus-missing state rows')
same_matrix(MB,saved(layout['moment_beta_matrix']),'27 vertex group-moment beta rows')
same_matrix(W,saved(layout['moment_selector_matrix']),'27 packed selector rows (twice row-group sum)')
same_matrix(H3,saved(e3['beta_hypergeom']),'204 both-orientation triple hypergeometric numerators')
leafpath=SCOPE/'LEAF_NEIGHBOR_FEATURES.npz';used[str(leafpath)]=sha(leafpath);leaf=np.load(leafpath)
CAPAL=np.array([[(8*t-comb(t,2))*p['degrees'][t] for p in profiles] for t in range(9)])
assert np.array_equal(CAP,leaf['neighbor_beta_upper']) and np.array_equal(CAPAL,leaf['neighbor_alpha_upper_numerator'])
assert np.array_equal(SDEG[:,8]-SDEG[:,1],leaf['leaf_alpha_lower'])

# Reconstruct every 204 edge3 kernel independently, by literal three-label
# indicators at each root edge. No exported lift or producer module is called.
K3=np.zeros((204,START[-1]),dtype=np.int16)
edge_lift=[]
qe=[];cursor=7
for n in (8,7):
    q=np.zeros((n,n),dtype=object)
    for i in range(n):
        for j in range(i,n):q[i,j]=q[j,i]=y[cursor]*(2 if i==j else 1);cursor+=1
    qe.append(q)
assert cursor==71
for b,(r,codes) in enumerate(zip(ROOTS,STATES)):
    n=len(codes);ii,jj=np.triu_indices(n);aa=np.zeros((204,n,n),dtype=np.int16)
    lifted=np.zeros((n,n),dtype=object)
    for e,(u,v) in enumerate(SQ):
        rr=r>>e&1;other=3^(u^v)
        oldbits=[SQ.index(tuple(sorted(pair))) for pair in [(u,u^other),(v,v^other),(u^other,v^other)]]
        base=sum((r>>k&1)<<j for j,k in enumerate(oldbits))
        ext=[(f>>u&1)+2*(f>>v&1)+4*(f>>(4+e)&1) for f in codes]
        lookup=np.array([[triple_index(rr,[base,a,c]) for c in range(8-rr)] for a in range(8-rr)])
        revlookup=np.array([[triple_index(rr,[flip(base),flip(a),flip(c)]) for c in range(8-rr)] for a in range(8-rr)])
        for i,a in enumerate(ext):
            for j,c in enumerate(ext):
                aa[lookup[a,c],i,j]+=1;aa[revlookup[a,c],i,j]+=1
                # Independent bilinear expansion of (6 e_a+e_base)^T
                # (Q+PQP^T) (6 e_c+e_base). Raw Q has no flip average.
                def symq(x,w):return qe[rr][x,w]+qe[rr][flip(x),flip(w)]
                lifted[i,j]+=36*symq(a,c)+6*symq(a,base)+6*symq(base,c)+symq(base,base)
    diag=np.diagonal(aa,axis1=1,axis2=2)
    K3[:,START[b]:START[b+1]]=12*aa[:,ii,jj]-diag[:,ii]-diag[:,jj]
    edge_lift.append(lifted)
assert np.all(K3[:,:START[5]].sum(axis=0)==80) and np.all(K3[:,START[5]:]==0)
same_matrix(K3,saved(e3['lift_packed']),'all204 independently rebuilt edge3 packed kernels')

def factor(v,den):
    assert D%den==0,den
    return int(v)*(D//den)
def add(to,arr,v,den):to+=np.asarray(arr,dtype=object)*factor(v,den)
def kernel(b,m,v,den):
    assert len(m)==DIM[b] and all(len(row)==DIM[b] for row in m)
    assert all(m[i][j]==m[j][i] for i in range(DIM[b]) for j in range(DIM[b]))
    add(NW[START[b]:START[b+1]],[m[i][j] for i,j in PACK[b]],v,den)
NA=np.zeros(645,dtype=object);NB=np.zeros(1751,dtype=object)
NH=np.array([factor(64512*(y[0]+y[2+j]),16*Dy) for j in range(5)],dtype=object)
NA[:]=factor(y[1],Dy)
for j in range(5):add(NA,B[:,j],-y[2+j],Dy*8960)
for b,m in enumerate(edge_lift):kernel(b,m,1,Dy*784)
for rows,vec,matrix,den in [(y[7:71],NB,G,98),(y[71:89],NA,RHS,512),(y[125:152],NB,MB,56),(y[152:356],NB,H3,70)]:
    for v,arr in zip(rows,matrix):add(vec,arr,-v,Dy*den)
for v,arr in zip(y[71:89],EP):add(NB,arr,v,Dy)
for v,arr in zip(y[89:125],BAL):add(NB,arr,v,Dy*7)
for v,arr in zip(y[125:152],W):add(NW[START[5]:],arr,7*v,Dy*2)
for v,arr in zip(y[152:356],K3):add(NW,arr,v,Dy*80)

finite_checks=[]
for index,row,weight in active:
    kind=row['kind'];b=row.get('block');s=row.get('positive_power2_normalization',1)
    if kind=='PSD':
        q=row['q'];kernel(b,[[a*c for c in q] for a in q],weight,Dy*s)
    elif kind=='INTEGER_ROUNDING':
        q=row['q'];n=row['n'];t=row['t']
        kernel(b,[[n*n*a*c-Q(n,2)*(2*t+1)*(a+c)+t*(t+1) for c in q] for a in q],weight,Dy*s)
    elif kind=='GLOBAL_MAXIMAL_LEAF':add(NA,SDEG[:,8]-SDEG[:,1],weight,Dy)
    elif kind=='RETAINED_NEIGHBOR_DEGREE_CAPACITY':
        t=row['degree'];add(NA,CAPAL[t],weight,Dy*8192);add(NB,CAP[t],-weight,Dy*16)
    elif kind=='CONDITIONAL_VERTEX_EXTRA':
        c=scientific(row['source']);kernel(5,c['integer_Q'],weight,Dy*s)
        add(NA,SDEG@np.array(c['degree_bias_raw'],dtype=object),weight,Dy*s*128*784)
        # Independently enumerate unshifted three-group compositions, then
        # filter the explicit maximality condition. No native oracle is read.
        def comp(n,k):
            if k==1:yield(n,);return
            for a in range(n+1):
                for tail in comp(n-a,k-1):yield(a,)+tail
        minima=[];counts=[]
        qq=np.array(c['integer_Q'],dtype=np.int64)
        for degree in range(9):
            vectors=[]
            totals=(comb(8-degree,2),degree*(8-degree),comb(degree,2))
            for a in comp(totals[0],3):
                for b0 in comp(totals[1],4):
                    if b0[3]<8-degree:continue
                    for cc in comp(totals[2],2):
                        vv=[0]*9
                        for group,values in zip(VG,(a,b0,cc)):
                            for j,value in zip(group,values):vv[j]=value
                        vectors.append(vv)
            counts.append(len(vectors))
            if not vectors:assert degree==0;minima.append(None);continue
            vv=np.array(vectors,dtype=np.int64)
            assert 784*int(np.max(abs(qq)))<2**63
            values=np.einsum('bi,ij,bj->b',vv,qq,vv,optimize=True)
            minimum=int(min(values));assert minimum+c['degree_bias_raw'][degree]==0
            minima.append(minimum)
        assert counts==[0,253,22848,75504,89180,50050,13728,1848,29] and sum(counts)==253440
        finite_checks.append(dict(kind=kind,index=index,source=row['source'],complete_histograms=253440,degree_counts=counts,degree_quadratic_minima=minima,all_nonempty_degree_minimum_plus_bias_zero=True))
    elif kind=='CONNECTOR_FINITE6_EXTRA':
        c=scientific(row['source']);q=c['connector_Q'];codes=[f&15 for f in STATES[b]]
        assert codes==c['full_state_connector_codes']
        assert all(q[(flag_action(i,h)&15)][(flag_action(j,h)&15)]==q[i][j] for h in STAB[b] for i in range(16) for j in range(16))
        mn=min(sum(q[i][j] for i in xs for j in xs) for xs in combinations_with_replacement(range(16),6))
        assert mn>=0 and mn==c['finite6']['minimum']
        kernel(b,[[q[i][j] for j in codes] for i in codes],weight,Dy*s)
        finite_checks.append(dict(kind=kind,index=index,source=row['source'],histograms=54264,minimum=mn))
    elif kind=='FULL_FINITE6_PROJECTION_EXTRA':
        c=scientific(row['source']);q=c['small_Q'];codes=STATES[b]
        full=[[sum(q[flag_action(f,h)>>4][flag_action(g,h)>>4] for h in STAB[b]) for g in codes] for f in codes]
        assert full==c['full_Q'] and codes==c['full_state_codes']
        mn=min(sum(q[i][j] for i in xs for j in xs) for xs in combinations_with_replacement(range(15),6))
        assert mn>=0 and mn==c['finite6']['minimum']
        kernel(b,full,weight,Dy*s)
        finite_checks.append(dict(kind=kind,index=index,source=row['source'],histograms=38760,minimum=mn,no_extra_stabilizer=True))
    else:raise ValueError(kind)

for name,actual in [('packed_kernel_numerators',NW),('histogram_packed_numerators',NH),('alpha_numerators',NA),('beta_numerators',NB)]:
    assert list(map(int,actual))==exact_source[name],name
    checks.append(dict(name='independent exact '+name,coordinates=len(actual),exact_nonzero_differences=0))
query=np.array([nearest(Q(int(v)*T,D)) for v in NW],dtype=np.int64)
qh=np.array([nearest(Q(int(v)*T,D)) for v in NH],dtype=np.int64)
eps=Q(max(abs(int(v)*T-int(q)*D) for v,q in zip(NW[:START[5]],query[:START[5]]))+max(abs(int(v)*T-int(q)*D) for v,q in zip(NW[START[5]:],query[START[5]:])),D*T)+Q(16*max(abs(int(v)*T-int(q)*D) for v,q in zip(NH,qh)),64512*D*T)
delta=Q(y[0]+y[1],Dy);am=Q(int(max(NA)),D);bm=Q(int(max(NB)),D)
evaluation=read(REFERENCE/'FULL_CERTIFICATE_EVALUATION.json')
rawmax=evaluation['query_raw_complete_maximum']
margin=delta-am-bm-eps-Q(rawmax,64512*T)
assert margin==Q(evaluation['exact_safe_margin'])
np.savez_compressed(OUT/'independent_coefficients.npz',query=query,histogram_query=qh)
with (OUT/'oracle_matrices.txt').open('w') as f:
    f.write('1 -1 64512\n')
    for b,n in enumerate(DIM):
        f.write(str(n)+'\n');mat=np.zeros((n,n),dtype=np.int64)
        for (i,j),v in zip(PACK[b],query[START[b]:START[b+1]]):mat[i,j]=mat[j,i]=v
        for rr in mat:f.write(' '.join(map(str,rr))+'\n')
(OUT/'oracle_linear.txt').write_text('0 '+' '.join(map(str,qh))+'\n')
for filename in ('oracle_matrices.txt','oracle_linear.txt'):
    assert (OUT/filename).read_bytes()==(REFERENCE/filename).read_bytes()
    used[str(OUT/filename)]=sha(OUT/filename)
    used[str(REFERENCE/filename)]=sha(REFERENCE/filename)

# Independent literal geometry for every library graph. Generate sparse folded
# F directly; no finite_flags, edge_flags, or lift import is used.
graphs=scientific('POOL_GRAPH_CODES.json')
gm=np.array(graphs,dtype=np.uint32);N=len(graphs);degrees=np.zeros((N,16),dtype=np.int16)
for k,(u,v) in enumerate(EDGES):
    bit=(gm>>k)&1;degrees[:,u]+=bit;degrees[:,v]+=bit
H=np.stack([(degrees==d).sum(axis=1) for d in range(5)],axis=1)
assert np.all(H.sum(axis=1)==16) and np.array_equal(H,marg['hist'])
fr=[];fc=[];fv=[]
def chunk(rows,cols,val):
    rows=np.asarray(rows);cols=np.asarray(cols)
    fr.append(rows.astype(np.int32));fc.append(cols.astype(np.int32));fv.append(np.full(len(rows),val,dtype=np.int32))
def eb(u,v):return ((gm>>EI[tuple(sorted((u,v)))])&1).astype(np.int16)
ALL=np.arange(N,dtype=np.int32)
for a,b in combinations(range(4),2):
    for base in range(16):
        if base&((1<<a)|(1<<b)):continue
        vs=[base,base^(1<<a),base^(1<<b),base^(1<<a)^(1<<b)]
        r=sum(eb(vs[u],vs[v])<<k for k,(u,v) in enumerate(SQ));assert np.all(r<15)
        fs=[]
        for c in range(4):
            if c in (a,b):continue
            fs.append(sum(eb(vs[u],vs[u]^(1<<c))<<u for u in range(4))+sum(eb(vs[u]^(1<<c),vs[v]^(1<<c))<<(4+k) for k,(u,v) in enumerate(SQ)))
        for root in range(15):
            rows=ALL[r==root]
            if not len(rows):continue
            canonical=min(root_action(root,h) for h in GROUP);bb=ROOTS.index(canonical)
            h0=next(h for h in GROUP if root_action(root,h)==canonical)
            fs0=[[flag_action(int(f),h0) for f in ff[rows]] for ff in fs]
            for h in STAB[bb]:
                i=np.array([IDS[bb][flag_action(f,h)] for f in fs0[0]]);j=np.array([IDS[bb][flag_action(f,h)] for f in fs0[1]])
                lo=np.minimum(i,j);hi=np.maximum(i,j)
                ids=START[bb]+lo*DIM[bb]-lo*(lo-1)//2+hi-lo
                chunk(rows,ids,2240//len(STAB[bb]))
                for v in (i,j):chunk(rows,START[bb]+v*DIM[bb]-v*(v-1)//2,224//len(STAB[bb]))
PAIRS=list(combinations(range(4),2))
for v in range(16):
    states=[]
    for a,b in PAIRS:
        code=eb(v,v^(1<<a))+2*eb(v,v^(1<<b))+4*eb(v^(1<<a),v^(1<<a)^(1<<b))+8*eb(v^(1<<b),v^(1<<a)^(1<<b))
        assert np.all(code<15)
        states.append(np.array([VINDEX[int(c)] for c in code]))
    for i,A in enumerate(PAIRS):
        for j,Bp in enumerate(PAIRS[i:],i):
            s=states[i];t=states[j];lo=np.minimum(s,t);hi=np.maximum(s,t)
            coords=START[5]+lo*9-lo*(lo-1)//2+hi-lo
            chunk(ALL,coords,24 if i==j else (144 if set(A)&set(Bp) else 720))
F=sparse.csr_matrix((np.concatenate(fv),(np.concatenate(fr),np.concatenate(fc))),shape=(N,START[-1]),dtype=np.int64);F.eliminate_zeros()
same_matrix(F,saved('INTEGER_FEATURES.npz'),f'all{N} literal graph feature rows, all{START[-1]} packed coordinates')
assert np.all(np.asarray(F[:,:START[5]].sum(axis=1)).ravel()==64512)
assert np.all(np.asarray(F[:,START[5]:].sum(axis=1)).ravel()==64512)
scores=np.asarray(F@query+H@qh,dtype=np.int64)
np.savez_compressed(OUT/'independent_library_scores.npz',scores=scores)

# All64 local upper moment rows built directly from two endpoint orientations.
U=np.zeros((64,N),dtype=np.int64);EIDX={v:i for i,v in enumerate(EROW)}
for a in range(4):
    for u in range(16):
        if u&(1<<a):continue
        v=u^(1<<a);ret=eb(u,v);ss=[]
        for c in range(4):
            if c!=a:ss.append(eb(u,u^(1<<c))+2*eb(v,v^(1<<c))+4*eb(u^(1<<c),v^(1<<c)))
        for reverse in (False,True):
            vals=[((s&4)|((s&1)<<1)|((s&2)>>1)) if reverse else s for s in ss]
            for i,j in combinations(range(3),2):
                lo=np.minimum(vals[i],vals[j]);hi=np.maximum(vals[i],vals[j])
                for r in (0,1):
                    rr=ALL[ret==r]
                    idx=np.array([EIDX[r,int(lo[k]),int(hi[k])] for k in rr]);np.add.at(U,(idx,rr),np.where(lo[rr]==hi[rr],576,288))
            for s in vals:
                for r in (0,1):
                    rr=ALL[ret==r];idx=np.array([EIDX[r,int(s[k]),int(s[k])] for k in rr]);np.add.at(U,(idx,rr),96)
same_matrix(U,saved('EDGE_U_NUMERATOR.npz'),f'all64 by{N} literal edge second moments')

# Construct exact all356 row maps on the scientific denominator L. This checks
# the maps themselves, independently of the selected multipliers and DUAL_*.
L=lcm(16,129024,8960,98,512,7,56,80*64512,70)
EL=sparse.vstack([sparse.csr_matrix(np.ones((1,N),dtype=np.int64)*(L)),sparse.csr_matrix((1,N),dtype=np.int64),sparse.csr_matrix(H.T*(L//16)),sparse.csr_matrix(U*(L//129024)),sparse.csr_matrix((18,N),dtype=np.int64),sparse.csr_matrix((36,N),dtype=np.int64),sparse.csr_matrix(W@F[:,START[5]:].T*(7*(L//129024))),sparse.csr_matrix(K3@F.T*(L//(80*64512)))],format='csr')
ER=sparse.vstack([sparse.csr_matrix((1,645+1751),dtype=np.int64),sparse.csr_matrix(np.r_[np.full(645,L,dtype=np.int64),np.zeros(1751,dtype=np.int64)][None,:]),sparse.hstack([sparse.csr_matrix(-B.T*(L//8960)),sparse.csr_matrix((5,1751),dtype=np.int64)]),sparse.hstack([sparse.csr_matrix((64,645),dtype=np.int64),sparse.csr_matrix(-G*(L//98))]),sparse.hstack([sparse.csr_matrix(-RHS*(L//512)),sparse.csr_matrix(EP*L)]),sparse.hstack([sparse.csr_matrix((36,645),dtype=np.int64),sparse.csr_matrix(BAL*(L//7))]),sparse.hstack([sparse.csr_matrix((27,645),dtype=np.int64),sparse.csr_matrix(-MB*(L//56))]),sparse.hstack([sparse.csr_matrix((204,645),dtype=np.int64),sparse.csr_matrix(-H3*(L//70))])],format='csr')
assert EL.shape==(356,N) and ER.shape==(356,645+1751)
sparse.save_npz(OUT/'independent_EL_integer.npz',EL);sparse.save_npz(OUT/'independent_ER_integer.npz',ER)
# Native float comparisons retained explicitly as diagnostics only.
elerr=EL.astype(float)/L-saved('DUAL_EL.npz');ererr=ER.astype(float)/L-saved('DUAL_ER.npz')
elmax=float(max(abs(elerr.data),default=0));ermax=float(max(abs(ererr.data),default=0))
assert elmax<1e-12 and ermax<1e-12
oldquery=read(REFERENCE/'LOCAL_PRICE_SCORE.json')
coords=[]
for b in range(6):
    for (i,j),v in zip(PACK[b],query[START[b]:START[b+1]]):
        if v:coords.append([b,i,j,int(v)])
assert coords==oldquery['original_finite8_upper_coefficient_weights'] and qh.tolist()==oldquery['histogram_weights_j0_to_j4']
out=dict(status='LOCAL_RECONSTRUCTION_ARITHMETIC_MATCHES_INDEPENDENT_SCIENTIFIC_REBUILD',scope=str(SCOPE),requested_reviewer_route=dict(backend='codex',host='codex',source='host-default',model='gpt-6.1-sol',effort='ultra',transport='native',fresh_tool='spawn_agent',continuation_tool='send_input'),actual_identity_and_effort_attested=False,same_family_provisional=True,main682='OPEN',canonical_proof_checker_invoked=False,active_exact_inequalities=len(active),active_kinds=dict(Counter(row['kind'] for _,row,_ in active)),common_denominator=str(D),equality_row_denominator=L,delta=str(delta),alpha_max=str(am),alpha_argmax=int(np.argmax(NA)),beta_max=str(bm),beta_argmax=int(np.argmax(NB)),uniform_error=str(eps),raw_complete_max_reused=rawmax,exact_safe_margin=str(margin),library_size=N,library_minmax=[int(min(scores)),int(max(scores))],all356_exact_equality_maps_rebuilt=True,native_EL_diagnostic_max=elmax,native_ER_diagnostic_max=ermax,checks=checks,finite_active_checks=finite_checks,hashes=used,seconds=time.monotonic()-t0)
(OUT/'INDEPENDENT_RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ('hashes','checks','finite_active_checks')},indent=2),flush=True)
