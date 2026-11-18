"""An actual marked-root projection that survives the remaining nine4 case.

The36-edge union is only a partial graph; its other parity-P stars are FREE
in a possible completion. marked_L is NOT the low count of that partial graph.
"""
from itertools import combinations
from pathlib import Path
import json
import sys

HERE=Path(__file__).resolve().parent
CO=HERE.parents[2]
sys.path.insert(0,str(CO))
from cube_coevolve.graphs import validate


def main():
    lines=sorted({tuple(sorted((a,b,a^b))) for a in range(1,8) for b in range(a+1,8)})
    assert len(lines)==7
    full7=(1<<7)-1
    marks=[]
    for line in lines:
        line_mask=sum(1<<(j-1) for j in line)
        marks.append((line_mask|(1<<7),full7^line_mask))
    retained=marks[0][1]
    outside=[j for j in range(7) if not retained&(1<<j)]
    marks += [(retained,retained),(retained|(1<<outside[0])|(1<<outside[1]),retained)]
    assert len({v for v,r in marks})==9
    assert all(v.bit_count()%2==0 and r.bit_count()==4 for v,r in marks)
    edges=sorted({tuple(sorted((v,v^(1<<j)))) for v,r in marks for j in range(8) if r&(1<<j)})
    assert len(edges)==36
    _,verification=validate(8,list(edges))
    rows=[]
    for a,b in combinations(range(8),2):
        omit=(1<<a)|(1<<b)
        for bits in range(4):
            fixed=((bits&1)<<a)|(((bits>>1)&1)<<b)
            roots=[v for v,r in marks if v&omit==fixed and r&omit==omit]
            assert len(roots) in (0,2)
            rows.append({'omitted':[a,b],'fixed':fixed,'marked_L':len(roots),'marked_roots':roots})
    (HERE/'partial_fano9.edges').write_text(''.join(f'{u} {v}\n' for u,v in edges))
    out={'scope':'Nine actual degree4 marked stars only;36-edge union is partial, other P stars free. NOT a683 graph or a completed degree profile.',
         'refuted_projection_claim':'No compatible9 degree4 stars can give marked_L in{0,2} on every containingQ6 face.',
         'marks':[{'vertex':v,'retained_mask':r} for v,r in marks],
         'marked_low_face_distribution':{str(k):sum(row['marked_L']==k for row in rows) for k in (0,2)},
         'rows':rows,'positive_partial_verification':verification,
         'unresolved':'Complete all unmarked P stars with71degree5,45degree6,2degree7,1degree8 in the same actualQ8; no completion is supplied.'}
    assert out['marked_low_face_distribution']=={'0':85,'2':27}
    (HERE/'PARTIAL_FANO9.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='rows'},indent=2))


if __name__=='__main__':main()
