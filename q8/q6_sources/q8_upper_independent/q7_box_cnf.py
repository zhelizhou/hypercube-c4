"""SAT form of the three Q7 M300/eight-six-root full-box patterns."""
import argparse,json,subprocess,time
from itertools import combinations
from pathlib import Path
from pysat.card import CardEnc,EncType
from pysat.formula import CNF,IDPool
from cube import Cube
ROOT=Path(__file__).resolve().parent
patterns=[{(0,0),(1,0),(2,0),(3,0)},{(0,0),(0,1),(1,0),(2,0)},{(0,0),(0,1),(1,0),(1,1)}]
ap=argparse.ArgumentParser();ap.add_argument('pattern',type=int,choices=range(3));ap.add_argument('--seconds',type=int,default=120);ap.add_argument('--subcase',type=int,choices=[0,1]);ap.add_argument('--opposite-min',type=int,choices=[0,3,4],default=0)
a=ap.parse_args();q=Cube(7);f=CNF();pool=IDPool(start_from=449);five=[];full={}
for row in q.squares:f.append([-i-1 for i in row])
for v in range(128):
 inc=[i+1 for i in q.incident[v]]
 if v.bit_count()%2:
  if a.opposite_min:
   for row in combinations(inc,8-a.opposite_min):f.append(list(row))
  continue
 for row in combinations(inc,4):f.append(list(row))
 f.append([-e for e in inc])
 z=pool.id();five.append(z)
 for row in combinations(inc,3):f.append([-z]+list(row))
 for row in combinations(inc,5):f.append([z]+[-e for e in row])
 for axis in range(7):
  selected=[q.index[tuple(sorted((v,v^(1<<j))))]+1 for j in range(7) if j!=axis]
  y=pool.id();full[v,axis]=y
  for e in selected:f.append([-y,e])
  f.append([y]+[-e for e in selected])
f.extend(CardEnc.equals(five,36,vpool=pool,encoding=EncType.seqcounter).clauses)
for axis in range(7):
 for side in range(2):
  inputs=[full[v,axis] for v in range(128) if not v.bit_count()%2 and (v>>axis)&1==side]
  f.extend(CardEnc.equals(inputs,2 if (axis,side) in patterns[a.pattern] else 0,vpool=pool,encoding=EncType.seqcounter).clauses)
if a.subcase is not None:
 assert a.pattern==2
 for v,missing in [(0,0),(60,a.subcase)]:
  for axis in range(7):
   e=q.index[tuple(sorted((v,v^(1<<axis))))]+1;f.append([-e if axis==missing else e])
name=f'q7_boxpattern{a.pattern}_oppmin{a.opposite_min}'+(f'_sub{a.subcase}' if a.subcase is not None else '')
p=ROOT/'results'/name;f.to_file(str(p)+'.cnf');start=time.monotonic()
with p.with_suffix('.log').open('w') as out:r=subprocess.run(['/tmp/cadical-master/build/cadical','-t',str(a.seconds),'--no-binary',str(p.with_suffix('.cnf')),str(p.with_suffix('.drat'))],stdout=out,stderr=subprocess.STDOUT)
result={'status':{10:'SAT',20:'UNSAT'}.get(r.returncode,'UNKNOWN'),'paired_Q6_facets':sorted(patterns[a.pattern]),'M':300,'P_degree6_count':8,'P_degree_range':[4,6],'opposite_minimum':a.opposite_min,'subcase':a.subcase,'variables':f.nv,'clauses':len(f.clauses),'seconds':time.monotonic()-start,'proof_checked':False}
if r.returncode==10:
 positive={int(v) for line in p.with_suffix('.log').read_text().splitlines() if line.startswith('v ') for v in line[2:].split() if int(v)>0}
 result['edges']=[list(e) for i,e in enumerate(q.edges,1) if i in positive]
if r.returncode!=20:p.with_suffix('.drat').unlink(missing_ok=True)
p.with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='edges'}),flush=True)
