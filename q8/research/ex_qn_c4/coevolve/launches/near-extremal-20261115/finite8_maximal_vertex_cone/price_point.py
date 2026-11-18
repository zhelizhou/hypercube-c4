"""Bounded MAXIMAL-ONLY vertex-cone separation. CLI: POINT_JSON NEW_RUN_DIR [MAX_ROUNDS].
A negative cut is exact-validated on the whole refined domain; no-cut is inconclusive.
"""
from fractions import Fraction
from itertools import combinations_with_replacement, product
from math import comb
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import time

BASE=Path(__file__).resolve().parent.parent
HERE=BASE/'finite8_maximal_vertex_cone'
if len(sys.argv) not in (3,4):raise SystemExit('usage: price_point.py POINT_JSON NEW_RUN_DIR [MAX_ROUNDS]')
RUN=Path(sys.argv[2]).resolve()
RUN.mkdir(parents=True,exist_ok=True)
MAX_ROUNDS=int(sys.argv[3]) if len(sys.argv)==4 else 80
if not 1<=MAX_ROUNDS<=80:raise SystemExit('MAX_ROUNDS must be in 1..80')
sys.dont_write_bytecode=True
sys.path.insert(0,str(BASE/'finite8_flags/deps'))
sys.path.insert(0,str(BASE/'finite8_flags'))
import numpy as np
from scipy.optimize import linprog
import finite_flags as ff

GROUPS=((0,3,7),(1,4,5,8),(2,6))
COORDS=list(combinations_with_replacement(range(9),2))


def generator(degree,x):
    return [Fraction(x[i]*x[j]*(1 if i==j else 2),784) for i,j in COORDS]+[int(d==degree) for d in range(9)]


