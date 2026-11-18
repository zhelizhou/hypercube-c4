"""Independent standard-library checks of the auxiliary graph witnesses."""
from collections import Counter
from itertools import combinations
from pathlib import Path
import hashlib
import json

ROOT=Path(__file__).resolve().parent


def inspect(n,rows):
    E={tuple(sorted(edge)) for edge in rows}
    assert len(E)==len(rows)
    adjacency=[set() for _ in range(1<<n)]
    for u,v in E:
        assert 0<=u<v<1<<n and (u^v).bit_count()==1
        adjacency[u].add(v);adjacency[v].add(u)
    # Verify C4-freeness without using a square list from any generator.
    for u in range(1<<n):
        for v in range(u+1,1<<n):
            assert len(adjacency[u]&adjacency[v])<=1
    degrees=list(map(len,adjacency))
    hist=Counter();opposite=0
    for i,j in combinations(range(n),2):
        for u in range(1<<n):
            if u&((1<<i)|(1<<j)):continue
            corners=[u,u^(1<<i),u^(1<<i)^(1<<j),u^(1<<j)]
            bits=[int(tuple(sorted((corners[k],corners[(k+1)%4]))) in E) for k in range(4)]
            hist[sum(bits)]+=1;opposite+=bits in ([1,0,1,0],[0,1,0,1])
    star_sums=[sum((degrees[v]*(degrees[v]-1)*(degrees[v]-2))//6 for v in range(1<<n) if v.bit_count()%2==p) for p in (0,1)]
    return {'n':n,'edges':len(E),'degree_histogram':dict(Counter(degrees)),
            'square_histogram':dict(hist),'opposite_squares':opposite,'D':hist[0]-opposite,
            'parity_star_sums':star_sums,'weighted_score':2*len(E)+sum(d>=6 for d in degrees)},degrees


def main():
    outputs={}
    for name,n in [('q6_positive_defect',6),('q6_stack_orbit',7),('q6_positive_stack_orbit',7)]:
        data=json.loads((ROOT/'results'/f'{name}.json').read_text())
        checked,deg=inspect(n,data['edges'])
        if n==6:assert checked['edges']==127 and checked['D']==1 and min(deg)>=3 and max(deg)<=5
        else:assert checked['weighted_score']==data['best_weighted']
        outputs[name]=checked
    probes=json.loads((ROOT/'results/small_star_probes.json').read_text())
    for index,data in enumerate(probes):
        checked,deg=inspect(data['n'],data['edges'])
        assert deg[0]==data['root_degree']
        assert min(deg[v] for v in range(1<<data['n']) if v.bit_count()%2==0)>=data['minimum_degree_on_even_side']
        assert checked['parity_star_sums'][0]==data['target_stars']
        outputs[f'small_probe_{index}']=checked
    (ROOT/'results/example_verification.json').write_text(json.dumps(outputs,indent=2)+'\n')
    print(json.dumps({'checked_graph_witnesses':len(outputs),'all_C4_free':True}))


if __name__=='__main__':main()
