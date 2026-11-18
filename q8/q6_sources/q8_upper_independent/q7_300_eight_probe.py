"""New local target forced by K3: Q7 M300 and eight six-roots on one side.

Four Q6 facets must contain paired full roots. Normalize one pair to 0,w,
w15 or63, missing axis6. The opposite parity constraints are explicit.
"""
import argparse,json,time
from pathlib import Path
from ortools.sat.python import cp_model
from cube import Cube
ROOT=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('second',type=int,choices=[15,63],nargs='?',default=15);ap.add_argument('--opposite-min',type=int,choices=[0,3,4],default=0);ap.add_argument('--seconds',type=int,default=180);ap.add_argument('--box-pattern',type=int,choices=[0,1,2]);ap.add_argument('--box2-subcase',type=int,choices=[0,1]);ap.add_argument('--opposite-low-limit',type=int,choices=[0,1,2])
a=ap.parse_args();q=Cube(7);m=cp_model.CpModel();x=[m.new_bool_var(f'e{i}') for i in range(448)]
for face in q.squares:m.add(sum(x[i] for i in face)<=3)
m.add(sum(x)==300);d=[];six={}
for v in range(128):
 if v.bit_count()%2:dv=m.new_int_var(a.opposite_min,7,f'd{v}')
 else:
  dv=m.new_int_var(4,6,f'd{v}');z=m.new_bool_var(f'six{v}')
  m.add(dv==6).only_enforce_if(z);m.add(dv!=6).only_enforce_if(z.Not());six[v]=z
 m.add(dv==sum(x[i] for i in q.incident[v]));d.append(dv)
m.add(sum(six.values())==8)
if a.opposite_low_limit is not None:
 assert a.opposite_min>=3
 lows=[];sevens=[];opposite_stars=[]
 for v in range(128):
  if not v.bit_count()%2:continue
  low=m.new_bool_var(f'global_low{v}');m.add(d[v]==3).only_enforce_if(low);m.add(d[v]!=3).only_enforce_if(low.Not());lows.append(low)
  seven=m.new_bool_var(f'global_seven{v}');m.add(d[v]==7).only_enforce_if(seven);m.add(d[v]!=7).only_enforce_if(seven.Not());sevens.append(seven)
  sv=m.new_int_var(0,35,f'global_star{v}');m.add_element(d[v],[0,0,0,1,4,10,20,35],sv);opposite_stars.append(sv)
 m.add(sum(lows)<=a.opposite_low_limit);m.add(sum(sevens)<=1)
 m.add(sum(opposite_stars)+sum(sevens)<=552+sum(lows))
if a.box_pattern is None:
 for v in [0,a.second]:
  for axis in range(7):m.add(x[q.index[tuple(sorted((v,v^(1<<axis))))]]==int(axis<6))
box_patterns=[{(0,0),(1,0),(2,0),(3,0)},{(0,0),(0,1),(1,0),(2,0)},{(0,0),(0,1),(1,0),(1,1)}]
if a.box2_subcase is not None:
 assert a.box_pattern==2
 for v,missing in [(0,0),(60,a.box2_subcase)]:
  for axis in range(7):m.add(x[q.index[tuple(sorted((v,v^(1<<axis))))]]==int(axis!=missing))
 for s0 in range(2):
  for s1 in range(2):
   V=[v for v in six if (v&1)==s0 and ((v>>1)&1)==s1]
   rows=[]
   for i in range(len(V)):
    for j in range(i+1,len(V)):
     if (V[i]^V[j]).bit_count()==4:rows.append(tuple(int(k==i or k==j) for k in range(len(V))))
   assert len(rows)==40
   m.add_allowed_assignments([six[v] for v in V],rows)
