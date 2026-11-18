"""One genuine common-lambda probe: complete edge7 cone, endpoint global degree,
120 fixed and dynamically priced integer6/28 rounding plus original six PSDs.
Inventory is only a column pool. Numerical results are never exact acceptance.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1');os.environ.setdefault('OMP_NUM_THREADS','1')
from pathlib import Path
import sys,json,time,math,argparse,hashlib
P=Path(__file__).resolve().parent;R=P/'pool_edge_degree_dynamic';SRC=P.parent/'finite8_flags';sys.path.insert(0,str(SRC/'deps'));sys.path.insert(0,str(SRC));sys.path.insert(0,str(P))
import numpy as np
from scipy import sparse
from scipy.optimize import linprog
import finite_flags as ff
import dynamic_rounding as dr

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--rounds',type=int,default=12);ap.add_argument('--seconds',type=float,default=300);a=ap.parse_args();assert not (R/'LP_STARTED.json').exists()
 base=P/'pool_inventory_rounding';info=json.loads((base/'LP_STARTED.json').read_text());graphs=json.loads((R/'POOL_GRAPH_CODES.json').read_text());profiles=json.loads((R/'PROFILE_SNAPSHOT.json').read_text())['remaining'];G=len(graphs);A=len(profiles);F=sparse.load_npz(R/'INTEGER_FEATURES.npz');z=np.load(R/'MARGINAL_FEATURES.npz');H=z['hist'];B=z['profile_hypergeom'];EV=z['even'];K=z['kernel_raw'];scales=z['kernel_scales'];rr=np.load(R/'ROUNDING_FEATURES.npz');roundraw=rr['raw'];roundscales=rr['scales'];U=sparse.load_npz(R/'EDGE_U_NUMERATOR.npz');Gamma=sparse.load_npz(R/'EDGE_GENERATOR_DEDUP_NUMERATOR.npz');EP=sparse.load_npz(R/'EDGE_ENDPOINT_DEDUP.npz');RHS=sparse.load_npz(R/'EDGE_DEGREE_PROFILE_RHS_NUMERATOR.npz');Nbeta=Gamma.shape[1];N=G+A+Nbeta+1;D=F.shape[1]
 Edegree=sparse.csr_matrix(np.block([[np.ones((1,G)),np.zeros((1,A+Nbeta+1))],[np.zeros((1,G)),np.ones((1,A)),np.zeros((1,Nbeta+1))],[H.T/16,-B.T/8960,np.zeros((5,Nbeta+1))]]));Eedge=sparse.hstack([U/129024,sparse.csr_matrix((64,A)),-Gamma/98,sparse.csr_matrix((64,1))],format='csr');Eendpoint=sparse.hstack([sparse.csr_matrix((18,G)),-RHS/512,EP,sparse.csr_matrix((18,1))],format='csr');E=sparse.vstack([Edegree,Eedge,Eendpoint],format='csr');beq=np.r_[1.,1.,np.zeros(87)]
 starts=info['packed_starts'];supports=info['supports'];lookups=[{s:i for i,s in enumerate(ss)} for ss in supports];ix=[];fac=[];tris=[]
 for b,(d,ss) in enumerate(zip(ff.DIMS,supports)):
  ix.append(np.array([[starts[b]+min(i,j)*d-min(i,j)*(min(i,j)-1)//2+max(i,j)-min(i,j) for j in ss] for i in ss],dtype=np.int64));fac.append(np.array([[1. if i==j else .5 for j in ss] for i in ss]));tris.append(np.triu_indices(d))
 rays=[];psdcuts=[];seen=set()
 def add(b,q,origin):
  q=np.asarray(q,dtype=np.int64);gg=math.gcd(*map(abs,map(int,q)))
  if not gg:return False
  q=q//gg
  if q[np.argmax(abs(q))]<0:q=-q
  key=(b,tuple(map(int,q)))
  if key in seen:return False
  seen.add(key);norm=sum(int(v)**2 for v in q);full=np.zeros(ff.DIMS[b],dtype=np.int64);full[supports[b]]=q;coords=np.zeros(D,dtype=np.int64);i,j=tris[b];coords[starts[b]:starts[b+1]]=full[i]*full[j];vals=(F@coords).astype(float)/(64512*norm);psdcuts.append(sparse.csr_matrix(vals.reshape(1,-1)));rays.append({'block':b,'support':supports[b],'q':q.tolist(),'norm_squared':norm,'origin':origin});return True
 for old in json.loads((base/'EIGEN_RAYS.json').read_text()):
  b=old['block'];q=np.zeros(len(supports[b]),dtype=np.int64)
  for i,v in zip(old['support'],old['q']):q[lookups[b][i]]=v
  add(b,q,{'prior_scope':'pool_inventory_rounding'})
 family=json.loads((R/'ROUNDING_FAMILY.json').read_text());round_seen=set()
 for cut in family['cuts']:
  b,bit,t=cut['block'],cut['bit'],cut['t'];round_seen.add(dr.key(b,dr.BITS[b][:,bit],t))
 frozen=dict(np.load(base/'FLOAT_MOMENTS.npz'));dyn_defs,dyn_vals=dr.price(frozen,F,starts,round_seen,per_block=3);dyn_features=[sparse.csr_matrix(v.reshape(1,-1)) for v in dyn_vals]
 for d in dyn_defs:d['origin']='frozen pool_inventory_rounding finalpoint'
 aux=np.zeros((3+len(roundscales),N));aux[0,:G]=-EV;aux[1:3,:G]=-K.T/(64512*scales)[:,None];aux[3:,:G]=-roundraw.T/(64512*roundscales)[:,None];static=sparse.csr_matrix(aux);bstatic=np.r_[-57/224,np.zeros(2+len(roundscales))]
 dedup=json.loads((R/'GENERATOR_DEDUPLICATION.json').read_text());selected=dedup['selected_original_indices'];root1=np.array([i>=3432 for i in selected]);obj=np.r_[np.zeros(N-1),-1.]
 meta={'scope':'13962Q4 pool,792 profiles,complete5148 edge7 cone (exact2788-column merge),18endpoint-degree equalities,120fixed+dynamicinteger6/28 kernels,6PSD','graphs':G,'profiles':A,'beta_variables':Nbeta,'equalities':E.shape[0],'initial_PSD_rays':len(rays),'initial_new_dynamic_rounding_cuts':len(dyn_defs),'fixed_rounding_cuts':len(roundscales),'LP_method':'highs-ipm','round_limit':a.rounds,'wall_limit_seconds':a.seconds,'extra_bridge_status':'Root geometric derivation + author independent proof/check pending; own1024edge682regression passed'}
 (R/'LP_STARTED.json').write_text(json.dumps(meta,indent=2)+'\n');print(json.dumps(meta),flush=True);start=time.monotonic();history=[];final={}
 for iteration in range(a.rounds):
  if time.monotonic()-start>a.seconds:final={'status':'ACTUAL_WALL_BOUND','iteration':iteration};break
  pused=len(psdcuts);dused=len(dyn_features);PC=sparse.vstack(psdcuts,format='csr');Apsd=sparse.hstack([-PC,sparse.csr_matrix((pused,A+Nbeta)),np.ones((pused,1))],format='csr')
  Adyn=sparse.hstack([-sparse.vstack(dyn_features),sparse.csr_matrix((dused,A+Nbeta+1))],format='csr') if dused else sparse.csr_matrix((0,N));Aub=sparse.vstack([Apsd,Adyn,static],format='csr');bub=np.r_[np.zeros(pused+dused),bstatic]
  st=time.monotonic();lp=linprog(obj,A_ub=Aub,b_ub=bub,A_eq=E,b_eq=beq,bounds=[(0,None)]*(N-1)+[(-1,1)],method='highs-ipm',options={'time_limit':90,'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9,'ipm_optimality_tolerance':1e-10})
  if not lp.success:
   final={'status':'RESTRICTED_LP_INFEASIBLE_FLOAT' if lp.status==2 else 'LP_EXECUTION_STATUS','lp_status':lp.status,'message':lp.message,'iteration':iteration,'LP_seconds':time.monotonic()-st};history.append(final);break
  lam=lp.x[:G];alpha=lp.x[G:G+A];beta=lp.x[G+A:-1];margin=float(lp.x[-1]);pack=np.asarray(F.T@lam)/64512;moments={};mins=[];adds=[]
  for b,ss in enumerate(supports):
   M=pack[ix[b]]*fac[b];moments[f'block{b}']=M;ev,vec=np.linalg.eigh(M);mins.append(float(ev[0]))
   for k in np.where(ev<margin-1e-9)[0][:4]:adds.append((b,np.rint(vec[:,k]*10**6).astype(np.int64),{'iteration':iteration,'eigenvalue':float(ev[k]),'margin':margin}))
  added=sum(add(*v) for v in adds);new_defs,new_features=dr.price(moments,F,starts,round_seen,per_block=3)
  for d in new_defs:d['origin']={'iteration':iteration}
  dyn_defs.extend(new_defs);dyn_features.extend(sparse.csr_matrix(v.reshape(1,-1)) for v in new_features)
  row={'iteration':iteration,'margin':margin,'block_min_eigenvalues':mins,'PSD_cuts_used':pused,'PSD_rays_added':added,'dynamic_rounding_cuts_used':dused,'dynamic_rounding_cuts_added':len(new_defs),'lambda_positive':int(sum(lam>1e-10)),'alpha_positive':int(sum(alpha>1e-10)),'beta_positive':int(sum(beta>1e-10)),'beta_root_masses':[float(sum(beta[~root1])),float(sum(beta[root1]))],'equality_residual_max':float(max(abs(E@lp.x-beq))),'even_expectation':float(EV@lam),'fixed_rounding_min':float(min(roundraw.T@lam/(64512*roundscales))),'LP_seconds':time.monotonic()-st,'elapsed_seconds':time.monotonic()-start};history.append(row);print(json.dumps(row),flush=True)
  final={'status':'FLOAT_PRIMAL_CANDIDATE' if min(mins)>1e-10 and not new_defs else 'EIGEN_AND_INTEGER_CUT_ITERATION_BOUND','iteration':iteration,'margin':margin,'block_min_eigenvalues':mins,'lambda':[[g,float(x)] for g,x in zip(graphs,lam) if x>1e-12],'alpha':[[i,float(x),profiles[i]['degrees']] for i,x in enumerate(alpha) if x>1e-12],'beta':[[i,float(x)] for i,x in enumerate(beta) if x>1e-12],'beta_column_order':'GENERATOR_DEDUPLICATION selected_original_indices','beta_root_masses':row['beta_root_masses'],'equality_residual_max':row['equality_residual_max'],'is_graph':False,'exact_acceptance_done':False,'primary683_goal':'OPEN'}
  (R/'FLOAT_CANDIDATE.json').write_text(json.dumps(final,indent=2)+'\n');np.savez_compressed(R/'FLOAT_MOMENTS.npz',**moments);(R/'LP_HISTORY.json').write_text(json.dumps(history,indent=2)+'\n');(R/'EIGEN_RAYS.json').write_text(json.dumps(rays)+'\n');(R/'DYNAMIC_ROUNDING_CUTS.json').write_text(json.dumps(dyn_defs,indent=2)+'\n')
  if final['status']=='FLOAT_PRIMAL_CANDIDATE':break
  if margin<-1e-8:final['status']='RESTRICTED_PSD_INFEASIBLE_FLOAT_DUAL_CANDIDATE';final['inequality_duals']=lp.ineqlin.marginals.tolist();final['equality_duals']=lp.eqlin.marginals.tolist();final['PSD_cuts_used']=pused;final['dynamic_cuts_used']=dused;break
  if not added and not new_defs:break
 (R/'EIGEN_RAYS.json').write_text(json.dumps(rays)+'\n');(R/'DYNAMIC_ROUNDING_CUTS.json').write_text(json.dumps(dyn_defs,indent=2)+'\n');(R/'LP_HISTORY.json').write_text(json.dumps(history,indent=2)+'\n');(R/'LP_RESULT.json').write_text(json.dumps(final,indent=2)+'\n');print(json.dumps({'final_status':final['status'],'iterations':len(history),'seconds':time.monotonic()-start,'scope':'restricted pool; exact final acceptance separate'}),flush=True)
if __name__=='__main__':main()
