"""Two full roots, M130 and parity stars157/158: six normalized cases.

Fixed degree histograms eliminate large weighted cardinality encodings.
The degree5 root on the full-root side is unique. The canonical cases are
derived in LOCAL_PAIR_RIGIDITY.md; a SAT witness refutes the proposed exclusion.
"""
import argparse,json,subprocess,time
from itertools import combinations
from pathlib import Path
from pysat.card import CardEnc,EncType
from pysat.formula import CNF,IDPool
from cube import Cube
ROOT=Path(__file__).resolve().parent
CASES=[(15,48,4),(15,17,0),(15,17,4),(15,51,0),(15,51,4),(63,3,0),(15,None,None),(63,None,None)]
ap=argparse.ArgumentParser();ap.add_argument('case',type=int,choices=range(8));ap.add_argument('--seconds',type=int,default=120)
a=ap.parse_args();second,special,missing=CASES[a.case]
q=Cube(6);f=CNF();pool=IDPool(start_from=193);four={};five={};Pthree=[];Qthree=[];Qfive=[]
for row in q.squares:f.append([-i-1 for i in row])
for v in range(64):
 inc=[i+1 for i in q.incident[v]]
 if v in [0,second]:
  for e in inc:f.append([e])
 elif v==special:
  for axis in range(6):
   e=q.index[tuple(sorted((v,v^(1<<axis))))]+1;f.append([-e if axis==missing else e])
 else:
  for row in combinations(inc,4):f.append(list(row))
  maximum=5 if v.bit_count()%2 else 4
  for row in combinations(inc,maximum+1):f.append([-e for e in row])
  for r,store in [(4,four),(5,five)]:
   z=pool.id();store[v]=z
   for row in combinations(inc,7-r):f.append([-z]+list(row))
   for row in combinations(inc,r):f.append([z]+[-e for e in row])
  if v.bit_count()%2:Qthree.append(-four[v]);Qfive.append(five[v])
  else:Pthree.append(-four[v])
for inputs,bound in [(Pthree,3 if special is not None else 2),(Qthree,6),(Qfive,8)]:
 f.extend(CardEnc.equals(inputs,bound=bound,vpool=pool,encoding=EncType.seqcounter).clauses)
# The two disjoint full-root neighborhoods each have exactly three d3 and
# three d4 roots. This follows from min degree3, total Q-side N3=6, and the
# C4-free full-root neighbor degree bound21.
for root in [0,second]:
 neighbors=[root^(1<<i) for i in range(6)]
 for v in neighbors:f.append([-five[v]])
 f.extend(CardEnc.equals([-four[v] for v in neighbors],bound=3,vpool=pool,encoding=EncType.seqcounter).clauses)
p=ROOT/f'results/q6_pair130_case{a.case}';f.to_file(str(p)+'.cnf');t=time.monotonic()
with p.with_suffix('.log').open('w') as out:r=subprocess.run(['/tmp/cadical-master/build/cadical','-t',str(a.seconds),'--no-binary',str(p.with_suffix('.cnf')),str(p.with_suffix('.drat'))],stdout=out,stderr=subprocess.STDOUT)
x={'case':a.case,'full_roots':[0,second],'unique_degree5_root':special,'missing_axis_at_degree5':missing,
   'target_edges':130,'target_parity_stars':[157 if special is not None else 154,158],'status':{10:'SAT',20:'UNSAT'}.get(r.returncode,'UNKNOWN'),
   'seconds':time.monotonic()-t,'variables':f.nv,'clauses':len(f.clauses),'proof_checked':False}
if r.returncode==10:
 positive={int(v) for line in p.with_suffix('.log').read_text().splitlines() if line.startswith('v ') for v in line[2:].split() if int(v)>0}
 x['edges']=[list(e) for i,e in enumerate(q.edges,1) if i in positive]
if r.returncode!=20:p.with_suffix('.drat').unlink(missing_ok=True)
p.with_suffix('.json').write_text(json.dumps(x,indent=2)+'\n');print(json.dumps({k:v for k,v in x.items() if k!='edges'}),flush=True)
