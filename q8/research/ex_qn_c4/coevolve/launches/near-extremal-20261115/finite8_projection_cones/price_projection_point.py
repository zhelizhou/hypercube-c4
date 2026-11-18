"""Bounded small-alphabet finite-six discovery. All output stays in OUTPUT_DIR."""
from pathlib import Path
from fractions import Fraction as F
from math import lcm, comb
from collections import Counter
import argparse, json, sys, hashlib, shutil, time
sys.dont_write_bytecode=True
BASE=Path(__file__).resolve().parent.parent
sys.path[:0]=[str(BASE/'finite8_flags/deps'),str(BASE/'finite8_flags'),str(BASE/'finite8_connector_frequency')]
import numpy as np
from scipy.optimize import linprog
import finite_flags as ff
from membership import load_domain

def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,d): p.write_text(json.dumps(d,indent=2)+'\n')
def mappings(mode,path=None):
 codes=[sorted(s) for s in ff.STATE_IDS]
 if mode=='parallel15': return 15,[[f>>4 for f in c] for c in codes]
 if mode=='connector16': return 16,[[f&15 for f in c] for c in codes]
 d=json.loads(Path(path).read_text());L=d['labels'];maps=d['full_state_to_label']
 assert type(L) is int and 1<=L<=16 and [len(m) for m in maps]==list(ff.DIMS[:5])
 assert all(type(v) is int and 0<=v<L for m in maps for v in m)
 return L,maps

