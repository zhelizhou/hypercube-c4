"""Exact Q6 degree-profile probe using only unweighted cardinality counters."""
import argparse,json,subprocess,time
from itertools import combinations
from pathlib import Path
from pysat.card import CardEnc,EncType
from pysat.formula import CNF,IDPool
from cube import Cube
ROOT=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('M',type=int);ap.add_argument('code',choices=['1','2d4','2d6','3','4']);ap.add_argument('cq',type=int);ap.add_argument('bp',type=int);ap.add_argument('bq',type=int);ap.add_argument('--seconds',type=int,default=90);ap.add_argument('--q-root',type=int);ap.add_argument('--root-neighbor-case',type=int,choices=range(3))
a=ap.parse_args();roots={'1':(0,),'2d4':(0,15),'2d6':(0,63),'3':(0,15,51),'4':(0,15,51,60)}[a.code]
c=[len(roots),a.cq];b=[a.bp,a.bq];n5=[a.M-128+b[p]-2*c[p] for p in range(2)];n4=[32-b[p]-c[p]-n5[p] for p in range(2)]
assert min(c+b+n5+n4)>=0
q=Cube(6);f=CNF();pool=IDPool(start_from=193);t={}
for row in q.squares:f.append([-i-1 for i in row])
for v in range(64):
 inc=[i+1 for i in q.incident[v]]
 if v in roots:
  for e in inc:f.append([e])
 else:
  for row in combinations(inc,4):f.append(list(row))
  if not v.bit_count()%2:f.append([-e for e in inc])
 for r in [4,5,6]:
  z=pool.id();t[v,r]=z
  for row in combinations(inc,7-r):f.append([-z]+list(row))
  for row in combinations(inc,r):f.append([z]+[-e for e in row])
for parity in range(2):
 V=[v for v in range(64) if v.bit_count()%2==parity]
 for inputs,count in [([-t[v,4] for v in V],b[parity]),([t[v,5] for v in V],n5[parity]+c[parity]),([t[v,6] for v in V],c[parity])]:
  f.extend(CardEnc.equals(inputs,count,vpool=pool,encoding=EncType.seqcounter).clauses)
for v in range(64):
 inputs=[t[v^(1<<i),r] for i in range(6) for r in [4,5,6]]
 cnf=CardEnc.atmost(inputs,3,vpool=pool,encoding=EncType.seqcounter)
 f.extend([[-t[v,6]]+row for row in cnf.clauses])
name=f'q6_hist_M{a.M}_{a.code}_cQ{a.cq}_b{a.bp}_{a.bq}'
if a.q_root is not None:
 assert a.cq==1 and a.q_root.bit_count()%2
 for e in q.incident[a.q_root]:f.append([e+1])
 name+=f'_qroot{a.q_root}'
if a.root_neighbor_case is not None:
 assert (a.M,a.code,a.cq,a.bp,a.bq)==(131,'1',0,2,4)
 pattern=[(3,3,3,4,4,4),(3,3,3,3,4,4),(3,3,3,3,5,4)][a.root_neighbor_case]
 for i,dv in enumerate(pattern):
  for r in [4,5,6]:f.append([t[1<<i,r] if dv>=r else -t[1<<i,r]])
 name+=f'_neighbors{a.root_neighbor_case}'
p=ROOT/'results'/name;f.to_file(str(p)+'.cnf');start=time.monotonic()
with p.with_suffix('.log').open('w') as out:run=subprocess.run(['/tmp/cadical-master/build/cadical','-t',str(a.seconds),'--no-binary',str(p.with_suffix('.cnf')),str(p.with_suffix('.drat'))],stdout=out,stderr=subprocess.STDOUT)
result={'status':{10:'SAT',20:'UNSAT'}.get(run.returncode,'UNKNOWN'),'M':a.M,'roots':roots,'c':c,'b3':b,'n4':n4,'n5':n5,'stars':[6*a.M-640+3*b[k]+4*c[k] for k in range(2)],'T2':4*a.M+sum(b)+2*sum(c),'seconds':time.monotonic()-start,'proof_checked':False,'variables':f.nv,'clauses':len(f.clauses)}
if a.q_root is not None:result['q_root']=a.q_root
if a.root_neighbor_case is not None:result['root_neighbor_case']=a.root_neighbor_case
if run.returncode==10:
 positive={int(v) for line in p.with_suffix('.log').read_text().splitlines() if line.startswith('v ') for v in line[2:].split() if int(v)>0}
 result['edges']=[list(e) for i,e in enumerate(q.edges,1) if i in positive]
if run.returncode!=20:p.with_suffix('.drat').unlink(missing_ok=True)
p.with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='edges'}),flush=True)
