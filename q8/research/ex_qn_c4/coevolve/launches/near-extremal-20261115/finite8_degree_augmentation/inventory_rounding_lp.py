"""Actual broad inventory degree/frequency/PSD primal using sparse exact features.
No scheduler or theorem gate: finite feature preparation and eigen-cut LP only.
All evidence is run-local; inventory is an enrichment, not full flag coverage.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1');os.environ.setdefault('OMP_NUM_THREADS','1')
from pathlib import Path
import sys,json,math,time,hashlib,struct,array,argparse
P=Path(__file__).resolve().parent;R=P/'pool_inventory_rounding';SRC=P.parent/'finite8_flags'
sys.path.insert(0,str(SRC/'deps'));sys.path.insert(0,str(SRC))
import numpy as np
from scipy import sparse
from scipy.optimize import linprog
import finite_flags as ff

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--rounds',type=int,default=100);ap.add_argument('--seconds',type=float,default=180);a=ap.parse_args();assert not (R/'LP_STARTED.json').exists(),'Preserve original run.'
 R.mkdir(exist_ok=True);prev=P/'pool_fourth_frequency'
 for n in ['PROFILE_SNAPSHOT.json','block1.EXACT_SEPARATOR.json','block4.EXACT_SEPARATOR.json','FINITE6_ROOT_CHECK.json','KERNEL_SOURCE_SNAPSHOT.json']:(R/n).write_bytes((prev/n).read_bytes())
 old=P/'pool_inventory';st=time.monotonic()
 import shutil
 for n in ['INVENTORY_INPUT.bin','POOL_GRAPH_CODES.json','INTEGER_FEATURES.npz','MARGINAL_FEATURES.npz']:
  shutil.copyfile(old/n,R/n)
 for n in ['ROUNDING_FAMILY.json','FAMILY_EXACT_CHECK.json']:
  shutil.copyfile(SRC.parent/'finite8_rounding_kernels'/n,R/n)
 graphs=json.loads((R/'POOL_GRAPH_CODES.json').read_text());G=len(graphs);profile=json.loads((R/'PROFILE_SNAPSHOT.json').read_text());rows=[r['degrees'] for r in profile['remaining']];A=len(rows)
 prior=json.loads((old/'LP_STARTED.json').read_text());F=sparse.load_npz(R/'INTEGER_FEATURES.npz');D=F.shape[1];starts=np.array(prior['packed_starts']);supports=[set(x) for x in prior['supports']];oldz=np.load(R/'MARGINAL_FEATURES.npz');H=oldz['hist'];EV=oldz['even'];K=oldz['kernel_raw'];scales=oldz['kernel_scales'].tolist();B=oldz['profile_hypergeom'];iraw=(R/'INVENTORY_INPUT.bin').read_bytes();inventory=list(struct.unpack('<'+'I'*(len(iraw)//4),iraw));extra=[g for g in graphs if g not in set(inventory)]
 family=json.loads((R/'ROUNDING_FAMILY.json').read_text());roundraw=[];roundscales=[]
 for cut in family['cuts']:
  b,bit,t=cut['block'],cut['bit'],cut['t'];dim=ff.DIMS[b];states=sorted(ff.STATE_IDS[b],key=ff.STATE_IDS[b].get);q=np.array([(code>>bit)&1 for code in states],dtype=np.int64);ii,jj=np.triu_indices(dim)
  kernel=36*q[ii]*q[jj]-3*(2*t+1)*(q[ii]+q[jj])+t*(t+1);coords=np.zeros(D,dtype=np.int64);coords[int(starts[b]):int(starts[b+1])]=kernel;roundraw.append(F@coords);roundscales.append(cut['scale'])
 roundraw=np.array(roundraw,dtype=np.int64).T;roundscales=np.array(roundscales,dtype=np.int64);np.savez_compressed(R/'ROUNDING_FEATURES.npz',raw=roundraw,scales=roundscales)
 # Literal exact interface regression for two graphs against all120 kernels.
 for rowid in [0,len(graphs)-1]:
  _,co=ff.local_coefficients(ff.q4_edges_from_mask(graphs[rowid]))
  for k,cut in enumerate(family['cuts']):
   b,bit,t=cut['block'],cut['bit'],cut['t'];states=sorted(ff.STATE_IDS[b],key=ff.STATE_IDS[b].get);q=[(code>>bit)&1 for code in states]
   vv=sum(v*(36*q[i]*q[j]-3*(2*t+1)*(q[i]+q[j])+t*(t+1)) for (bb,i,j),v in co.items() if bb==b);assert vv==int(roundraw[rowid,k])
 supports=[sorted(ss) for ss in supports];lookups=[{x:i for i,x in enumerate(ss)} for ss in supports];ixs=[];factors=[];tris=[]
 for b,d in enumerate(ff.DIMS):
  ss=supports[b];ix=np.array([[int(starts[b])+min(i,j)*d-min(i,j)*(min(i,j)-1)//2+max(i,j)-min(i,j) for j in ss] for i in ss],dtype=np.int64);ixs.append(ix);factors.append(np.array([[1. if i==j else .5 for j in ss] for i in ss]));tris.append(np.triu_indices(d))
 Aeq=sparse.csr_matrix(np.block([[np.ones((1,G)),np.zeros((1,A+1))],[np.zeros((1,G)),np.ones((1,A)),np.zeros((1,1))],[H.T/16,-B.T/8960,np.zeros((5,1))]]));beq=np.r_[1.,1.,np.zeros(5)]
 rays=[];cuts=[];seen=set()
 def add(b,q,origin):
  q=np.asarray(q,dtype=np.int64);gg=math.gcd(*map(abs,map(int,q)))
  if not gg:return False
  q=q//gg
  if q[np.argmax(np.abs(q))]<0:q=-q
  key=(b,tuple(map(int,q)))
  if key in seen:return False
  seen.add(key);norm=sum(int(x)**2 for x in q);full=np.zeros(ff.DIMS[b],dtype=np.int64);full[supports[b]]=q;coords=np.zeros(D,dtype=np.int64);ii,jj=tris[b];coords[int(starts[b]):int(starts[b+1])]=full[ii]*full[jj]
  raw=F@coords;v=raw.astype(float)/(ff.DEN*norm);cuts.append(sparse.csr_matrix(v.reshape(1,-1)));rays.append({'block':b,'support':supports[b],'q':q.tolist(),'norm_squared':norm,'origin':origin});return True
 for b,ss in enumerate(supports):
  for i in range(len(ss)):
   q=np.zeros(len(ss),dtype=np.int64);q[i]=1;add(b,q,'coordinate')
 # Valid previously generated directions are reusable on the new full states.
 for old in json.loads((P/'pool_inventory'/'EIGEN_RAYS.json').read_text()):
  b=old['block'];q=np.zeros(len(supports[b]),dtype=np.int64)
  for state,v in zip(old['support'],old['q']):q[lookups[b][state]]=v
  add(b,q,{'prior_valid_ray':str(prev)})
 started={'graph_count':G,'inventory_graph_count':len(inventory),'extra_actual_column_count':len(set(extra)-set(inventory)),'profile_rows':A,'supports':supports,'dimensions':ff.DIMS,'packed_starts':starts.tolist(),'feature_nnz':F.nnz,'feature_prepare_seconds':time.monotonic()-st,'finite6_scales':scales,'finite6_validity':'Root exact finite6 fullstate checks; formal review separately pending','new_rounding_kernels':len(roundscales),'rounding_source_sha256':hashlib.sha256((R/'ROUNDING_FAMILY.json').read_bytes()).hexdigest(),'initial_rays':len(rays),'round_limit':a.rounds,'wall_limit_seconds':a.seconds,'scope':'same13962 columns plus120 exact integer-six rounding constraints; not full feature classification'}
 (R/'LP_STARTED.json').write_text(json.dumps(started,indent=2)+'\n');print(json.dumps({k:v for k,v in started.items() if k!='supports'}),flush=True)
 start=time.monotonic();history=[];final={};obj=np.r_[np.zeros(G+A),-1.]
 for iteration in range(a.rounds):
  if time.monotonic()-start>a.seconds:final={'status':'ACTUAL_WALL_BOUND','iteration':iteration};break
  oldcutcount=len(cuts);C=sparse.vstack(cuts,format='csr');AB=sparse.hstack([-C,sparse.csr_matrix((len(cuts),A)),np.ones((len(cuts),1))],format='csr');aux=np.zeros((3+len(roundscales),G+A+1));aux[0,:G]=-EV;aux[1:3,:G]=-K.T/(ff.DEN*np.array(scales))[:,None];aux[3:,:G]=-roundraw.T/(ff.DEN*roundscales)[:,None];Aub=sparse.vstack([AB,sparse.csr_matrix(aux)],format='csr');bub=np.r_[np.zeros(len(cuts)),-57/224,np.zeros(2+len(roundscales))]
  lp=linprog(obj,A_ub=Aub,b_ub=bub,A_eq=Aeq,b_eq=beq,bounds=[(0,None)]*(G+A)+[(-1,1)],method='highs',options={'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9})
  if not lp.success:final={'status':'RESTRICTED_LP_INFEASIBLE_FLOAT' if lp.status==2 else 'LP_EXECUTION_STATUS','lp_status':lp.status,'message':lp.message,'iteration':iteration};history.append(final);break
  lam=lp.x[:G];alpha=lp.x[G:G+A];margin=float(lp.x[-1]);packed=np.asarray(F.T@lam)/ff.DEN;mins=[];adds=[];moments={}
  for b,ss in enumerate(supports):
   M=packed[ixs[b]]*factors[b];moments[f'block{b}']=M
   if not ss:mins.append(None);continue
   ev,vec=np.linalg.eigh(M);mins.append(float(ev[0]))
   for k in np.where(ev<margin-1e-9)[0][:4]:adds.append((b,np.rint(vec[:,k]*10**6).astype(np.int64),{'iteration':iteration,'eigenvalue':float(ev[k]),'margin':margin}))
  added=sum(add(*x) for x in adds);row={'iteration':iteration,'max_margin_lp':margin,'block_min_eigenvalues':mins,'cuts_used':oldcutcount,'rays_added':added,'lambda_positive':int(sum(lam>1e-10)),'alpha_positive':int(sum(alpha>1e-10)),'even_expectation':float(EV@lam),'finite6_expectations':(K.T@lam/(ff.DEN*np.array(scales))).tolist(),'rounding_expectation_min':float(min(roundraw.T@lam/(ff.DEN*roundscales))),'elapsed_seconds':time.monotonic()-start};history.append(row);print(json.dumps(row),flush=True)
  final={'status':'FLOAT_PRIMAL_CANDIDATE' if min(x for x in mins if x is not None)>1e-10 else 'EIGEN_CUT_ITERATION_BOUND','iteration':iteration,'margin':margin,'block_min_eigenvalues':mins,'lambda':[[g,float(x)] for g,x in zip(graphs,lam) if x>1e-12],'alpha':[[i,float(x),rows[i]] for i,x in enumerate(alpha) if x>1e-12],'even_expectation':row['even_expectation'],'finite6_expectations':row['finite6_expectations'],'rounding_expectation_min':row['rounding_expectation_min'],'profile_snapshot_rows':A,'pool_graphs':G,'is_graph':False,'primary683_goal':'OPEN'}
  (R/'FLOAT_CANDIDATE.json').write_text(json.dumps(final,indent=2)+'\n');np.savez_compressed(R/'FLOAT_MOMENTS.npz',**moments);(R/'LP_HISTORY.json').write_text(json.dumps(history,indent=2)+'\n')
  if final['status']=='FLOAT_PRIMAL_CANDIDATE':break
  if margin<-1e-8:final['status']='RESTRICTED_PSD_INFEASIBLE_FLOAT_DUAL_CANDIDATE';final['inequality_duals']=lp.ineqlin.marginals.tolist();final['equality_duals']=lp.eqlin.marginals.tolist();final['cuts_used']=oldcutcount;break
  if not added:break
 (R/'EIGEN_RAYS.json').write_text(json.dumps(rays,indent=2)+'\n');(R/'LP_HISTORY.json').write_text(json.dumps(history,indent=2)+'\n');(R/'LP_RESULT.json').write_text(json.dumps(final,indent=2)+'\n');print(json.dumps({'final_status':final['status'],'iterations':len(history),'seconds':time.monotonic()-start,'scope':'inventory restricted pool, not full NO or graph'}),flush=True)
if __name__=='__main__':main()
