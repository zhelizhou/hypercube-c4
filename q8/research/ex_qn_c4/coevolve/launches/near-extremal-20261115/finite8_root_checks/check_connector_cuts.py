"""Root multiset and original-face replay, independent of connector producers."""
from fractions import Fraction
from itertools import combinations_with_replacement
from pathlib import Path
import hashlib
import json
import sys

HERE=Path(__file__).resolve().parent
BASE=HERE.parent
sys.dont_write_bytecode=True
sys.path.insert(0,str(BASE/'finite8_flags'))
import finite_flags as ff


def main():
    p=BASE/'finite8_connector_frequency/CONNECTOR_CUTS.json'
    data=json.loads(p.read_text())
    source=BASE/'finite8_vertex_degree_cone/INPUT_EDGE_STAGE_POINT.json'
    point=json.loads(source.read_text(),parse_float=Fraction)
    weights=point['lambda']
    results=[]
    for cut in data['cuts']:
        b=cut['block'];Q=cut['integer_connector_Q']
        assert len(Q)==16 and all(len(row)==16 for row in Q)
        assert all(Q[i][j]==Q[j][i] for i in range(16) for j in range(16))
        minimum=None;count=0
        for x in combinations_with_replacement(range(16),6):
            value=sum(Q[i][j] for i in x for j in x)
            minimum=value if minimum is None else min(minimum,value);count+=1
        assert count==54264 and minimum==0
        states=sorted(ff.STATE_IDS[b],key=ff.STATE_IDS[b].get)
        mapping=[code&15 for code in states]
        assert mapping==cut['full_state_connector_codes'] and set(mapping)==set(range(16))
        root=ff.ROOT_MASKS[b]
        stabilizers=[s for r,s in ff.TRANSFORMS if r[root]==root]
        for action in stabilizers:
            assert all(Q[action[i]&15][action[j]&15]==Q[i][j] for i in range(16) for j in range(16))
        pairing=Fraction()
        for graph,w in weights:
            E=ff.q4_edges_from_mask(graph);numerator=0
            adj=[set() for _ in range(16)]
            for x,y in E:adj[x].add(y);adj[y].add(x)
            assert all(len(adj[x]&adj[y])<=1 for x in range(16) for y in range(x))
            for face_root,flags in ff.face_data(E,4):
                canonical=min(r[face_root] for r,_ in ff.TRANSFORMS)
                if canonical!=root:continue
                h=next(k for k,(r,_) in enumerate(ff.TRANSFORMS) if r[face_root]==root)
                a,c=[ff.TRANSFORMS[h][1][flag]&15 for flag in flags]
                numerator+=2240*Q[a][c]+224*(Q[a][a]+Q[c][c])
            pairing+=w*numerator/64512
        expected=cut.get('target_pairing_raw') or cut.get('point_pairing_raw') or cut.get('strict_target_pairing_raw')
        if expected is not None:assert str(pairing)==expected
        scale=cut['positive_normalization']
        assert scale==max(abs(v) for row in Q for v in row)>0
        assert str(pairing/scale)==cut['normalized_exact_target_feature']
        x=cut['non_PSD_non_copositive_witness']
        assert sum(Q[i][j]*x[i]*x[j] for i in range(16) for j in range(16))==cut['witness_quadratic']<0
        assert pairing<0
        results.append(dict(block=b,all_six_histograms=count,minimum=minimum,
                            root_stabilizer_order=len(stabilizers),full_states=len(states),
                            raw_original_decimal_weight_pairing=str(pairing)))
    report=dict(status='PASS',checks=results,lambda_mass=str(sum(w for _,w in weights)),
                source_point_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                cut_file_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
                scope='Two exact finite6 connector kernels/full-state lifts/point pairings only; no full682 conclusion')
    (HERE/'CONNECTOR_ROOT_CHECK.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
