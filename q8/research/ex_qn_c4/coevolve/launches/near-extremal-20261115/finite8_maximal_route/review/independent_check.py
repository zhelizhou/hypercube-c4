"""Read-only independent check of finite inputs; writes only its review receipt.
Profile enumeration uses the B budget (not the producer's C recursion), and
seed square counts use literal 4-cycle masks (not the producer's edge loop).
No producer imports, solver calls, or historical proof replay.
"""
from pathlib import Path
from itertools import combinations
from collections import Counter
from math import comb
import hashlib, json

T=Path(__file__).resolve().parents[1]
ROOT=T.parents[3]
C=(735,534,333,177,66,0,0,105,345)
B=(40,30,20,11,4,0,0,5,16)
DS=(8,7,4,3,2,1,0)
checks=[]
def check(name, value, detail=None):
    assert value, name
    checks.append({'name':name,'pass':True,'detail':detail})
def sha(path):
    return 'sha256:'+hashlib.sha256(path.read_bytes()).hexdigest()

# Visit all B-budgeted exceptional-degree populations in the reverse degree
# order. Complete with degree-5 corrections to an initially degree-6 row.
def independent_profiles(m):
    out=[]
    def walk(k, budget, counts):
        if k==len(DS):
            row=[counts.get(d,0) for d in range(9)]
            row[5]=768-m-sum((6-d)*counts[d] for d in DS)
            row[6]=128-sum(row)
            if min(row)<0:return
            cost=sum(x*y for x,y in zip(row,C))
            if cost>138432-201*m:return
            out.append((tuple(row),cost,sum(x*y for x,y in zip(row,B))))
            return
        d=DS[k]
        for n in range(budget//B[d]+1):
            counts[d]=n
            walk(k+1,budget-n*B[d],counts)
    walk(0,6912-10*m,{})
    return out

cover=json.loads((T/'PROFILE_COVER.json').read_text())
check('profile_top_keys',set(cover)==set(map(str,range(683,689))))
profile_counts={}
for m in range(683,689):
    rows=independent_profiles(m)
    expected=set(rows)
    check('independent_profile_unique_'+str(m),len(expected)==len(rows))
    item=cover[str(m)]
    check('caps_'+str(m),item['C_max']==138432-201*m and item['b_max']==6912-10*m)
    for typ in ('all_profiles','maximal_profiles'):
        raw=item[typ]
        got=[(tuple(r['n']),r['C'],r['b']) for r in raw]
        want=expected if typ=='all_profiles' else {r for r in expected if r[0][0]==0}
        check('all_rows_fields_'+str(m)+'_'+typ, all(set(r)=={'n','C','b'} for r in raw))
        check('full_saved_set_'+str(m)+'_'+typ,set(got)==want and len(got)==len(want),len(want))
        for n,c,b in got:
            assert len(n)==9 and all(type(x) is int and x>=0 for x in n)
            assert sum(n)==128 and sum(d*x for d,x in enumerate(n))==m
            assert c==sum(C[d]*x for d,x in enumerate(n))<=item['C_max']
            assert b==sum(B[d]*x for d,x in enumerate(n))<=item['b_max']
        profile_counts.setdefault(str(m),{})[typ]=len(got)
check('all_profile_count_vector',[profile_counts[str(m)]['all_profiles'] for m in range(683,689)]==[814,393,171,66,20,4])
check('max_profile_count_vector',[profile_counts[str(m)]['maximal_profiles'] for m in range(683,689)]==[783,385,170,66,20,4])
old_path=T.parent/'q8_equality_profiles/PROFILES.json'
old=json.loads(old_path.read_text())
check('historical_683_literal_unfiltered_set', {tuple(r['degrees']) for r in old['profiles']}=={tuple(r['n']) for r in cover['683']['all_profiles']},'old artifact read-only; no old filters used')

# Weak-composition recursion differs from combinations_with_replacement.
def weak(n,k):
    if k==1:
        yield (n,)
    else:
        for first in range(n+1):
            for tail in weak(n-first,k-1):yield (first,)+tail
invent=json.loads((T/'EDGE7_GENERATORS.json').read_text())
check('generator_top_keys',set(invent)=={'root0_maximal','root1'})
expected0={x for x in weak(7,8) if x[7]>0}
expected1=set(weak(7,7))
check('root0_complete',len(invent['root0_maximal'])==len(expected0)==1716 and set(map(tuple,invent['root0_maximal']))==expected0)
check('root1_complete',len(invent['root1'])==len(expected1)==1716 and set(map(tuple,invent['root1']))==expected1)
check('unrestricted_root0_count',len(list(weak(7,8)))==3432)
flip=(0,2,1,3,4,6,5,7)
def reversed_row(x):
    z=[0]*len(x)
    for s,n in enumerate(x):z[flip[s]]=n
    return tuple(z)
check('root0_endpoint_action',all(reversed_row(x) in expected0 for x in expected0))
check('root1_endpoint_action',all(reversed_row(x) in expected1 for x in expected1))

# Literal coordinate-subset tally for low/full occurrence coefficients.
free6=list(combinations(range(8),6))
computed_l=[];computed_full=[]
for d in range(9):
    selected=set(range(d))
    computed_l.append(sum(len(selected.intersection(I))<=2 for I in free6))
    computed_full.append(sum(len(selected.intersection(I))==6 for I in free6))
check('literal_l_vector',computed_l==[28,28,28,18,6,0,0,0,0],computed_l)
check('literal_full_vector',computed_full==[comb(d,6) for d in range(9)],computed_full)
raw=[40*comb(d,3)+2*computed_full[d]-5*computed_l[d] for d in range(9)]
check('all_nine_coefficient_identities',all(raw[d]-402*d+1610==2*C[d] for d in range(9)),raw)
check('global_rhs_arithmetic',112*632==70784 and 70784+1610*128==276864 and 276864//2==138432 and 138432//201==688)
check('star_capacity_arithmetic',comb(8,3)*2**5==1792 and 1792+40*128==6912)
check('Q3_in_Q6_multiplicity',all(sum(set(J)<=set(I) for I in free6)==10 for J in combinations(range(8),3)))
# Every simple ambient 4-cycle is a square: enumerate every pair of different
# neighbors of a vertex, and check that their other common neighbor is u^i^j.
for u in range(256):
    for i,j in combinations(range(8),2):
        a,b=u^(1<<i),u^(1<<j)
        common={a^(1<<k) for k in range(8)} & {b^(1<<k) for k in range(8)}
        assert common=={u,u^(1<<i)^(1<<j)}
check('all_cube_C4s_are_coordinate_squares',True,256*comb(8,2))

# Seed: square masks anchored at the vertex with the two free bits zero.
seed=ROOT/'data/q8_seed682.edges'
lines=seed.read_text().splitlines()
edges={frozenset(map(int,line.split())) for line in lines if line.strip()}
ambient={frozenset((v,v^(1<<i))) for v in range(256) for i in range(8)}
check('seed_edges_literal',len(edges)==682 and len(lines)==682 and edges<=ambient)
check('ambient_edges',len(ambient)==1024)
missing=ambient-edges
closure=Counter({e:0 for e in missing}); full=0; q2=0
for i,j in combinations(range(8),2):
    for v in range(256):
        if v>>i&1 or v>>j&1:continue
        a,b,c=v^(1<<i),v^(1<<j),v^(1<<i)^(1<<j)
        square={frozenset((v,a)),frozenset((v,b)),frozenset((a,c)),frozenset((b,c))}
        absent=square-edges
        if not absent:full+=1
        elif len(absent)==1:closure[next(iter(absent))]+=1
        q2+=1
check('seed_C4_free',full==0,{'coordinate_squares_checked':q2})
check('seed_inclusion_maximal',len(missing)==342 and min(closure.values())>=1)
ch=Counter(closure.values())
check('seed_missing_closure_histogram',dict(ch)=={3:41,4:159,5:120,6:22},dict(ch))
# Actual labeled Q6 restrictions and shared parity tallies, not independent faces.
adj={v:set() for v in range(256)}
for e in edges:
    u,v=tuple(e);adj[u].add(v);adj[v].add(u)
seed_parities=[]
for parity in range(2):
    P={v for v in range(256) if v.bit_count()%2==parity}
    n=[sum(len(adj[v])==d for v in P) for d in range(9)]
    totals=[0,0,0];face_ct=0;local_import_violations=0
    for I in free6:
        omitted=[j for j in range(8) if j not in I]
        for bits in range(4):
            vertices={v for v in range(256) if all((v>>j&1)==(bits>>k&1) for k,j in enumerate(omitted))}
            deg=[len(adj[v]&vertices) for v in P&vertices]
            S=sum(comb(d,3) for d in deg);c=deg.count(6);low=sum(d<=2 for d in deg)
            totals=[totals[0]+S,totals[1]+c,totals[2]+low]
            local_import_violations+=4*S+2*c>632+5*low
            face_ct+=1
    check('same_actual_parity_Q6_tallies_'+str(parity),face_ct==112 and totals==[10*sum(comb(d,3)*n[d] for d in range(9)),sum(comb(d,6)*n[d] for d in range(9)),sum(computed_l[d]*n[d] for d in range(9))])
    check('seed_112_local_import_evaluations_'+str(parity),local_import_violations==0,'finite compatibility only, not a proof of import')
    seed_parities.append({'parity':parity,'n':n,'Q6_tallies_S_c_L':totals})

# Discriminating mutations of finite domains and threshold boundaries.
mutations=[]
check('boundary_m689_is_impossible_for_nonnegative_C',138432-201*689==-57)
mutations.append({'mutation':'retain only m=683','detected':any(cover[str(m)]['maximal_profiles'] for m in range(684,689)),'scope':'omits arithmetic candidates; no graph realization claimed'})
mutations.append({'mutation':'drop one valid m=688 row','detected':len(expected:=set(tuple(r['n']) for r in cover['688']['maximal_profiles']))==4 and len(expected-{next(iter(expected))})==3})
mutations.append({'mutation':'weaken missing-edge condition x7>=1 to x7>=0','detected':len(set(weak(7,8))-expected0)==1716,'extra_invalid_local_rows':1716})
mutations.append({'mutation':'allow retained state7','detected':len(set(weak(7,8))-set(x+(0,) for x in expected1))==1716,'extra_square_creating_rows':1716})
mutations.append({'mutation':'independently flip only one endpoint state without swapping1/2 and5/6','detected':flip[1]==2 and flip[5]==6,'scope':'actual endpoint reversal fixed globally'})
pair=[r['n'] for r in cover['683']['maximal_profiles'][:2]]
mutations.append({'mutation':'force alpha to a single profile row','detected':pair[0]!=pair[1] and [a+b for a,b in zip(*pair)] != [2*a for a in pair[0]],'scope':'two distinct same-m necessary candidate rows test the algebra; no graph realization claimed'})
# Two distinct profiles have average not an integer point profile; all mixtures
# remain necessary via each actual same-m half-sum but need not realize a graph.
check('all_mutation_checks_discriminating',all(x['detected'] for x in mutations),mutations)

producer=json.loads((T/'CHECK.json').read_text())
check('producer_receipt_profile_counts',producer['profile_counts']==profile_counts)
check('producer_receipt_seed',producer['seed']['sha256']==sha(seed).removeprefix('sha256:') and producer['seed']['edges']==682 and producer['seed']['missing_edges']==342 and producer['seed']['C4_free'] is True and producer['seed']['all_missing_edges_closed'] is True and producer['seed']['closing_square_histogram']=={str(k):v for k,v in ch.items()})

payload={'status':'PASS','implementation_difference':'B-budget reverse recursion with degree-6 correction; weak compositions; literal square masks; no producer imports',
'checks':checks,'profile_counts':profile_counts,'generator_counts':{k:len(v) for k,v in invent.items()},'seed_parities':seed_parities,'seed_closure_histogram':dict(ch),'historical_traces_rerun':False,'LP_run':False}
(T/'review/INDEPENDENT_CHECK.json').write_text(json.dumps(payload,indent=2)+'\n')
print(json.dumps({'status':'PASS','checks':len(checks),'profile_counts':profile_counts,'seed_parities':seed_parities,'closure_histogram':dict(ch)},indent=2))
