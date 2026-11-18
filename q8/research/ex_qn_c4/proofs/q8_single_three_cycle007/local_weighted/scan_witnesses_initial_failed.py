#!/usr/bin/env python3
"""A bounded, read-only scan of actual historical Q6 edge-list JSON files."""
from collections import Counter
from hashlib import sha256
from math import comb
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
SOURCE=Path('q6_sources/q8_upper_independent/results')


def main():
    rows=[]; scanned=[]; actual={}
    for p in sorted(SOURCE.glob('*.json')):
        try:
            r=json.loads(p.read_text())
        except (UnicodeDecodeError,json.JSONDecodeError):
            continue
        es=r.get('edges') if isinstance(r,dict) else None
        if not es or not isinstance(es,list) or not all(
                isinstance(e,list) and len(e)==2 and all(isinstance(v,int) for v in e)
                for e in es):
            continue
        if max(max(e) for e in es)>=64:
            continue
        pairs=[tuple(sorted(e)) for e in es]
        assert len(set(pairs))==len(pairs)
        assert all(0<=u<v<64 and (u^v).bit_count()==1 for u,v in pairs)
        degrees=Counter(v for e in pairs for v in e)
        scanned.append({'file':str(p),'sha256':sha256(p.read_bytes()).hexdigest()})
        actual[str(p)]=pairs
        for parity in (0,1):
            hist=Counter(degrees[v] for v in range(64) if v.bit_count()%2==parity)
            low=sum(hist[d] for d in range(3))
            if low>1:
                continue
            stars=sum(count*comb(d,3) for d,count in hist.items())
            c=hist[6]
            rows.append({'file':str(p),'parity':parity,'S':stars,'c6':c,
                         'weighted':2*stars+c,'low_count':low,
                         'histogram':dict(sorted(hist.items()))})
    assert len(scanned)==13 and len(rows)==26
    assert all(r['low_count']==0 for r in rows)
    best=max(rows,key=lambda r:r['weighted'])
    assert best['weighted']==316 and best['S']==157 and best['c6']==2
    es=actual[best['file']]
    (HERE/'historical_316.edges').write_text(''.join(f'{u} {v}\n' for u,v in sorted(es)))
    out={'scope':'Only top-level .json files in the named historical results directory with explicit edges below64',
         'claim':'This bounded scan finds no single-low example; it is not a search of all graphs or all project files.',
         'edge_list_files':scanned,'eligible_parity_sides':rows,
         'maximum_observed':best,'scanner_sha256':sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE/'WITNESS_SCAN.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'edge_files':len(scanned),'eligible_sides':len(rows),
                      'maximum_observed':best},indent=2))


if __name__=='__main__':
    main()
