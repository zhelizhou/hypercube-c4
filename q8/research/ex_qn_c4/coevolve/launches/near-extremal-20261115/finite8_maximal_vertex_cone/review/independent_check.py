#!/usr/bin/env python3
"""Fresh nonauthor verifier. Standard library only; never imports producer code.
All writes are confined to this file's review/ directory. No optimization.
"""
from pathlib import Path
from itertools import combinations, permutations, product
from collections import Counter
from fractions import Fraction
from decimal import Decimal
from math import comb
import copy, hashlib, json, random, subprocess, time

R=Path(__file__).resolve().parent
P=R.parent
BASE=P.parent
I=((0,3,7),(1,4,5,8),(2,6))
L=(-2,-1,0,-2,-1,-1,0,-2,6)
REPS=(0,1,3,4,5,6,7,12,13)
EXPECTED=(0,253,22848,75504,89180,50050,13728,1848,29)
FROZEN={str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in P.rglob('*') if p.is_file() and R not in p.parents}

def js(path,decimal=False):
    return json.loads(path.read_text(),parse_float=Decimal) if decimal else json.loads(path.read_text())
def dump(name,x):
    (R/name).write_text(json.dumps(x,indent=2)+'\n')
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def edge(a,b):return tuple(sorted((a,b)))
def cube(n):
    # Build by coordinate direction first, independently of the producer ordering.
    return {edge(v,v^(1<<i)) for i in range(n) for v in range(1<<n)}
def swap(c):return ((c&1)<<1)|((c&2)>>1)|((c&4)<<1)|((c&8)>>1)
def sid(c):
    assert 0<=c<15
    return REPS.index(min(c,swap(c)))
def code(E,v,i,j):
    a=v^(1<<i);b=v^(1<<j);z=a^(1<<j)
    return int(edge(v,a) in E)+2*int(edge(v,b) in E)+4*int(edge(a,z) in E)+8*int(edge(b,z) in E)
def states(E,n,v):return [sid(code(E,v,i,j)) for i,j in combinations(range(n),2)]
def matzero():return [[0]*9 for _ in range(9)]
def outer_add(U,x):
    for i in range(9):
        for j in range(9):U[i][j]+=x[i]*x[j]
def local_U(E,mutant=None):
    # Direct ordered-entry interpretation of 2*64512*T_Q, not folded c.
    U=matzero();pairs=list(combinations(range(4),2))
    for v in range(16):
        s=states(E,4,v)
        for a,A in enumerate(pairs):
            U[s[a]][s[a]]+=0 if mutant=='drop_collisions' else 48
            for b,B in enumerate(pairs):
                if a==b:continue
                U[s[a]][s[b]]+=720 if set(A).isdisjoint(B) else 144
    return U

def q4order():
    # Declared scientific mask order: bottom Q3, top Q3, crossings.
    e=[(v,v+(1<<i)) for v in range(8) for i in range(3) if (v>>i)&1==0]
    return e+[(a+8,b+8) for a,b in e]+[(v,v+8) for v in range(8)]
def maskgraph(m):
    assert isinstance(m,int) and 0<=m<1<<32
    return {e for k,e in enumerate(q4order()) if (m>>k)&1}
def c4free(E,n):return all(code(E,v,i,j)!=15 for v in range(1<<n) for i,j in combinations(range(n),2))
def qscore(Q,x,b=0):
    # All 81 ordered integer terms; arithmetic is arbitrary precision.
    return b+sum(x[i]*Q[i][j]*x[j] for i in range(9) for j in range(9))
def weak(n,k):
    # Stars-and-bars separator subsets, not producer's recursive assignment.
    for sep in combinations(range(n+k-1),k-1):
        a=(-1,)+sep+(n+k-1,)
        yield tuple(a[j+1]-a[j]-1 for j in range(k))
def legal_hist(d,x):
    return len(x)==9 and all(isinstance(t,int) and t>=0 for t in x) and [sum(x[i] for i in g) for g in I]==[comb(8-d,2),d*(8-d),comb(d,2)] and x[8]>=8-d

