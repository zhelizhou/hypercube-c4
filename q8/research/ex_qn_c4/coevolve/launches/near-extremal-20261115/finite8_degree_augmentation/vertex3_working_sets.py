"""Two working sets, one unchanged mathematical relaxation.
Every omitted stored valid row remains in the full checker; a phase0 tuple
is not a real point for the stored scope until those rows and signs pass.
"""
from pathlib import Path
import shutil
P=Path(__file__).resolve().parent;OLD=P/'pool_dual_working_sets';NEW=P/'pool_vertex3_working_sets'
if not NEW.exists():
 NEW.mkdir()
 for f in OLD.iterdir():
  if f.suffix in ['.npz','.json'] and not f.name.startswith(('DUAL_','RESULT','NONOPTIMAL','LAST_NATIVE')) and f.name not in ['FLOAT_CANDIDATE.json','FLOAT_MOMENTS.npz','MASTER_HISTORY.json','STARTED.json','CONTINUED.json','INITIAL_ALIAS_MAP.json','INITIAL_BASIS.json']:shutil.copyfile(f,NEW/f.name)
 (NEW/'STARTED.json').write_text('{"scope":"same full stored model; cold IPM two working sets","preparation_only":true}\n')
# Reuse the actual source construction, alias checks and integer row builders;
# its local functions remain in this main code by source generation below.

