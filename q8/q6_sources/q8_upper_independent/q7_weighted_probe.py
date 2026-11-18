"""Test a NEW proposed Q7 weighted inequality; never reads Q8 research files.

The inequality 2|E| + #{degree-6 vertices} <=608 would be particularly useful
when lifted to Q8. A found counterexample rejects this proposal; UNKNOWN proves
nothing. A bare INFEASIBLE result is not treated as a checked proof certificate.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import sys
import time
from ortools.sat.python import cp_model
from cube import Cube

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--minimum-degree', type=int, default=4)
    parser.add_argument('--maximum-degree', type=int, default=6)
    parser.add_argument('--root-degree', type=int, choices=[6,7])
    parser.add_argument('--edges', type=int)
    parser.add_argument('--seconds', type=float, default=120)
    parser.add_argument('--out', default='q7_weighted_min4.json')
    parser.add_argument('--local-cuts', action='store_true')
    a = parser.parse_args()
    q = Cube(7)
    m = cp_model.CpModel()
    x = [m.new_bool_var(f'e{i}') for i in range(len(q.edges))]
    for square in q.squares:
        m.add(sum(x[e] for e in square) <= 3)
    d = [m.new_int_var(a.minimum_degree, a.maximum_degree, f'd{v}') for v in q.vertices]
    six = [m.new_bool_var(f'z6_{v}') for v in q.vertices]
    for v in q.vertices:
        m.add(d[v] == sum(x[e] for e in q.incident[v]))
        m.add(d[v] >= 6).only_enforce_if(six[v])
        m.add(d[v] <= 5).only_enforce_if(six[v].Not())
    m.add(sum(x) <= 304)  # Allowed Q7 theorem, independently cited in notes.
    m.add(2 * sum(x) + sum(six) >= 609)
    if a.edges is not None:
        m.add(sum(x) == a.edges)
    if a.root_degree is not None:
        for i in range(7):
            e = q.index[(0, 1 << i)]
            m.add(x[e] == int(i < a.root_degree))
        m.add(sum(d[1 << i] for i in range(a.root_degree)) <=
              a.root_degree * 7 - a.root_degree * (a.root_degree - 1) // 2)
    stars = []
    for v in q.vertices:
        s = m.new_int_var(0, 35, f's{v}')
        m.add_element(d[v], [0,0,0,1,4,10,20,35], s)
        stars.append(s)
    for parity in range(2):
        m.add(sum(stars[v] for v in q.vertices if v.bit_count()%2 == parity) <= 560)
    if a.local_cuts:
        manifest=json.loads((ROOT/'results/q6_star158_certificate_manifest.json').read_text())
        assert manifest['total_verified_additions']==256403
        def eq_flag(expr,value,name):
            z=m.new_bool_var(name)
            m.add(expr==value).only_enforce_if(z)
            m.add(expr!=value).only_enforce_if(z.Not())
            return z
        for axis in range(7):
            for side in range(2):
                vertices=[v for v in q.vertices if v>>axis&1==side]
                local={};sums=[];lows=[];highs=[]
                for v in vertices:
                    cross=q.index[tuple(sorted((v,v^(1<<axis))))]
                    dl=m.new_int_var(0,6,f'dl{axis}_{side}_{v}')
                    m.add(dl==d[v]-x[cross])
                    sl=m.new_int_var(0,20,f'sl{axis}_{side}_{v}')
                    m.add_element(dl,[0,0,0,1,4,10,20],sl)
                    low=m.new_bool_var(f'low{axis}_{side}_{v}')
                    m.add(dl<=2).only_enforce_if(low)
                    m.add(dl>=3).only_enforce_if(low.Not())
                    high=eq_flag(dl,6,f'high{axis}_{side}_{v}')
                    local[v]=(dl,sl,low,high)
                for p in range(2):
                    group=[local[v] for v in vertices if v.bit_count()%2==p]
                    s=sum(t[1] for t in group);l=sum(t[2] for t in group);h=sum(t[3] for t in group)
                    m.add(s<=160)
                    m.add(s<=158+2*l)  # New, checked star158 lemma.
                    sums.append(s);lows.append(l);highs.append(h)
                    # Allowed Q7-proof lemma A: unique local degree 2,
                    # all other parity degrees in 3..5, forbids star sum160.
                    under=[]
                    for v in vertices:
                        if v.bit_count()%2!=p:continue
                        dl=local[v][0];z=m.new_bool_var(f'under{axis}_{side}_{v}')
                        m.add(dl<=1).only_enforce_if(z)
                        m.add(dl>=2).only_enforce_if(z.Not());under.append(z)
                    condition=[eq_flag(l,1,f'one_low{axis}_{side}_{p}'),
                               eq_flag(h,0,f'no_high{axis}_{side}_{p}'),
                               eq_flag(sum(under),0,f'no_under{axis}_{side}_{p}')]
                    m.add(s<=157).only_enforce_if(condition)
                face_edges=[x[e] for e,(u,v) in enumerate(q.edges) if u>>axis&1==side and v>>axis&1==side]
                mh=sum(face_edges)
                good=eq_flag(sum(lows)+sum(highs),0,f'good{axis}_{side}')
                m.add(mh<=132).only_enforce_if(good)
                a158=[eq_flag(sums[p],158,f'e158_{axis}_{side}_{p}') for p in range(2)]
                a155=[eq_flag(sums[p],155,f'e155_{axis}_{side}_{p}') for p in range(2)]
                m.add(mh>=132).only_enforce_if([good,*a158])
                m.add(mh>=130).only_enforce_if([good,a158[0],a155[1]])
                m.add(mh>=130).only_enforce_if([good,a158[1],a155[0]])
    # This helper creates only Q3--Q7 graphs and contains no existing Q8 result.
    sys.path.insert(0, str(ROOT.parent / 'c4_local_inequalities'))
    from src.hypercube import build_bhn_graphs_up_to_q7
    mask = build_bhn_graphs_up_to_q7()[7]
    for e in range(len(x)):
        m.add_hint(x[e], (mask >> e) & 1)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = a.seconds
    solver.parameters.num_search_workers = 2
    start = time.monotonic()
    status = solver.solve(m)
    result = {'status': solver.status_name(status), 'minimum_degree': a.minimum_degree,
              'maximum_degree': a.maximum_degree, 'root_degree': a.root_degree,
              'fixed_edge_count': a.edges, 'seconds': time.monotonic()-start,
              'local_cuts': a.local_cuts,
              'candidate_inequality': '2m+N_ge6<=608', 'response': solver.response_stats()}
    if status in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        chosen = [q.edges[e] for e in range(len(x)) if solver.value(x[e])]
        deg = [0]*128
        for u,v in chosen:
            deg[u]+=1;deg[v]+=1
        result.update(edges=chosen, edge_count=len(chosen), degree_histogram=dict(Counter(deg)),
                      weighted_value=2*len(chosen)+sum(t>=6 for t in deg))
        assert result['weighted_value'] >= 609
    out = ROOT / 'results' / a.out
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['edges','response']}),flush=True)


if __name__ == '__main__':
    main()