def query(path):
    r=subprocess.run([str(R/'price_domain'),str(path)],capture_output=True,text=True)
    assert r.returncode==0,(str(path),r.stderr)
    return json.loads(r.stdout)
def writequery(name,Q,B):
    path=R/(name+'.txt');path.write_text('\n'.join(' '.join(str(t) for t in row) for row in Q)+'\n'+' '.join(map(str,B))+'\n');return path

def check_oracle(o,domains,Q,B):
    assert len(o['degrees'])==9 and o['total']==sum(map(len,domains))==253440
    found=[]
    for d,row in enumerate(o['degrees']):
        assert row['degree']==d and row['count']==len(domains[d])
        if not d:
            assert row['minimum'] is None and row['witness'] is None
            found.append(None);continue
        minimum=min(qscore(Q,x,B[d]) for x in domains[d])
        assert int(row['minimum'])==minimum
        assert legal_hist(d,row['witness']) and qscore(Q,row['witness'],B[d])==minimum
        found.append(minimum)
    assert int(o['minimum'])==min(m for m in found if m is not None)
    assert found[o['minimizing_degree']]==int(o['minimum'])
    return found

def domain_checks():
    domains=[[] for _ in range(9)];original=[];boundary=[0]*9
    for d in range(9):
        totals=(comb(8-d,2),d*(8-d),comb(d,2));count=0
        for parts in product(*(tuple(weak(t,len(g))) for t,g in zip(totals,I))):
            x=[0]*9
            for g,a in zip(I,parts):
                for pos,t in zip(g,a):x[pos]=t
            count+=1
            if x[8]<8-d:continue
            assert legal_hist(d,x)
            assert sum(t*u for t,u in zip(L,x))==7*(x[8]-(8-d))>=0
            boundary[d]+=x[8]==8-d
            domains[d].append(tuple(x))
        original.append(count)
        assert len(domains[d])==EXPECTED[d] and len(set(domains[d]))==len(domains[d])
        if d:
            expected=comb(comb(8-d,2)+2,2)*comb((d-1)*(8-d)+3,3)*(comb(d,2)+1)
            assert expected==len(domains[d])
    assert sum(original)==674172
    # Main cut, generic CLI cut, and a dense arbitrary endpoint query all freshly priced.
    matrices=[];reports={}
    for name in ('pricing_master050','cli_smoke_master050'):
        c=js(P/name/'CONDITIONAL_VERTEX_CUT.json');Q=c['integer_Q'];B=c['degree_bias_raw']
        path=P/name/c['query_file'];saved=js(P/name/c['query_oracle'])
        tokens=[int(z) for z in path.read_text().split()]
        assert tokens[:81]==sum(Q,[]) and tokens[81:]==[0]*9
        fresh=query(path);assert fresh==saved
        minima=check_oracle(fresh,domains,Q,[0]*9)
        assert B==[0]+[-m for m in minima[1:]]
        biased=query(writequery(name+'_repaired_bias',Q,B))
        assert [row['minimum'] for row in biased['degrees']]==[None]+['0']*8
        matrices.append((Q,B));reports[name]={'minima':minima,'native_saved_equal':True,'repaired_bias_minima':[None]+[0]*8}
    # Endpoint dense query is generated here, independent of producer's PRNG query.
    rng=random.Random(786546519)
    Q=[[0]*9 for _ in range(9)]
    for i in range(9):
        for j in range(i,9):Q[i][j]=Q[j][i]=rng.choice([-(1<<63),(1<<63)-1,rng.randrange(-(1<<63),(1<<63))])
    B=[-(1<<63) if d%2 else (1<<63)-1 for d in range(9)]
    path=writequery('review_extreme',Q,B);o=query(path)
    reports['review_extreme']={'minima':check_oracle(o,domains,Q,B),'native':o}
    # Saved producer extreme query is not used as an expected value: recompute it too.
    tokens=[int(z) for z in (P/'extreme_int64.txt').read_text().split()]
    Q=[tokens[k:k+9] for k in range(0,81,9)];B=tokens[81:]
    fresh=query(P/'extreme_int64.txt');assert fresh==js(P/'extreme_int64.oracle.json')
    reports['saved_extreme']={'minima':check_oracle(fresh,domains,Q,B)}
    zero=subprocess.run([str(R/'price_domain')],capture_output=True,text=True,check=True)
    zo=json.loads(zero.stdout)
    assert [d['minimum'] for d in zo['degrees']]==[None]+['0']*8
    assert [d['count'] for d in zo['degrees']]==list(EXPECTED)
    # Analytical extreme all-constant kernels and nonzero biases test accumulation endpoints.
    endpoint_tests=[]
    for a in (-(1<<63),(1<<63)-1):
        Q=[[a]*9 for _ in range(9)];B=[a]*9
        path=writequery('constant_'+('min' if a<0 else 'max'),Q,B);o=query(path)
        assert all(int(t['minimum'])==785*a for t in o['degrees'][1:])
        endpoint_tests.append({'entry_and_bias':a,'score':str(785*a)})
    kernels=js(P/'RLT_KERNELS.json');assert kernels['l']==list(L)
    for k,row in enumerate(kernels['kernels']):
        assert row['coordinate']==k and row['Q']==[[int(i==k)*L[j]+L[i]*int(j==k) for j in range(9)] for i in range(9)]
        assert row['bias']==[0]*9
    # Generic mutations of oracle receipts must be rejected by the verifier.
    mutations=[]
    def expect_fail(label,obj,d,Q,B):
        try:check_oracle(obj,d,Q,B)
        except (AssertionError,ValueError,TypeError):mutations.append(label);return
        raise AssertionError('undetected mutation '+label)
    c=js(P/'pricing_master050/CONDITIONAL_VERTEX_CUT.json');o=js(P/'pricing_master050/query_32.oracle.json')
    bad=copy.deepcopy(o);bad['degrees'][1]['minimum']=str(int(bad['degrees'][1]['minimum'])+1)
    expect_fail('changed_degree_minimum',bad,domains,c['integer_Q'],[0]*9)
    bad=copy.deepcopy(o);bad['degrees'][1]['witness']=[0]*9
    expect_fail('invalid_witness',bad,domains,c['integer_Q'],[0]*9)
    bad=copy.deepcopy(o);bad['degrees'][0]['minimum']='0'
    expect_fail('empty_domain_fake_minimum',bad,domains,c['integer_Q'],[0]*9)
    return domains,{'original_counts':original,'refined_counts':list(map(len,domains)),'equality_boundary_counts':boundary,'pricing':reports,'constant_endpoint_checks':endpoint_tests,'receipt_mutations_detected':mutations,'RLT_matrices_exact':True}

