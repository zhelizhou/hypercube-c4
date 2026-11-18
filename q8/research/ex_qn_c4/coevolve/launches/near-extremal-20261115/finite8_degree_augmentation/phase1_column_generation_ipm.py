"""Actual small-master lambda-column generation on one frozen maximal scope.
Full alpha/beta stay present. L1 artificial slacks provide a dual even when a
restricted master has no true point. Complete library pricing is not fullQ4NO.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1');os.environ.setdefault('OMP_NUM_THREADS','1')
from pathlib import Path
from math import gcd
import sys,json,time,shutil,hashlib,argparse
P=Path(__file__).resolve().parent;OLD=P/'pool_maximal_vertex_feasibility';R=P/'pool_maximal_phase1_columns_ipm';SRC=P.parent/'finite8_flags';EDGE=P.parent/'finite8_edge_flags';sys.path.insert(0,str(SRC/'deps'));sys.path.insert(0,str(SRC));sys.path.insert(0,str(EDGE));sys.path.insert(0,str(P))
import numpy as np
from scipy import sparse
from scipy.optimize import linprog
import finite_flags as ff,edge_flags
import dynamic_rounding as dr

def pow2(n):return 1<<max(0,(int(n)-1).bit_length())
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--seconds',type=float,default=240);ap.add_argument('--max-masters',type=int,default=100);ap.add_argument('--batch',type=int,default=64);args=ap.parse_args();R.mkdir(exist_ok=True);assert not (R/'STARTED.json').exists()
 for n in ['PROFILE_SNAPSHOT.json','POOL_GRAPH_CODES.json','INTEGER_FEATURES.npz','MARGINAL_FEATURES.npz','ROUNDING_FEATURES.npz','ROUNDING_FAMILY.json','block1.EXACT_SEPARATOR.json','block4.EXACT_SEPARATOR.json','EDGE_U_NUMERATOR.npz','EDGE_GENERATOR_DEDUP_NUMERATOR.npz','EDGE_ENDPOINT_DEDUP.npz','EDGE_DEGREE_PROFILE_RHS_NUMERATOR.npz','GENERATOR_DEDUPLICATION.json','GENERATOR_HISTOGRAMS.json','CONDITIONAL_VERTEX_CUT.json','CONDITIONAL_VERTEX_FEATURES.npz','NEW_CUT_SEED682_CALIBRATION.json','SEED682_JOINT_CALIBRATION.json']:shutil.copyfile(OLD/n,R/n)
 graphs=json.loads((R/'POOL_GRAPH_CODES.json').read_text());index={g:i for i,g in enumerate(graphs)};profiles=json.loads((R/'PROFILE_SNAPSHOT.json').read_text())['remaining'];G=len(graphs);A=len(profiles);F=sparse.load_npz(R/'INTEGER_FEATURES.npz');zz=np.load(R/'MARGINAL_FEATURES.npz');H=zz['hist'];B=zz['profile_hypergeom'];K=zz['kernel_raw'];U=sparse.load_npz(R/'EDGE_U_NUMERATOR.npz');Uc=U.tocsc();Gamma=sparse.load_npz(R/'EDGE_GENERATOR_DEDUP_NUMERATOR.npz');EP=sparse.load_npz(R/'EDGE_ENDPOINT_DEDUP.npz');RHS=sparse.load_npz(R/'EDGE_DEGREE_PROFILE_RHS_NUMERATOR.npz');Nb=Gamma.shape[1];info=json.loads((P/'pool_inventory/LP_STARTED.json').read_text());starts=info['packed_starts'];supports=info['supports'];D=F.shape[1]
 # Full normalized equality map, before selecting lambda columns.
 EL=sparse.vstack([np.ones((1,G)),np.zeros((1,G)),H.T/16,U/129024,sparse.csr_matrix((18,G))],format='csr');ER=sparse.vstack([sparse.csr_matrix((1,A+Nb)),sparse.hstack([np.ones((1,A)),sparse.csr_matrix((1,Nb))]),sparse.hstack([-B.T/8960,sparse.csr_matrix((5,Nb))]),sparse.hstack([sparse.csr_matrix((64,A)),-Gamma/98]),sparse.hstack([-RHS/512,EP])],format='csr');beq=np.r_[1.,1.,np.zeros(87)];neq=len(beq)
 rowmeta=[];features=[];restrows=[];seenpsd=set();roundseen=set()
 def append(v,meta,alpha=None):
  features.append(sparse.csr_matrix((-np.asarray(v)).reshape(1,-1)));restrows.append(sparse.csr_matrix((1,A+Nb)) if alpha is None else sparse.hstack([sparse.csr_matrix((-np.asarray(alpha)).reshape(1,-1)),sparse.csr_matrix((1,Nb))],format='csr'));rowmeta.append(meta)
 def add_psd(b,q,origin):
  q=np.array(q,dtype=np.int64);gg=gcd(*map(abs,map(int,q)))
  if not gg or np.count_nonzero(q)==1:return False
  q=q//gg
  if q[np.argmax(abs(q))]<0:q=-q
  key=(b,tuple(map(int,q)))
  if key in seenpsd:return False
  seenpsd.add(key);norm=pow2(sum(int(v)**2 for v in q));i,j=np.triu_indices(ff.DIMS[b]);coords=np.zeros(D,dtype=np.int64);coords[starts[b]:starts[b+1]]=q[i]*q[j];raw=F@coords;append(raw.astype(float)/(64512*norm),{'kind':'PSD','block':b,'q':q.tolist(),'positive_power2_normalization':norm,'origin':origin});return True
 for ray in json.loads((P/'pool_maximal_union_dynamic/EIGEN_RAYS.json').read_text()):
  b=ray['block'];q=np.zeros(ff.DIMS[b],dtype=np.int64);q[ray['support']]=ray['q'];add_psd(b,q,'retained valid prior')
 def add_round(cut,origin):
  b,q,t=cut['block'],cut['q'],int(cut['t']);finger=dr.key(b,q,t)
  if finger in roundseen:return False
  roundseen.add(finger);coords,ss=dr.full_packed(b,q,t,starts,D);scale=pow2(ss);append((F@coords).astype(float)/(64512*scale),{'kind':'INTEGER_ROUNDING','block':b,'q':list(map(int,q)),'t':t,'n':28 if b==5 else 6,'positive_power2_normalization':scale,'origin':origin});return True
 for cut in json.loads((P/'pool_maximal_union_dynamic/DYNAMIC_ROUNDING_CUTS.json').read_text()):add_round(cut,'retained prior dynamic')
 family=json.loads((R/'ROUNDING_FAMILY.json').read_text())
 for cut in family['cuts']:
  b,bit,t=cut['block'],cut['bit'],cut['t'];add_round({'block':b,'q':dr.BITS[b][:,bit].tolist(),'t':t},'fixed120 family')
 for k,b in enumerate([1,4]):
  data=json.loads((R/f'block{b}.EXACT_SEPARATOR.json').read_text());scale=pow2(max(abs(v) for row in data['full_Q'] for v in row));append(K[:,k].astype(float)/(64512*scale),{'kind':'FINITE6_KERNEL','block':b,'source':f'block{b}.EXACT_SEPARATOR.json','positive_power2_normalization':scale})
 cv=np.load(R/'CONDITIONAL_VERTEX_FEATURES.npz');vc=json.loads((R/'CONDITIONAL_VERTEX_CUT.json').read_text());vscale=pow2(vc['positive_normalization']);append(cv['local_raw'].astype(float)/(64512*vscale),{'kind':'CONDITIONAL_VERTEX','source':'CONDITIONAL_VERTEX_CUT.json','positive_power2_normalization':vscale},cv['profile_bias_raw'].astype(float)/(128*784*vscale))
 # Active seed818 graphs are represented by EXACT equal-feature aliases in
 # the full library, rather than introducing hundreds of redundant columns.
 aliases={}
 for group in json.loads((P/'pool_second_violation/FEATURE_DEDUPLICATION.json').read_text())['groups']:
  rep=min(group)
  for g in group:aliases[g]=rep
 alias_records=[]
 def resolve(g):
  if g in index:return index[g]
  rep=aliases.get(g);assert rep in index,('unrepresented actual initial graph',g)
  eg,er=ff.q4_edges_from_mask(g),ff.q4_edges_from_mask(rep);assert ff.local_coefficients(eg)==ff.local_coefficients(er) and edge_flags.local_coefficients(eg)==edge_flags.local_coefficients(er)
  dg=[sum(x==v or y==v for x,y in eg) for v in range(16)];dd=[sum(x==v or y==v for x,y in er) for v in range(16)];assert sorted(dg)==sorted(dd)
  alias_records.append({'actual_mask':g,'library_equal_feature_mask':rep});return index[rep]
 seed=json.loads((SRC/'Q8_seed682_point.json').read_text());initial={resolve(int(g)) for g,w in seed['graph_distribution']}
 initial|={resolve(int(g)) for g,v in json.loads((P/'pool_edge_degree_dynamic/FLOAT_CANDIDATE.json').read_text())['lambda']}
 for scope in ['pool_second_violation','pool_third_violation','pool_fourth_frequency']:
  for name in ['SECOND_ORACLE_VIOLATOR.json','THIRD_ORACLE_VIOLATOR.json','FOURTH_ORACLE_VIOLATOR.json','OWN_ORACLE_VIOLATOR.json']:
   f=P/scope/name
   if f.exists():initial.add(resolve(int(json.loads(f.read_text())['graph_mask'])))
 # Exact active-feature dedup, with all library columns still priced.
 def fkey(i):
  a,b=F.indptr[i:i+2];u,v=Uc.indptr[i:i+2]
  return (F.indices[a:b].tobytes(),F.data[a:b].tobytes(),H[i].tobytes(),Uc.indices[u:v].tobytes(),Uc.data[u:v].tobytes())
 keys={};active=[]
 for i in sorted(initial):
  key=fkey(i)
  if key not in keys:keys[key]=i;active.append(i)
 (R/'INITIAL_ALIAS_MAP.json').write_text(json.dumps({'seed_actual_types':818,'actual_old_edge_support':len(json.loads((P/'pool_edge_degree_dynamic/FLOAT_CANDIDATE.json').read_text())['lambda']),'aliases_checked_exactly':alias_records,'initial_unique_library_columns':len(active),'full_library_still_priced':G},indent=2)+'\n')
 st=time.monotonic();history=[];outer=0;final={};meta={'scope':'same maximal sixm+V05+all old valid constraints, lambda column generation; L1phaseI artificialslacks numerical only','library':G,'alpha':A,'beta':Nb,'initial_lambda_columns':len(active),'initial_valid_inequalities':len(features),'equalities':neq,'batch':args.batch,'seconds':args.seconds,'max_masters':args.max_masters,'fixed683_density':False,'even_gate':'DROP','positive_row_rescaling':'all homogeneous kernel features use power2normalizations; identical feasible predicate','wiki_actual_read':['ideas/q8-finite-eight-flags.md','claims/q8-maximal-counterexample-cover.md','claims/q8-edge-degree-incidence-bridge.md','claims/q8-vertex-degree-frequency-cone.md'],'V05_specific_actual_fresh_review':'PASS same-family/provisional perRoot; rawreview_cut'}
 (R/'STARTED.json').write_text(json.dumps(meta,indent=2)+'\n');print(json.dumps(meta),flush=True)
 for master in range(args.max_masters):
  if time.monotonic()-st>args.seconds:final={'status':'ACTUAL_WALL_BOUND','masters':master};break
  inds=np.array(active,dtype=np.int64);AL=sparse.vstack(features,format='csr');AR=sparse.vstack(restrows,format='csr');m=AL.shape[0];nreal=len(active)+A+Nb;EE=sparse.hstack([EL[:,inds],ER],format='csr');AA=sparse.hstack([AL[:,inds],AR],format='csr')
  # Always-feasible phaseI: +/- equality slack, nonnegative upper slack.
  ME=sparse.hstack([EE,sparse.eye(neq),-sparse.eye(neq),sparse.csr_matrix((neq,m))],format='csr');MA=sparse.hstack([AA,sparse.csr_matrix((m,2*neq)),-sparse.eye(m)],format='csr');obj=np.r_[np.zeros(nreal),np.ones(2*neq+m)]
  t=time.monotonic();lp=linprog(obj,A_ub=MA,b_ub=np.zeros(m),A_eq=ME,b_eq=beq,bounds=(0,None),method='highs-ipm',options={'time_limit':30,'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9})
  if not lp.success:final={'status':'PHASE1_EXECUTION_STATUS','lp_status':lp.status,'message':lp.message,'master':master,'seconds':time.monotonic()-t};history.append(final);break
  price=-np.asarray(EL.T@lp.eqlin.marginals+AL.T@lp.ineqlin.marginals).ravel();active_set=set(active);new=[]
  if lp.fun>1e-9:
   for i in np.argsort(price):
    if price[i]>=-1e-8:break
    if int(i) in active_set:continue
    key=fkey(int(i))
    if key in keys:continue
    keys[key]=int(i);new.append(int(i));active_set.add(int(i))
    if len(new)>=args.batch:break
   row={'master':master,'outer_check':outer,'phase1_objective':float(lp.fun),'artificial_max':float(max(lp.x[nreal:])),'active_lambda_columns':len(active),'valid_rows':m,'library_min_reduced_cost':float(min(price)),'new_lambda_columns':len(new),'LP_seconds':time.monotonic()-t,'elapsed_seconds':time.monotonic()-st};history.append(row);print(json.dumps(row),flush=True)
   if not new:
    final={'status':'NUMERIC_LIBRARY_DUAL_CANDIDATE','master':master,'phase1_objective':float(lp.fun),'library_min_price':float(min(price)),'equality_duals':lp.eqlin.marginals.tolist(),'inequality_duals':lp.ineqlin.marginals.tolist(),'valid_rows':m,'equalities':neq,'library':G,'exact_full_Q4_separation_done':False};sparse.save_npz(R/'DUAL_EL.npz',EL);sparse.save_npz(R/'DUAL_ER.npz',ER);sparse.save_npz(R/'DUAL_AL.npz',AL);sparse.save_npz(R/'DUAL_AR.npz',AR);break
   active.extend(new)
  else:
   # Real normalized master check, with no artificial slack accepted.
   real=linprog(np.zeros(nreal),A_ub=AA,b_ub=np.zeros(m),A_eq=EE,b_eq=beq,bounds=(0,None),method='highs-ipm',options={'time_limit':30,'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9})
   if not real.success:final={'status':'ZERO_PHASE1_RECHECK_EXECUTION','status_code':real.status,'message':real.message,'master':master};break
   lam=np.zeros(G);lam[inds]=real.x[:len(active)];alpha=real.x[len(active):len(active)+A];beta=real.x[len(active)+A:];pack=np.asarray(F.T@lam)/64512;moments={};mins=[];padded=0
   for b,(d,ss) in enumerate(zip(ff.DIMS,supports)):
    ii=np.array([[starts[b]+min(i,j)*d-min(i,j)*(min(i,j)-1)//2+max(i,j)-min(i,j) for j in ss] for i in ss]);M=pack[ii]*np.array([[1 if i==j else .5 for j in ss] for i in ss]);moments[f'block{b}']=M;ev,v=np.linalg.eigh(M);mins.append(float(ev[0]))
    for k in np.where(ev<-1e-9)[0][:4]:padded+=add_psd(b,np.rint(v[:,k]*10**6).astype(np.int64),{'master':master})
   nd=0
   for fn in [dr.price,dr.price_full_state]:
    dd,vv=fn(moments,F,starts,roundseen,per_block=3)
    # fn inserts its keys; append exact kernels without calling dedup twice.
    for cut in dd:
     b,q,t0=cut['block'],cut['q'],cut['t'];coords,ss=dr.full_packed(b,q,t0,starts,D);scale=pow2(ss);append((F@coords).astype(float)/(64512*scale),{'kind':'INTEGER_ROUNDING','block':b,'q':q,'t':t0,'n':28 if b==5 else 6,'positive_power2_normalization':scale,'origin':{'master':master}});nd+=1
   mixture_m=sum(float(x)*p['m'] for x,p in zip(alpha,profiles));row={'master':master,'outer_check':outer,'phase1_objective':float(lp.fun),'active_lambda_columns':len(active),'valid_rows':m,'block_min_eigenvalues':mins,'PSD_rows_added':padded,'integer_rows_added':nd,'lambda_support':int(sum(lam>1e-12)),'alpha_support':int(sum(alpha>1e-12)),'beta_support':int(sum(beta>1e-12)),'mixture_m':mixture_m,'LP_seconds':time.monotonic()-t,'elapsed_seconds':time.monotonic()-st};history.append(row);print(json.dumps(row),flush=True)
   point={'status':'FLOAT_REAL_MASTER_POINT' if min(mins)>=-1e-10 and nd==0 else 'NONPSD_REAL_MASTER_POINT','master':master,'lambda':[[g,float(x)] for g,x in zip(graphs,lam) if x>1e-12],'alpha':[[i,float(x),profiles[i]['degrees']] for i,x in enumerate(alpha) if x>1e-12],'beta':[[i,float(x)] for i,x in enumerate(beta) if x>1e-12],'block_min_eigenvalues':mins,'mixture_m':mixture_m,'equality_residual_max':float(max(abs(EE@real.x-beq))),'exact_acceptance_done':False,'is_graph':False,'primary683_goal':'OPEN'}
   (R/'FLOAT_CANDIDATE.json').write_text(json.dumps(point,indent=2)+'\n');np.savez_compressed(R/'FLOAT_MOMENTS.npz',**moments);outer+=1
   if point['status']=='FLOAT_REAL_MASTER_POINT':final=point;break
   if not padded and not nd:final={'status':'NO_NEW_NUMERIC_CUT','point':point};break
  (R/'MASTER_HISTORY.json').write_text(json.dumps(history,indent=2)+'\n');(R/'ACTIVE_COLUMNS.json').write_text(json.dumps({'indices':active,'graph_masks':[graphs[i] for i in active]})+'\n');(R/'CUT_ROW_METADATA.json').write_text(json.dumps(rowmeta)+'\n')
 (R/'MASTER_HISTORY.json').write_text(json.dumps(history,indent=2)+'\n');(R/'ACTIVE_COLUMNS.json').write_text(json.dumps({'indices':active,'graph_masks':[graphs[i] for i in active]})+'\n');(R/'CUT_ROW_METADATA.json').write_text(json.dumps(rowmeta)+'\n');(R/'RESULT.json').write_text(json.dumps(final,indent=2)+'\n');print(json.dumps({'final_status':final['status'],'masters':len(history),'seconds':time.monotonic()-st,'scope':'working library only; no fullNO or acceptedgraph'}),flush=True)
if __name__=='__main__':main()
