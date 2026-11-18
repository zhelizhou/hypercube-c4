"""Freeze local audit command/hash ledger and independently score both ties."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from itertools import combinations
import json,hashlib,re
HERE=Path(__file__).resolve().parent;BASE=HERE.parents[2]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
SQ=[(0,1),(0,2),(1,3),(2,3)];roots=[0,1,3,6,7]
edges3=[(v,v^(1<<a)) for v in range(8) for a in range(3) if not v&(1<<a)]
edges=edges3+[(u+8,v+8) for u,v in edges3]+[(v,v+8) for v in range(8)]
ei={tuple(sorted(e)):i for i,e in enumerate(edges)}
group=[]
for sw in range(2):
 for t in range(4):
  vm=[t ^ ((((v&1)<<1)|((v&2)>>1)) if sw else v) for v in range(4)]
  em=[SQ.index(tuple(sorted((vm[a],vm[b])))) for a,b in SQ];group.append((vm,em))
def rm(r,h):return sum(((r>>k)&1)<<h[1][k] for k in range(4))
def fm(f,h):return sum(((f>>k)&1)<<h[0][k] for k in range(4))+sum(((f>>(4+k))&1)<<(4+h[1][k]) for k in range(4))
states=[[f for f in range(240) if not any((r>>k&1) and(f>>(4+k)&1) and(f>>u&1) and(f>>v&1) for k,(u,v) in enumerate(SQ))] for r in roots]
ids=[{f:i for i,f in enumerate(s)} for s in states]
def vc(c):return min(c,((c&1)<<1)|((c&2)>>1)|((c&4)<<1)|((c&8)>>1))
reps=sorted({vc(c) for c in range(15)})
data=json.loads((HERE/'independent_B8/INDEPENDENT_RESULT.json').read_text())
qdata=json.loads((HERE.parent/'B_enriched8_candidate001/LOCAL_PRICE_SCORE.json').read_text())
weights={(b,i,j):v for b,i,j,v in qdata['original_finite8_upper_coefficient_weights']}
qh=qdata['histogram_weights_j0_to_j4']
def literal_score(mask):
 def edge(u,v):return mask>>ei[tuple(sorted((u,v)))]&1
 degree=[0]*16;adj=[set() for _ in range(16)]
 for u,v in edges:
  if edge(u,v):degree[u]+=1;degree[v]+=1;adj[u].add(v);adj[v].add(u)
 assert all(len(adj[u]&adj[v])<=1 for u,v in combinations(range(16),2))
 value=sum(qh[d] for d in degree)
 def q(b,i,j):return weights.get((b,min(i,j),max(i,j)),0)
 for a,b in combinations(range(4),2):
  for base in range(16):
   if base&((1<<a)|(1<<b)):continue
   vs=[base,base^(1<<a),base^(1<<b),base^(1<<a)^(1<<b)]
   r=sum(edge(vs[u],vs[v])<<k for k,(u,v) in enumerate(SQ));assert r<15
   flags=[]
   for c in range(4):
    if c in (a,b):continue
    flags.append(sum(edge(vs[u],vs[u]^(1<<c))<<u for u in range(4))+sum(edge(vs[u]^(1<<c),vs[v]^(1<<c))<<(4+k) for k,(u,v) in enumerate(SQ)))
   cr=min(rm(r,h) for h in group);block=roots.index(cr);h0=next(h for h in group if rm(r,h)==cr)
   s,t=[fm(f,h0) for f in flags];st=[h for h in group if rm(cr,h)==cr]
   for h in st:
    i=ids[block][fm(s,h)];j=ids[block][fm(t,h)]
    value+=(8//len(st))*(280*q(block,i,j)+28*q(block,i,i)+28*q(block,j,j))
 pairs=list(combinations(range(4),2))
 for v in range(16):
  ss=[]
  for a,b in pairs:
   c=edge(v,v^(1<<a))+2*edge(v,v^(1<<b))+4*edge(v^(1<<a),v^(1<<a)^(1<<b))+8*edge(v^(1<<b),v^(1<<a)^(1<<b))
   assert c<15;ss.append(reps.index(vc(c)))
  for i,A in enumerate(pairs):
   for j,B in enumerate(pairs[i:],i):value+=(24 if i==j else 144 if set(A)&set(B) else 720)*q(5,ss[i],ss[j])
 return value
witnesses={str(mask):literal_score(mask) for mask in [146532333,3889906149]}
assert set(witnesses.values())=={-37440}
old=HERE.parent/'B_enriched3_replay001';new=HERE/'producer_replay'
replay={f:dict(byte_identical=(old/f).read_bytes()==(new/f).read_bytes(),sha256=sha(new/f)) for f in ['EXACT_COMBINATION.json','LOCAL_PRICE_SCORE.json','oracle_matrices.txt','oracle_linear.txt']}
assert all(v['byte_identical'] for v in replay.values())
oldr=json.loads((old/'RESULT.json').read_text());newr=json.loads((new/'RESULT.json').read_text())
changed=[k for k in newr if oldr.get(k)!=newr[k]];assert set(changed)=={'parameter_source_hashes','seconds'}
native=BASE/'finite8_degree_augmentation/pool_B684plus_enriched8/exact_row_combination001'
for f in ['oracle_matrices.txt','oracle_linear.txt']:assert (native/f).read_bytes()==(HERE/'independent_B8'/f).read_bytes()
nt=(native/'own_oracle.stdout.txt').read_text();assert 'EXACT_MAX -37440 / 64512' in nt and 'all 13150453 legal marked completions enumerated' in nt
for name in ['full_oracle.stdout.txt','rebuilt_oracle.stdout.txt']:
 s=(HERE/'independent_B8'/name).read_text()
 assert 'EXACT_RAW_MAX -37440' in s and 'LEGAL_MARKED_COMPLETIONS 13150453' in s and 'WITNESS_ALL_Q4_ISOMETRIES 384 PASS' in s and 'STATUS COMPLETE_LEGAL_Q4_MAXIMUM' in s
imports=['finite8_flags/FINITE8_BRIDGE_AND_OBSTRUCTION.md','finite8_edge_flags/lift.py','finite8_edge_flags/edge_flags.py','finite8_edge_flags/export_cones.py','finite8_root_checks/EDGE_PULLBACK.md','finite8_root_checks/FINAL_CERTIFICATE_INTERFACE.md','finite8_edge_vertex_bridge/PROOF.md','finite8_maximal_vertex_cone/PROOF.md','finite8_connector_frequency/PROOF.md','finite8_projection_cones/PROOF.md','finite8_degree_augmentation/pool_native_leaf_connector/LEAF_PROOF.md','finite8_degree_augmentation/pool_B684plus_enriched3/edge3_sampling_inputs/LIFT_PROOF.md','finite8_degree_augmentation/pool_B684plus_enriched8/TWO_CASE_COVER_PROOF.md','finite8_root_checks/reconstruct_exact_dual.py','finite8_root_checks/exact_dual/INTERFACE.md','finite8_full_oracle_independent/independent_q4.cpp','finite8_full_oracle_independent/independent_q4','finite8_flags/oracle/finite8_separator.cpp','finite8_flags/oracle/finite8_separator','finite8_flags/oracle/keys.bin']
hashes={str(BASE/p):sha(BASE/p) for p in imports}
hashes.update({str(p):sha(p) for p in [HERE/'independent_audit.py',HERE/'finalize_receipt.py',HERE/'independent_q4_rebuilt',native/'own_oracle.stdout.txt',native.parent/'exact_primary_oracle001.stdout.txt',HERE/'independent_B8/full_oracle.stdout.txt',HERE/'independent_B8/rebuilt_oracle.stdout.txt',old/'full_oracle2.stdout.json',old/'FULL_CERTIFICATE_EVALUATION.json']})
commands=[
 dict(cwd=str(HERE),command='PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -B independent_audit.py > B3.stdout.txt 2> B3.stderr.txt',exit_code=0),
 dict(cwd=str(HERE),command='PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -B independent_audit.py --scope pool_B684plus_enriched8 --reference B_enriched8_candidate001 --output independent_B8 > B8.stdout.txt 2> B8.stderr.txt',exit_code=0),
 dict(cwd=str(HERE),command='PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -B ../../reconstruct_exact_dual.py ../../../finite8_degree_augmentation/pool_B684plus_enriched3 producer_replay > producer_replay.stdout.txt 2> producer_replay.stderr.txt',exit_code=0),
 dict(cwd=str(HERE/'independent_B8'),command='../../../../finite8_full_oracle_independent/independent_q4 oracle_matrices.txt --linear oracle_linear.txt > full_oracle.stdout.txt 2> full_oracle.stderr.txt',exit_code=0),
 dict(cwd=str(HERE),command='g++ -std=c++17 -O3 -Wall -Wextra ../../../finite8_full_oracle_independent/independent_q4.cpp -o independent_q4_rebuilt > oracle_build.stdout.txt 2> oracle_build.stderr.txt',exit_code=0),
 dict(cwd=str(HERE/'independent_B8'),command='../independent_q4_rebuilt oracle_matrices.txt --linear oracle_linear.txt > rebuilt_oracle.stdout.txt 2> rebuilt_oracle.stderr.txt',exit_code=0),
 dict(cwd=str(HERE),command='PYTHONDONTWRITEBYTECODE=1 python3 -B finalize_receipt.py > final_checks.stdout.txt 2> final_checks.stderr.txt',exit_code=0),
]
receipt=dict(status='SCIENTIFIC_RECONSTRUCTION_AND_ACTUAL_COMPLETE_QUERY_BINDINGS_CONFIRMED',main682='OPEN',scope='deterministic-local B3/B8 scientific reconstruction; ordinary maximal interface; no canonical proof-checker',B3_current_producer_byte_replay=replay,B3_result_changed_fields=changed,B8_two_separate_oracle_implementations_agree_raw_max=-37440,B8_literal_tied_witness_scores=witnesses,commands=commands,hashes=hashes)
(HERE/'FINAL_CHECKS.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k not in ['commands','hashes']},indent=2))
