"""Primal max-min PSD margin on frozen792 degree rows +818 actual legal Q4s.
One lambda controls both degree marginals and six moments. Quantized integer
negative eigendirections give exact rational valid PSD cuts. Restricted only.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1');os.environ.setdefault('OMP_NUM_THREADS','1')
from pathlib import Path
import sys,json,hashlib,time,math,argparse
P=Path(__file__).resolve().parent/'pool_second_violation';SRC=P.parent.parent/'finite8_flags'
sys.path.insert(0,str(SRC/'deps'));sys.path.insert(0,str(SRC))
import numpy as np
from scipy.optimize import linprog
from scipy import sparse
import finite_flags as ff

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--rounds',type=int,default=80);args=ap.parse_args()
 assert not (P/'LP_STARTED.json').exists(),'Keep original run; do not silently overwrite.'
 profile=json.loads((P/'PROFILE_SNAPSHOT.json').read_text());rows=[r['degrees'] for r in profile['remaining']]
 graphs=json.loads((P/'POOL_GRAPH_CODES.json').read_text())
 coeff=[];hist=[];density=[];even=[]
 for g in graphs:
  E=ff.q4_edges_from_mask(g);rho,c=ff.local_coefficients(E);coeff.append(c);density.append(rho/ff.DEN)
  ds=[sum(x==v or y==v for x,y in E) for v in range(16)];hist.append([ds.count(j) for j in range(5)])
  even.append(sum(root.bit_count()%2==0 for root,states in ff.face_data(E,4)))
 supports=[sorted({i for c in coeff for bb,i,j in c if bb==b}|{j for c in coeff for bb,i,j in c if bb==b}) for b in range(6)]
 matrices=[]
 for b,ss in enumerate(supports):
  look={s:i for i,s in enumerate(ss)};C=np.zeros((len(graphs),len(ss),len(ss)),dtype=np.int64)
  for k,c in enumerate(coeff):
   for (bb,i,j),v in c.items():
    if bb!=b:continue
    ii,jj=look[i],look[j];C[k,ii,jj]+=v*(2 if i==j else 1)
    if ii!=jj:C[k,jj,ii]+=v
  matrices.append(C)
 # matrices are twice the symmetric integer coefficient matrix.
 G=len(graphs);R=len(rows);H=np.array(hist,dtype=np.int64)
 B=np.array([[sum(n[d]*math.comb(d,j)*math.comb(8-d,4-j) for d in range(9) if j<=d and 4-j<=8-d) for j in range(5)] for n in rows],dtype=np.int64)
 Aeq=np.zeros((7,G+R+1));beq=np.zeros(7);Aeq[0,:G]=1;beq[0]=1;Aeq[1,G:G+R]=1;beq[1]=1
 Aeq[2:,:G]=H.T/16;Aeq[2:,G:G+R]=-B.T/8960
 rays=[];cuts=[];seen=set()
 def add(b,q,origin):
  q=np.asarray(q,dtype=np.int64);gg=0
  for a in q:gg=math.gcd(gg,abs(int(a)))
  if not gg:return False
  q=q//gg
  if q[np.argmax(np.abs(q))]<0:q=-q
  sig=(b,tuple(map(int,q)))
  if sig in seen:return False
  seen.add(sig);norm=sum(int(a)**2 for a in q)
  # int64 sufficient: q<=1e6, dimensions<=16, coeff<=64512.
  vals=np.einsum('i,gij,j->g',q,matrices[b],q,optimize=True)
  cut=vals.astype(float)/(2*ff.DEN*norm)
  cuts.append(cut);rays.append({'block':b,'support':supports[b],'q':q.tolist(),'norm_squared':norm,'origin':origin})
  return True
 for b,ss in enumerate(supports):
  for i in range(len(ss)):
   q=np.zeros(len(ss),dtype=np.int64);q[i]=1;add(b,q,'coordinate PSD diagonal')
 started={'profiles':R,'profile_sha256':hashlib.sha256((P/'PROFILE_SNAPSHOT.json').read_bytes()).hexdigest(),'graphs':G,'graph_codes':graphs,'supports':supports,'density_target':'683/1024','snapshot_remaining_count':profile['remaining_count'],'criterion':'max margin s on each nonempty support block; absent states identically zero','new_even_square_gate':'Eλ even_Q2(K)>=57/224','round_limit':args.rounds}
 (P/'LP_STARTED.json').write_text(json.dumps(started,indent=2)+'\n')
 np.savez_compressed(P/'COUPLED_COEFFICIENTS.npz',hist=H,profile_hypergeom_numerators=B,even=np.array(even,dtype=np.int64),**{f'block{b}':C for b,C in enumerate(matrices)})
 start=time.monotonic();history=[];final={}
 for it in range(args.rounds):
  Aub=np.zeros((len(cuts)+1,G+R+1));Aub[:-1,:G]=-np.array(cuts);Aub[:-1,-1]=1;Aub[-1,:G]=-np.array(even);bub=np.r_[np.zeros(len(cuts)),-57/224]
  obj=np.zeros(G+R+1);obj[-1]=-1
  result=linprog(obj,A_ub=Aub,b_ub=bub,A_eq=Aeq,b_eq=beq,bounds=[(0,None)]*(G+R)+[(-1,1)],method='highs',options={'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9})
  if not result.success:
   final={'status':'RESTRICTED_LP_INFEASIBLE' if result.status==2 else 'LP_EXECUTION_STATUS','message':result.message,'lp_status':result.status};history.append({'iteration':it,**final});break
  lam=result.x[:G];alpha=result.x[G:G+R];margin=float(result.x[-1]);mins=[];toadd=[]
  for b,C in enumerate(matrices):
   if not len(supports[b]):mins.append(None);continue
   M=np.einsum('g,gij->ij',lam,C)/(2*ff.DEN);ev,vec=np.linalg.eigh(M);mins.append(float(ev[0]))
   for k in np.where(ev<margin-1e-9)[0][:6]:
    q=np.rint(vec[:,k]*10**6).astype(np.int64);toadd.append((b,q,{'iteration':it,'eigenvalue':float(ev[k]),'margin':margin}))
  added=sum(add(*r) for r in toadd)
  row={'iteration':it,'max_margin_lp':margin,'actual_block_min_eigenvalues':mins,'cuts':len(cuts),'rays_added':added,'lambda_positive':int(sum(lam>1e-10)),'alpha_positive':int(sum(alpha>1e-10)),'equality_residual_max':float(np.max(np.abs(Aeq@result.x-beq))),'elapsed_seconds':time.monotonic()-start}
  history.append(row);print(json.dumps(row),flush=True)
  final={'status':'FLOAT_PRIMAL_CANDIDATE' if min(x for x in mins if x is not None)>1e-10 else 'EIGEN_CUT_ITERATION_BOUND','lambda':[[g,float(v)] for g,v in zip(graphs,lam) if v>1e-12],'alpha':[[i,float(v),rows[i]] for i,v in enumerate(alpha) if v>1e-12],'margin':margin,'min_eigenvalues':mins,'density':float(np.array(density)@lam),'equality_residual_max':row['equality_residual_max'],'iteration':it,'restricted_pool':G,'profile_count':R,'primary683_goal':'OPEN','is_graph':False}
  (P/'FLOAT_CANDIDATE.json').write_text(json.dumps(final,indent=2)+'\n')
  (P/'LP_HISTORY.json').write_text(json.dumps(history,indent=2)+'\n')
  if final['status']=='FLOAT_PRIMAL_CANDIDATE':break
  if margin<-1e-8:
   final['status']='RESTRICTED_PSD_INFEASIBLE_FLOAT_DUAL_CANDIDATE'
   final['lp_inequality_duals']=result.ineqlin.marginals.tolist();final['lp_equality_duals']=result.eqlin.marginals.tolist();break
  if not added:break
 (P/'EIGEN_RAYS.json').write_text(json.dumps(rays,indent=2)+'\n');(P/'LP_HISTORY.json').write_text(json.dumps(history,indent=2)+'\n');(P/'LP_RESULT.json').write_text(json.dumps(final,indent=2)+'\n')
 print(json.dumps({'final_status':final['status'],'iterations':len(history),'seconds':time.monotonic()-start,'scope':'exact-feature dedup of1176 plus second actual violation,792 profiles,even>=57/224'}))
if __name__=='__main__':main()
