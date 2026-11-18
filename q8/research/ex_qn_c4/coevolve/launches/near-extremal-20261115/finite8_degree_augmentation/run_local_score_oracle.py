"""Deterministic adapter for the existing Root full-Q4 integer oracle.
Reads keys.bin in Root cwd; every input, receipt and output is written only
beside the supplied task-local score JSON. No compilation or source mutation.
"""
from pathlib import Path
import argparse,json,subprocess,time,hashlib,re,sys,itertools as it
P=Path(__file__).resolve().parent;SRC=P.parent/'finite8_flags';sys.path.insert(0,str(SRC));import finite_flags as ff
ap=argparse.ArgumentParser();ap.add_argument('score',type=Path);a=ap.parse_args();f=a.score.resolve();R=f.parent;d=json.loads(f.read_text());assert not (R/'OWN_ORACLE_RUN.json').exists(),'Preserve completed full oracle run.'
Q=[[[0]*n for _ in range(n)] for n in ff.DIMS]
for b,i,j,v in d['original_finite8_upper_coefficient_weights']:
 Q[b][i][j]+=int(v)
 if i!=j:Q[b][j][i]+=int(v)
mat=R/'oracle_matrices.txt';lin=R/'oracle_linear.txt'
with mat.open('w') as s:
 s.write('1 -1 64512\n')
 for n,M in zip(ff.DIMS,Q):
  s.write(str(n)+'\n')
  for row in M:s.write(' '.join(map(str,row))+'\n')
lin.write_text(' '.join(map(str,[d.get('edge_weight',0)]+d['histogram_weights_j0_to_j4']))+'\n')
root=SRC/'oracle';cmd=[str(root/'finite8_separator'),str(mat),'--linear',str(lin)];st=time.monotonic();r=subprocess.run(cmd,cwd=root,text=True,capture_output=True)
(R/'own_oracle.stdout.txt').write_text(r.stdout);(R/'own_oracle.stderr.txt').write_text(r.stderr)
assert r.returncode==0,(r.returncode,r.stdout,r.stderr)
m=re.search(r'EXACT_MAX (-?\d+) / (\d+)',r.stdout);gmatch=re.search(r'WORST_GRAPH (\d+)',r.stdout);assert m and gmatch
best=int(m.group(1));g=int(gmatch.group(1));E=ff.q4_edges_from_mask(g);h=[sum(sum(x==v or y==v for x,y in E)==j for v in range(16)) for j in range(5)];rho,c=ff.local_coefficients(E)
score=d.get('edge_weight',0)*len(E)+sum(x*y for x,y in zip(h,d['histogram_weights_j0_to_j4']))+sum(v*Q[b][i][j] for (b,i,j),v in c.items());assert score==best
adj={v:{y if x==v else x for x,y in E if x==v or y==v} for v in range(16)};assert max(len(adj[u]&adj[v]) for u,v in it.combinations(range(16),2))<=1
receipt={'status':'FULL_ORACLE_POSITIVE_LOCAL_VIOLATOR' if best>0 else 'FULL_ORACLE_NONPOSITIVE_CANDIDATE','command':cmd,'cwd_readonly_root_oracle':str(root),'returncode':r.returncode,'seconds':time.monotonic()-st,'exact_max_integer_numerator':best,'printed_denominator':int(m.group(2)),'worst_graph':g,'literal_C4_common_neighbor_check':'PASS','python_exact_score_equals_oracle':True,'source_scope':'Root existing complete common-Q4 layer-pair oracle; independent full proof review not performed here','primary683_goal':'OPEN','hashes':{str(x):hashlib.sha256(x.read_bytes()).hexdigest() for x in [f,mat,lin,root/'finite8_separator',root/'finite8_separator.cpp',root/'keys.bin',R/'own_oracle.stdout.txt']}}
(R/'OWN_ORACLE_RUN.json').write_text(json.dumps(receipt,indent=2)+'\n');(R/'OWN_ORACLE_VIOLATOR.json').write_text(json.dumps({'graph_mask':g,'edges':[list(e) for e in sorted(E)],'edge_count':len(E),'degree_histogram':{j:x for j,x in enumerate(h) if x},'score':best,'C4_common_neighbor_check':'PASS','scope':'Actual local Q4 score maximizer; no Q8 graph asserted'},indent=2)+'\n');print(json.dumps(receipt))
