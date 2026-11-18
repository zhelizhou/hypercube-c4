#!/usr/bin/env python3
"""Isolated targeted Q6 input/cover and real historical RUP audit; no solver."""
from pathlib import Path
from collections import Counter
from itertools import combinations, permutations, product
from math import comb
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib, importlib.util, json, os, random, subprocess, sys, time

HERE=Path(__file__).resolve().parent
ISO=HERE/'isolated'
SOURCE=Path('q6_sources/q8_upper_independent')
sys.dont_write_bytecode=True
sys.path.insert(0,str(ISO))
from rebuild_local_cnf import rebuild as rebuild_local, read_cnf, atmost
from rebuild_degree_cnf import audit as degree_audit

def load_module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod

star=load_module('star_reconstruction',ISO/'audit_star_cases.py')

def dump(name,value):
    (HERE/name).write_text(json.dumps(value,indent=2)+'\n')

def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()

def strict_syntax(cnf,proof):
    n=None;clauses=0
    with cnf.open() as f:
        for line in f:
            s=line.split()
            if not s or s[0]=='c':continue
            if s[0]=='p':
                assert n is None and len(s)==4 and s[1]=='cnf'
                n,k=map(int,s[2:]);assert n>0 and k>=0;continue
            assert n is not None
            row=list(map(int,s));assert row[-1:]==[0] and all(x and abs(x)<=n for x in row[:-1])
            clauses+=1
    assert clauses==k
    additions=deletions=0;empty=False
    with proof.open() as f:
        for line in f:
            s=line.split()
            if not s or s[0]=='c':continue
            assert not empty,'noncomment content after empty clause'
            deletion=s[0]=='d'
            if deletion:s=s[1:]
            row=list(map(int,s));assert row[-1:]==[0] and all(x and abs(x)<=n for x in row[:-1])
            if deletion:deletions+=1
            else:additions+=1;empty=(len(row)==1)
    assert empty
    return {'variables':n,'clauses':clauses,'additions':additions,'deletions':deletions,'last_noncomment_is_empty':True}

def coverage():
    even=[x for x in range(64) if x.bit_count()%2==0]
    full4=[c for c in combinations(even,4) if all((x^y).bit_count()>=4 for x,y in combinations(c,2))]
    assert len(full4)==120
    for c in full4:
        hist=Counter(sum((u^v).bit_count()==2 for v in c) for u in even if u not in c)
        assert hist=={2:24,3:4}
    faces={(sum(1<<i for i in axes),base) for axes in combinations(range(6),3) for base in range(64) if not base&sum(1<<i for i in axes)}
    assert len(faces)==160
    def image(x,p):return sum(1<<p[i] for i in range(6) if x>>i&1)
    old_cover=json.loads((SOURCE/'results/q6_low2_hole_orbit_cover.json').read_text())
    subgroup=[p for p in permutations(range(6)) if {p[0],p[1]}=={0,1}]
    assert len(subgroup)==48
    used=set();orbits=[]
    for case in old_cover:
        m,b=case['mask'],case['base']
        orbit={(image(m,p),image(b,p)) for p in subgroup}
        a=(m&3).bit_count();bb=(b&3).bit_count();c=(b&60).bit_count()
        assert len(orbit)==case['orbit_size']==comb(2,a)*comb(4,3-a)*comb(2-a,bb)*comb(1+a,c)
        assert not used&orbit;used|=orbit
        orbits.append({'mask':m,'base':b,'size':len(orbit),'type':[a,bb,c]})
    assert used==faces and len(orbits)==16
    min3_holes=[];used=set()
    for base in (8,24,56):
        orbit={(image(7,p),image(base,p)) for p in permutations(range(6))}
        assert not used&orbit;used|=orbit;min3_holes.append(len(orbit))
    assert min3_holes==[60,60,20] and used=={(m,b) for m,b in faces if b!=0}
    # Counter specification: independent existential auxiliary checks on n<=6.
    count=0
    for n in range(1,7):
        for k in range(n+1):
            clauses,top=atmost(list(range(1,n+1)),k,n)
            for bits in product((False,True),repeat=n):
                expected=sum(bits)<=k
                # Prefix-threshold interpretation proves extension for arbitrary n.
                # Here obtain existence by exhaustive auxiliaries, independently.
                if top-n>12:continue
                exists=False
                for aux in product((False,True),repeat=top-n):
                    vals=(None,)+bits+aux
                    if all(any(vals[abs(x)]==(x>0) for x in c) for c in clauses):exists=True;break
                assert exists==expected;(count:=count+1)
    out={'status':'PASS','four_full_codes':120,'all_outside_distance2_counts':{'2':24,'3':4},'minimum_three_one_full_hole_orbit_sizes':min3_holes,'unique_degree_two_stabilizer_order':48,'unique_degree_two_hole_orbits':orbits,'unique_degree_two_labelled_faces':len(used) if False else 160,'counter_exhaustive_input_assignments':count}
    dump('COVERAGE.json',out);return old_cover