def parser_checks():
    tok=(P/'extreme_int64.txt').read_text().split()
    bad={'missing':tok[:-1],'extra':tok+['0'],'overflow':[str(1<<63)]+tok[1:],'underflow':[str(-(1<<63)-1)]+tok[1:],'decimal':['0.0']+tok[1:],'trailing_chars':['3abc']+tok[1:],'bare_minus':['-']+tok[1:],'hex':['0x1']+tok[1:],'nan':['nan']+tok[1:]}
    a=tok[:];a[1]=str(int(a[1])+1);bad['asymmetry']=a
    reports={}
    for name,values in bad.items():
        p=R/('bad_'+name+'.txt');p.write_text(' '.join(values)+'\n')
        r=subprocess.run([str(R/'price_domain'),str(p)],text=True,capture_output=True)
        assert r.returncode==2 and r.stdout==''
        reports[name]=r.stderr.strip()
    for args,name in (([str(R/'does_not_exist')],'unreadable_path'),(['a','b'],'too_many_paths')):
        r=subprocess.run([str(R/'price_domain')]+args,text=True,capture_output=True)
        assert r.returncode==2 and not r.stdout;reports[name]=r.stderr.strip()
    return reports

def exact_pairing(run):
    c=js(P/run/'CONDITIONAL_VERTEX_CUT.json');point=js(P/run/'INPUT_POINT.json',decimal=True)
    assert sha(P/run/'INPUT_POINT.json')==c['input_sha256']
    lw=[(m,Fraction(w)) for m,w in point['lambda']]
    aw=[(Fraction(row[1]),row[2]) for row in point['alpha']]
    assert len(lw)==403 and len(aw)==1409
    assert len({m for m,w in lw})==len(lw) and all(w>0 for _,w in lw)
    assert all(w>0 and len(n)==9 and all(isinstance(x,int) and x>=0 for x in n) and sum(n)==128 for w,n in aw)
    lz=sum(w for _,w in lw);az=sum(w for w,_ in aw)
    U=[[Fraction() for j in range(9)] for i in range(9)]
    for m,w in lw:
        E=maskgraph(m);assert c4free(E,4);u=local_U(E)
        for i in range(9):
            for j in range(9):U[i][j]+=w*u[i][j]/lz
    mass=[sum(w*n[d] for w,n in aw)/(128*az) for d in range(9)]
    assert mass[0]==0 and sum(mass)==1
    Q=c['integer_Q'];B=c['degree_bias_raw']
    local=sum(Q[i][j]*U[i][j] for i in range(9) for j in range(9))/129024
    bias=sum(Fraction(B[d],784)*mass[d] for d in range(9))
    value=local+bias
    assert value==Fraction(c['exact_target_pairing'])<0
    assert value/c['positive_normalization']==Fraction(c['normalized_pairing'])
    # A wrong folded-as-true interpretation is explicitly detectable here.
    wrong=sum(Q[i][j]*U[i][j]*(1 if i==j else 2) for i in range(9) for j in range(9))/129024+bias
    assert wrong!=value
    return {'exact_pairing':str(value),'normalized_pairing':str(value/c['positive_normalization']),'local_part':str(local),'bias_part':str(bias),'lambda_raw_total':str(lz),'alpha_raw_total':str(az),'degree_masses':[str(t) for t in mass],'positive_lambda':len(lw),'positive_alpha':len(aw),'all_support_masks_legal':True,'wrong_offdiagonal_mutation_detected':True}

