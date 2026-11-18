"""Independent CNF reconstruction and counter semantics; imports no SAT code."""
from pathlib import Path
from itertools import combinations,product
from collections import Counter
import json,hashlib
H=Path(__file__).resolve().parent

class IndependentCNF:
 def __init__(self):self.top=0;self.cs=[]
 def var(self):self.top+=1;return self.top
 def atmost(self,x,k):
  n=len(x)
  assert 0<=k<=n
  if k==n:return
  if k==0:self.cs.extend([[-z] for z in x]);return
  if k==n-1:self.cs.append([-z for z in x]);return
  q={}
  def counter(i,j):
   if (i,j) not in q:q[i,j]=self.var()
   return q[i,j]
  # q(i,j) corresponds to >=j true literals among x[1..i+j-1].
  for i in range(1,n-k+1):
   self.cs.append([-x[i-1],counter(i,1)])
   if i<n-k:self.cs.append([-counter(i,1),counter(i+1,1)])
   for j in range(1,k):
    self.cs.append([-x[i+j-1],-counter(i,j),counter(i,j+1)])
    if i<n-k:self.cs.append([-counter(i,j+1),counter(i+1,j+1)])
   self.cs.append([-x[i+k-1],-counter(i,k)])
 def atleast(self,x,k):self.atmost([-z for z in x],len(x)-k)
 def exact(self,x,k):self.atleast(x,k);self.atmost(x,k)

def horn_extend(clauses,assignment):
 """After fixing all inputs, auxiliary CNF is Horn; compute its least model."""
 a=dict(assignment)
 while True:
  changed=False
  for c in clauses:
   if any(a.get(abs(z))==(z>0) for z in c):continue
   free=[z for z in c if abs(z) not in a]
   if not free:return None
   if len(free)==1:
    z=free[0];a[abs(z)]=z>0;changed=True
  if not changed:break
 # Auxiliary constraints are Horn and contain no positive input remaining.
 # Unforced auxiliary variables are false in the least satisfying model.
 for c in clauses:
  for z in c:a.setdefault(abs(z),False)
 assert all(any(a[abs(z)]==(z>0) for z in c) for c in clauses)
 return a

def test_counters():
 tested=0
 for n in range(1,9):
  for k in range(n+1):
   for kind in ['atmost','atleast','exact']:
    c=IndependentCNF();xs=[c.var() for _ in range(n)];getattr(c,kind)(xs,k)
    for bits in product([False,True],repeat=n):
     ext=horn_extend(c.cs,dict(zip(xs,bits)))
     expected={'atmost':sum(bits)<=k,'atleast':sum(bits)>=k,'exact':sum(bits)==k}[kind]
     assert (ext is not None)==expected,(n,k,kind,bits)
     tested+=1
 return tested