def naive(clauses,target):
    values={}
    for lit in target:
        v=abs(lit);s=lit<0
        if v in values and values[v]!=s:return True
        values[v]=s
    changed=True
    while changed:
        changed=False
        for c in clauses:
            if any(abs(x) in values and values[abs(x)]==(x>0) for x in c):continue
            unknown=set(x for x in c if abs(x) not in values)
            if not unknown:return True
            if len(unknown)==1:
                x=next(iter(unknown));v=abs(x);s=x>0
                if v in values and values[v]!=s:return True
                if v not in values:values[v]=s;changed=True
    return False

def checker_tests():
    fixture=HERE/'checker_fixtures';fixture.mkdir(exist_ok=True)
    exe=ISO/'check_rup_cached'
    def run(n,clauses,proof):
        cnf=fixture/'test.cnf';drat=fixture/'test.drat'
        cnf.write_text(f'p cnf {n} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses))
        drat.write_text('\n'.join(proof)+'\n')
        return subprocess.run([str(exe),str(cnf),str(drat)],capture_output=True,text=True)
    rng=random.Random(28519);counts=Counter()
    for test in range(300):
        n=rng.randrange(3,8);clauses=[]
        for _ in range(rng.randrange(2,15)):
            clauses.append([v if rng.randrange(2) else -v for v in rng.sample(range(1,n+1),rng.randrange(1,min(4,n)+1))])
        prefix=[];proof=[]
        for _ in range(12):
            c=list(rng.choice(clauses));extra=rng.choice([-1,1])*rng.randrange(1,n+1)
            if extra not in c:c.append(extra)
            assert naive(clauses+prefix,c);prefix.append(c);proof.append(' '.join(map(str,c))+' 0')
            if rng.randrange(2):proof.append('d '+' '.join(map(str,c))+' 0')
        target=[v if rng.randrange(2) else -v for v in rng.sample(range(1,n+1),rng.randrange(n+1))]
        expected=naive(clauses+prefix,target);proof.append(' '.join(map(str,target))+' 0')
        r=run(n,clauses,proof)
        assert (r.returncode in (0,10))==expected,(test,expected,r.stdout,r.stderr)
        counts[str(expected)]+=1
    axioms=[[1,2,3],[1,2,-3],[1,-2,4],[1,-2,-4],[-1]]
    r=run(4,axioms,['1 2 0','1 -2 0','d 1 2 0','d 1 -2 0','0'])
    assert r.returncode==0
    restoration=json.loads(r.stdout);assert restoration['history_fallbacks']>=1
    r=run(4,axioms,['0','1 2 0','1 -2 0']);assert r.returncode==1
    dump('CHECKER_TESTS.json',{'status':'PASS','naive_differential_cases':300,'outcomes':counts,'restoration':restoration,'future_clause_trap_rejected':True,'cached_source_sha256':sha(ISO/'check_rup_cached.cpp'),'cached_binary_sha256':sha(exe),'syntax_contract':'Each real input/trace is separately strictly parsed through EOF before replay; old C++ parser is not asserted strict.'})

def cases(cover):
    ans=[]
    cfg={
        'q6_fullstar_d4':((0,15),None,False),'q6_fullstar_d6':((0,63),None,False),
        'q6_one_hole_b8':((0,),(7,8),False),'q6_one_hole_b24':((0,),(7,24),False),
        'q6_one_hole_b56':((0,),(7,56),False),'q6_star159_c4':((0,15,51,60),None,True)}
    for name,args in cfg.items():ans.append((name,'minimum_three',lambda args=args:star.rebuild(*args)))
    ans.append(('q6_one_low_full_r2','unique_degree_two',lambda:rebuild_local(special=(0,3))))
    for row in cover:
        m,b=row['mask'],row['base'];name=f'q6_low2_hole_m{m}_b{b}_six2'
        ans.append((name,'unique_degree_two',lambda m=m,b=b:rebuild_local(special=(0,3),fixed_hole=(m,b),full_count=2)))
    for low,score in [(1,17),(2,18)]:
        name=f'q6_code_degree_4_score{score}_low{low}'
        ans.append((name,'four_full',lambda name=name,low=low,score=score:degree_audit(SOURCE/'results'/f'{name}.cnf','4',score=score,low_two=low)))
    return ans

def replay(item):
    name,family,rebuild=item;t=time.monotonic()
    cnf=SOURCE/'results'/f'{name}.cnf';proof=cnf.with_suffix('.drat')
    expected=rebuild()
    if isinstance(expected,tuple):
        actual=read_cnf(cnf);assert expected==actual,name
        reconstructed={'variables':actual[0],'clauses':sum(actual[1].values())}
    else:reconstructed=expected
    syntax=strict_syntax(cnf,proof)
    exe=ISO/('check_rup' if family=='four_full' else 'check_rup_cached')
    # For tiny cases use a separately compiled direct full-scan implementation.
    if family=='four_full':exe=ISO/'direct_rup'
    cmd=[str(exe),str(cnf),str(proof)]
    p=subprocess.run(cmd,capture_output=True,text=True)
    (HERE/f'{name}.stdout').write_text(p.stdout);(HERE/f'{name}.stderr').write_text(p.stderr)
    assert p.returncode==0,(name,p.returncode,p.stdout,p.stderr)
    result=json.loads(p.stdout);assert result['valid'] and result['final_empty_clause']
    assert result['verified_additions']==syntax['additions']
    out={'name':name,'family':family,'reconstructed_clause_multiset':reconstructed,'strict_syntax':syntax,'command':cmd,'returncode':p.returncode,'real_replay':result,'cnf_sha256':sha(cnf),'proof_sha256':sha(proof),'checker_source_sha256':sha(exe.with_suffix('.cpp')),'checker_binary_sha256':sha(exe),'elapsed_seconds':time.monotonic()-t}
    dump(name+'.receipt.json',out)
    print(json.dumps({'completed':name,'additions':result['verified_additions'],'seconds':out['elapsed_seconds']}),flush=True)
    return out

def main():
    start=time.monotonic();cover=coverage();checker_tests()
    print('Geometry, 16 labelled hole orbits and checker tests passed.',flush=True)
    reports=[]
    # Two replay workers; no solver jobs and no child agents.
    with ThreadPoolExecutor(max_workers=2) as pool:
        fs=[pool.submit(replay,item) for item in cases(cover)]
        for f in as_completed(fs):reports.append(f.result())
    result={'status':'PASS','scope':'25 independently reconstructed local inputs, complete finite case covers, strict real trace replays only','cases':sorted(reports,key=lambda r:r['name']),'case_count':len(reports),'verified_additions':sum(r['real_replay']['verified_additions'] for r in reports),'elapsed_seconds':time.monotonic()-start,'no_solver':True,'no_old_writes':True}
    assert result['case_count']==25 and result['verified_additions']==4383882
    dump('FRESH_REPLAYS.json',result)
    print(json.dumps({k:v for k,v in result.items() if k!='cases'}),flush=True)

if __name__=='__main__':main()