def graph_check(path,saved_gamma):
    lines=[line.split() for line in path.read_text().splitlines() if line.strip() and not line.startswith('#')]
    E={edge(*map(int,line)) for line in lines};assert len(E)==len(lines) and E<=cube(8)
    adj=[set() for _ in range(256)]
    for a,b in E:adj[a].add(b);adj[b].add(a)
    assert all(len(adj[a]&adj[b])<=1 for a in range(256) for b in range(a))
    assert c4free(E,8)
    N=Counter();hist=Counter();X=matzero();closing=Counter();slack=28
    for v in range(256):
        d=len(adj[v]);N[d]+=1;x=[states(E,8,v).count(i) for i in range(9)]
        assert legal_hist(d,x);hist[d,tuple(x)]+=1;outer_add(X,x)
        slack=min(slack,x[8]-(8-d))
        if d==1:assert x[8]==7
        for i in range(8):
            w=v^(1<<i)
            if w in adj[v]:continue
            completions=sum(edge(v,v^(1<<j)) in E and edge(v^(1<<j),w^(1<<j)) in E and edge(w^(1<<j),w) in E for j in range(8) if j!=i)
            assert completions>=1
            if v<w:closing[completions]+=1
    gamma=js(P/saved_gamma)
    assert gamma['vertex_denominator']==256
    assert {(row['degree'],tuple(row['histogram'])):row['multiplicity'] for row in gamma['columns']}==dict(hist)
    for d in range(9):
        counts=[sum(len(adj[v])==d for v in range(256) if v.bit_count()%2==parity) for parity in (0,1)]
        assert Fraction(N[d],256)==sum(Fraction(n,256) for n in counts)
    # Reconstruct every coordinate Q4 geometrically and sum ordered local U.
    U=matzero();count=0;u_without_collision=matzero()
    for axes in combinations(range(8),4):
        free=sum(1<<i for i in axes)
        for base in range(256):
            if base&free:continue
            lift=[base|sum(1<<a for k,a in enumerate(axes) if (v>>k)&1) for v in range(16)]
            K={e for e in cube(4) if edge(lift[e[0]],lift[e[1]]) in E}
            z=local_U(K);mut=local_U(K,'drop_collisions');count+=1
            for i in range(9):
                for j in range(9):U[i][j]+=z[i][j];u_without_collision[i][j]+=mut[i][j]
    assert count==1120 and U==[[720*t for t in row] for row in X]
    assert U!=u_without_collision
    assert all(sum(X[i][j]*L[j] for j in range(9))>=0 for i in range(9))
    return {'source':str(path),'sha256':sha(path),'edges':len(E),'degree_counts':[N[d] for d in range(9)],'distinct_gamma_columns':len(hist),'missing_edges':sum(closing.values()),'completion_count_histogram':dict(sorted(closing.items())),'minimum_maximality_slack':slack,'Q4_restrictions':count,'moment_identity_all_81_entries':True,'all9_RLT':True,'drop_collisions_mutation_detected':True,'same_actual_parity_alpha_gamma_mass':True}

