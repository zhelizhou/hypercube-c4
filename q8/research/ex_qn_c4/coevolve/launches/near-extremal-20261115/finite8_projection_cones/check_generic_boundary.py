"""Deterministic boundary checks; no optimizer and no discovery on old points."""
from pathlib import Path
from itertools import combinations_with_replacement
from collections import Counter
from math import comb
import json,sys,hashlib
sys.dont_write_bytecode=True
import check_projection_point as check
BASE=Path(__file__).resolve().parent.parent
sys.path[:0]=[str(BASE/'finite8_flags/deps'),str(BASE/'finite8_connector_frequency')]
from membership import load_domain
A,X,pairs,domain=load_domain();rows=[]
for L in range(1,17):
 n=int((X[:,L:]==0).all(axis=1).sum());assert n==comb(L+5,6);rows.append(dict(labels=L,histograms=n))
# An arbitrary map generally has no induced permutation on labels. Exhibit this
# failure and calibrate the full-state averaging mechanism without assuming one.
L=3;maps=[[i%L for i in range(d)] for d in check.DIMS];non_equivariant=[]
for b in range(5):
 for h in check.GROUP:
  if check.rootmap(check.ROOTS[b],h)!=check.ROOTS[b]:continue
  images={}
  for i,f in enumerate(check.CODES[b]):images.setdefault(maps[b][i],set()).add(maps[b][check.IDS[b][check.move(f,h)]])
  if any(len(s)>1 for s in images.values()):non_equivariant.append(b);break
assert non_equivariant
q=[0,1,0];Q=[[36*q[i]*q[j]-15*(q[i]+q[j])+6 for j in range(L)] for i in range(L)]
values=[check.quadratic(Q,Counter(xs)) for xs in combinations_with_replacement(range(L),6)];assert len(values)==28 and min(values)==0
full=[check.full_lift(Q,b,maps)[0] for b in range(5)];cal=check.calibration(maps,L,full)
out=dict(status='PASS_ALL_SMALL_ALPHABET_COUNTS_AND_NON_EQUIVARIANT_LITERAL_CALIBRATION',complete_filtered_domain_counts=rows,non_equivariant_mapping=dict(labels=L,full_state_to_label=maps,blocks_without_induced_label_action=non_equivariant,histograms=28,finite6_minimum=0),true682_calibration=cal,checker_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),scope='Concrete implementation boundary test plus analytic general theorem; no optimizer, old-point probe, or whole682 proof.')
Path(__file__).with_name('GENERIC_BOUNDARY_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
