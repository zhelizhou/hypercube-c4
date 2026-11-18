"""Actual small-master lambda-column generation on one frozen maximal scope.
Full alpha/beta stay present. L1 artificial slacks provide a dual even when a
restricted master has no true point. Complete library pricing is not fullQ4NO.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1');os.environ.setdefault('OMP_NUM_THREADS','1')
from pathlib import Path
from math import gcd
import sys,json,time,shutil,hashlib,argparse
P=Path(__file__).resolve().parent;OLD=P/'pool_maximal_vertex_feasibility';R=P/'pool_native_oracle_extension1';SRC=P.parent/'finite8_flags';EDGE=P.parent/'finite8_edge_flags';sys.path.insert(0,str(SRC/'deps'));sys.path.insert(0,str(SRC));sys.path.insert(0,str(EDGE));sys.path.insert(0,str(P))
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
 st=time.monotonic();history=json.loads((R/'MASTER_HISTORY.json').read_text()) if resume else [];outer=0;final={};AL=sparse.vstack(features,format='csr');AR=sparse.vstack(restrows,format='csr');m=AL.shape[0];inds=np.array(active,dtype=np.int64);nreal=len(active)+A+Nb
 EE=sparse.hstack([EL[:,inds],ER],format='csr');AA=sparse.hstack([AL[:,inds],AR],format='csr')
 ME=sparse.hstack([EE,sparse.eye(neq),-sparse.eye(neq),sparse.csr_matrix((neq,m))],format='csr');MA=sparse.hstack([AA,sparse.csr_matrix((m,2*neq)),-sparse.eye(m)],format='csr');MAT=sparse.vstack([ME,MA],format='csc');cost=np.r_[np.zeros(nreal),np.ones(2*neq+m)];ncol=len(cost)
 # Column maps stay explicit as lambda columns and artificial rows are appended.
 lambda_cols={i:k for k,i in enumerate(active)};alpha_cols=np.arange(len(active),len(active)+A);beta_cols=np.arange(len(active)+A,nreal);artcols=list(range(nreal,ncol))
 if resume:
  maps=json.loads((R/'NATIVE_COLUMN_MAP.json').read_text());lambda_cols={int(i):j for i,j in maps['lambda'].items()};alpha_cols=np.array(maps['alpha']);beta_cols=np.array(maps['beta']);artcols=maps['artificial'];ncol=max(list(lambda_cols.values())+alpha_cols.tolist()+beta_cols.tolist()+artcols)+1
  assert len(artcols)==2*neq+m
  colmap=np.array([lambda_cols[i] for i in active]+alpha_cols.tolist()+beta_cols.tolist());realmat=sparse.vstack([EE,AA],format='coo');rr=realmat.row.tolist();cc=colmap[realmat.col].tolist();vv=realmat.data.tolist()
  for k in range(neq):rr.extend([k,k]);cc.extend([artcols[k],artcols[neq+k]]);vv.extend([1.,-1.])
  for k in range(m):rr.append(neq+k);cc.append(artcols[2*neq+k]);vv.append(-1.)
  MAT=sparse.csc_matrix((vv,(rr,cc)),shape=(neq+m,ncol));cost=np.zeros(ncol);cost[artcols]=1
 lp=hs.HighsLp();lp.num_col_=ncol;lp.num_row_=neq+m;lp.col_cost_=cost;lp.col_lower_=np.zeros(ncol);lp.col_upper_=np.full(ncol,hs.kHighsInf);lp.row_lower_=np.r_[beq,np.full(m,-hs.kHighsInf)];lp.row_upper_=np.r_[beq,np.zeros(m)];lp.a_matrix_.format_=hs.MatrixFormat.kColwise;lp.a_matrix_.start_=MAT.indptr.astype(np.int32);lp.a_matrix_.index_=MAT.indices.astype(np.int32);lp.a_matrix_.value_=MAT.data
 h=hs.Highs();h.setOptionValue('output_flag',True);h.setOptionValue('log_file',str(R/'highs.log'));h.setOptionValue('threads',1);h.setOptionValue('solver','simplex');h.setOptionValue('simplex_strategy',4);h.setOptionValue('presolve','off');h.setOptionValue('primal_feasibility_tolerance',1e-9);h.setOptionValue('dual_feasibility_tolerance',1e-7);h.setOptionValue('time_limit',30.);h.setOptionValue('small_matrix_value',1e-12);passed=h.passModel(lp);print('PASS_MODEL_STATUS',str(passed),flush=True);assert passed!=hs.HighsStatus.kError
 meta={'scope':'maximal m683..688 shared lambda alpha beta, L1 artificial phaseI with native reusable basis','library':G,'alpha':A,'beta':Nb,'initial_lambda_columns':len(active),'initial_valid_inequalities':m,'equalities':neq,'new_gates':['global leaf N1<=N8','230 raw retained leaf hist forbidden','2 connector finite6','9 retained neighbor degree capacities'],'V05':'freshPASS same-family/provisional','even_gate':'DROP','fixed683density':False,'old23exclusions':'not applied','initialization':'explicit feasible artificial basis or actual full native checkpoint; no crossover','seconds':args.seconds,'batch':args.batch,'full_library_priced':True,'fullQ4NO':False}
 (R/('CONTINUED.json' if resume else 'STARTED.json')).write_text(json.dumps(meta,indent=2)+'\n');print(json.dumps(meta),flush=True)
 # Restore the actual appended-column/row basis by index. Its file names
 # can differ after native addRows; positions are pinned by NATIVE_COLUMN_MAP.
 if resume:
  lines=(R/'checkpoint.bas').read_text().splitlines();k=lines.index(next(x for x in lines if x.startswith('# Columns ')));nc=int(lines[k].split()[-1]);cv=[hs.HighsBasisStatus(int(x.split()[-1])) for x in lines[k+1:k+1+nc]];k=lines.index(next(x for x in lines if x.startswith('# Rows ')));nr=int(lines[k].split()[-1]);rv=[hs.HighsBasisStatus(int(x.split()[-1])) for x in lines[k+1:k+1+nr]];assert nc==ncol and nr==neq+m
  basis=hs.HighsBasis();basis.col_status=cv;basis.row_status=rv;basis.valid=True;assert h.setBasis(basis)!=hs.HighsStatus.kError;print('RESTORED_FULL_NATIVE_CHECKPOINT',nc,nr,flush=True)
 else:
  basis=hs.HighsBasis();cb=[hs.HighsBasisStatus.kLower]*ncol;rb=[hs.HighsBasisStatus.kUpper]*(neq+m)
  for k in range(neq):cb[nreal+k]=hs.HighsBasisStatus.kBasic
  for k in range(m):cb[nreal+2*neq+k]=hs.HighsBasisStatus.kBasic
  basis.col_status=cb;basis.row_status=rb;basis.valid=True;assert h.setBasis(basis)!=hs.HighsStatus.kError
 def checkpoint():
  (R/'MASTER_HISTORY.json').write_text(json.dumps(history,indent=2)+'\n');(R/'ACTIVE_COLUMNS.json').write_text(json.dumps({'indices':active,'graph_masks':[graphs[i] for i in active],'native_column_map':{str(i):j for i,j in lambda_cols.items()}})+'\n');(R/'CUT_ROW_METADATA.json').write_text(json.dumps(rowmeta)+'\n');(R/'NATIVE_COLUMN_MAP.json').write_text(json.dumps({'lambda':lambda_cols,'alpha':alpha_cols.tolist(),'beta':beta_cols.tolist(),'artificial':artcols})+'\n');h.writeBasis(str(R/'checkpoint.bas'));h.writeModel(str(R/'checkpoint.mps'))
 startmaster=max([z.get('master',-1) for z in history]+[-1])+1
 for master in range(startmaster,startmaster+args.max_masters):
  if time.monotonic()-st>args.seconds:final={'status':'ACTUAL_WALL_BOUND','master':master};break
  h.setOptionValue('time_limit',h.getRunTime()+min(30.,max(1.,args.seconds-(time.monotonic()-st))));tt=time.monotonic();run=h.run();status=h.getModelStatus();ss=h.getSolution();inf=h.getInfo()
  if status!=hs.HighsModelStatus.kOptimal:
   # A phaseI primal with zero artificial slack can be checked without any
   # dual. Positive phaseI requires an optimal dual for library pricing.
   sx=np.asarray(ss.col_value);sl=np.zeros(G)
   for i,c in lambda_cols.items():sl[i]=sx[c]
   sr=np.r_[sx[alpha_cols],sx[beta_cols]];er=float(max(abs(EL@sl+ER@sr-beq)));av=float(max(AL@sl+AR@sr));am=float(max(abs(sx[artcols])));mn=float(min(sx))
   diag={'model_status':str(status),'eqres':er,'ineqviol':av,'artificial_max':am,'minimum_variable':mn,'objective':float(inf.objective_function_value),'master':master}
   (R/f'NONOPTIMAL_CHECK_{master:03d}.json').write_text(json.dumps(diag,indent=2)+'\n');print(json.dumps({'nonoptimal_primal_check':diag}),flush=True)
   if er>=1e-7 or av>=1e-7 or am>=1e-8 or mn< -1e-8:
    final={'status':'NATIVE_EXECUTION_STATUS','diagnostic':diag,'seconds':time.monotonic()-tt,'primal_status':inf.primal_solution_status,'dual_status':inf.dual_solution_status,'simplex_iteration_count':inf.simplex_iteration_count};history.append(final);np.savez_compressed(R/'LAST_NATIVE_NONOPTIMAL.npz',x=sx,row_duals=np.asarray(ss.row_dual));checkpoint();break
  x=np.asarray(ss.col_value);dual=np.asarray(ss.row_dual);obj=0. if status!=hs.HighsModelStatus.kOptimal else float(inf.objective_function_value);price=-np.asarray(EL.T@dual[:neq]+AL.T@dual[neq:]).ravel();new=[];aset=set(active)
  if obj>1e-9:
   for i in np.argsort(price):
    if price[i]>=-1e-8:break
    i=int(i)
    if i in aset:continue
    key=fkey(i)
    if key in keys:continue
    keys[key]=i;new.append(i);aset.add(i)
    if len(new)>=args.batch:break
   row={'master':master,'phase1_objective':obj,'library_min_reduced_cost':float(min(price)),'new_lambda_columns':len(new),'active_lambda_columns':len(active),'valid_rows':m,'LP_seconds':time.monotonic()-tt,'elapsed_seconds':time.monotonic()-st,'simplex_iterations':inf.simplex_iteration_count};history.append(row);print(json.dumps(row),flush=True)
   if not new:
    final={'status':'NUMERIC_LIBRARY_DUAL_CANDIDATE','phase1_objective':obj,'library_min_price':float(min(price)),'equality_duals':dual[:neq].tolist(),'inequality_duals':dual[neq:].tolist(),'master':master,'no_fullQ4_separation':True};sparse.save_npz(R/'DUAL_EL.npz',EL);sparse.save_npz(R/'DUAL_ER.npz',ER);sparse.save_npz(R/'DUAL_AL.npz',AL);sparse.save_npz(R/'DUAL_AR.npz',AR);checkpoint();break
   block=sparse.vstack([EL[:,new],AL[:,new]],format='csc');start=h.getNumCol();assert h.addCols(len(new),np.zeros(len(new)),np.zeros(len(new)),np.full(len(new),hs.kHighsInf),block.nnz,block.indptr.astype(np.int32),block.indices.astype(np.int32),block.data)!=hs.HighsStatus.kError
   for k,i in enumerate(new):lambda_cols[i]=start+k
   active.extend(new)
  else:
   lam=np.zeros(G)
   for i,c in lambda_cols.items():lam[i]=x[c]
   alpha=x[alpha_cols];beta=x[beta_cols];realrest=np.r_[alpha,beta];res=EL@lam+ER@realrest-beq;viol=AL@lam+AR@realrest;assert max(abs(res))<1e-7 and max(viol)<1e-7,('zero phase check',max(abs(res)),max(viol));pack=np.asarray(F.T@lam)/64512;moments={};mins=[];before=len(features);padded=0
   for b,(d,support) in enumerate(zip(ff.DIMS,supports)):
    ii=np.array([[starts[b]+min(i,j)*d-min(i,j)*(min(i,j)-1)//2+max(i,j)-min(i,j) for j in support] for i in support]);M=pack[ii]*np.array([[1 if i==j else .5 for j in support] for i in support]);moments[f'block{b}']=M;ev,v=np.linalg.eigh(M);mins.append(float(ev[0]))
    for k in np.where(ev<-1e-9)[0][:4]:padded+=add_psd(b,np.rint(v[:,k]*10**6).astype(np.int64),{'native_master':master})
   nd=0
   for fn in [dr.price,dr.price_full_state]:
    dd,vv=fn(moments,F,starts,roundseen,per_block=3)
    for cut in dd:
     b,q,t0=cut['block'],cut['q'],cut['t'];coords,scale0=dr.full_packed(b,q,t0,starts,D);scale=pow2(scale0);append((F@coords).astype(float)/(64512*scale),{'kind':'INTEGER_ROUNDING','block':b,'q':q,'t':t0,'n':28 if b==5 else 6,'positive_power2_normalization':scale,'origin':{'native_master':master}});nd+=1
   mm=sum(float(w)*p['m'] for w,p in zip(alpha,profiles));record={'master':master,'phase1_objective':obj,'active_lambda_columns':len(active),'valid_rows':m,'block_min_eigenvalues':mins,'PSD_rows_added':padded,'integer_rows_added':nd,'lambda_support':int(sum(lam>1e-12)),'alpha_support':int(sum(alpha>1e-12)),'beta_support':int(sum(beta>1e-12)),'mixture_m':mm,'LP_seconds':time.monotonic()-tt,'elapsed_seconds':time.monotonic()-st,'simplex_iterations':inf.simplex_iteration_count};history.append(record);print(json.dumps(record),flush=True)
   point={'status':'FLOAT_REAL_MASTER_POINT' if min(mins)>=-1e-10 and nd==0 else 'NONPSD_REAL_MASTER_POINT','master':master,'lambda':[[g,float(w)] for g,w in zip(graphs,lam) if w>1e-12],'alpha':[[i,float(w),profiles[i]['degrees']] for i,w in enumerate(alpha) if w>1e-12],'beta':[[i,float(w)] for i,w in enumerate(beta) if w>1e-12],'block_min_eigenvalues':mins,'mixture_m':mm,'equality_residual_max':float(max(abs(res))),'inequality_violation_max':float(max(viol)),'leaf_slack':float(leaf['leaf_alpha_lower']@alpha),'exact_acceptance_done':False,'is_graph':False,'primary683_goal':'OPEN'}
   (R/'point_bank').mkdir(exist_ok=True);(R/'point_bank'/f'master_{master:03d}.json').write_text(json.dumps(point,indent=2)+'\n');(R/'FLOAT_CANDIDATE.json').write_text(json.dumps(point,indent=2)+'\n');np.savez_compressed(R/'FLOAT_MOMENTS.npz',**moments);outer+=1
   if point['status']=='FLOAT_REAL_MASTER_POINT':final=point;checkpoint();break
   added=len(features)-before
   if not added:final={'status':'NO_NEW_NUMERIC_CUT','point':point};checkpoint();break
   # Append violated valid rows and their artificial slack. All old basis
   # columns retain their identities. The new artificial is explicitly basic.
   AL=sparse.vstack(features,format='csr');AR=sparse.vstack(restrows,format='csr');basis=h.getBasis();oldn=h.getNumCol();oldm=h.getNumRow();assert h.addCols(added,np.ones(added),np.zeros(added),np.full(added,hs.kHighsInf),0,np.zeros(added+1,dtype=np.int32),np.array([],dtype=np.int32),np.array([],dtype=float))!=hs.HighsStatus.kError
   rr=[]
   for k in range(added):
    vec=sparse.lil_matrix((1,h.getNumCol()))
    for i,c in lambda_cols.items():
     value=AL[before+k,i]
     if value:vec[0,c]=value
    vec[0,alpha_cols]=AR[before+k,:A];vec[0,beta_cols]=AR[before+k,A:];vec[0,oldn+k]=-1;rr.append(vec.tocsr())
   rows=sparse.vstack(rr,format='csr');assert h.addRows(added,np.full(added,-hs.kHighsInf),np.zeros(added),rows.nnz,rows.indptr.astype(np.int32),rows.indices.astype(np.int32),rows.data)!=hs.HighsStatus.kError
   cb=list(basis.col_status)+[hs.HighsBasisStatus.kBasic]*added;rb=list(basis.row_status)+[hs.HighsBasisStatus.kUpper]*added;basis.col_status=cb;basis.row_status=rb;basis.valid=True;h.setBasis(basis);artcols.extend(range(oldn,oldn+added));m+=added
  checkpoint()
 checkpoint();(R/'RESULT.json').write_text(json.dumps(final,indent=2)+'\n');print(json.dumps({'final_status':final.get('status'),'masters':len(history),'seconds':time.monotonic()-st,'scope':'working library numerical only, no graph/fullNO'}),flush=True)
if __name__=='__main__':main()
