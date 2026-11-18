"""Transparent proposal target from a rejected IPM tuple; never a feasible point.

The independent finite-domain validity check of a proposed universal kernel
does not assume feasibility of this target. The raw signed vector is retained.
"""
from pathlib import Path
import sys,json,hashlib,time
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P.parent/'finite8_flags/deps'))
import numpy as np
from scipy import sparse

R=(P/sys.argv[1]).resolve(); O=(P/sys.argv[2]).resolve()
O.mkdir(parents=True,exist_ok=False)
rawfile=R/'LAST_REJECTED_IPM.npz'; raw=np.load(rawfile)['x']
indices=json.loads((R/'ACTIVE_COLUMNS.json').read_text())['indices']
graphs=json.loads((R/'POOL_GRAPH_CODES.json').read_text())
profiles=json.loads((R/'PROFILE_SNAPSHOT.json').read_text())['remaining']
nb=sparse.load_npz(R/'EDGE_GENERATOR_DEDUP_NUMERATOR.npz').shape[1]
sizes=(len(indices),len(profiles),nb); n=sum(sizes)
np.savez_compressed(O/'RAW_SIGNED_TUPLE.npz',real=raw[:n],full_ipm=raw)
blocks=np.split(raw[:n],np.cumsum(sizes)[:-1]); transformed=[]; changes=[]
for name,x in zip(('lambda','alpha','beta'),blocks):
    xp=np.maximum(x,0); mass=float(xp.sum()); assert mass>0
    q=xp/mass; transformed.append(q)
    changes.append({'block':name,'raw_sum':float(x.sum()),'raw_min':float(x.min()),
      'negative_count':int(sum(x<0)),'positive_sum':mass,
      'transform':'clip negatives to zero, divide by positive sum',
      'L1_change':float(sum(abs(q-x)))})
l,a,b=transformed
point={'status':'DISCOVERY_ONLY_REJECTED_RAW_IPM_TRANSFORMED_TARGET',
 'lambda':[[graphs[i],float(v)] for i,v in zip(indices,l) if v>0],
 'alpha':[[i,float(v),p['degrees']] for i,(v,p) in enumerate(zip(a,profiles)) if v>0],
 'beta':[[i,float(v)] for i,v in enumerate(b) if v>0],
 'is_graph':False,'passed_complete_model':False,'exact_acceptance_done':False,
 'primary_goal':'OPEN','transforms':changes,
 'raw_rejection':json.loads((R/'RESULT.json').read_text()),
 'source_hashes':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in
   [rawfile,R/'ACTIVE_COLUMNS.json',R/'PROFILE_SNAPSHOT.json',R/'RESULT.json']},
 'validity_contract':'A proposed kernel must be independently verified over its complete finite domain and replayed literally. This target has no feasibility assertion.'}
(O/'DISCOVERY_TARGET.json').write_text(json.dumps(point,indent=2)+'\n')
print(json.dumps({'status':point['status'],'sizes':sizes,'transforms':changes}))
