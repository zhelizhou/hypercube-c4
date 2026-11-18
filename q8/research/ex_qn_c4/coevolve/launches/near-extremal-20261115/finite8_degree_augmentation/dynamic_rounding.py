"""Exact integer-six kernel definitions; numeric pricing on current moments.
Every returned cut is valid by xQx=36(L-t)(L-t-1), sumx6.
No PSD or graph-feasibility claim is made from a negative numeric pairing.
"""
from itertools import product
import numpy as np
import finite_flags as ff
WEIGHTS=np.array(list(product((-1,0,1),repeat=8)),dtype=np.int64)
STATES=[sorted(ff.STATE_IDS[b],key=ff.STATE_IDS[b].get) for b in range(5)]
BITS=[np.array([[(s>>j)&1 for j in range(8)] for s in states],dtype=np.int64) for states in STATES]
ACTIONS=[[np.array([ff.STATE_IDS[b][move[s]] for s in STATES[b]],dtype=np.int64) for roots,move in ff.TRANSFORMS if roots[ff.ROOT_MASKS[b]]==ff.ROOT_MASKS[b]] for b in range(5)]
def basic(q,t,n=6):
 q=np.asarray(q,dtype=np.int64);lo=int(min(q));q=q-lo;t=int(t)-n*lo;high=int(max(q));reverse=high-q;rt=n*high-t-1
 a=(tuple(map(int,q)),t);b=(tuple(map(int,reverse)),rt)
 return min(a,b)
def key(b,q,t):
 n=28 if b==5 else 6;actions=ACTIONS[b] if b<5 else [np.arange(9)]
 return (b,min(basic(np.asarray(q)[a],t,n) for a in actions))
def full_packed(b,q,t,starts,D):
 q=np.asarray(q,dtype=np.int64);n=28 if b==5 else 6;ii,jj=np.triu_indices(ff.DIMS[b]);v=n*n*q[ii]*q[jj]-(n//2)*(2*t+1)*(q[ii]+q[jj])+t*(t+1);coords=np.zeros(D,dtype=np.int64);coords[int(starts[b]):int(starts[b+1])]=v;scale=max(1,int(max(abs(v))));return coords,scale

def price(matrices,F,starts,seen,per_block=3):
 definitions=[];features=[]
 for b in range(6):
  n=28 if b==5 else 6
  M=matrices[f'block{b}'];mass=float(M.sum())
  if mass<1e-12:continue
  if b<5:
   qs=WEIGHTS@BITS[b].T;extra=[];labels=[]
   for lo,hi,name in [(0,4,'connectors'),(4,8,'parallel'),(0,8,'all')]:
    count=BITS[b][:,lo:hi].sum(axis=1)
    for threshold in range(1,hi-lo+1):extra.append((count>=threshold).astype(np.int64));labels.append(f'{name}>={threshold}')
   qs=np.vstack([qs,np.array(extra)])
  else:qs=np.array(list(product((0,1),repeat=9)),dtype=np.int64)
  B=qs@M.sum(axis=1);C=np.einsum('ij,ij->i',qs@M,qs);ts=np.floor(n*B/mass).astype(np.int64);values=n*n*C-n*(2*ts+1)*B+ts*(ts+1)*mass
  lo=qs.min(axis=1);hi=qs.max(axis=1);scales=np.maximum.reduce([abs(n*n*lo*lo-n*(2*ts+1)*lo+ts*(ts+1)),abs(n*n*hi*hi-n*(2*ts+1)*hi+ts*(ts+1)),abs(n*n*lo*hi-(n//2)*(2*ts+1)*(lo+hi)+ts*(ts+1)),np.ones(len(ts),dtype=np.int64)]);normalized=values/scales
  added=0
  for i in np.argsort(normalized):
   if normalized[i]>=-1e-9:break
   q=qs[i];t=int(ts[i]);finger=key(b,q,t)
   if finger in seen:continue
   seen.add(finger);coords,scale=full_packed(b,q,t,starts,F.shape[1]);assert scale==int(scales[i]);raw=F@coords;features.append(raw.astype(float)/(ff.DEN*scale))
   label=({'bit_weights':WEIGHTS[i].tolist()} if i<len(WEIGHTS) else {'predicate':labels[i-len(WEIGHTS)]}) if b<5 else {'vertex_subset':q.tolist()}
   definitions.append({'block':b,'q':q.tolist(),'t':t,'scale':scale,'definition':label,'raw_pairing_float':float(values[i]),'normalized_pairing_float':float(normalized[i]),'count_total':n,'empirical_mean_count_float':float(n*B[i]/mass),'exact_validity':'integer q,t; sumx=n; xQx=n^2(L-t)(L-t-1)>=0'})
   added+=1
   if added>=per_block:break
 return definitions,features

def price_full_state(matrices,F,starts,seen,per_block=3):
 """Same already-proved integer6 family, arbitrary state-integer q seeds.
 Quantizes small covariance/eigen directions; no assumption that q is a bit
 linear form. Every selected inequality is independently globally valid.
 """
 definitions=[];features=[]
 for b in range(5):
  M=matrices[f'block{b}'];mass=float(M.sum())
  if mass<1e-12:continue
  ev,vec=np.linalg.eigh(M);choices=[]
  for k in range(min(10,len(ev))):
   for factor in [1,2,3,4,8,16]:
    q=np.rint(vec[:,k]*factor/max(abs(vec[:,k]))).astype(np.int64);B=float(q@M.sum(axis=1));C=float(q@M@q);t=int(np.floor(6*B/mass));finger=key(b,q,t)
    if finger in seen:continue
    # Mark only after selecting; another seed may give same kernel and is
    # deduplicated in the sorted loop below.
    coord,scale=full_packed(b,q,t,starts,F.shape[1]);value=(36*C-6*(2*t+1)*B+t*(t+1)*mass)/scale
    if value < -1e-9:choices.append((value,q,t,scale,finger,float(ev[k]),factor))
  choices.sort(key=lambda x:x[0]);added=0
  for value,q,t,scale,finger,eig,factor in choices:
   if finger in seen:continue
   seen.add(finger);coords,ss=full_packed(b,q,t,starts,F.shape[1]);assert ss==scale;features.append((F@coords).astype(float)/(ff.DEN*scale));definitions.append({'block':b,'q':q.tolist(),'t':t,'scale':scale,'definition':{'full_state_eigen_integerization':factor,'source_eigenvalue':eig},'normalized_pairing_float':value,'count_total':6,'exact_validity':'arbitrary integer q,t; sumx6; xQx=36(L-t)(L-t-1)>=0'});added+=1
   if added>=per_block:break
 return definitions,features
