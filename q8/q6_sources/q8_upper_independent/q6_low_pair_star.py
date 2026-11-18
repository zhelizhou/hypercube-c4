"""Two degree-two roots with the same selected axes and equal bits there."""
import argparse
from itertools import combinations
from pathlib import Path
import json,subprocess,time
from pysat.card import CardEnc,EncType
from cube import Cube

ROOT=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('second',type=int,choices=[12,60]);ap.add_argument('--seconds',type=int,default=120)
args=ap.parse_args();q=Cube(6);f=[[-e-1 for e in row] for row in q.squares];nv=192
for v in range(64):
 if v.bit_count()%2:continue
 if v in (0,args.second):
  for i in range(6):
   e=q.index[tuple(sorted((v,v^(1<<i))))]+1;f.append([e if i<2 else -e])
 else:f.extend([list(a) for a in combinations([e+1 for e in q.incident[v]],4)])
groups=[]
for axes in combinations(range(6),3):
 mask=sum(1<<i for i in axes)
 for base in range(64):
  if base&mask:continue
  stars=[]
  for sub in range(64):
   if sub&~mask:continue
   v=base|sub
   if v.bit_count()%2:continue
   nv+=1;stars.append(nv);ee=[q.index[tuple(sorted((v,v^(1<<i))))]+1 for i in axes]
   f.extend([[-nv,e] for e in ee]);f.append([nv]+[-e for e in ee])
  groups.append(stars)
holes=[]
for stars in groups:
 nv+=1;holes.append(nv);f.append([nv]+stars);f.extend([[-nv,-s] for s in stars])
card=CardEnc.atmost(holes,1,top_id=nv,encoding=EncType.seqcounter);f+=card.clauses;nv=card.nv
p=ROOT/'results'/f'q6_lowpair_w{args.second}_star159plus'
p.with_suffix('.cnf').write_text(f'p cnf {nv} {len(f)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in f))
t=time.monotonic()
with p.with_suffix('.log').open('w') as out:r=subprocess.run(['/tmp/cadical-master/build/cadical','-t',str(args.seconds),'--no-binary',str(p.with_suffix('.cnf')),str(p.with_suffix('.drat'))],stdout=out,stderr=subprocess.STDOUT)
x={'status':{10:'SAT',20:'UNSAT'}.get(r.returncode,'UNKNOWN'),'two_low_roots':[0,args.second],'selected_axes':[0,1],'other_specified_parity_minimum_degree':3,'opposite_parity_restriction':'none','target_stars_atleast':159,'seconds':time.monotonic()-t,'proof_checked':False}
if r.returncode==10:
 positive={int(v) for line in p.with_suffix('.log').read_text().splitlines() if line.startswith('v ') for v in line[2:].split() if int(v)>0}
 x['edges']=[list(e) for i,e in enumerate(q.edges,1) if i in positive]
if r.returncode!=20:p.with_suffix('.drat').unlink(missing_ok=True)
p.with_suffix('.json').write_text(json.dumps(x,indent=2)+'\n');print(json.dumps({k:v for k,v in x.items() if k!='edges'}),flush=True)
