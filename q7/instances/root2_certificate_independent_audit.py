"""Independent structural reconstruction; does not invoke a SAT solver."""
import itertools as it, json, hashlib
from pathlib import Path
from collections import Counter
H=Path(__file__).resolve().parent
prefix=H/'star_q6_def0_root2_flushed'
lines=prefix.with_suffix('.cnf').read_text().splitlines()
assert lines[0]=='p cnf 832 4422'
actual=[tuple(map(int,l.split()[:-1])) for l in lines[1:]]
assert all(l.split()[-1]=='0' for l in lines[1:])
edges=[(v,v^(1<<i)) for v in range(64) for i in range(6) if (v>>i)&1==0]
idx={frozenset(e):k+1 for k,e in enumerate(edges)}
eid=lambda v,i:idx[frozenset((v,v^(1<<i)))]
even=[v for v in range(64) if v.bit_count()%2==0]
triples=list(it.combinations(range(6),3))
sid={(v,T):193+k for k,(v,T) in enumerate(it.product(even,triples))}
groups={k:[] for k in ['star_definition','C4','face_one','face_at_most_one','root','other_degrees']}
for (v,T),s in sid.items():
    es=[eid(v,i) for i in T]
    groups['star_definition'] += [(-s,e) for e in es]+[(s,*[-e for e in es])]
for i,j in it.combinations(range(6),2):
    rest=[k for k in range(6) if k not in [i,j]]
    for bits in it.product(range(2),repeat=4):
        v=sum(b<<k for b,k in zip(bits,rest))
        groups['C4'].append(tuple(-eid(w,k) for w,k in [(v,i),(v,j),(v^(1<<i),j),(v^(1<<j),i)]))
for T in triples:
    outside=[i for i in range(6) if i not in T]
    for bits in it.product(range(2),repeat=3):
        base=sum(b<<i for b,i in zip(bits,outside))
        roots=[base+sum(b<<i for b,i in zip(inside,T)) for inside in it.product(range(2),repeat=3)]
        ss=[sid[v,T] for v in roots if v in even]
        assert len(ss)==4
        groups['face_one'].append(tuple(ss))
        groups['face_at_most_one'] += [(-a,-b) for a,b in it.combinations(ss,2)]
groups['root']=[(eid(0,i)*(1 if i in [0,1] else -1),) for i in range(6)]
for v in even[1:]:
    es=[eid(v,i) for i in range(6)]
    groups['other_degrees'] += list(it.combinations(es,4))+[tuple(-e for e in es)]
key=lambda c:tuple(sorted(c))
assert Counter(map(key,actual))==Counter(key(c) for g in groups.values() for c in g)
degree_truth=[]
for bits in it.product(range(2),repeat=6):
    encoded=all(any(bits[i] for i in C) for C in it.combinations(range(6),4)) and not all(bits)
    assert encoded==(3<=sum(bits)<=5)
    degree_truth.append(encoded)
meta=json.loads(prefix.with_suffix('.json').read_text())
checked=json.loads(Path(str(prefix)+'.checked_cs.json').read_text(encoding='utf-8-sig'))
hashes={name:hashlib.sha256(prefix.with_suffix(ext).read_bytes()).hexdigest() for name,ext in [('cnf_sha256','.cnf'),('proof_sha256','.drup')]}
assert all(meta[k]==checked[k]==v for k,v in hashes.items())
proof=prefix.with_suffix('.drup').read_text().splitlines()
assert proof[-1]=='0'
result={'clause_groups':{k:len(v) for k,v in groups.items()},'variables':832,'clauses':len(actual),'exact_multiset_match':True,'degree_truth_table_assignments':64,'hashes_match_solver_and_checker':True,**hashes,'proof_lines':len(proof),'scope':'Independent encoding reconstruction and metadata audit; full RUP proof not rerun here.'}
(H/'root2_certificate_independent_audit.json').write_text(json.dumps(result,indent=2))
tests=H/'rup_small_tests';tests.mkdir(exist_ok=True)
cases=[
 ('unit_conflict',1,[[1],[-1]],'0\n',True),
 ('sat_false_empty',1,[[1]],'0\n',False),
 ('fallback_restores_validated',2,[[1,2],[1,-2],[-1,2],[-1,-2]],'1 0\nd 1 0\n0\n',True),
 ('retain_original_axioms',1,[[1],[-1]],'d 1 0\n0\n',True),
 ('missing_terminator',1,[[1],[-1]],'1\n0\n',False),
 ('embedded_zero',1,[[1],[-1]],'1 0 -1 0\n0\n',False),
 ('out_of_range',1,[[1],[-1]],'2 0\n0\n',False),
 ('no_empty',1,[[1],[-1]],'1 0\n',False),
 ('tautology_not_contradiction',2,[[1,2]],'1 -1 0\n0\n',False),
 ('sat_nonrup_unit',2,[[1,2]],'-1 0\n0\n',False),
]
for name,n,cs,proof,expected in cases:
    p=tests/name
    p.with_suffix('.cnf').write_text(f'p cnf {n} {len(cs)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in cs))
    p.with_suffix('.drup').write_text(proof)
(tests/'cases.json').write_text(json.dumps([{'name':name,'expected':expected} for name,n,cs,p,expected in cases]))
print(json.dumps(result))