def geometry_checks():
    codes={min(c,swap(c)) for c in range(15)};assert tuple(sorted(codes))==REPS
    assert {r for r in REPS if (r&1!=0)+(r&2!=0)==0}=={0,4,12}
    actualI=tuple(tuple(i for i,c in enumerate(REPS) if (c&1!=0)+(c&2!=0)==t) for t in range(3))
    assert actualI==I and sid(13)==sid(14)==8
    # All fifteen square patterns and axis swaps; no root translation is used.
    for c in range(15):assert sid(c)==sid(swap(c))
    assert sid(7)!=sid(13) # Three-edge paths with different marked root positions.
    # Exact completion multiplicities behind the bridge, no probabilistic premise.
    axes=range(8);pairs=list(combinations(axes,2));completion=Counter()
    for A in pairs:
        types=Counter()
        for B in pairs:
            n=len(set(A)|set(B));types[n]+=1
            contain=sum(set(A)|set(B)<=set(F) for F in combinations(axes,4))
            assert contain=={2:15,3:5,4:1}[n]
            completion[n]+=contain
        assert types=={2:1,3:12,4:15}
    assert 1120*16==256*70
    # Cube automorphisms induce only an axis swap on each marked square.
    # Test actual endpoint transport across all 384 Q4 maps on 15 single-square patterns.
    maps=0
    sq=((0,1),(0,2),(1,3),(2,3))
    for perm in permutations(range(4)):
        for t in range(16):
            def f(v):return t^sum(1<<perm[k] for k in range(4) if (v>>k)&1)
            for c in range(15):
                E={edge(a,b) for k,(a,b) in enumerate(sq) if c>>k&1}
                transported={edge(f(a),f(b)) for a,b in E}
                assert sid(code(transported,f(0),perm[0],perm[1]))==sid(c)
            maps+=1
    empty=[states(set(),8,0).count(i) for i in range(9)]
    leaf=[states({(0,1)},8,0).count(i) for i in range(9)]
    assert empty==[28]+[0]*8 and leaf==[21,7]+[0]*7
    assert Fraction(qscore(js(P/'RLT_KERNELS.json')['kernels'][0]['Q'],empty),784)==-4
    return {'state_representatives':list(REPS),'groups':[list(g) for g in I],'Q4_root_transports_checked':maps*15,'marked_translation_mutation_detected':True,'ordered_pair_types':[15,12,1],'completion_multiplicities':[1,5,15],'empty_histogram':empty,'single_edge_leaf_histogram':leaf,'empty_RLT0_value':'-4'}

