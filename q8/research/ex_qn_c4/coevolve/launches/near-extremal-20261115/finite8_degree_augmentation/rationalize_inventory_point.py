"""Exact affine/inequality/PSD certificate for a numerically discovered point.
Rounding + exact affine repair; PSD via rational LL^T plus strictly diagonally
 dominant residual. A failure is a rejection of this rationalization, not
an infeasibility theorem. Uses no global optimizer or proof-acceptance status.
"""
from pathlib import Path
from fractions import Fraction as Q
from math import lcm
import sys,json,argparse,time
P=Path(__file__).resolve().parent;R=P/'pool_inventory';SRC=P.parent/'finite8_flags';sys.path.insert(0,str(SRC/'deps'))
import numpy as np
from scipy import sparse
ap=argparse.ArgumentParser();ap.add_argument('input',type=Path);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--denominator',type=int,default=10**12);a=ap.parse_args();O=a.output.resolve();assert not O.exists();O.mkdir(parents=True)
d=json.loads(a.input.read_text());graphs=json.loads((R/'POOL_GRAPH_CODES.json').read_text());profiles=json.loads((R/'PROFILE_SNAPSHOT.json').read_text())['remaining'];G=len(graphs);A=len(profiles);features=np.load(R/'MARGINAL_FEATURES.npz');H=features['hist'];B=features['profile_hypergeom'];E=features['even'];K=features['kernel_raw'];scales=features['kernel_scales'];F=sparse.load_npz(R/'INTEGER_FEATURES.npz');start=json.loads((R/'LP_STARTED.json').read_text());idx={g:i for i,g in enumerate(graphs)}
weights={}
for g,v in d['lambda']:
 if v>0:weights[idx[g]]=float(v)
for row in d['alpha']:
 i,v=row[:2]
 if v>0:weights[G+i]=float(v)
D=a.denominator;nums={i:int(round(v*D)) for i,v in weights.items() if round(v*D)>0}
def col(i):return [1,0]+[560*int(x) for x in H[i]] if i<G else [0,1]+[-int(x) for x in B[i-G]]
# Greedily choose independent large-weight repair variables over exact Q.
basis={};chosen=[]
for i in sorted(nums,key=lambda i:nums[i],reverse=True):
 v=list(map(Q,col(i)))
 for r in sorted(basis):
  if v[r]:
   f=v[r];v=[x-f*y for x,y in zip(v,basis[r])]
 if any(v):
  r=next(j for j,x in enumerate(v) if x);f=v[r];basis[r]=[x/f for x in v];chosen.append(i)
assert len(chosen)>=6
res=[D,D,0,0,0,0,0]
for i,n in nums.items():res=[x-n*y for x,y in zip(res,col(i))]
M=[[Q(col(i)[r]) for i in chosen]+[Q(res[r])] for r in range(7)];piv=[];rr=0
for j in range(len(chosen)):
 k=next((k for k in range(rr,7) if M[k][j]),None)
 if k is None:continue
 M[rr],M[k]=M[k],M[rr];f=M[rr][j];M[rr]=[x/f for x in M[rr]]
 for k in range(7):
  if k!=rr and M[k][j]:
   f=M[k][j];M[k]=[x-f*y for x,y in zip(M[k],M[rr])]
 piv.append((rr,j));rr+=1
assert all(any(row[:-1]) or not row[-1] for row in M)
cor=[Q(0)]*len(chosen)
for r,j in piv:cor[j]=M[r][-1]
L=lcm(*(x.denominator for x in cor));den=D*L;exact={i:n*L for i,n in nums.items()}
for i,x in zip(chosen,cor):exact[i]+=int(x*L)
assert min(exact.values())>=0
balance=[0]*7
for i,n in exact.items():balance=[x+n*y for x,y in zip(balance,col(i))]
assert balance==[den,den,0,0,0,0,0]
lam=[exact.get(i,0) for i in range(G)];alpha=[exact.get(G+i,0) for i in range(A)];even=sum(int(e)*n for e,n in zip(E,lam));kernel=[sum(int(K[i,b])*lam[i] for i in range(G)) for b in range(2)];assert 224*even>=57*den and min(kernel)>=0
packed=[0]*F.shape[1]
for i,n in enumerate(lam):
 if not n:continue
 for pos in range(F.indptr[i],F.indptr[i+1]):packed[int(F.indices[pos])]+=n*int(F.data[pos])
