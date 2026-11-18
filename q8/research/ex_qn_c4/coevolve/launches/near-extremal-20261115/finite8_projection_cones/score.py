"""Exact scorer and full-face-kernel interface for an explicit emitted cut path."""
from pathlib import Path
from fractions import Fraction
from functools import lru_cache
import json,sys
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'finite8_flags'))
import finite_flags as ff
@lru_cache(None)
def load(cut_path):return json.loads(Path(cut_path).read_text())
def value_on_graph(mask,cut_path,normalize=True):
 cut=load(str(cut_path));Q=cut['full_Q'];b=cut['block'];_,c=ff.local_coefficients(ff.q4_edges_from_mask(mask))
 return Fraction(sum(v*Q[i][j] for (block,i,j),v in c.items() if block==b),ff.DEN*(cut['positive_normalization'] if normalize else 1))
def full_face_kernel(cut_path,normalize=True):
 cut=load(str(cut_path));matrices=[[[0]*d for _ in range(d)] for d in ff.DIMS[:5]];matrices[cut['block']]=cut['full_Q']
 return matrices,cut['positive_normalization'] if normalize else 1
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('CUT_JSON');p.add_argument('--graph',type=int,required=True);a=p.parse_args();v=value_on_graph(a.graph,a.CUT_JSON)
 print(json.dumps(dict(value_exact=str(v),value_decimal=float(v))))
