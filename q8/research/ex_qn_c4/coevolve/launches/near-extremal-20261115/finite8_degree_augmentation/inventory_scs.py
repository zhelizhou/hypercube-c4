"""Direct cone feasibility/max-margin with the same frozen sparse actual data.
Numerical discovery only; exact same-input rational/PSD acceptance is separate.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1');os.environ.setdefault('OMP_NUM_THREADS','1')
from pathlib import Path
import sys,json,time,math
P=Path(__file__).resolve().parent;R=P/'pool_inventory';O=P/'pool_inventory_scs';O.mkdir(exist_ok=True);SRC=P.parent/'finite8_flags';sys.path.insert(0,str(SRC/'deps'));sys.path.insert(0,str(P/'scs_deps'))
import numpy as np
from scipy import sparse
import scs
assert not (O/'SCS_STARTED.json').exists(),'Preserve original SCS scope.'
start=json.loads((R/'LP_STARTED.json').read_text());graphs=json.loads((R/'POOL_GRAPH_CODES.json').read_text());profiles=json.loads((R/'PROFILE_SNAPSHOT.json').read_text())['remaining'];G=len(graphs);A=len(profiles);F=sparse.load_npz(R/'INTEGER_FEATURES.npz');z=np.load(R/'MARGINAL_FEATURES.npz');H=z['hist'];B=z['profile_hypergeom'];EV=z['even'];K=z['kernel_raw'];scales=z['kernel_scales'];N=G+A+1
E=sparse.csr_matrix(np.block([[np.ones((1,G)),np.zeros((1,A+1))],[np.zeros((1,G)),np.ones((1,A)),np.zeros((1,1))],[H.T/16,-B.T/8960,np.zeros((5,1))]]));beq=np.r_[1.,1.,np.zeros(5)]
L=sparse.hstack([-sparse.eye(G+A,format='csr'),np.zeros((G+A,1))],format='csr');aux=np.zeros((5,N));aux[0,:G]=-EV;aux[1:3,:G]=-K.T/(64512*scales)[:,None];aux[3,-1]=1;aux[4,-1]=-1;L=sparse.vstack([L,sparse.csr_matrix(aux)],format='csr');bl=np.r_[np.zeros(G+A),-57/224,0.,0.,1.,1.]
sel=[];fac=[];diag=[];off=0
for b,(d,ss) in enumerate(zip(start['dimensions'],start['supports'])):
 for ii,i in enumerate(ss):
  for j in ss[ii:]:
   sel.append(start['packed_starts'][b]+i*d-i*(i-1)//2+j-i);fac.append(1. if i==j else 1/math.sqrt(2))
   if i==j:diag.append(off)
   off+=1
Z=F[:,sel].T.multiply(np.array(fac)[:,None]).tocsr()*(-1000/64512);T=sparse.csr_matrix((np.ones(len(diag)),(diag,np.zeros(len(diag),dtype=int))),shape=(len(sel),1));PSD=sparse.hstack([Z,sparse.csr_matrix((len(sel),A)),T],format='csr')
AA=sparse.vstack([E,L,PSD],format='csc');bb=np.r_[beq,bl,np.zeros(len(sel))];cc=np.zeros(N);cc[-1]=-1;cone={'z':7,'l':len(bl),'s':[len(ss) for ss in start['supports']]}
meta={'scs_version':scs.__version__,'linear_solver':'CPU_INDIRECT','variables':N,'rows':len(bb),'nnz':AA.nnz,'cone':cone,'PSD_scaling':1000,'same_lambda_hypergeom_PSD_even_and_two_finite6':True,'scope':'same13962 working pool; direct numeric cone discovery, no exact acceptance','profile_rows':A,'eps_abs':1e-7,'eps_rel':1e-7,'max_iters':5000,'time_limit_secs':150}
(O/'SCS_STARTED.json').write_text(json.dumps(meta,indent=2)+'\n');np.savez_compressed(O/'SCS_b_c.npz',b=bb,c=cc);print(json.dumps(meta),flush=True)
x0=np.zeros(N);cand=json.loads((R/'FLOAT_CANDIDATE.json').read_text());index={g:i for i,g in enumerate(graphs)}
for g,v in cand['lambda']:x0[index[g]]=v
for i,v,n in cand['alpha']:x0[G+i]=v
x0[-1]=cand['margin']*1000
st=time.monotonic();solver=scs.SCS({'A':AA,'b':bb,'c':cc},cone,linear_solver=scs.LinearSolver.CPU_INDIRECT,eps_abs=1e-7,eps_rel=1e-7,max_iters=5000,time_limit_secs=150,verbose=True,acceleration_lookback=10);sol=solver.solve(warm_start=True,x=x0)
np.savez_compressed(O/'SCS_RAW.npz',x=sol['x'],y=sol['y'],s=sol['s']);x=sol['x'];lam=x[:G];alpha=x[G:G+A];packed=np.asarray(F.T@lam)/64512;mins=[];moments={}
for b,(d,ss) in enumerate(zip(start['dimensions'],start['supports'])):
 M=np.array([[packed[start['packed_starts'][b]+min(i,j)*d-min(i,j)*(min(i,j)-1)//2+max(i,j)-min(i,j)]*(1 if i==j else .5) for j in ss] for i in ss]);moments[f'block{b}']=M;mins.append(float(np.linalg.eigvalsh(M)[0]) if len(ss) else None)
np.savez_compressed(O/'FLOAT_MOMENTS.npz',**moments)
out={'status':'NUMERIC_DIRECT_CONE_RESULT','scs_info':sol['info'],'seconds':time.monotonic()-st,'lambda':[[g,float(v)] for g,v in zip(graphs,lam) if abs(v)>1e-13],'alpha':[[i,float(v),profiles[i]['degrees']] for i,v in enumerate(alpha) if abs(v)>1e-13],'raw_margin':float(x[-1]/1000),'block_min_eigenvalues':mins,'lambda_min':float(min(lam)),'alpha_min':float(min(alpha)),'equality_residual_max':float(max(abs(E@x-beq))),'even_expectation':float(EV@lam),'finite6_expectations':(K.T@lam/(64512*scales)).tolist(),'exact_acceptance_done':False,'is_graph':False,'primary683_goal':'OPEN'}
(O/'FLOAT_CANDIDATE.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['lambda','alpha']}),flush=True)
