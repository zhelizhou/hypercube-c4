"""Hash-bound ledger of this turn's 11 actually RUP-checked local cases."""
from pathlib import Path
import hashlib
import json
from audit_pair_rigidity import specs, rebuild as pair_rebuild
from audit_histogram_profiles import CASES, rebuild as profile_rebuild
from rebuild_local_cnf import read_cnf

ROOT = Path(__file__).resolve().parent


def main():
    files = [(f'q6_pair130_case{i}',pair_rebuild(spec)) for i,spec in enumerate(specs)]
    for name in CASES:
        spec = json.loads((ROOT/'results'/(name+'.json')).read_text())
        files.append((name,profile_rebuild(spec)))
    checker_hash = hashlib.sha256((ROOT/'check_rup_active.cpp').read_bytes()).hexdigest()
    certificates = {}
    for name,expected in files:
        p = ROOT/'results'/name
        assert expected == read_cnf(p.with_suffix('.cnf'))
        result = json.loads(p.with_suffix('.checked.json').read_text())
        assert result['valid'] and result['final_empty_clause'] and result['independently_rebuilt']
        assert result['checker_sha256'] == checker_hash
        for suffix,key in [('.cnf','cnf_sha256'),('.drat','proof_sha256')]:
            assert result[key] == hashlib.sha256(p.with_suffix(suffix).read_bytes()).hexdigest()
        certificates[name] = result
    output = {'status':'PASS','certificate_cases':len(certificates),
              'verified_additions':sum(x['verified_additions'] for x in certificates.values()),
              'replay_results_reused_only_after_hash_match':True,
              'certificates':certificates,
              'prior_branch_cases':33,'prior_branch_verified_additions':5780679}
    output['branch_certificate_cases'] = 33+len(certificates)
    output['branch_verified_additions'] = 5780679+output['verified_additions']
    (ROOT/'results/local_pair_certificate_manifest.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k!='certificates'}))


if __name__ == '__main__':
    main()
