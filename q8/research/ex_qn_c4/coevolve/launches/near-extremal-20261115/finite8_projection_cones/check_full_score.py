"""Independent full-kernel local scores, including nonzero explicit root6 graphs."""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations_with_replacement
from collections import Counter
import json,sys,hashlib
sys.dont_write_bytecode=True
import check_projection_point as independent
import score
HERE=Path(__file__).resolve().parent;R=HERE/'parallel15_master102';path=R/'block3.EXACT_CUT.json';cut=json.loads(path.read_text());b=cut['block'];Q=cut['full_Q'];scale=cut['positive_normalization'];point=json.loads((R/'INPUT_POINT.json').read_text(),parse_float=F)
def literal(mask):
 E={e for k,e in enumerate(independent.ORDER) if mask>>k&1};independent.legal(E,4);numerator=0
 for block,fs in independent.faces(E,4):
  if block==b:
   s,t=[independent.IDS[b][f] for f in fs];numerator+=10*Q[s][t]+Q[s][s]+Q[t][t]
 return F(numerator,288*scale)
point_pair=F()
for mask,w in point['lambda']:
 v=literal(mask);assert v==score.value_on_graph(mask,path);point_pair+=w*v
assert str(point_pair)==cut['normalized_pairing']
# These actual Q4 graphs contain root mask6 and give nonzero evaluations.
explicit=[]
for root in [6,7,3]:
 E={independent.SQ[k] for k in range(4) if root>>k&1};mask=sum(1<<k for k,e in enumerate(independent.ORDER) if e in E)
 v=literal(mask);assert v==score.value_on_graph(mask,path);explicit.append(dict(mask=mask,root_mask=root,value=str(v)))
assert explicit[0]['value']!='0'
# A smaller-count negative witness, if found, establishes the precise nonPSD
# boundary without conflating it with finite6 validity.
small=cut['small_Q'];witness=None
for xs in combinations_with_replacement(range(cut['labels']),4):
 value=independent.quadratic(small,Counter(xs))
 if value<0:witness=dict(total=4,histogram=dict(Counter(xs)),quadratic=value);break
representatives=[independent.IDS[b][16*p] for p in range(15)]
restricted=[[Q[i][j] for j in representatives] for i in representatives];full_witness=None
for xs in combinations_with_replacement(range(15),4):
 value=independent.quadratic(restricted,Counter(xs))
 if value<0:full_witness=dict(total=4,full_flag_code_histogram={str(16*p):n for p,n in Counter(xs).items()},quadratic=value);break
out=dict(status='PASS_ALL_LITERAL_POINT_FULL_SCORES_AND_NONZERO_ROOT6',actual_Q4_masks=len(point['lambda']),exact_normalized_pairing=str(point_pair),explicit_legal_Q4s=explicit,small_kernel_total4_negative_witness=witness,full_kernel_total4_negative_witness=full_witness,cut_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),checker_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
(R/'FULL_SCORE_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