for axis in range(7):
 for side in range(2):
  verts=[v for v in range(128) if (v>>axis)&1==side]
  P=[v for v in verts if not v.bit_count()%2];full=[];three=[]
  for v in P:
   cross=x[q.index[tuple(sorted((v,v^(1<<axis))))]]
   z=m.new_bool_var(f'full{axis}_{side}_{v}')
   m.add(z<=six[v]);m.add(z+cross<=1);m.add(z>=six[v]-cross);full.append(z)
   low=m.new_bool_var(f'three{axis}_{side}_{v}')
   m.add(d[v]-cross==3).only_enforce_if(low);m.add(d[v]-cross!=3).only_enforce_if(low.Not());three.append(low)
  C=m.new_int_var(0,2,f'C{axis}_{side}');m.add(C==sum(full));m.add_allowed_assignments([C],[(0,),(2,)])
  if a.box_pattern is not None:m.add(C==2*int((axis,side) in box_patterns[a.box_pattern]))
  M=m.new_int_var(0,132,f'M{axis}_{side}')
  m.add(M==sum(d[v]-x[q.index[tuple(sorted((v,v^(1<<axis))))]] for v in P))
  m.add(4*M+2*sum(three)+3*C==532)
  # Opposite-side degree penalty: basic star160 on this Q6 parity.
  terms=[];q_twos=[];q_threes=[];q_sixes=[]
  for v in verts:
   if not v.bit_count()%2:continue
   cross=x[q.index[tuple(sorted((v,v^(1<<axis))))]];dv=m.new_int_var(0,6,f'local{axis}_{side}_{v}');m.add(dv==d[v]-cross)
   s=m.new_int_var(0,20,f'star{axis}_{side}_{v}');m.add_element(dv,[0,0,0,1,4,10,20],s);terms.append(s)
   if a.opposite_low_limit is not None:
    for degree,flags in [(2,q_twos),(3,q_threes),(6,q_sixes)]:
     z=m.new_bool_var(f'qdeg{axis}_{side}_{v}_{degree}');m.add(dv==degree).only_enforce_if(z);m.add(dv!=degree).only_enforce_if(z.Not());flags.append(z)
  m.add(sum(terms)<=160)
  if a.opposite_low_limit is not None:
   L=m.new_int_var(0,2,f'Q2_{axis}_{side}');m.add(L==sum(q_twos))
   B=m.new_int_var(0,32,f'Q3_{axis}_{side}');m.add(B==sum(q_threes))
   F=m.new_int_var(0,4,f'Q6_{axis}_{side}');m.add(F==sum(q_sixes))
   cap=m.new_int_var(0,160,f'qcap{axis}_{side}')
   caps=[[158,156,157,152,144],[158,158,158,158,155],[160,160,160,156,157]]
   m.add_allowed_assignments([L,F,cap],[(l,f,caps[l][f]) for l in range(3) for f in range(5)])
   m.add(sum(terms)<=cap)
   m.add(B+2*L>=3*C);m.add(sum(three)>=3*F)
   good=m.new_bool_var(f'whole_min3_{axis}_{side}');m.add(L==0).only_enforce_if(good);m.add(L>=1).only_enforce_if(good.Not())
   m.add(M+C+F<=132).only_enforce_if(good)
   m.add(M+2*C<=133).only_enforce_if(good)
   m.add(M+2*F<=133).only_enforce_if(good)
s=cp_model.CpSolver();s.parameters.max_time_in_seconds=a.seconds;s.parameters.num_search_workers=2
t=time.monotonic();status=s.solve(m)
r={'target':'Q7 M300; specified parity d4..6 and exactly eight d6','pair':[0,a.second],'missing_axis':6,'opposite_minimum':a.opposite_min,'status':s.status_name(status),'seconds':time.monotonic()-t,'checked_unsat_certificate':False,'response':s.response_stats()}
name=f'q7_300_eight_w{a.second}_oppmin{a.opposite_min}'
if a.box_pattern is not None:
 r['pair']=None;r['box_pattern']=a.box_pattern;r['paired_Q6_facets']=sorted(box_patterns[a.box_pattern]);name=f'q7_300_eight_boxes{a.box_pattern}_oppmin{a.opposite_min}'
if a.box2_subcase is not None:r['box2_subcase']=a.box2_subcase;name+=f'_sub{a.box2_subcase}'
if a.opposite_low_limit is not None:r['opposite_low_limit']=a.opposite_low_limit;r['opposite_seven_limit']=1;r['new_checked_local_cuts']=True;name+=f'_lowlimit{a.opposite_low_limit}_rigid'
if status in (cp_model.FEASIBLE,cp_model.OPTIMAL):r['edges']=[list(e) for i,e in enumerate(q.edges) if s.boolean_value(x[i])]
(ROOT/f'results/{name}.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({k:v for k,v in r.items() if k not in ['edges','response']}),flush=True)