def main():
    start=time.monotonic()
    path=RUN/'INPUT_POINT.json'
    if not path.exists():
        import shutil
        shutil.copyfile(Path(sys.argv[1]).resolve(),path)
    if path.read_bytes()!=Path(sys.argv[1]).resolve().read_bytes():
        raise ValueError('existing INPUT_POINT differs; use a new run directory')
    if (RUN/'SEPARATION_HISTORY.json').exists():
        raise ValueError('completed/partial run exists; use a new run directory to preserve evidence')
    source=json.loads(path.read_text())
    w=[(g,Fraction(str(p))) for g,p in source['lambda']]
    z=sum(p for _,p in w)
    assert all(p>0 for _,p in w) and z>0
    target=[Fraction() for _ in range(54)]
    lookup={ij:k for k,ij in enumerate(COORDS)}
    for graph,p in w:
        _,c=ff.local_coefficients(ff.q4_edges_from_mask(graph))
        for (b,i,j),v in c.items():
            if b==5:target[lookup[i,j]]+=p*v/(z*ff.DEN)
    alpha=[(Fraction(str(row[1])),row[2]) for row in source['alpha']]
    alpha_sum=sum(p for p,_ in alpha)
    assert alpha_sum>0 and all(p>0 for p,_ in alpha)
    for p,n in alpha:
        for d in range(9):target[45+d]+=p*n[d]/(alpha_sum*128)
    assert sum(target[45:])==1
    assert target[45]==0, "maximal-only domain requires degree-zero mass exactly zero"
    candidates={}
    for d in range(1,9):
        totals=(comb(8-d,2),(d-1)*(8-d),comb(d,2))
        for positions in product(*GROUPS):
            x=[0]*9
            for pos,total in zip(positions,totals):x[pos]=total
            x[8]+=8-d
            candidates[d,tuple(x)]=generator(d,x)
    seed=json.loads((BASE/'finite8_vertex_degree_cone/SEED_GAMMA.json').read_text())
    for c in seed['columns']:
        d,x=c['degree'],c['histogram'];candidates[d,tuple(x)]=generator(d,x)
    for previous in sorted(HERE.glob('pricing_*/query_*.oracle.json'))+list((BASE/'finite8_root_checks').glob('pricing_*/query_*.oracle.json')):
        for row in json.loads(previous.read_text())['degrees']:
            if row['witness'] is None or row['degree']==0 or row['witness'][8]<8-row['degree']:continue
            key=row['degree'],tuple(row['witness'])
            candidates[key]=generator(*key)
    history=[]
    accepted=None
    for iteration in range(MAX_ROUNDS):
        matrix=np.array([[float(v) for v in row] for row in candidates.values()])
        objective=np.array([float(v) for v in target])
        result=linprog(objective,A_ub=-matrix,b_ub=np.zeros(len(matrix)),bounds=[(-1,1)]*54,method='highs')
        if not result.success:
            history.append(dict(iteration=iteration,status=result.message));break
        qvec=np.rint(result.x[:45]*1000000).astype(np.int64)
        Q=[[0]*9 for _ in range(9)]
        for (i,j),v in zip(COORDS,qvec):Q[i][j]=Q[j][i]=int(v)
        query=RUN/f'query_{iteration:02d}.txt'
        query.write_text('\n'.join(' '.join(map(str,row)) for row in Q)+'\n'+'0 '*9+'\n')
        run=subprocess.run([str(HERE/'price_domain'),str(query)],capture_output=True,text=True,check=True)
        oracle=json.loads(run.stdout)
        (RUN/f'query_{iteration:02d}.oracle.json').write_text(run.stdout)
        biases=[-int(row['minimum']) if row['minimum'] is not None else 0 for row in oracle['degrees']]
        # S/784 = tr(Q M5)+sum_d(B_d/784)*degree_mass_d.
        pairing=sum(Fraction(int(q))*v for q,v in zip(qvec,target[:45]))
        pairing+=sum(Fraction(b,784)*v for b,v in zip(biases,target[45:]))
        scale=max(1,max(abs(int(v)) for v in qvec),max(abs(b)//784 for b in biases))
        normalized=pairing/scale
        entry=dict(iteration=iteration,restricted_dual_objective=float(result.fun),
                   exact_repaired_pairing=str(pairing),normalized_pairing=float(normalized),
                   active_generators=len(candidates),elapsed=time.monotonic()-start)
        history.append(entry)
        print(json.dumps(entry),flush=True)
        (RUN/'SEPARATION_HISTORY.json').write_text(json.dumps(history,indent=2)+'\n')
        if normalized<0:
            accepted=dict(status='EXACT_VALID_MAXIMAL_ONLY_CONDITIONAL_VERTEX_CUT',integer_Q=Q,
                          degree_bias_raw=biases,positive_normalization=scale,
                          query_file=query.name,query_oracle=f'query_{iteration:02d}.oracle.json',
                          validity='MAXIMAL ONLY: xTQx+B_d>=0 on all refinedOmega_d by complete exact minima; refinedOmega0 is empty and actual mass0=0.',
                          local_functional='T_Q(K)=sum_(i<=j) c_(5,i,j)(K)*Q_ij/64512, with existing folded c',
                          same_object_inequality='E_lambda T_Q + sum_alpha[sum_d B_d*n_d/(128*784)]>=0; divideallbypositivescaleifdesired.',
                          exact_target_pairing=str(pairing),normalized_pairing=str(normalized),
                          input_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                          scope='MAXIMAL ONLY. Separates one rationalized nonPSD local lambda/alpha tuple; not a Q8 graph or full682 certificate')
            (RUN/'CONDITIONAL_VERTEX_CUT.json').write_text(json.dumps(accepted,indent=2)+'\n')
            break
        additions=0
        for row in oracle['degrees']:
            if row['witness'] is None:continue
            key=row['degree'],tuple(row['witness'])
            if key not in candidates:
                candidates[key]=generator(*key);additions+=1
        if not additions or result.fun>-1e-9:break
    summary=dict(status='CUT_FOUND' if accepted else 'NO_EXACT_CUT_IN_BOUNDED_PROBE',
                 rounds=len(history),seconds=time.monotonic()-start,
                 scope='MAXIMAL ONLY conditional vertex-cone discovery; no-cut is inconclusive, no accepted global feasibility/NO')
    (RUN/'SEPARATION_RESULT.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary))


if __name__=='__main__':main()
