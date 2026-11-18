"""Independent degree-CNF reconstruction; no SAT, generator, or cube imports."""
from collections import Counter
from itertools import combinations
from rebuild_local_cnf import atmost, exactly, read_cnf

ROOTS={'1':(0,),'2d4':(0,15),'2d6':(0,63),'3':(0,15,51),'4':(0,15,51,60)}

def rebuild(code, *, score=None, opposite_six=None,neighbor_case=None,sharp_code_cuts=False,six_coefficient=3,forbidden_potential=533,low_two=0,opposite_minimum=0):
    roots=ROOTS[code];coupled=opposite_six is not None
    edges=[(u,v) for u in range(64) for v in range(u+1,64) if (u^v).bit_count()==1]
    index={e:i+1 for i,e in enumerate(edges)}
    inc={v:[i+1 for i,e in enumerate(edges) if v in e] for v in range(64)}
    square_set=set()
    for u in range(64):
        for w in range(u+1,64):
            if (u^w).bit_count()!=2:continue
            middle=[v for v in range(64) if (u^v).bit_count()==1 and (w^v).bit_count()==1]
            square_set.add(tuple(sorted(index[tuple(sorted(e))] for v in middle for e in [(u,v),(w,v)])))
    assert len(square_set)==240
    clauses=[[-e for e in row] for row in square_set]
    top=192;threshold={};weighted=[[],[]];six=[[],[]]
    for v in range(64):
        p=v.bit_count()%2
        if not coupled and p:
            if opposite_minimum:clauses.extend(map(list,combinations(inc[v],7-opposite_minimum)))
            continue
        if v in roots:clauses.extend([[e] for e in inc[v]])
        else:
            clauses.extend(map(list,combinations(inc[v],5 if low_two else 4)))
            if p==0 or coupled and opposite_six==0:clauses.append([-e for e in inc[v]])
        for r in range(3 if low_two else 4,7):
            top+=1;threshold[v,r]=top
            clauses.extend([[-top]+list(a) for a in combinations(inc[v],7-r)])
            clauses.extend([[top]+[-e for e in a] for a in combinations(inc[v],r)])
        weighted[p].extend([threshold[v,4],threshold[v,5],threshold[v,5]])
        six[p].append(threshold[v,6])
    def card(inputs,k,kind):
        nonlocal top
        if kind=='exact':part,top=exactly(inputs,k,top)
        elif kind=='lower':part,top=atmost([-x for x in inputs],len(inputs)-k,top)
        else:part,top=atmost(inputs,k,top)
        clauses.extend(part)
    if coupled:
        card(six[1],opposite_six,'exact')
        for p,c in [(0,len(roots)),(1,opposite_six)]:
            cap=min((126-10*c)//3,(84-7*c)//2)
            if sharp_code_cuts:cap=min(cap,[42,38,35,30,24][c])
            card(weighted[p],cap,'upper')
        forbidden_H=forbidden_potential-448-(six_coefficient+2)*(len(roots)+opposite_six)
        card(weighted[0]+weighted[1],forbidden_H,'lower')
        for v in range(64):
            inputs=[threshold[v^(1<<i),r] for i in range(6) for r in range(4,7)]
            part,top=atmost(inputs,3,top)
            clauses.extend([[-threshold[v,6]]+c for c in part])
        if sharp_code_cuts:
            caps=[42,38,35,30,24]
            for p,c,other in [(0,len(roots),opposite_six),(1,opposite_six,len(roots))]:
                card(weighted[p],forbidden_H-caps[other],'lower')
        if neighbor_case is not None:
            assert code=='1' and opposite_six==0
            patterns=[(3,3,3,3,3,3),(4,3,3,3,3,3),(5,3,3,3,3,3),
                      (4,4,3,3,3,3),(5,4,3,3,3,3),(4,4,4,3,3,3)]
            for i,d in enumerate(patterns[neighbor_case]):
                for r in range(4,7):clauses.append([threshold[1<<i,r] if d>=r else -threshold[1<<i,r]])
            card(weighted[0],38,'lower');card(weighted[1],42,'lower')
    else:
        if low_two:card([-threshold[v,3] for v in range(64) if not v.bit_count()%2 and v not in roots],low_two,'exact')
        inputs=[threshold[v,r] for v in range(64) if not v.bit_count()%2 and v not in roots for r in [4,5,5]]
        card(inputs,score,'lower')
    return top,Counter(tuple(sorted(c)) for c in clauses)

def audit(path,code,**kwargs):
    expected=rebuild(code,**kwargs);actual=read_cnf(path)
    assert expected==actual,(path,expected[0],actual[0],sum(expected[1].values()),sum(actual[1].values()))
    return {'variables':expected[0],'clauses':sum(expected[1].values()),'independently_rebuilt':True}