def main():
 ap=argparse.ArgumentParser();ap.add_argument('POINT_JSON',type=Path);ap.add_argument('OUTPUT_DIR',type=Path)
 ap.add_argument('--mapping-mode',choices=['parallel15','connector16','json'],default='parallel15');ap.add_argument('--mapping-json',type=Path);ap.add_argument('--seconds',type=float,default=8)
 args=ap.parse_args();R=args.OUTPUT_DIR.resolve();R.mkdir(parents=True,exist_ok=True);assert not (R/'STARTED.json').exists()
 src=args.POINT_JSON.resolve();d=json.loads(src.read_text(),parse_float=F)
 increment=BASE/'finite8_degree_augmentation/pool_edge3_allclass1/SCOPE_INCREMENT_004_CONNECTOR4.json'
 assert d.get('actual_full_stored_cuts_checked',0)>=7894,'Requires new complete post-connector4 point'
 assert src.stat().st_mtime_ns>increment.stat().st_mtime_ns,'Point must postdate connector4 increment'
 shutil.copyfile(src,R/'INPUT_POINT.json');snap=R/'INPUT_POINT.json';L,maps=mappings(args.mapping_mode,args.mapping_json)
 mapping=dict(mode=args.mapping_mode,labels=L,full_state_codes=[sorted(s) for s in ff.STATE_IDS],full_state_to_label=maps)
 write(R/'MAPPING.json',mapping)
 write(R/'STARTED.json',dict(source=str(src),source_sha256=digest(src),input_sha256=digest(snap),scope_increment_sha256=digest(increment),actual_full_stored_cuts_checked=d['actual_full_stored_cuts_checked'],mapping_sha256=digest(R/'MAPPING.json'),producer_sha256=digest(__file__),time_limit_per_block=args.seconds,primary_goal='OPEN'))
 w=d['lambda'];den=lcm(*(v.denominator for _,v in w));proj=Counter()
 for g,v in w:
  _,c=ff.local_coefficients(ff.q4_edges_from_mask(g));n=int(v*den)
  for (b,i,j),value in c.items():
   if b<5:
    a,z=sorted((maps[b][i],maps[b][j]));proj[b,a,z]+=n*value
 Us=[]
 for b in range(5):
  U=[[0]*L for _ in range(L)]
  for (block,i,j),v in proj.items():
   if block==b:
    U[i][j]+=v*(2 if i==j else 1)
    if i!=j:U[j][i]+=v
  Us.append(U)
 write(R/'PROJECTED_MOMENTS.json',dict(blocks=Us,moment_denominator=2*ff.DEN*den,lambda_sum=str(sum(v for _,v in w)),input_sha256=digest(snap)))
 A16,X16,p16,domain=load_domain();keep=np.all(X16[:,L:]==0,axis=1);X=X16[keep,:L].astype(np.int64);pairs=[(i,j) for i in range(L) for j in range(i,L)]
 rows=[p16.index(p) for p in pairs];A=A16[rows,:][:,keep];assert X.shape==(comb(L+5,6),L)
 domain.update(labels=L,histograms=len(X),tail_zero_filter=True,source_domain_labels=16)
 write(R/'DOMAIN.json',domain);found=[];history=[]
 for b,U in enumerate(Us):
  mass=sum(map(sum,U));row=dict(block=b,ordered_mass=str(mass),status='ZERO_MASS' if not mass else 'PENDING')
  if not mass:history.append(row);continue
  target=np.array([U[i][j]/mass for i,j in pairs]);start=time.monotonic()
  sol=linprog(target,A_ub=-A.T,b_ub=np.zeros(len(X)),bounds=[(-1,1)]*len(pairs),method='highs',options={'time_limit':args.seconds,'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9})
  row.update(LP_seconds=time.monotonic()-start,numeric_status=int(sol.status),message=sol.message)
  if sol.success:
   Q=np.zeros((L,L),dtype=np.int64)
   for (i,j),v in zip(pairs,np.rint(sol.x*1000000).astype(np.int64)): Q[i,j]=Q[j,i]=int(v)*(2 if i==j else 1)
   assert 36*int(abs(Q).max())<2**60
   values=np.einsum('ij,ij->i',X@Q,X,dtype=np.int64);before=int(values.min());repair=max(0,(-before+35)//36);Q+=repair
   values=np.einsum('ij,ij->i',X@Q,X,dtype=np.int64);minimum=int(values.min());assert minimum>=0
   ids=ff.STATE_IDS[b];codes=sorted(ids);root=ff.ROOT_MASKS[b];perms=[[ids[move[f]] for f in codes] for roots,move in ff.TRANSFORMS if roots[root]==root]
   base=Q[np.ix_(maps[b],maps[b])];full=sum((base[np.ix_(p,p)] for p in perms),np.zeros_like(base));h=len(perms)
   # Native moments are already averaged over precisely these root actions.
   trace=h*sum(int(Q[i,j])*U[j][i] for i in range(L) for j in range(L));scale=max(1,int(abs(full).max()));raw=F(trace,2*ff.DEN*den);value=raw/scale
   row.update(numeric_objective=float(sol.fun),exact_normalized_pairing=str(value),float_normalized_pairing=float(value),finite6_minimum=minimum,positive_scale=scale)
   if value<F(-1,10000000):
    cut=dict(status='EXACT_SMALL_PROJECTION_FINITE6_CUT',mapping_mode=args.mapping_mode,labels=L,block=b,root_mask=root,small_Q=Q.tolist(),full_Q=full.tolist(),positive_normalization=scale,full_state_to_label=maps[b],full_state_codes=codes,root_state_permutations=perms,root_stabilizer_size=h,finite6=dict(histograms=len(X),minimum=minimum,minimum_before_repair=before,J_repair=repair),exact_target_pairing=str(raw),normalized_pairing=str(value),input_sha256=digest(snap),mapping_sha256=digest(R/'MAPPING.json'),scope='Every actual C4-free Q8; no PSD assumption. Diagnostic point is not a graph or accepted full-family point. Whole682 OPEN.')
    name=f'block{b}.EXACT_CUT.json';write(R/name,cut);found.append(name);row['status']='MEANINGFUL_EXACT_CUT_FOUND'
   else:row['status']='NO_MEANINGFUL_CUT_IN_BOUNDED_PROBE'
  else:row['status']='UNKNOWN_BOUNDED_LP'
  history.append(row);write(R/'HISTORY.json',history);print(json.dumps(row),flush=True)
 write(R/'RESULT.json',dict(status='BOUNDED_SMALL_PROJECTION_DISCOVERY',cuts=found,history=history,domain=domain,scope='NoCut/timeout is inconclusive, not cone membership or whole-family NO; whole682 OPEN.'))
 print(json.dumps(dict(cuts=found)),flush=True)
if __name__=='__main__':main()
