"""Discriminating integer score/isometry calibration for the new finite8 oracle.

This checks named actual Q4 graphs and one nonconstant rank1 matrix per block;
it is not a full-domain bound or the global expectation proof.
"""
from pathlib import Path
import sys,random,struct,subprocess,json,hashlib,itertools
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
from finite_flags import DIMS,DEN,local_coefficients,q4_edges_original,q4_edges_from_mask

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write_matrices(path,blocks,D):
    with path.open('w') as out:
        out.write(f'{D} -1 {DEN*D*D}\n')
        for n,Q in zip(DIMS,blocks):
            out.write(str(n)+'\n')
            for row in Q:out.write(' '.join(map(str,row))+'\n')

def main():
    rng=random.Random(20261116);edges=q4_edges_original();ei={e:k for k,e in enumerate(edges)}
    squares=[]
    for a,b in itertools.combinations(range(4),2):
        for x in range(16):
            if x&((1<<a)|(1<<b)):continue
            vs=[x,x^(1<<a),x^(1<<b),x^(1<<a)^(1<<b)]
            E=[(vs[i],vs[j]) for i,j in [(0,1),(0,2),(1,3),(2,3)]]
            squares.append(sum(1<<ei[tuple(sorted(e))] for e in E))
    graphs=[]
    for _ in range(12):
        g=rng.getrandbits(32)
        while True:
            bad=next((s for s in squares if g&s==s),None)
            if bad is None:break
            bit=rng.choice([i for i in range(32) if bad>>i&1]);g&=~(1<<bit)
        assert all(g&s!=s for s in squares);graphs.append(g)
    originals=list(graphs);transports=[]
    for g in originals:
        for _ in range(7):
            perm=list(range(4));rng.shuffle(perm);translation=rng.randrange(16)
            def image(v):return translation^sum(((v>>a)&1)<<perm[a] for a in range(4))
            h=sum(1<<ei[tuple(sorted((image(u),image(v))))] for k,(u,v) in enumerate(edges) if g>>k&1)
            graphs.append(h);transports.append((g,h))
    factors=[[rng.randrange(-2,3) for _ in range(n)] for n in DIMS]
    blocks=[[[u*v for v in f] for u in f] for f in factors];D=7
    write_matrices(HERE/'calibration_matrices.txt',blocks,D)
    (HERE/'calibration_graphs.bin').write_bytes(struct.pack('<'+'I'*len(graphs),*graphs))
    run=subprocess.run([str(HERE/'finite8_oracle'),str(HERE/'calibration_matrices.txt'),'--graphs',str(HERE/'calibration_graphs.bin')],cwd=HERE,capture_output=True,text=True,check=True)
    (HERE/'calibration.stdout.txt').write_text(run.stdout)
    vals={}
    for line in run.stdout.splitlines():
        if line.startswith('SCORE '):
            _,g,z,slash,den=line.split();assert slash=='/' and int(den)==DEN*D*D;vals[int(g)]=int(z)
    assert len(vals)==len(set(graphs))
    for g in graphs:
        rho,coeff=local_coefficients(q4_edges_from_mask(g))
        z=rho*D*D+sum(c*blocks[b][i][j] for (b,i,j),c in coeff.items())
        assert vals[g]==z,(g,vals[g],z)
    for g,h in transports:assert vals[g]==vals[h],(g,h,vals[g],vals[h])
    zero=[[[0]*n for _ in range(n)] for n in DIMS];write_matrices(HERE/'zero_matrices.txt',zero,1)
    result={'status':'PASS','actual_legal_Q4_graphs':len(graphs),'independent_integer_score_comparisons':len(graphs),'simultaneous_cube_isometry_checks':len(transports),'matrix_type':'six nonconstant integer rank1 PSD matrices, exactfactor vv^T','denominator':DEN*D*D,'source_hashes':{'finite8_oracle.cpp':sha(HERE/'finite8_oracle.cpp'),'finite8_oracle':sha(HERE/'finite8_oracle'),'finite_flags.py':sha(HERE.parent/'finite_flags.py'),'calibration_matrices.txt':sha(HERE/'calibration_matrices.txt')},'scope':'Named graph scores and covariance only, not allQ4coverage or aQ8upperbound'}
    (HERE/'CALIBRATION.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
