"""Replay a concrete cut via the independent stars-and-bars oracle and geometry."""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json
import subprocess

HERE=Path(__file__).resolve().parent
EDGES3=[(v,v^(1<<a)) for v in range(8) for a in range(3) if not v&(1<<a)]
ORDER=EDGES3+[(u+8,v+8) for u,v in EDGES3]+[(v,v+8) for v in range(8)]
SQUARE=((0,1),(0,2),(1,3),(2,3))
PAIRS=list(combinations(range(4),2))


def swap(c):return ((c&1)<<1)|((c&2)>>1)|((c&4)<<1)|((c&8)>>1)
REPS=sorted({min(c,swap(c)) for c in range(15)})


def matrix(graph):
    assert type(graph) is int and 0<=graph<2**32
    E={edge for i,edge in enumerate(ORDER) if graph>>i&1}
    adj=[set() for _ in range(16)]
    for x,y in E:adj[x].add(y);adj[y].add(x)
    assert all(len(adj[x]&adj[y])<=1 for x in range(16) for y in range(x))
    R=[[0]*9 for _ in range(9)]
    for v in range(16):
        states=[]
        for a,b in PAIRS:
            vertices=(v,v^(1<<a),v^(1<<b),v^(1<<a)^(1<<b))
            code=sum(1<<i for i,(s,t) in enumerate(SQUARE) if vertices[t] in adj[vertices[s]])
            assert code!=15
            states.append(REPS.index(min(code,swap(code))))
        for a,A in enumerate(PAIRS):
            for b,B in enumerate(PAIRS):
                weight=24 if a==b else (360 if not set(A)&set(B) else 72)
                R[states[a]][states[b]]+=weight
    return R


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('cut');parser.add_argument('point');parser.add_argument('output')
    args=parser.parse_args()
    cut_path=Path(args.cut).resolve();point_path=Path(args.point).resolve()
    cut=json.loads(cut_path.read_text());point=json.loads(point_path.read_text(),parse_float=F)
    assert hashlib.sha256(point_path.read_bytes()).hexdigest()==cut['input_sha256']
    Q=cut['integer_Q'];B=cut['degree_bias_raw'];scale=cut['positive_normalization']
    assert len(Q)==9 and all(len(row)==9 for row in Q) and len(B)==9
    assert all(type(Q[i][j]) is int and Q[i][j]==Q[j][i] for i in range(9) for j in range(9))
    bound=784*max(abs(v) for row in Q for v in row)
    assert bound<2**60 and type(scale) is int and scale>0
    query=cut_path.parent/cut['query_file']
    assert list(map(int,query.read_text().split()))==sum(Q,[])+[0]*9
    oracle=HERE/'independent_vertex_pricer'
    run=subprocess.run([str(oracle),str(query)],capture_output=True,text=True,check=True)
    reference=json.loads(run.stdout)
    claimed=json.loads((cut_path.parent/cut['query_oracle']).read_text())
    assert len(reference)==9 and sum(row['count'] for row in reference)==674172
    for row,other in zip(reference,claimed['degrees']):
        d=row['degree'];assert row['count']==other['count'] and row['minimum']==other['minimum']
        assert int(row['minimum'])+B[d]==0
    weights=point['lambda'];alpha=point['alpha'];wl=sum(w for _,w in weights);wa=sum(row[1] for row in alpha)
    assert wl>0 and wa>0 and all(w>0 for _,w in weights) and all(row[1]>0 for row in alpha)
    trace=F()
    for graph,w in weights:
        R=matrix(graph)
        trace+=w*sum(Q[i][j]*R[j][i] for i in range(9) for j in range(9))/(wl*64512)
    degree=F()
    for _,w,n in alpha:
        assert len(n)==9 and all(type(v) is int and v>=0 for v in n) and sum(n)==128
        degree+=w*sum(B[d]*n[d] for d in range(9))/(wa*128*784)
    value=trace+degree
    assert value<0 and str(value)==cut['exact_target_pairing']
    assert str(value/scale)==cut['normalized_pairing']
    result=dict(status='PASS_EXACT_INDEPENDENT_REPLAY',histograms=674172,
                reference_minimum_slacks=[int(row['minimum'])+B[row['degree']] for row in reference],
                actual_Q4_masks=len(weights),actual_profile_weights=len(alpha),
                exact_pairing=str(value),normalized_pairing=str(value/scale),
                decimal_normalized=float(value/scale),
                cut_sha256=hashlib.sha256(cut_path.read_bytes()).hexdigest(),
                input_sha256=hashlib.sha256(point_path.read_bytes()).hexdigest(),
                independent_pricer_sha256=hashlib.sha256(oracle.read_bytes()).hexdigest(),
                scope='Concrete parameter replay of the already reviewed universal vertex-cone implication, not a new semantic model or full682 certificate')
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