def reconstruct(meta,orbits):
 c=IndependentCNF();groups={}
 def end(name,start):groups[name]=len(c.cs)-start
 edges=[(v,v^(1<<i)) for v in range(64) for i in range(6) if not v>>i&1]
 ids={e:c.var() for e in edges}
 def edge(v,i):return ids[tuple(sorted([v,v^(1<<i)]))]
 triples=list(combinations(range(6),3));stars={};even3=[];odd3=[]
 start=len(c.cs)
 for v in range(64):
  inc=[edge(v,i) for i in range(6)]
  c.cs.extend([list(z) for z in combinations(inc,4)])
  c.cs.append([-z for z in inc])
  z=c.var();(odd3 if v.bit_count()%2 else even3).append(z)
  c.cs.extend([[-z]+[-x for x in C] for C in combinations(inc,4)])
  c.cs.extend([[z]+list(C) for C in combinations(inc,3)])
  for T in triples:
   z=c.var();stars[v,T]=z;xs=[edge(v,i) for i in T]
   c.cs.extend([[-z,x] for x in xs]);c.cs.append([z]+[-x for x in xs])
 end('degree_and_star_definitions',start)
 start=len(c.cs)
 for i,j in combinations(range(6),2):
  for base in range(64):
   if not base&((1<<i)|(1<<j)):
    c.cs.append([-edge(base,i),-edge(base,j),-edge(base^(1<<i),j),-edge(base^(1<<j),i)])
 end('C4_exclusion',start)
 start=len(c.cs);holes={(7,0),tuple(orbits[meta['case']]['representative'])}
 for T in triples:
  mask=sum(1<<i for i in T)
  for base in range(64):
   if base&mask:continue
   ss=[stars[v,T] for v in range(64) if v.bit_count()%2==0 and v&~mask==base]
   if (mask,base) in holes:c.cs.extend([[-s] for s in ss])
   else:c.cs.append(ss)
   c.cs.extend([[-x,-y] for x,y in combinations(ss,2)])
 end('even_faces_exact_two_holes',start)
 start=len(c.cs)
 if 'min_even3' in meta:c.atleast(even3,meta['min_even3'])
 else:
  c.exact(even3,266-2*meta['m'])
  c.exact(odd3,266-2*meta['m']-meta['other_p'])
 end('degree_cardinality',start)
 start=len(c.cs);hs=[]
 for T in triples:
  mask=sum(1<<i for i in T)
  for base in range(64):
   if base&mask:continue
   ss=[stars[v,T] for v in range(64) if v.bit_count()%2==1 and v&~mask==base]
   hole=c.var();hs.append(hole);c.cs.append(ss+[hole])
   c.cs.extend([[-hole,-s] for s in ss])
   c.cs.extend([[-x,-y] for x,y in combinations(ss,2)])
 end('odd_faces_hole_equivalence',start)
 start=len(c.cs);c.exact(hs,2+3*meta['other_p']);end('odd_hole_cardinality',start)
 return c,groups

def run():
 truthcases=test_counters()
 # Direct truth-table validation of the two propositional definitions.
 degreecases=0
 for bits in product([False,True],repeat=6):
  for z in [False,True]:
   inc=list(range(6))
   lower=all(any(bits[i] for i in C) for C in combinations(inc,4))
   upper=not all(bits)
   d3=all(not z or any(not bits[i] for i in C) for C in combinations(inc,4)) and all(z or any(bits[i] for i in C) for C in combinations(inc,3))
   assert (lower and upper and d3)==(3<=sum(bits)<=5 and z==(sum(bits)==3));degreecases+=1
 for bits in product([False,True],repeat=4):
  for h in [False,True]:
   encoding=(any(bits) or h) and all(not h or not b for b in bits)
   assert encoding==(h==(not any(bits)))
 orbits=json.loads((H/'two_hole_orbits.json').read_text())
 rows=[]
 paths=sorted(H.glob('star_rigidity_p*_b*_case*_odd_degrees_cert.cnf'))
 paths+=[H/'six_profiles_sat_m131_p0_case0_odd_degrees_cert.cnf']
 for path in paths:
  if not path.with_suffix('.json').exists():continue # Producer is still solving.
  meta=json.loads(path.with_suffix('.json').read_text())
  c,groups=reconstruct(meta,orbits)
  lines=path.read_text().splitlines();header=lines[0].split()
  assert header[:2]==['p','cnf'] and int(header[2])==c.top and int(header[3])==len(c.cs)
  actual=[]
  for line in lines[1:]:
   vals=list(map(int,line.split()));assert vals[-1]==0 and 0 not in vals[:-1];actual.append(vals[:-1])
  assert actual==c.cs, path.name
  assert max(abs(z) for C in c.cs for z in C)==c.top
  sha=hashlib.sha256(path.read_bytes()).hexdigest();assert sha==meta['cnf_sha256']
  rows.append({'file':path.name,'case':meta['case'],'min_even3':meta.get('min_even3'),'other_p':meta['other_p'],'variables':c.top,'clauses':len(c.cs),'groups':groups,'ordered_clause_match':True,'cnf_sha256':sha})
 report={'counter_input_assignments_tested':truthcases,'counter_truth_table_passed':True,'degree_iff_truth_assignments':degreecases,'files':rows,'imports_no_pysat':True,'scope':'Independent complete clause reconstruction with independently implemented sequential counters; cardinality equivalence proved in star_rigidity_encoding_review.md.'}
 (H/'star_rigidity_encoding_audit.json').write_text(json.dumps(report,indent=2))
 print(json.dumps(report,indent=2))
if __name__=='__main__':run()
