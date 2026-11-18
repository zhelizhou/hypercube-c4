"""Independent specification-to-CNF reconstruction for the new local lemmas.

No generator, cube helper, SAT package, or solver is imported.
"""
from collections import Counter
from itertools import combinations, product


def atmost(inputs,k,top):
    n=len(inputs)
    if k>=n:return [],top
    if k<0:return [[]],top
    if k==0:return [[-x] for x in inputs],top
    if k==n-1:return [[-x for x in inputs]],top
    q={};clauses=[]
    def var(i,j):
        nonlocal top
        if (i,j) not in q:top+=1;q[i,j]=top
        return q[i,j]
    for i in range(1,n-k+1):
        clauses.append([-inputs[i-1],var(i,1)])
        for j in range(1,k+1):
            if i<n-k:clauses.append([-var(i,j),var(i+1,j)])
            if j<k:clauses.append([-inputs[i+j-1],-var(i,j),var(i,j+1)])
            else:clauses.append([-inputs[i+k-1],-var(i,k)])
    return clauses,top


def exactly(inputs,k,top):
    lower,top=atmost([-x for x in inputs],len(inputs)-k,top)
    upper,top=atmost(inputs,k,top)
    return lower+upper,top


def rebuild(*,special=None,specials=(),full_roots=(),fixed_hole=None,hole_count=None,hole_max=None,full_count=None):
    edges=[(u,v) for u in range(64) for v in range(u+1,64) if (u^v).bit_count()==1]
    ids={e:k+1 for k,e in enumerate(edges)}
    inc={v:[i+1 for i,e in enumerate(edges) if v in e] for v in range(64)}
    squares=set()
    for u in range(64):
        for v in range(u+1,64):
            if (u^v).bit_count()!=2:continue
            w=[x for x in range(64) if (u^x).bit_count()==(v^x).bit_count()==1]
            squares.add(tuple(sorted(ids[tuple(sorted(e))] for e in [(u,w[0]),(v,w[0]),(u,w[1]),(v,w[1])])))
    assert len(squares)==240
    clauses=[[-e for e in square] for square in squares]
    special_map=dict(specials)
    if special is not None:special_map[special[0]]=special[1]
    for v in range(64):
        if v.bit_count()%2:continue
        if v in special_map:
            mask=special_map[v]
            for i in range(6):
                e=ids[tuple(sorted((v,v^(1<<i))))]
                clauses.append([e if mask>>i&1 else -e])
        elif v in full_roots:clauses += [[e] for e in inc[v]]
        else:
            clauses += [list(group) for group in combinations(inc[v],4)]
            if full_roots:clauses.append([-e for e in inc[v]])
    top=192;groups=[]
    for axes in combinations(range(6),3):
        mask=sum(1<<i for i in axes)
        for base in range(64):
            if base&mask:continue
            vertices=sorted(base ^ sum(1<<axes[i] for i in range(3) if bits[i]) for bits in product(range(2),repeat=3))
            stars=[]
            for v in vertices:
                if v.bit_count()%2:continue
                top+=1;stars.append(top)
                ee=[ids[tuple(sorted((v,v^(1<<i))))] for i in axes]
                clauses += [[-top,e] for e in ee]
                clauses.append([top]+[-e for e in ee])
            groups.append(stars)
            if hole_count is None and hole_max is None:
                clauses += [[-s] for s in stars] if fixed_hole==(mask,base) else [stars]
    assert top==832
    if hole_count is not None or hole_max is not None:
        holes=[]
        for stars in groups:
            top+=1;holes.append(top)
            clauses.append([top]+stars)
            clauses += [[-top,-s] for s in stars]
        counter,top=exactly(holes,hole_count,top) if hole_count is not None else atmost(holes,hole_max,top)
        clauses+=counter
    if full_count is not None:
        full=[]
        for v in range(64):
            if v.bit_count()%2 or special is not None and v==special[0]:continue
            top+=1;full.append(top)
            clauses += [[-top,e] for e in inc[v]]
            clauses.append([top]+[-e for e in inc[v]])
        counter,top=exactly(full,full_count,top);clauses+=counter
    return top,Counter(tuple(sorted(c)) for c in clauses)


def read_cnf(path):
    clauses=[];nv=nc=None
    for line in path.read_text().splitlines():
        if not line or line.startswith('c'):continue
        if line.startswith('p'):
            _,_,nv,nc=line.split();nv,nc=int(nv),int(nc);continue
        row=list(map(int,line.split()));assert row[-1]==0;clauses.append(tuple(sorted(row[:-1])))
    assert len(clauses)==nc
    return nv,Counter(clauses)