"""Actual small-master lambda-column generation on one frozen maximal scope.
Full alpha/beta stay present. L1 artificial slacks provide a dual even when a
restricted master has no true point. Complete library pricing is not fullQ4NO.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1');os.environ.setdefault('OMP_NUM_THREADS','1')
from pathlib import Path
from math import gcd
import sys,json,time,shutil,hashlib,argparse
P=Path(__file__).resolve().parent;OLD=P/'pool_maximal_vertex_feasibility';R=P/'pool_vertex3_working_sets';SRC=P.parent/'finite8_flags';EDGE=P.parent/'finite8_edge_flags';sys.path.insert(0,str(SRC/'deps'));sys.path.insert(0,str(SRC));sys.path.insert(0,str(EDGE));sys.path.insert(0,str(P))
import numpy as np
from scipy import sparse
import highspy as hs
import finite_flags as ff,edge_flags
import dynamic_rounding as dr

def pow2(n):return 1<<max(0,(int(n)-1).bit_length())
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--seconds',type=float,default=240);ap.add_argument('--max-masters',type=int,default=100);ap.add_argument('--batch',type=int,default=64);args=ap.parse_args();R.mkdir(exist_ok=True);resume=(R/'STARTED.json').exists()
 graphs=json.loads((R/'POOL_GRAPH_CODES.json').read_text());index={g:i for i,g in enumerate(graphs)};profiles=json.loads((R/'PROFILE_SNAPSHOT.json').read_text())['remaining'];G=len(graphs);A=len(profiles);F=sparse.load_npz(R/'INTEGER_FEATURES.npz');zz=np.load(R/'MARGINAL_FEATURES.npz');H=zz['hist'];B=zz['profile_hypergeom'];K=zz['kernel_raw'];U=sparse.load_npz(R/'EDGE_U_NUMERATOR.npz');Uc=U.tocsc();Gamma=sparse.load_npz(R/'EDGE_GENERATOR_DEDUP_NUMERATOR.npz');EP=sparse.load_npz(R/'EDGE_ENDPOINT_DEDUP.npz');RHS=sparse.load_npz(R/'EDGE_DEGREE_PROFILE_RHS_NUMERATOR.npz');Nb=Gamma.shape[1];info=json.loads((P/'pool_inventory/LP_STARTED.json').read_text());starts=info['packed_starts'];supports=info['supports'];D=F.shape[1]
 # Full normalized equality map, before selecting lambda columns.
 EL=sparse.vstack([np.ones((1,G)),np.zeros((1,G)),H.T/16,U/129024,sparse.csr_matrix((18,G))],format='csr');ER=sparse.vstack([sparse.csr_matrix((1,A+Nb)),sparse.hstack([np.ones((1,A)),sparse.csr_matrix((1,Nb))]),sparse.hstack([-B.T/8960,sparse.csr_matrix((5,Nb))]),sparse.hstack([sparse.csr_matrix((64,A)),-Gamma/98]),sparse.hstack([-RHS/512,EP])],format='csr');beq=np.r_[1.,1.,np.zeros(87)];neq=len(beq)
 rowmeta=[];features=[];restrows=[];seenpsd=set();roundseen=set()
 def append(v,meta,alpha=None,beta=None):
  features.append(sparse.csr_matrix((-np.asarray(v)).reshape(1,-1)))
  aa=np.zeros(A) if alpha is None else np.asarray(alpha);bb=np.zeros(Nb) if beta is None else np.asarray(beta)
  restrows.append(sparse.csr_matrix(-np.r_[aa,bb].reshape(1,-1)));rowmeta.append(meta)
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
 # Genuine new gates, all on the same lambda/alpha/beta.
 con=np.load(R/'CONNECTOR_FEATURES.npz')
 for k,b in enumerate([0,4]):
  scale=pow2(con['scales'][k]);append(con['raw'][:,k]/(64512*scale),{'kind':'CONNECTOR_FINITE6','block':b,'positive_power2_normalization':scale,'source':'CONNECTOR_CUTS.json'})
 leaf=np.load(R/'LEAF_NEIGHBOR_FEATURES.npz')
 append(np.zeros(G),{'kind':'GLOBAL_MAXIMAL_LEAF','formula':'N1<=N8','positive_normalization':1},leaf['leaf_alpha_lower'])
 for t in range(9):append(np.zeros(G),{'kind':'RETAINED_NEIGHBOR_DEGREE_CAPACITY','degree':t,'positive_normalization':16},leaf['neighbor_alpha_upper_numerator'][t]/(512*16),-leaf['neighbor_beta_upper'][t]/16)
 # Preserve all valid later rows from the preceding IPM checkpoint.
 for row in json.loads((P/'pool_maximal_phase1_columns_ipm/CUT_ROW_METADATA.json').read_text()):
  if row['kind']=='PSD':add_psd(row['block'],row['q'],'prior phaseI actual row')
  elif row['kind']=='INTEGER_ROUNDING':add_round(row,'prior phaseI actual row')
 # On continuation reconstruct every actual appended valid row in order.
 if resume:
  for row in json.loads((R/'CUT_ROW_METADATA.json').read_text()):
   if row['kind']=='PSD':add_psd(row['block'],row['q'],row.get('origin','continued'))
   elif row['kind']=='INTEGER_ROUNDING':add_round(row,row.get('origin','continued'))
   elif row['kind']=='CONDITIONAL_VERTEX_EXTRA':
    zz=np.load(R/row['feature_source']);sc=row['positive_power2_normalization'];append(zz['local_raw']/(64512*sc),row,zz['profile_bias_raw']/(128*784*sc))
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
 initial|=set(json.loads((P/'pool_maximal_phase1_columns_ipm/ACTIVE_COLUMNS.json').read_text())['indices'])
 # Exact active-feature dedup, with all library columns still priced.
 def fkey(i):
  a,b=F.indptr[i:i+2];u,v=Uc.indptr[i:i+2]
  return (F.indices[a:b].tobytes(),F.data[a:b].tobytes(),H[i].tobytes(),Uc.indices[u:v].tobytes(),Uc.data[u:v].tobytes())
 keys={};active=[]
 for i in sorted(initial):
  key=fkey(i)
  if key not in keys:keys[key]=i;active.append(i)
 if resume:
  active=json.loads((R/'ACTIVE_COLUMNS.json').read_text())['indices'];keys={fkey(i):i for i in active}
 (R/'INITIAL_ALIAS_MAP.json').write_text(json.dumps({'seed_actual_types':818,'actual_old_edge_support':len(json.loads((P/'pool_edge_degree_dynamic/FLOAT_CANDIDATE.json').read_text())['lambda']),'aliases_checked_exactly':alias_records,'initial_unique_library_columns':len(active),'full_library_still_priced':G},indent=2)+'\n')
 st=time.monotonic();history=json.loads((R/'MASTER_HISTORY.json').read_text()) if (R/'MASTER_HISTORY.json').exists() else [];final={};structural={i for i,r in enumerate(rowmeta) if r['kind'] not in ['PSD','INTEGER_ROUNDING']};olddual=json.loads((P/'pool_native_leaf_simplex/RESULT.json').read_text())['inequality_duals'];selected=set(structural)|{i for i,v in enumerate(olddual) if abs(v)>1e-10}|set(range(max(0,len(features)-64),len(features)));recent=list(sorted(selected));mfull=len(features);fullAL=sparse.vstack(features,format='csr');fullAR=sparse.vstack(restrows,format='csr');pointcount=0
 runmeta={'scope':'same full maximal sixm+leaf+connector+two vertex kernels; dual lambda/cut working sets','library':G,'alpha':A,'beta':Nb,'initial_active_lambda':len(active),'full_stored_valid_rows':len(features),'initial_active_valid_rows':len(selected),'full_oldcut_check_before_PSD':True,'inactive_dual_rows':'zero, so weak-model exactNO would still suffice','solver':'native Highs IPM, crossover off','cold_masters':True,'seconds':args.seconds,'fixed683density':False,'even_gate':'DROP','primary_goal':'OPEN'};(R/('RUN_CONTINUED.json' if history else 'RUN_STARTED.json')).write_text(json.dumps(runmeta,indent=2)+'\n');print(json.dumps(runmeta),flush=True)
 def checkpoint():
  (R/'MASTER_HISTORY.json').write_text(json.dumps(history,indent=2)+'\n');(R/'ACTIVE_COLUMNS.json').write_text(json.dumps({'indices':active,'graph_masks':[graphs[i] for i in active]})+'\n');(R/'CUT_ROW_METADATA.json').write_text(json.dumps(rowmeta)+'\n');(R/'ACTIVE_CUT_ROWS.json').write_text(json.dumps(sorted(selected))+'\n')
 startmaster=max([z.get('master',-1) for z in history]+[-1])+1
 for master in range(startmaster,startmaster+args.max_masters):
  if time.monotonic()-st>=args.seconds:final={'status':'ACTUAL_WALL_BOUND','master':master};break
  inds=np.array(active,dtype=np.int64);sel=np.array(sorted(selected),dtype=np.int64);AL=fullAL[sel];AR=fullAR[sel];m=len(sel);nreal=len(active)+A+Nb;EE=sparse.hstack([EL[:,inds],ER],format='csr');AA=sparse.hstack([AL[:,inds],AR],format='csr');ME=sparse.hstack([EE,sparse.eye(neq),-sparse.eye(neq),sparse.csr_matrix((neq,m))],format='csr');MA=sparse.hstack([AA,sparse.csr_matrix((m,2*neq)),-sparse.eye(m)],format='csr');MAT=sparse.vstack([ME,MA],format='csc');cost=np.r_[np.zeros(nreal),np.ones(2*neq+m)];nc=len(cost)
  lp=hs.HighsLp();lp.num_col_=nc;lp.num_row_=neq+m;lp.col_cost_=cost;lp.col_lower_=np.zeros(nc);lp.col_upper_=np.full(nc,hs.kHighsInf);lp.row_lower_=np.r_[beq,np.full(m,-hs.kHighsInf)];lp.row_upper_=np.r_[beq,np.zeros(m)];lp.a_matrix_.format_=hs.MatrixFormat.kColwise;lp.a_matrix_.start_=MAT.indptr.astype(np.int32);lp.a_matrix_.index_=MAT.indices.astype(np.int32);lp.a_matrix_.value_=MAT.data
  h=hs.Highs();h.setOptionValue('output_flag',False);h.setOptionValue('threads',1);h.setOptionValue('solver','ipm');h.setOptionValue('run_crossover','off');h.setOptionValue('presolve','on');h.setOptionValue('small_matrix_value',1e-12);h.setOptionValue('ipm_optimality_tolerance',1e-10);h.setOptionValue('primal_feasibility_tolerance',1e-9);h.setOptionValue('dual_feasibility_tolerance',1e-9);h.setOptionValue('time_limit',min(25.,max(1.,args.seconds-(time.monotonic()-st))));assert h.passModel(lp)!=hs.HighsStatus.kError;tt=time.monotonic();rr=h.run();status=h.getModelStatus();sol=h.getSolution();inf=h.getInfo();xs=np.asarray(sol.col_value);duals=np.asarray(sol.row_dual)
  if not sol.value_valid or len(xs)!=nc:
   final={'status':'IPM_EXECUTION_NO_POINT','model_status':str(status),'master':master,'seconds':time.monotonic()-tt};history.append(final);break
  x=xs[:nreal];obj=float(cost@xs);maxart=float(max(abs(xs[nreal:])));sumart=float(sum(np.maximum(xs[nreal:],0)));er=float(max(abs(EE@x-beq)));av=float(max(AA@x));mn=float(min(x));base={'master':master,'phase1_objective':obj,'sum_positive_artificial':sumart,'max_absolute_artificial':maxart,'minimum_real_variable':mn,'equality_residual_max':er,'active_inequality_violation_max':av,'active_lambda':len(active),'active_cuts':m,'full_stored_cuts':len(features),'LP_seconds':time.monotonic()-tt,'elapsed_seconds':time.monotonic()-st,'model_status':str(status)}
  if obj>1e-8 and status==hs.HighsModelStatus.kOptimal:
   y=duals[:neq];za=duals[neq:];price=-np.asarray(EL.T@y+AL.T@za).ravel();new=[];aset=set(active)
   for i in np.argsort(price):
    if price[i]>=-1e-8:break
    i=int(i)
    if i in aset:continue
    key=fkey(i)
    if key in keys:continue
    keys[key]=i;new.append(i);aset.add(i)
    if len(new)>=args.batch:break
   base.update({'library_min_reduced_cost':float(min(price)),'new_lambda_columns':len(new)});history.append(base);print(json.dumps(base),flush=True)
   if not new:
    zfull=np.zeros(len(features));zfull[sel]=za;final={'status':'NUMERIC_LIBRARY_DUAL_CANDIDATE','master':master,'phase1_objective':obj,'library_min_price':float(min(price)),'equality_duals':y.tolist(),'inequality_duals':zfull.tolist(),'active_rows':sel.tolist(),'inactive_dual_zero':True,'fullQ4_checked':False};sparse.save_npz(R/'DUAL_EL.npz',EL);sparse.save_npz(R/'DUAL_ER.npz',ER);sparse.save_npz(R/'DUAL_AL.npz',fullAL);sparse.save_npz(R/'DUAL_AR.npz',fullAR);checkpoint();break
   active.extend(new);checkpoint();continue
  if maxart>=1e-8 or er>=1e-8 or av>=1e-8 or mn< -1e-10:
   final={'status':'IPM_REAL_PRIMAL_CHECK_REJECTED','diagnostic':base};history.append(base);print(json.dumps(final),flush=True);np.savez_compressed(R/'LAST_REJECTED_IPM.npz',x=xs,rowduals=duals);checkpoint();break
  # Before matrix work, the same actual tuple must satisfy EVERY old cut.
  lam=np.zeros(G);lam[inds]=x[:len(active)];alpha=x[len(active):len(active)+A];beta=x[len(active)+A:];rest=np.r_[alpha,beta];allviol=np.asarray(fullAL@lam+fullAR@rest).ravel();bad=np.where(allviol>1e-8)[0];base['full_stored_inequality_violation_max']=float(max(allviol))
  if len(bad):
   add=sorted(bad,key=lambda i:allviol[i],reverse=True)[:64];selected.update(map(int,add));recent.extend(map(int,add));base.update({'status':'INACTIVE_STORED_CUT_VIOLATION','old_rows_reactivated':len(add)});history.append(base);print(json.dumps(base),flush=True);checkpoint();continue
  pack=np.asarray(F.T@lam)/64512;moments={};mins=[];before=len(features);nPSD=0;nd=0
  for b,(d,support) in enumerate(zip(ff.DIMS,supports)):
   ii=np.array([[starts[b]+min(i,j)*d-min(i,j)*(min(i,j)-1)//2+max(i,j)-min(i,j) for j in support] for i in support]);M=pack[ii]*np.array([[1 if i==j else .5 for j in support] for i in support]);moments[f'block{b}']=M;ev,v=np.linalg.eigh(M);mins.append(float(ev[0]))
   for k in np.where(ev< -1e-9)[0][:4]:nPSD+=add_psd(b,np.rint(v[:,k]*10**6).astype(np.int64),{'dual_working_master':master})
  for fn in [dr.price,dr.price_full_state]:
   dd,unused=fn(moments,F,starts,roundseen,per_block=3)
   for cut in dd:
    b,q,t0=cut['block'],cut['q'],cut['t'];coords,sc=dr.full_packed(b,q,t0,starts,D);sc=pow2(sc);append((F@coords)/(64512*sc),{'kind':'INTEGER_ROUNDING','block':b,'q':q,'t':t0,'n':28 if b==5 else 6,'positive_power2_normalization':sc,'origin':{'dual_working_master':master}});nd+=1
  mm=sum(float(v)*p['m'] for v,p in zip(alpha,profiles));base.update({'status':'FULL_STORED_SCOPE_FLOAT_POINT_NONPSD' if min(mins)< -1e-10 else 'FULL_STORED_SCOPE_FLOAT_POINT','block_min_eigenvalues':mins,'PSD_rows_added':nPSD,'integer_rows_added':nd,'lambda_support':int(sum(lam>1e-12)),'alpha_support':int(sum(alpha>1e-12)),'beta_support':int(sum(beta>1e-12)),'mixture_m':mm});history.append(base);print(json.dumps(base),flush=True)
  point={'status':base['status'],'master':master,'lambda':[[g,float(v)] for g,v in zip(graphs,lam) if v>1e-12],'alpha':[[i,float(v),profiles[i]['degrees']] for i,v in enumerate(alpha) if v>1e-12],'beta':[[i,float(v)] for i,v in enumerate(beta) if v>1e-12],'block_min_eigenvalues':mins,'mixture_m':mm,'minimum_variable':mn,'equality_residual_max':er,'all_stored_cut_violation_max':float(max(allviol)),'actual_full_stored_cuts_checked':before,'exact_acceptance_done':False,'is_graph':False,'primary_goal':'OPEN'};(R/'point_bank').mkdir(exist_ok=True);(R/'point_bank'/f'master_{master:03d}.json').write_text(json.dumps(point,indent=2)+'\n');(R/'FLOAT_CANDIDATE.json').write_text(json.dumps(point,indent=2)+'\n');np.savez_compressed(R/'FLOAT_MOMENTS.npz',**moments);pointcount+=1
  if min(mins)>=-1e-10 and nd==0:final=point;checkpoint();break
  if len(features)==before:final={'status':'NO_NEW_GENUINE_KERNEL','point':point};checkpoint();break
  selected.update(range(before,len(features)));recent.extend(range(before,len(features)));fullAL=sparse.vstack(features,format='csr');fullAR=sparse.vstack(restrows,format='csr')
  if len(selected)>550:
   nz={int(i) for i,v in zip(sel,duals[neq:]) if abs(v)>1e-10};selected=set(structural)|nz|set(recent[-256:]);base['active_cut_prune_after_full_check']=len(selected)
  checkpoint()
 if not final:final={'status':'ACTUAL_ITERATION_BOUND','masters_total':len(history),'full_stored_scope_points_this_attempt':pointcount}
 checkpoint();(R/'RESULT.json').write_text(json.dumps(final,indent=2)+'\n');print(json.dumps({'final_status':final.get('status'),'masters':len(history),'full_stored_scope_points':pointcount,'seconds':time.monotonic()-st,'no_fullNO_or_graph':True}),flush=True)
if __name__=='__main__':main()