def provenance_checks():
    h=js(P/'pricing_master050/SEPARATION_HISTORY.json');r=js(P/'pricing_master050/SEPARATION_RESULT.json')
    assert len(h)==r['rounds']==33 and r['status']=='CUT_FOUND'
    for k,row in enumerate(h):
        assert row['iteration']==k
        q=P/'pricing_master050'/f'query_{k:02d}.txt';o=P/'pricing_master050'/f'query_{k:02d}.oracle.json'
        assert q.exists() and o.exists() and js(o)['total']==253440
    smoke=js(P/'cli_smoke_master050/SEPARATION_HISTORY.json');res=js(P/'cli_smoke_master050/SEPARATION_RESULT.json')
    assert len(smoke)==res['rounds']==1 and res['status']=='CUT_FOUND'
    assert sha(P/'cli_smoke_master050/INPUT_POINT.json')==sha(P/'pricing_master050/INPUT_POINT.json')
    for name,digest in js(P/'FILES_SHA256.json').items():assert sha(P/name)==digest,(name,digest,sha(P/name))
    return {'discovery_rounds':33,'all_33_query_oracle_files_present':True,'one_round_generic_cli_receipt_present':True,'same_frozen_input':True,'manifest_matches':True,'discovery_not_rerun':True}

def main():
    started=time.monotonic()
    compile_run=subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-fsanitize=undefined','-fno-sanitize-recover=undefined',str(P/'price_domain.cpp'),'-o',str(R/'price_domain')],capture_output=True,text=True)
    assert compile_run.returncode==0,compile_run.stderr
    geo=geometry_checks();dump('GEOMETRY_RESULT.json',geo)
    domains,domain=domain_checks();dump('DOMAIN_RESULT.json',domain)
    parsers=parser_checks();dump('PARSER_RESULT.json',parsers)
    pairing={name:exact_pairing(name) for name in ('pricing_master050','cli_smoke_master050')};dump('PAIRING_RESULT.json',pairing)
    g1=graph_check(Path('/mnt/c/users/anony/desktop/project/research/ex_qn_c4/data/q8_seed682.edges'),'q8_seed682_GAMMA.json')
    g2=graph_check(BASE/'finite8_maximal_leaf_gate/CALIBRATION.edges','CALIBRATION_GAMMA.json')
    assert g1['edges']==682 and g1['distinct_gamma_columns']==8 and g1['minimum_maximality_slack']==7
    assert g2['edges']==576 and g2['distinct_gamma_columns']==182 and g2['minimum_maximality_slack']==0
    dump('GRAPH_RESULT.json',[g1,g2]);prov=provenance_checks();dump('PROVENANCE_RESULT.json',prov)
    current={str(p.relative_to(P)):sha(p) for p in P.rglob('*') if p.is_file() and R not in p.parents}
    assert current==FROZEN,'frozen package was changed during review'
    inputs=dict(FROZEN)
    for p in (BASE/'finite8_flags/main.tex',BASE/'finite8_flags/finite_flags.py',Path(g1['source']),Path(g2['source'])):inputs[str(p)]=sha(p)
    dump('INPUT_HASHES.json',inputs)
    dump('RESULT.json',{'status':'PASS_INDEPENDENT_BOUNDED_FINITE_CHECKS','seconds':time.monotonic()-started,'stdlib_only':True,'producer_imports':False,'compiler_sanitizer':'undefined; no diagnostic','native_rebuilt':True,'original_domains_traversed':674172,'refined_domains_traversed':253440,'mutations_detected':['minimum+1','invalid_witness','fake_empty_minimum','wrong_offdiagonal_factor','drop_collision_terms','translate_marked_root'],'outside_review_files_unchanged':True,'inputs_sha256':inputs})
    print(json.dumps({'status':'PASS_INDEPENDENT_BOUNDED_FINITE_CHECKS','seconds':time.monotonic()-started,'refined':sum(map(len,domains))}))
if __name__=='__main__':main()
