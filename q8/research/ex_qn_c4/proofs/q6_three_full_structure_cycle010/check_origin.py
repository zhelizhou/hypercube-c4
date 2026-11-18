#!/usr/bin/env python3
"""Exact local check of Root's separate origin-excess corollary."""
from pathlib import Path
from itertools import product
from collections import Counter
from hashlib import sha256
import json
HERE=Path(__file__).resolve().parent
rows=[]
for mask in range(63):
    d=mask.bit_count()
    if d<3:continue
    counts=[(mask&b).bit_count() for b in (3,12,48)]
    pairs=sum(mask&b==b for b in (3,12,48))
    faces=sum(mask&(a|b|c)==(a|b|c) for a,b,c in product((1,2),(4,8),(16,32)))
    q=pairs+faces;h={3:0,4:1,5:3}[d]
    assert q==counts.count(2)+counts[0]*counts[1]*counts[2]
    assert q-h>=1
    rows.append({'mask':mask,'degree':d,'block_counts':counts,'slots':q,'H_contribution':h,'excess':q-h})
assert len(rows)==41
out={'status':'PASS','mask_count':len(rows),'rows':rows,
     'pattern_counts':{str(k):v for k,v in sorted(Counter((r['degree'],tuple(sorted(r['block_counts'],reverse=True)),r['excess']) for r in rows).items())},
     'scope':'Direction masks at the distinguished missing-full root only; no graph existence/attainment assertion.',
     'source_hashes':{p.name:sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),HERE/'ORIGIN_COROLLARY.md',HERE/'PROOF.md']}}
(HERE/'ORIGIN_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='rows'},indent=2))
