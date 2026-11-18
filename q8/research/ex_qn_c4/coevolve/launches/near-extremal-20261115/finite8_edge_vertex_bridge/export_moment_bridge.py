"""27 degree-group moment equations, exact same-lambda packed9 interface."""
from pathlib import Path
from math import comb
import json
import numpy as np
from scipy import sparse
from export_bridge import HERE,BASE,CURRENT,save,sha
GROUPS=((0,3,7),(1,4,5,8),(2,6))
def F(g,d):return (comb(8-d,2),d*(8-d),comb(d,2))[g]
def main():
 C=sparse.load_npz(HERE/'C_FULL_162x5148.npz').toarray()
 CA=C[:81]+C[81:]
 roworder=[(g,i) for g in range(3) for i in range(9)]
 B=np.stack([sum(F(g,d)*CA[9*d+i] for d in range(9)) for g,i in roworder])
 order=json.loads((HERE/'ORDER.json').read_text());adapter=order['current_to_original5148_indices']
 BC=B[:,adapter]
 pairs=[(i,j) for i in range(9) for j in range(i,9)]
 W=np.zeros((27,45),dtype=np.int32)
 for row,(g,i) in enumerate(roworder):
  for j in GROUPS[g]:
   a,b=sorted((i,j));W[row,pairs.index((a,b))]+=2 if a==b else 1
 # Packed feature stores U_ii on diagonal and 2U_ij off diagonal.
 # W @ packed_U = 2 sum_(j in Ig) U_ij.
 info=json.loads((BASE/'finite8_degree_augmentation/pool_inventory/LP_STARTED.json').read_text())
 starts=info['packed_starts'];features=sparse.load_npz(CURRENT/'INTEGER_FEATURES.npz')
 assert starts[6]-starts[5]==45
 FV=features[:,starts[5]:starts[6]]
 LL=196*sparse.csr_matrix(W)@FV.T
 assert np.issubdtype(LL.dtype,np.integer)
 graphs=json.loads((CURRENT/'POOL_GRAPH_CODES.json').read_text());assert len(graphs)==LL.shape[1]
 artifacts={
 'full_beta':save('MOMENT_BETA_FULL_27x5148',B),
 'current_beta':save('MOMENT_BETA_CURRENT_27x1751',BC),
 'packed9_selector_twice':save('MOMENT_PACKED9_SELECTOR_TWICE_27x45',W),
 'current_lambda_numerator':save('MOMENT_LAMBDA_CURRENT_POOL_27x'+str(len(graphs)),LL)}
 (HERE/'MOMENT_ORDER.json').write_text(json.dumps({'row_order':roworder,'groups_by_root_retained_degree':GROUPS,'packed9_order':pairs,'current_graph_order':graphs},separators=(',',':'))+'\n')
 result={'status':'EXACT_27_ROW_MOMENT_EXPORT_PASS','equation':'2304*B27 @ beta = 7*W @ F_vertex.T @ lambda; equivalently B27 @ beta =392*sum_j M5[i,j](lambda)=L27 @lambda/64512','beta_matrix':'MOMENT_BETA_CURRENT_27x1751.npz','packed_feature_contract':'F_vertex columns upper_triangle(9): U_ii on diagonal and 2U_ij off diagonal, M5=U/64512. W times packed_F gives twice row-group sum. Do not divide offdiag twice.','constant_392':'784/2, because E_gamma x_i=2 E_beta C_all_di and M5=E_gamma xxT/784','artifacts':artifacts,'sources':{str(p):sha(p) for p in [CURRENT/'INTEGER_FEATURES.npz',CURRENT/'POOL_GRAPH_CODES.json',BASE/'finite8_degree_augmentation/pool_inventory/LP_STARTED.json',HERE/'ORDER.json']},'moment_order_sha256':sha(HERE/'MOMENT_ORDER.json'),'new_graph_formula':'For any new graph feature column f with the identical packed9 contract, L27_new =196*W@f_vertex. Keep same original lambda.','scope':'All C4-free Q8, no maximality or fixed edgecount. Necessary identities only, not full682 proof; rows need not be linearly independent.'}
 (HERE/'MOMENT_INTERFACE.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
