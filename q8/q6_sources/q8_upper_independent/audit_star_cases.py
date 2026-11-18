"""Rebuild all six lemma CNFs independently and persist real RUP replays."""
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import subprocess

ROOT=Path(__file__).resolve().parent
RESULTS=ROOT/'results'


def canonical(c):return tuple(sorted(c))


def prefix_counter(inputs,first):
    aux=list(range(first,first+len(inputs)-1))
    clauses=[[-inputs[0],aux[0]],[-inputs[-1],-aux[-1]]]
    for i in range(1,len(inputs)-1):
        clauses += [[-inputs[i],aux[i]],[-aux[i-1],aux[i]],[-inputs[i],-aux[i-1]]]
    return clauses


def rebuild(roots,hole=None,one_unknown_hole=False):
    # Independent indexing: scan all endpoint pairs in lexical order.
    edges=[(u,v) for u in range(64) for v in range(u+1,64) if (u^v).bit_count()==1]
    ids={e:k+1 for k,e in enumerate(edges)}
    incident={v:[k+1 for k,e in enumerate(edges) if v in e] for v in range(64)}
    square_set=set()
    for u in range(64):
        for v in range(u+1,64):
            if (u^v).bit_count()!=2:continue
            common=[w for w in range(64) if (u^w).bit_count()==(v^w).bit_count()==1]
            assert len(common)==2
            square_set.add(tuple(sorted(ids[tuple(sorted(e))] for e in [(u,common[0]),(v,common[0]),(u,common[1]),(v,common[1])])))
    assert len(square_set)==240
    clauses=[[-e for e in face] for face in square_set]
    for v in range(64):
        if v.bit_count()%2:continue
        if v in roots:clauses += [[e] for e in incident[v]]
        else:
            clauses += [list(group) for group in combinations(incident[v],4)]
            clauses.append([-e for e in incident[v]])
    nv=192;face_stars=[]
    for axes in combinations(range(6),3):
        mask=sum(1<<a for a in axes)
        for base in range(64):
            if base&mask:continue
            verts=sorted(base ^ sum((1<<axes[i]) for i in range(3) if b[i]) for b in product(range(2),repeat=3))
            stars=[]
            for v in verts:
                if v.bit_count()%2:continue
                nv+=1;stars.append(nv)
                ee=[ids[tuple(sorted((v,v^(1<<a))))] for a in axes]
                clauses += [[-nv,e] for e in ee]
                clauses.append([nv]+[-e for e in ee])
            face_stars.append(stars)
            if not one_unknown_hole:
                clauses += [[-s] for s in stars] if hole==(mask,base) else [stars]
    assert nv==832 and len(face_stars)==160
    if one_unknown_hole:
        holes=list(range(833,993))
        for h,stars in zip(holes,face_stars):
            clauses.append([h]+stars)
            clauses += [[-h,-s] for s in stars]
        clauses.append(holes)
        clauses += prefix_counter(holes,993)
        nv=1151
    return nv,Counter(map(canonical,clauses))


def read_cnf(path):
    clauses=[];nv=nc=None
    for line in path.read_text().splitlines():
        if not line or line.startswith('c'):continue
        if line.startswith('p'):
            _,_,nv,nc=line.split();nv,nc=int(nv),int(nc);continue
        values=list(map(int,line.split()));assert values[-1]==0
        clauses.append(values[:-1])
    assert len(clauses)==nc
    return nv,Counter(map(canonical,clauses))


def replay(name):
    prefix=RESULTS/name
    r=subprocess.run(['/tmp/q8-independent-check-rup',str(prefix.with_suffix('.cnf')),str(prefix.with_suffix('.drat'))],capture_output=True,text=True)
    assert r.returncode==0,(name,r.stdout,r.stderr)
    checked=json.loads(r.stdout)
    checked.update(cnf_sha256=hashlib.sha256(prefix.with_suffix('.cnf').read_bytes()).hexdigest(),
                   proof_sha256=hashlib.sha256(prefix.with_suffix('.drat').read_bytes()).hexdigest(),
                   checker_sha256=hashlib.sha256((ROOT/'check_rup.cpp').read_bytes()).hexdigest())
    prefix.with_suffix('.checked.json').write_text(json.dumps(checked,indent=2)+'\n')
    record=json.loads(prefix.with_suffix('.json').read_text());record['checked_proof']=True
    prefix.with_suffix('.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({'case':name,**checked}),flush=True)
    return checked


def main():
    configurations={
        'q6_fullstar_d4':((0,15),None,False),
        'q6_fullstar_d6':((0,63),None,False),
        'q6_one_hole_b8':((0,),(7,8),False),
        'q6_one_hole_b24':((0,),(7,24),False),
        'q6_one_hole_b56':((0,),(7,56),False),
        'q6_star159_c4':((0,15,51,60),None,True),
    }
    encodings={}
    for name,args in configurations.items():
        expected=rebuild(*args);actual=read_cnf((RESULTS/name).with_suffix('.cnf'))
        assert expected==actual,name
        encodings[name]={'variables':actual[0],'clauses':sum(actual[1].values()),'independently_rebuilt':True}
    # Truth tables for the two defining local extensions and prefix counters.
    for bits in product(range(2),repeat=6):
        positives=all(any(bits[i] for i in group) for group in combinations(range(6),4))
        assert positives==(sum(bits)>=3)
        assert (positives and not all(bits))==(3<=sum(bits)<=5)
    for bits in product(range(2),repeat=3):
        for y in range(2):
            formula=all(not y or b for b in bits) and (bool(y) or not all(bits))
            assert formula==(bool(y)==all(bits))
    for n in range(2,10):
        clauses=prefix_counter(list(range(1,n+1)),n+1)
        for bits in product(range(2),repeat=n):
            assignment={i+1:bool(b) for i,b in enumerate(bits)}
            assignment.update({n+1+i:any(bits[:i+1]) for i in range(n-1)})
            satisfied=all(any(assignment[abs(l)]==(l>0) for l in c) for c in clauses)
            assert satisfied==(sum(bits)<=1)
    # Two earlier replays are reusable only after checking the actual hashes.
    replays={}
    for name in ['q6_fullstar_d4','q6_fullstar_d6']:
        report=json.loads((RESULTS/name).with_suffix('.checked.json').read_text())
        assert report['valid'] and report['final_empty_clause']
        assert report['cnf_sha256']==hashlib.sha256((RESULTS/name).with_suffix('.cnf').read_bytes()).hexdigest()
        assert report['proof_sha256']==hashlib.sha256((RESULTS/name).with_suffix('.drat').read_bytes()).hexdigest()
        assert report['checker_sha256']==hashlib.sha256((ROOT/'check_rup.cpp').read_bytes()).hexdigest()
        replays[name]=report
    pending=[n for n in configurations if n not in replays]
    with ThreadPoolExecutor(max_workers=3) as pool:
        replays.update(zip(pending,pool.map(replay,pending)))
    audit=json.loads((RESULTS/'rup_audit.json').read_text())
    result={'lemma':'Every C4-free Q6 graph whose specified parity has minimum degree >=3 has parity full-three-star sum <=158.',
            'status':'all six cases encoded independently and RUP-checked',
            'encodings':encodings,'certificates':replays,
            'total_verified_additions':sum(r['verified_additions'] for r in replays.values()),
            'checker_differential_cases':audit['differential_cases']}
    (RESULTS/'q6_star158_certificate_manifest.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'total_verified_additions':result['total_verified_additions']}),flush=True)


if __name__=='__main__':main()