point={'scope':'Exact candidate in frozen13962 degree/PSD/even/two-finite6 relaxation; not graph','denominator':str(den),'lambda':[[g,str(n)] for g,n in zip(graphs,lam) if n],'alpha':[[i,str(n),profiles[i]['degrees']] for i,n in enumerate(alpha) if n],'affine_balance':list(map(str,balance)),'repair_variables':chosen,'source_float':str(a.input.resolve()),'even_expectation':str(Q(even,den)),'finite6_expectations':[str(Q(k,den*64512*int(sc))) for k,sc in zip(kernel,scales)],'exact_PSD_acceptance_done':False}
(O/'RATIONAL_POINT.json').write_text(json.dumps(point,indent=2)+'\n')
cert=[];Larrays={};base=2*64512*den;T=10**12;split=10**6;st=__import__('time').monotonic()
for b,(dim,ss) in enumerate(zip(start['dimensions'],start['supports'])):
 ids=[[start['packed_starts'][b]+min(i,j)*dim-min(i,j)*(min(i,j)-1)//2+max(i,j)-min(i,j) for j in ss] for i in ss]
 numer=[[packed[ids[i][j]]*(2 if i==j else 1) for j in range(len(ss))] for i in range(len(ss))];Mf=np.array([[float(Q(x,base)) for x in row] for row in numer]);mineig=float(np.linalg.eigvalsh(Mf)[0]);assert mineig>1e-11,(b,mineig,'affine repaired point not strictly PSD; no acceptance')
 delta=Q(1,2**int(np.ceil(np.log2(4/mineig))));lf=np.linalg.cholesky(Mf-float(delta)*np.eye(len(ss)));ln=np.rint(lf*T).astype(np.int64);hi=ln//split;lo=ln-hi*split;p00=hi@hi.T;p01=hi@lo.T+lo@hi.T;p11=lo@lo.T
 margins=[]
 for i in range(len(ss)):
  diag=None;offsum=0
  for j in range(len(ss)):
   product=int(p00[i,j])*split**2+int(p01[i,j])*split+int(p11[i,j]);rem=numer[i][j]*T*T-base*product
   if i==j:diag=rem
   else:offsum+=abs(rem)
  assert diag>offsum,(b,i,'exact residual not strictly diagonally dominant')
  margins.append(diag-offsum)
 Larrays[f'block{b}']=ln;cert.append({'block':b,'full_dimension':dim,'support':ss,'L_integer_scale':T,'matrix_numerator_denominator':str(base),'residual_common_denominator':str(base*T*T),'minimum_diagonal_dominance_numerator':str(min(margins)),'minimum_diagonal_dominance_exact':str(Q(min(margins),base*T*T)),'float_repaired_min_eigenvalue_for_factor_discovery_only':mineig,'exact_status':'M=LL^T+strictly_diagonally_dominant_positive_residual'})
 print(json.dumps({'block':b,'exact_PSD':'PASS','size':len(ss),'elapsed_seconds':__import__('time').monotonic()-st}),flush=True)
np.savez_compressed(O/'INTEGER_CHOLESKY_FACTORS.npz',**Larrays);(O/'EXACT_PSD_CERTIFICATES.json').write_text(json.dumps(cert,indent=2)+'\n');point['exact_PSD_acceptance_done']=True;point['status']='EXACT_COUPLED_RELAXATION_POINT';(O/'RATIONAL_POINT.json').write_text(json.dumps(point,indent=2)+'\n');print(json.dumps({'status':'EXACT_COUPLED_RELAXATION_POINT','lambda_support':sum(x>0 for x in lam),'alpha_support':sum(x>0 for x in alpha),'denominator_digits':len(str(den)),'output':str(O),'is_graph':False}))
