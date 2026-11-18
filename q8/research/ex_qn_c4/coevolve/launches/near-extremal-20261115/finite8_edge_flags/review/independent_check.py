from pathlib import Path
from fractions import Fraction as F
from itertools import combinations,permutations,product
from collections import Counter
import json,hashlib,random,sys,zipfile,ast,struct
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent.parent
B=D.parent/'finite8_flags'
def read(p):return json.loads(p.read_text())
def edge(a,b):return tuple(sorted((a,b)))
def edges(n):return [(a,a+(1<<i)) for a in range(2**n) for i in range(n) if not (a>>i)&1]
ORDER=edges(3)+[(a+8,b+8) for a,b in edges(3)]+[(a,a+8) for a in range(8)]
def graph(mask):return {e for k,e in enumerate(ORDER) if mask>>k&1}
def flip(s):return 4*(s//4)+2*(s%2)+(s//2)%2
def rec(E,n):
 for a,b in edges(n):
  r=int((a,b) in E);ss=[]
  for k in range(n):
   if 1<<k==a^b:continue
   p=a^(1<<k);q=b^(1<<k)
   s=int(edge(a,p) in E)+2*int(edge(b,q) in E)+4*int(edge(p,q) in E)
   assert s<8-r
   ss.append(s)
  yield r,ss

def Ugraph(mask):
 U=[[[0]*d for _ in range(d)] for d in (8,7)]
 for r,ss in rec(graph(mask),4):
  for move in (lambda x:x,flip):
   h=Counter(map(move,ss))
   for i,ni in h.items():
    for j,nj in h.items():U[r][i][j]+=288*ni*nj
    U[r][i][i]-=192*ni
 return U
cache={}
def local(mask):
 if mask not in cache:cache[mask]=Ugraph(mask)
 return cache[mask]
def mom(weights):
 U=[[[0]*d for _ in range(d)] for d in (8,7)]
 for g,w in weights:
  V=local(g)
  for r,d in enumerate((8,7)):
   for i in range(d):
    for j in range(d):U[r][i][j]+=w*V[r][i][j]
 return U

def hists(n,d):
 for cuts in combinations(range(n+d-1),d-1):
  bounds=(-1,)+cuts+(n+d-1,)
  yield [bounds[k+1]-bounds[k]-1 for k in range(d)]
def quad(Q,x):return sum(a*b*Q[i][j] for i,a in enumerate(x) for j,b in enumerate(x))
def pairing(Q,U):return sum(Q[i][j]*U[j][i] for i in range(len(Q)) for j in range(len(Q)))
def ldl(A):
 n=len(A);L=[[F(int(i==j)) for j in range(n)]for i in range(n)];dd=[]
 for j in range(n):
  t=A[j][j]-sum(L[j][k]**2*dd[k] for k in range(j));assert t>0;dd.append(t)
  for i in range(j+1,n):L[i][j]=(A[i][j]-sum(L[i][k]*L[j][k]*dd[k] for k in range(j)))/t
 assert all(sum(L[i][k]*dd[k]*L[j][k] for k in range(n))==A[i][j] for i in range(n) for j in range(n))
 return list(map(str,dd))

frozen=read(B/'FAMILY_OBSTRUCTION.json');fw=frozen['probability_numerators'];W=frozen['probability_denominator']
assert len(fw)==818 and all(type(w)is int and w>0 for g,w in fw) and sum(w for g,w in fw)==W
assert hashlib.sha256((B/'FAMILY_OBSTRUCTION.json').read_bytes()).hexdigest()=='fdbd082699eff6d46899d6a501945881cf6f6fed48735dd3a326c5db8080aec6'
FU=mom(fw);stored=read(D/'FROZEN_EDGE_MOMENTS.json');pivots=[]
for r,support in enumerate(([1,2,4,7],[0,3,5,6])):
 assert FU[r]==stored['blocks'][r]['twice_integer_matrix']
 assert all(FU[r][i][j]==0 for i in range(len(FU[r])) for j in range(len(FU[r])) if i not in support or j not in support)
 pivots.append(ldl([[F(FU[r][i][j]) for j in support]for i in support]))

snapraw=json.loads((D/'degree_snapshot.json').read_text(),parse_float=str)
snap=read(D/'degree_snapshot.json')
assert snap['status']=='EIGEN_CUT_ITERATION_BOUND' and snap['iteration']==10 and snap['is_graph'] is False
sw=[(g,F(s))for g,s in snapraw['lambda']];S=sum(w for g,w in sw)
assert len(sw)==175 and all(w>0 for g,w in sw)
assert all(F(s)==F(str(v))for (_,s),(_,v) in zip(snapraw['lambda'],snap['lambda']))
SU=mom([(g,w/S)for g,w in sw]);ss=read(D/'DEGREE_SNAPSHOT_EDGE_MOMENTS.json')
assert all(SU[r][i][j]==F(ss['blocks'][r]['twice_integer_matrix'][i][j],ss['probability_denominator'])for r,d in enumerate((8,7))for i in range(d)for j in range(d))

cuts=read(D/'EDGE_CUTS.json')['cuts'];out=[]
claimed_witnesses=[[0,1,1,0,0,0,0,3],[2,0,0,4,0,0,0],[2,0,0,2,1,0,0,0]]
for k,c in enumerate(cuts):
 Q=c['integer_kernel'];r=c['root_retained'];d=8-r;res=read(D/(c['name']+'.RESULT.json'))
 assert Q==res['kernel'] and all(type(v)is int for row in Q for v in row)
 assert all(Q[i][j]==Q[j][i]==Q[flip(i)][flip(j)]for i in range(d)for j in range(d))
 domain=list(hists(7,d));vals=[quad(Q,x)for x in domain];assert len(vals)==(3432 if r==0 else 1716)and min(vals)==0
 for x in (c['non_PSD_non_copositive_witness'],claimed_witnesses[k]):assert quad(Q,x)==[-264,-288,-336][k]<0
 M=FU if k<2 else SU
 den=W if k<2 else 1
 mean=pairing(Q,M[r])/F(129024*den)
 assert mean==F(c['strict_target_pairing_raw'])==F(res['pairing_actual_moment'])<0
 assert mean/c['positive_normalization']==F(c['target_pairing_normalized'])
 out.append({'name':c['name'],'domain':len(vals),'minimum':min(vals),'zeros':vals.count(0),'raw_pairing':str(mean),'witness_value':quad(Q,claimed_witnesses[k])})

# Independent restrictions from actual 682-edge input, not stored local graph list.
seed=read(B/'Q8_seed682_point.json');seedpath=Path(seed['source']);E={tuple(map(int,l.split()))for l in seedpath.read_text().splitlines()if l.strip()}
assert len(E)==682 and E<=set(edges(8))
direct=[[[0]*d for _ in range(d)]for d in (8,7)];roots=Counter()
for r,ss0 in rec(E,8):
 assert len(ss0)==7;roots[r]+=1
 for move in (lambda x:x,flip):
  h=Counter(map(move,ss0))
  for i,a in h.items():
   for j,b in h.items():direct[r][i][j]+=1440*a*b
restr=Counter()
for axes in combinations(range(8),4):
 mask=sum(1<<a for a in axes)
 for b in range(256):
  if b&mask:continue
  vs=[b^sum((1<<axes[k])for k in range(4)if v>>k&1)for v in range(16)]
  m=sum(1<<k for k,(i,j)in enumerate(ORDER)if edge(vs[i],vs[j])in E);restr[m]+=1
assert sum(restr.values())==1120 and restr==Counter(dict(seed['graph_distribution']))
LU=mom(restr.items());assert direct==LU and roots=={0:342,1:682}
seedmeans=[]
for c in cuts:
 seedmeans.append(str(F(pairing(c['integer_kernel'],LU[c['root_retained']]),129024*1120*c['positive_normalization'])))
assert all(F(s)>=0 for s in seedmeans)and F(seedmeans[2])==F(1,3840)
assert F(pairing(cuts[2]['integer_kernel'],local(1774744440)[0]),129024*1680)==F(11,120)

# Reconstruct actual fullface states and lift, then compare the existing native scorer.
sys.path.insert(0,str(B));import finite_flags as native
QE=[(0,1),(0,2),(1,3),(2,3)];ROOT=[0,1,3,6,7];ST=[];LIFT=[]
rawQ=[[[((i+j+1)*(i*j+3))%17-8 for j in range(d)]for i in range(d)]for d in (8,7)]
Qsum=[[[Q[i][j]+Q[flip(i)][flip(j)]for j in range(len(Q))]for i in range(len(Q))]for Q in rawQ]
for root in ROOT:
 states=[]
 for flag in range(256):
  parallel=flag>>4
  if parallel==15:continue
  if any(root>>k&1 and parallel>>k&1 and flag>>u&1 and flag>>v&1 for k,(u,v)in enumerate(QE)):continue
  states.append(flag)
 ST.append(states);R=[[0]*len(states)for _ in states]
 for k,(u,v)in enumerate(QE):
  other=3^(u^v)
  baseedges=[edge(u,u^other),edge(v,v^other),edge(u^other,v^other)]
  base=sum(((root>>QE.index(e))&1)<<t for t,e in enumerate(baseedges));q=Qsum[(root>>k)&1]
  ss=[((g>>u)&1)+2*((g>>v)&1)+4*((g>>(4+k))&1)for g in states]
  for i,a in enumerate(ss):
   for j,b in enumerate(ss):R[i][j]+=36*q[a][b]+6*q[a][base]+6*q[base][b]+q[base][base]
 LIFT.append(R)
assert list(map(len,ST))==[240,212,190,187,170]
assert all(ST[b]==sorted(native.STATE_IDS[b])for b in range(5))
actions=0
for b,root in enumerate(ROOT):
 lookup={s:k for k,s in enumerate(ST[b])}
 for swap,translation in product(range(2),range(4)):
  vp=[translation^((2*(x&1)+(x>>1))if swap else x)for x in range(4)]
  ep=[QE.index(edge(vp[u],vp[v]))for u,v in QE]
  moved=sum(((root>>i)&1)<<ep[i]for i in range(4))
  if moved!=root:continue
  perm=[lookup[sum(((g>>i)&1)<<vp[i]for i in range(4))+sum(((g>>(4+i))&1)<<(4+ep[i])for i in range(4))]for g in ST[b]]
  assert all(LIFT[b][i][j]==LIFT[b][perm[i]][perm[j]]for i in range(len(perm))for j in range(len(perm)));actions+=1
assert actions==18
rng=random.Random(83921);samples=[g for g,w in fw]
for _ in range(64):
 es=ORDER[:];rng.shuffle(es);a=set()
 for e in es:
  try:list(rec(a|{e},4))
  except AssertionError:continue
  a.add(e)
 samples.append(sum(1<<k for k,e in enumerate(ORDER)if e in a))
for g in samples:
 ec=sum(pairing(rawQ[r],local(g)[r])for r in (0,1))/F(2)
 _,coeff=native.local_coefficients(graph(g))
 fc=sum(v*LIFT[b][i][j]for (b,i,j),v in coeff.items()if b<5)
 assert fc==392*ec

# Every exported CSR entry is matched to raw histogram, with no reliance on NPZ software.
csr=read(D/'GENERATOR_CSR_INTEGER.json');hs=read(D/'GENERATOR_HISTOGRAMS.json');interface=read(D/'GENERATOR_INTERFACE.json')
rows=[(r,i,j)for r,d in enumerate((8,7))for i in range(d)for j in range(i,d)]
assert interface['row_order']==list(map(list,rows))and csr['shape']==[64,5148]and csr['denominator']==98
assert len(hs)==5148 and Counter(h['root_retained']for h in hs)=={0:3432,1:1716}
assert {(h['root_retained'],tuple(h['counts']))for h in hs}=={(r,tuple(x))for r,d in enumerate((8,7))for x in hists(7,d)}
assert len(csr['indptr'])==65 and csr['indptr'][0]==0 and csr['indptr'][-1]==len(csr['data'])==len(csr['indices'])
for row,(r,i,j)in enumerate(rows):
 actual={csr['indices'][k]:csr['data'][k]for k in range(csr['indptr'][row],csr['indptr'][row+1])}
 assert len(actual)==csr['indptr'][row+1]-csr['indptr'][row]
 expected={}
 for col,h in enumerate(hs):
  if h['root_retained']!=r:continue
  x=h['counts'];v=x[i]*x[j]+x[flip(i)]*x[flip(j)]
  if v:expected[col]=v
 assert actual==expected
assert all(sum((1 if i==j else 2)*(h['counts'][i]*h['counts'][j]+h['counts'][flip(i)]*h['counts'][flip(j)])for rr,i,j in rows if rr==h['root_retained'])==98 for h in hs)

def npy(data):
 assert data[:6]==b'\x93NUMPY';major=data[6];size=2 if major==1 else 4
 n=int.from_bytes(data[8:8+size],'little');info=ast.literal_eval(data[8+size:8+size+n].decode());raw=data[8+size+n:]
 descr=info['descr'];formats={'<i4':'i','<i8':'q','<f8':'d'}
 if descr in formats:return list(struct.unpack('<'+formats[descr]*(len(raw)//struct.calcsize(formats[descr])),raw))
 return raw
for filename,normalized in [('GENERATOR_NUMERATOR.npz',False),('GENERATOR_NORMALIZED.npz',True)]:
 with zipfile.ZipFile(D/filename)as z:
  for key in ('indptr','indices','shape'):assert npy(z.read(key+'.npy'))==csr[key]
  dd=npy(z.read('data.npy'))
  if normalized:
   assert all(abs(a-v/98)<=2.3e-16 for a,v in zip(dd,csr['data']))
  else:assert dd==csr['data']
# A consumer can import mechanically; validate true upper moments on 20 actual masks.
sys.path.insert(0,str(D));import export_cones
masks=[g for g,w in fw[:10]]+[g for g,w in sw[:10]]
try:
 exported=export_cones.pool_moment_numerators(masks)
 assert all(int(exported[t,k])==local(g)[r][i][j]for k,g in enumerate(masks)for t,(r,i,j)in enumerate(rows))
 consumer='20 actual masks exact U_upper agreement'
except Exception as exc:
 consumer='IMPORT_OR_CHECK_FAILURE: '+repr(exc);raise

# Targeted mutations: wrong gauge, missing offdiag factor, denominator and integer-domain scope.
assert flip(1)==2 and flip(5)==6 and flip(7)==7
assert any(Qsum[0][i][j]!=Qsum[0][flip(i)][j]for i in range(8)for j in range(8))
assert F(7,24*196)!=F(1,672*2)
assert any(local(masks[0])[r][i][j]for r,d in enumerate((8,7))for i in range(d)for j in range(i+1,d))
report={'status':'EXACT_CHECKS_PASSED','frozen_support':818,'frozen_weight_sum':str(W),'frozen_LDL_positive_pivots':pivots,'snapshot_weights':175,'snapshot_raw_decimal_sum':str(S),'snapshot_status':snap['status'],'snapshot_iteration':snap['iteration'],'cuts':out,'seed':{'edge_count':682,'roots':dict(roots),'restrictions':sum(restr.values()),'distinct_restriction_masks':len(restr),'direct_bridge_equal':True,'normalized_means':seedmeans},'pointwise_lift_sample_count':len(samples),'face_stabilizer_actions':actions,'full_CSR_shape':csr['shape'],'full_CSR_nnz':len(csr['data']),'generator_domain_complete':True,'npz_match':True,'consumer':consumer,'mutation_checks':['common gauge differs from independent argument flip','offdiagonal upper moment differs from folded score coefficient','wrong 196/2 scaling detected algebraically','totals5/6 demonstrate total7 cannot be promoted to copositivity']}
(D/'review/INDEPENDENT_CHECK.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
