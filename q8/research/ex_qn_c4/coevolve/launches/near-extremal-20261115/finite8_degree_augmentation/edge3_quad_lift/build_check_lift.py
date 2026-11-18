"""Exact pointwise lift of all204 edge-three-axis counts to old full-facequad."""
from pathlib import Path
from itertools import combinations_with_replacement
from collections import Counter
import sys,json,time,hashlib
HERE=Path(__file__).resolve().parent;P=HERE.parent;SRC=P.parent/'finite8_flags';CHECK=P.parent/'finite8_root_checks';sys.path.insert(0,str(SRC/'deps'));sys.path.insert(0,str(SRC));sys.path.insert(0,str(CHECK));import numpy as np
from scipy import sparse
import finite_flags as ff
from check_edge3_sampling import local
st=time.monotonic();R=P/'pool_profile1409_vertex_priced';graphs=json.loads((R/'POOL_GRAPH_CODES.json').read_text());F=sparse.load_npz(R/'INTEGER_FEATURES.npz');info=json.loads((P/'pool_inventory/LP_STARTED.json').read_text());starts=info['packed_starts'];D=F.shape[1];rows=[(r,tuple(xs.count(s) for s in range(8-r))) for r in (0,1) for xs in combinations_with_replacement(range(8-r),3)];assert len(rows)==204;index={key:i for i,key in enumerate(rows)}
def flip(s):return ((s&1)<<1)|((s&2)>>1)|(s&4)
def idx(r,a,b,c):
 z=[0]*(8-r)
 for x in (a,b,c):z[x]+=1
 return index[r,tuple(z)]
K=np.zeros((204,D),dtype=np.int16);Q2=list(map(tuple,ff.Q2_EDGES))
for block,root in enumerate(ff.ROOT_MASKS):
 states=sorted(ff.STATE_IDS[block],key=ff.STATE_IDS[block].get);n=len(states);ii,jj=np.triu_indices(n);pairs=np.arange(len(ii));A=np.zeros((204,len(ii)),dtype=np.int16)
 for e,(u,v) in enumerate(Q2):
  r=(root>>e)&1;axis=3^(u^v);c0=Q2.index(tuple(sorted((u,u^axis))));c1=Q2.index(tuple(sorted((v,v^axis))));opp=Q2.index(tuple(sorted((u^axis,v^axis))));base=((root>>c0)&1)|(((root>>c1)&1)<<1)|(((root>>opp)&1)<<2);ext=np.array([((s>>u)&1)|(((s>>v)&1)<<1)|(((s>>(4+e))&1)<<2) for s in states]);lookup=np.array([[idx(r,base,a,b) for b in range(8-r)] for a in range(8-r)]);lookupflip=np.array([[idx(r,flip(base),flip(a),flip(b)) for b in range(8-r)] for a in range(8-r)]);A[lookup[ext[ii],ext[jj]],pairs]+=1;A[lookupflip[ext[ii],ext[jj]],pairs]+=1
 diagidx=np.array([i*n-i*(i-1)//2 for i in range(n)]);diag=A[:,diagidx];K[:,starts[block]:starts[block+1]]=12*A-diag[:,ii]-diag[:,jj]
assert np.all(K[:,starts[5]:]==0);assert np.all(K[:,:starts[5]].sum(axis=0)==80);sparse.save_npz(HERE/'EDGE3_LIFT_PACKED_KERNELS.npz',sparse.csr_matrix(K));(HERE/'ROW_ORDER.json').write_text(json.dumps([{'root':r,'histogram':list(z)} for r,z in rows])+'\n');product=F@K.T;L=np.zeros((len(graphs),204),dtype=np.int32)
for i,g in enumerate(graphs):
 for key,value in local(g).items():L[i,index[key]]=value
assert np.all(L.sum(axis=1)==64);res=4*product-(5*64512)*L;assert np.count_nonzero(res)==0,(np.max(abs(res)),np.argwhere(res)[:10]);np.savez_compressed(HERE/'L_CURRENT_POOL_14090x204.npz',L=L);out={'status':'EXACT_ALL204_POINTWISE_QUAD_LIFTS_MATCH_ALL_CURRENT_ACTUAL_Q4S','actual_graphs':len(graphs),'all204_rows':204,'all_integer_residuals_zero':True,'identity':'5*64512*L_z(K)=4*sum_packed c(K)*K_z; vertexblockzero','kernel':'A=sum over4rootedges bothorientation edge3 histogramindicator; Kij=12Aij−Aii−Ajj','local_formula':'T_K=(1/288)sum_faces(10Kij+Kii+Kjj), henceL=(4/5)T_K','coordinate_sum_kernel_constant80':True,'literal_L_total64':True,'no_new_fulloracle_tensor_needed_for_this_family':True,'proof_still_to_be_read_independently':True,'seconds':time.monotonic()-st,'hashes':{str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in [Path(__file__),HERE/'EDGE3_LIFT_PACKED_KERNELS.npz',HERE/'ROW_ORDER.json',HERE/'L_CURRENT_POOL_14090x204.npz',R/'INTEGER_FEATURES.npz']}};(HERE/'CHECK_RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='hashes'}))
