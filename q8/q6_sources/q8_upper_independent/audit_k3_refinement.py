"""Rebuild new local inputs; check proof hashes, witnesses, and K3 arithmetic."""
from itertools import combinations
from pathlib import Path
import hashlib,json
from rebuild_degree_cnf import audit
from rebuild_local_cnf import rebuild,read_cnf
from verify_examples import inspect
ROOT=Path(__file__).resolve().parent
specs=[('4',15,0),('4',14,0),('4',13,0),('3',22,0),('4',17,1),('4',18,2),('3',24,2)]
certificates={}
def add(name,encoding):
 p=ROOT/'results'/name;c=json.loads(p.with_suffix('.checked.json').read_text())
 assert c['valid'] and c['final_empty_clause']
 c.update(encoding)
 for suffix,key in [('.cnf','cnf_sha256'),('.drat','proof_sha256')]:c[key]=hashlib.sha256(p.with_suffix(suffix).read_bytes()).hexdigest()
 c['checker_sha256']=hashlib.sha256((ROOT/'check_rup_active.cpp').read_bytes()).hexdigest()
 p.with_suffix('.checked.json').write_text(json.dumps(c,indent=2)+'\n')
 result=json.loads(p.with_suffix('.json').read_text());assert result['status']=='UNSAT'
 result['proof_checked']=True
 if 'minimum_other_parity_degree' in result:
  result['other_specified_parity_minimum_degree']=result.pop('minimum_other_parity_degree')
  result['opposite_parity_restriction']='none'
 p.with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
 certificates[name]=c
for code,score,low in specs:
 name=f'q6_code_degree_{code}_score{score}'+(f'_low{low}' if low else '')
 add(name,audit(ROOT/f'results/{name}.cnf',code,score=score,low_two=low))
for w in [12,60]:
 name=f'q6_lowpair_w{w}_star159plus';expected=rebuild(specials=((0,3),(w,3)),hole_max=1)
 assert expected==read_cnf(ROOT/f'results/{name}.cnf')
 add(name,{'independently_rebuilt':True,'variables':expected[0],'clauses':sum(expected[1].values())})
examples={}
for code,score,target in [('3',21,152),('4',12,144)]:
 name=f'q6_code_degree_{code}_score{score}'
 x=json.loads((ROOT/f'results/{name}.json').read_text());r,d=inspect(6,x['edges'])
 assert min(d[v] for v in range(64) if not v.bit_count()%2)>=3 and r['parity_star_sums'][0]==target
 examples[name]=r
for code,c in [('2d4',2),('3',2),('3',3),('4',3),('4',4)]:
 name=f'q6_coupled_degree_{code}_{c}_sharp';x=json.loads((ROOT/f'results/{name}.json').read_text())
 r,d=inspect(6,x['edges']);assert min(d)>=3
 T=4*len(x['edges'])+sum(a==3 for a in d)+3*sum(a==6 for a in d);assert T>=533
 r['coupled_potential']=T;examples[name]=r
canonical=set();raw=0
for w in range(1,256):
 if w.bit_count()%2:continue
 for axes in combinations(range(8),4):
  mask=sum(1<<i for i in axes);I=15&mask&(~w&255)
  if I.bit_count()!=3:continue
  raw+=1
  if mask==15:
   assert (w&15).bit_count()==1
   k=(w&240).bit_count();assert k in (1,3)
   canonical.add((8+sum(1<<(4+i) for i in range(k)),15))
  else:
   missing=(15&~mask);added=(mask&~15)
   assert missing.bit_count()==added.bit_count()==1 and w&I==0
   wa=bool(w&missing);wb=bool(w&added);k=(w&~(15|added)).bit_count()
   normalized=8*wa+16*wb+sum(1<<(5+i) for i in range(k))
   canonical.add((normalized,23))
expected={(96,23),(48,23),(240,23),(40,23),(232,23),(24,23),(120,23),(24,15),(120,15)}
assert canonical==expected
for w,T in canonical:
    data=[(0,15),(w,T)];facets=[(i,s) for i in range(8) for s in range(2)]
    b={(i,s):sum(((v>>i)&1)==s and bool(selected&(1<<i)) for v,selected in data) for i,s in facets}
    assert [list(b.values()).count(k) for k in range(3)]==[11,2,3]
    odd_edges=[]
    for left,right in combinations(facets,2):
        i,si=left;j,sj=right
        if i==j:continue
        lows=sum(((v>>i)&1)==si and ((v>>j)&1)==sj and selected&(1<<i)!=0 and selected&(1<<j)!=0 for v,selected in data)
        if b[left] or b[right]:
            predicted=bool(b[left] and b[right] and (b[left]==2 or b[right]==2))
            assert bool(lows)==predicted
            if predicted:odd_edges.append((left,right))
    assert len(odd_edges)==9
    for facet in facets:
        if b[facet]:assert sum(facet in pair for pair in odd_edges)==(3 if b[facet]==1 else 4)
# Independently enumerate possible b0 box-count histograms with star deficit4.
box_patterns={}
for total_c in [2,5,8]:
    possibilities=[]
    for n1 in range(15):
        for n2 in range(15-n1):
            if n1+2*n2!=total_c:continue
            deficit=2*n1+n2
            if deficit<=4 and (4-deficit)%3==0:possibilities.append((n1,n2))
    box_patterns[total_c]=possibilities
assert box_patterns=={2:[(0,1),(2,0)],5:[(1,2)],8:[(0,4)]}
table=[]
for a in range(12):
 for b in range(12-a):
  c=11-a-b
  if 304*a+302*b+300*c+2*303+3*302==7*688:table.append((a,b,c))
assert set(table)=={(1,0,10),(0,2,9)}
# A sole b0 facet of degree304 cannot carry odd c_F degree2; every other
# b0 facet has odd degree0 and the five special facets use all their odd edges.
# Its odd degree must therefore0, giving nine odd boxes versus total c_F=50.
assert 50%2!=9%2
out={'status':'PASS','new_certificate_count':len(certificates),
     'new_verified_additions':sum(c['verified_additions'] for c in certificates.values()),
     'certificates':certificates,'verified_examples':examples,
     'K_remaining_for_N4_2':[3],'K3_canonical_cases':sorted(canonical),'K3_raw_normalized_patterns':raw,
     'canonical_facet_and_odd_box_geometry_checked':True,'b0_box_patterns':box_patterns,
     'remaining_facet_edge_counts':{'300':9,'302':5,'303':2},
     'full6_Q6_boxes':{'count1':10,'count2':20},'upper_bound':688,'target_682_proved':False}
probes={}
for i in range(9):
 p=ROOT/f'results/q8_688_k3_case{i}.json'
 if p.exists():probes[str(i)]=json.loads(p.read_text())['status']
out['bounded_K3_probe_statuses']=probes
(ROOT/'results/k3_refinement_audit.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','new_certificate_count','new_verified_additions','K_remaining_for_N4_2','upper_bound','target_682_proved']}))
