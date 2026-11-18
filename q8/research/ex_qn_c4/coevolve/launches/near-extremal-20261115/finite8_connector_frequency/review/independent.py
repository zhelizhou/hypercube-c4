"""Fresh review reconstruction; no producer/checker imports before final interface comparison."""
from pathlib import Path
from itertools import combinations, combinations_with_replacement, permutations
from fractions import Fraction as F
from decimal import Decimal
from collections import Counter
import json, hashlib, math, sys, random
P=Path(__file__).resolve().parents[1]; R=P/'review'
def read(n): return json.loads((P/n).read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
inputs=['PROOF.md','PROOF_SKELETON.md','INPUT_POINT.json','CONNECTOR_CUTS.json','PROJECTED_MOMENTS.json','PSD_ELIGIBILITY.json','block0.EXACT_SEPARATOR.json','block4.EXACT_SEPARATOR.json','score.py','verify.py','project.py','certify_separator.py','membership.py','REVIEWER_ROUTE.json']
freeze={n:sha(P/n) for n in inputs}
units=[]
for n in ['PROOF.md','PROOF_SKELETON.md']:
 lines=(P/n).read_text().splitlines(); starts=[i for i,l in enumerate(lines,1) if l.startswith('#')]
 for k,a in enumerate(starts): units.append({'id':n+':'+str(a),'path':n,'first_line':a,'last_line':starts[k+1]-1 if k+1<len(starts) else len(lines),'heading':lines[a-1]})
(R/'INPUT_FREEZE.json').write_text(json.dumps({'hashes':freeze,'source_units':units},indent=2)+'\n')
roots=(0,1,3,6,7); sq=((0,1),(0,2),(1,3),(2,3))
def edge(a,b): return tuple(sorted((a,b)))
def cube(n): return [(v,v^(1<<a)) for v in range(1<<n) for a in range(n) if not (v>>a)&1]
q4=cube(3)+[(a+8,b+8) for a,b in cube(3)]+[(a,a+8) for a in range(8)]
assert len(set(q4))==32
# Construct all actual Q2 isometries and edge images directly.
acts=[]
for swap in [False,True]:
 for tr in range(4):
  p=[(((x>>1)|((x&1)<<1)) if swap else x)^tr for x in range(4)]
  ep=[sq.index(edge(p[a],p[b])) for a,b in sq]
  def move(k,p=p,ep=ep): return sum(((k>>i)&1)<<p[i] for i in range(4))+sum(((k>>(i+4))&1)<<(ep[i]+4) for i in range(4))
  rp=[sum(((z>>i)&1)<<ep[i] for i in range(4)) for z in range(16)]
  acts.append((rp,[move(k) for k in range(256)]))
valid=[]
for root in roots:
 states=[]
 for code in range(256):
  if code>>4==15: continue
  conn,para=code&15,code>>4
  if any((root>>k)&1 and (para>>k)&1 and (conn>>a)&1 and (conn>>b)&1 for k,(a,b) in enumerate(sq)):continue
  states.append(code)
 valid.append(states)
assert list(map(len,valid))==[240,212,190,187,170]
assert all(set(c&15 for c in v)==set(range(16)) for v in valid)
ids=[{v:i for i,v in enumerate(vs)} for vs in valid]
stab=[[s for r,s in acts if r[root]==root] for root in roots]
def faces(E,n):
 for a,b in combinations(range(n),2):
  support=(1<<a)|(1<<b)
  for v in range(1<<n):
   if v&support:continue
   vs=[v,v^(1<<a),v^(1<<b),v^support]
   root=sum(1<<i for i,(j,k) in enumerate(sq) if edge(vs[j],vs[k]) in E)
   if root==15:raise AssertionError('C4')
   flags=[]
   for ax in range(n):
    if ax in (a,b):continue
    bit=1<<ax
    flags.append(sum(1<<i for i,x in enumerate(vs) if edge(x,x^bit) in E)+sum(1<<(i+4) for i,(j,k) in enumerate(sq) if edge(vs[j]^bit,vs[k]^bit) in E))
   yield root,flags
point=json.loads((P/'INPUT_POINT.json').read_text(),parse_float=Decimal)
lam=[(mask,F(w)) for mask,w in point['lambda']]; D=10**22
assert len(lam)==202 and len({m for m,w in lam})==202 and all(w>0 for m,w in lam)
assert all((w*D).denominator==1 for m,w in lam)
assert sum(w for m,w in lam)==F(9999999999999698585929,D)
assert (P/'INPUT_POINT.json').read_bytes()==(P.parent/'finite8_vertex_degree_cone/INPUT_EDGE_STAGE_POINT.json').read_bytes()
full=Counter(); U=[[[0]*16 for i in range(16)] for b in roots]; graphUs={}; rootcounts=Counter()
for mask,w in lam:
 assert 0<=mask<2**32
 E={e for i,e in enumerate(q4) if (mask>>i)&1}; GU=[Counter() for b in roots]; count=0
 for root,flags in faces(E,4):
  count+=1; canonical=min(r[root] for r,s in acts); b=roots.index(canonical)
  coset=[s for r,s in acts if r[root]==canonical]; g=len(coset); rootcounts[b]+=1
  assert len(flags)==2 and g==len(stab[b])
  for s in coset:
   a,c=(s[k] for k in flags); i,j=ids[b][a],ids[b][c]
   for u,v,vv in [(i,j,2240//g),(j,i,2240//g),(i,i,448//g),(j,j,448//g)]:
    full[b,u,v]+=int(w*D)*vv
   for u,v,vv in [(a&15,c&15,2240//g),(c&15,a&15,2240//g),(a&15,a&15,448//g),(c&15,c&15,448//g)]:
    U[b][u][v]+=int(w*D)*vv; GU[b][u,v]+=vv
 assert count==24; graphUs[mask]=GU
U2=[[[0]*16 for i in range(16)] for b in roots]
for (b,i,j),v in full.items():U2[b][valid[b][i]&15][valid[b][j]&15]+=v
assert U2==U
pm=read('PROJECTED_MOMENTS.json'); den=2*64512*D
assert pm['moment_denominator']==den and pm['lambda_decimal_denominator']==D
assert pm['lambda_integer_numerators']==[[m,int(w*D)] for m,w in lam]
for b in range(5):assert U[b]==pm['blocks'][b]['twice_integer_matrix']
# Fresh exact LDL; compare recorded factors after independent calculation.
ps=read('PSD_ELIGIBILITY.json'); psd=[]
for b in range(5):
 A=[[F(v) for v in row] for row in U[b]]; L=[[F(int(i==j)) for j in range(16)] for i in range(16)]; piv=[]
 for j in range(16):
  d=A[j][j]-sum(L[j][k]**2*piv[k] for k in range(j));piv.append(d)
  if d==0:break
  for i in range(j+1,16):L[i][j]=(A[i][j]-sum(L[i][k]*L[j][k]*piv[k] for k in range(j)))/d
 ent=ps['blocks'][b]
 if b in (0,4):
  assert len(piv)==16 and all(d>0 for d in piv)
  assert [[F(z) for z in row] for row in ent['L']]==L
  assert [F(z) for z in ent['D']]==piv
  psd.append({'block':b,'status':'PD','positive_pivots':16,'min_pivot':str(min(piv))})
 else:
  print('NEGKEYS',b,list(ent))
  vec=ent.get('integer_direction')
  if vec is None: raise KeyError(ent.keys())
  q=sum(F(vec[i])*U[b][i][j]*F(vec[j]) for i in range(16) for j in range(16));assert q<0
  psd.append({'block':b,'status':'negative','quadratic_U':str(q)})
cuts=read('CONNECTOR_CUTS.json')['cuts']; results=[]; qby={}; muts=[]
def quad(Q,h):return sum(v*w*Q[i][j] for i,v in enumerate(h) if v for j,w in enumerate(h) if w)
def hist(total):
 for labels in combinations_with_replacement(range(16),total):
  h=[0]*16
  for i in labels:h[i]+=1
  yield h
for cut in cuts:
 b=cut['block']; Q=cut['integer_connector_Q'];qby[b]=Q;cert=read(f'block{b}.EXACT_SEPARATOR.json')
 assert len(Q)==16 and all(len(row)==16 and all(type(v)==int for v in row) for row in Q)
 assert all(Q[i][j]==Q[j][i] for i in range(16) for j in range(16));assert cert['connector_Q']==Q
 mapping=[c&15 for c in valid[b]];assert mapping==cut['full_state_connector_codes']==cert['full_state_connector_codes']
 lifted=[[Q[a][c] for c in mapping] for a in mapping];assert lifted==cert['full_Q']
 actionset={tuple(s[c]&15 for c in range(16)) for s in stab[b]};assert actionset==set(map(tuple,cut['root_connector_actions']))
 for s in stab[b]:
  assert all(s[c] in ids[b] for c in valid[b])
  assert all(Q[s[i]&15][s[j]&15]==Q[i][j] for i in range(16) for j in range(16))
  assert all(U[b][s[i]&15][s[j]&15]==U[b][i][j] for i in range(16) for j in range(16))
 values=[quad(Q,h) for h in hist(6)];assert len(values)==math.comb(21,6)==54264 and min(values)==0
 assert cert['finite6']['zeros']==values.count(0);assert quad(Q,cert['finite6']['minimizing_histogram'])==0
 witness=cut['non_PSD_non_copositive_witness'];assert sum(witness)==4 and quad(Q,witness)==cut['witness_quadratic']<0
 pairing=F(sum(Q[i][j]*U[b][i][j] for i in range(16) for j in range(16)),den)
 assert str(pairing)==cert['point_pairing']['exact_mean_feature'] and pairing<0
 scale=max(abs(v) for row in Q for v in row);assert scale==cut['positive_normalization']==cert['positive_normalization']
 assert pairing/scale==F(cut['normalized_exact_target_feature'])
 # Same offdiagonal folding in score, compared only after independent construction.
 sys.path.insert(0,str(P));import score
 for mask,w in lam:
  gv=F(sum(v*Q[i][j] for (i,j),v in graphUs[mask][b].items()),2*64512)
  assert score.value_on_graph(mask,b,False)==gv
  assert score.value_on_graph(mask,b)==gv/scale
 mats,sc=score.full_face_kernel(b);assert sc==scale and mats[b]==lifted
 assert all(not any(v for row in mat for v in row) for c,mat in enumerate(mats) if c!=b)
 # Targeted deterministic mutation: subtract1 on a zero-histogram diagonal -> detected.
 h=next(h for h in hist(6) if quad(Q,h)==0);ix=next(i for i,v in enumerate(h) if v);mut=[row[:] for row in Q];mut[ix][ix]-=1;assert quad(mut,h)<0
 muts.append({'block':b,'diagonal_minus_one_zero_domain_detected':True,'complete_full_lift_hash':hashlib.sha256(json.dumps(lifted,separators=(',',':')).encode()).hexdigest()})
 results.append({'block':b,'histograms':len(values),'minimum':min(values),'zeros':values.count(0),'pairing_raw':str(pairing),'pairing_normalized':str(pairing/scale),'scale':scale,'full_states':len(valid[b]),'root_actions':len(actionset),'small_total':sum(witness),'small_value':quad(Q,witness)})
# Whole-Q8 common-object bridge, directQ4 restrictions vs all1792 actual roots.
# Use axiswise parity bipartite edges subset for legal nontrivial examples; random forests.
rng=random.Random(181116)
q8=cube(8)
examples=[('empty',set()),('axis0',{e for e in q8 if e[0]^e[1]==1}),('star0',{(0,1<<a) for a in range(8)})]
forest=set()
for v in range(1,256):
 bits=[a for a in range(8) if v&(1<<a)];a=rng.choice(bits);forest.add(edge(v,v^(1<<a)))
examples.append(('random_spanning_tree',forest));bridges=[]
def actual_value(E,b):
 out=F();nf=0
 for root,flags in faces(E,8):
  nf+=1;canonical=min(r[root] for r,s in acts)
  if canonical!=roots[b]:continue
  s=next(s for r,s in acts if r[root]==canonical);h=[0]*16
  for code in flags:h[s[code]&15]+=1
  assert sum(h)==6;out+=F(quad(qby[b],h),36)
 assert nf==1792;return out/1792
# Compute local feature from direct root extraction, no precomputed source coefficient routines.
def local(E,b):
 out=F();Q=qby[b]
 for root,flags in faces(E,4):
  canonical=min(r[root] for r,s in acts)
  if canonical!=roots[b]:continue
  cos=[s for r,s in acts if r[root]==canonical]
  for s in cos:
   i,j=[s[k]&15 for k in flags];out+=(F(5,6)*Q[i][j]+F(Q[i][i]+Q[j][j],12))/(24*len(cos))
 return out
for name,E in examples:
 restrictions=[]
 for axes in combinations(range(8),4):
  support=sum(1<<a for a in axes)
  for base in range(256):
   if base&support:continue
   vs=[base^sum(1<<axes[j] for j in range(4) if (x>>j)&1) for x in range(16)]
   K={e for e in q4 if edge(vs[e[0]],vs[e[1]]) in E};restrictions.append(K)
 assert len(restrictions)==1120
 for b in (0,4):
  left=sum((local(K,b) for K in restrictions),F())/1120;right=actual_value(E,b)
  assert left==right and right>=0;bridges.append({'graph':name,'block':b,'value':str(left),'subcubes':1120,'roots':1792})
# Collision bridge algebra for arbitrary symmetric six-label matrix, including indefiniteQ.
X=[[F((i*17+j*13)%19-9) for j in range(6)] for i in range(6)];X=[[X[i][j]+X[j][i] for j in range(6)] for i in range(6)]
lhs=sum((F(5,6)*X[i][j]+F(X[i][i]+X[j][j],12) for i,j in combinations(range(6),2)),F())/15
assert lhs==sum(map(sum,X),F())/36
# Hypergeometric extension: average six-subsets for any external-size >=6 has same pair/diag mixture.
for t in (6,7,8,11):
 assert F(math.comb(t-2,4),math.comb(t,6))*F(1,36)*t*(t-1)==F(5,6)
 assert F(math.comb(t-1,5),math.comb(t,6))*F(1,36)*t==F(1,6)
assert freeze=={n:sha(P/n) for n in inputs}
report={'status':'PASS','same_original_decimal_mass':str(sum(w for m,w in lam)),'graphs':len(lam),'full_state_dimensions':list(map(len,valid)),'psd':psd,'kernels':results,'mutations':muts,'whole_Q8_bridge_checks':bridges,'arbitrary_symmetric_collision_identity':True,'external_sizes_tested':[6,7,8,11],'hashes':freeze,'units':units,'author_checker_used_as_premise':False}
(R/'INDEPENDENT_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ('hashes','units')},indent=2))
