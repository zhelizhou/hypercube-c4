#!/usr/bin/env python3
"""Portable replay entrypoints for the compiled sources and certificates.

quick: saved complete transcript + exact arithmetic (stdlib).
q4: recompile and fully enumerate the final Q4 query (stdlib + C++17).
reconstruct: rebuild exact combination from original parameters (NumPy/SciPy).
q6: replay all 25 import certificates in a new working copy (stdlib + C++17).
"""
from pathlib import Path
import argparse, hashlib, json, os, shutil, subprocess, sys, time

ROOT = Path(__file__).resolve().parent
BASE = ROOT/'research/ex_qn_c4/coevolve/launches/near-extremal-20261115'
SCOPE = BASE/'finite8_degree_augmentation/pool_B684plus_enriched8'
CANDIDATE = BASE/'finite8_root_checks/exact_dual/B_enriched8_candidate001'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('mode', choices=['quick', 'q4', 'reconstruct', 'q6'])
    ap.add_argument('--out', type=Path, required=True, help='must be a new directory')
    args = ap.parse_args(); out = args.out.resolve()
    if out.exists():
        ap.error('--out must not already exist')
    out.mkdir(parents=True)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    commands = []; start = time.monotonic()
    def run(cmd, name, cwd=out):
        cmd = list(map(str, cmd)); t = time.monotonic()
        with (out/(name+'.stdout.txt')).open('w') as so, (out/(name+'.stderr.txt')).open('w') as se:
            p = subprocess.run(cmd, cwd=cwd, env=env, stdout=so, stderr=se)
        commands.append({'command': cmd, 'cwd': str(cwd), 'exit_code': p.returncode,
                         'seconds': time.monotonic()-t, 'stdout': name+'.stdout.txt', 'stderr': name+'.stderr.txt'})
        (out/'COMMANDS.json').write_text(json.dumps(commands, indent=2)+'\n')
        if p.returncode:
            raise RuntimeError(f'{name} failed; see {out/(name+".stderr.txt")}')
    if args.mode in ('quick', 'q4'):
        data = out/'certificate'; shutil.copytree(CANDIDATE, data)
        transcript = data/'complete_oracle.stdout.txt'
        if args.mode == 'q4':
            exe = out/'independent_q4'
            run(['g++','-std=c++17','-O2',BASE/'finite8_full_oracle_independent/independent_q4.cpp','-o',exe], 'compile')
            run([exe,data/'oracle_matrices.txt','--linear',data/'oracle_linear.txt'], 'complete_q4')
            transcript = out/'complete_q4.stdout.txt'
        run([sys.executable,BASE/'finite8_degree_augmentation/check_B684_certificate.py',data,transcript], 'criterion')
        result = json.loads((data/'FINAL_CRITERION_CHECK.json').read_text())
        assert result['exact_safe_margin']=='782808475930428709/4209067950080000000000'
    elif args.mode == 'reconstruct':
        data = out/'reconstruction'
        run([sys.executable,BASE/'finite8_root_checks/reconstruct_exact_dual.py',SCOPE,data], 'reconstruct')
        for name in ['oracle_matrices.txt','oracle_linear.txt']:
            assert sha(data/name)==sha(CANDIDATE/name), name
        run([sys.executable,BASE/'finite8_degree_augmentation/check_B684_certificate.py',data,CANDIDATE/'complete_oracle.stdout.txt'], 'criterion')
        result = {'query_files_match_frozen_certificate': True,
                  'criterion': json.loads((data/'FINAL_CRITERION_CHECK.json').read_text())}
    else:
        work = out/'q6_audit'; shutil.copytree(BASE/'finite8_q6_import_audit', work)
        changes = []
        old = 'q6_sources/q8_upper_independent'
        new = (ROOT/'q6_sources/q8_upper_independent').as_posix()
        for name in ['run_audit.py','check_connections.py','isolated/three_full/check_exact.py']:
            p = work/name; before = p.read_bytes(); text = before.decode()
            assert old in text, name
            p.write_text(text.replace(old, new))
            changes.append({'file': name, 'before_sha256': hashlib.sha256(before).hexdigest(),
                            'after_sha256': sha(p), 'old_path': old, 'new_path': new,
                            'scope': 'literal input root only; no mathematical or checker change'})
        (out/'PATH_ADAPTATIONS.json').write_text(json.dumps(changes, indent=2)+'\n')
        run(['bash',work/'reproduce.sh'], 'q6_reproduce', work)
        result = json.loads((work/'FRESH_REPLAYS.json').read_text())
        assert result['case_count']==25 and result['verified_additions']==4383882
        result = {k:v for k,v in result.items() if k!='cases'}
    receipt = {'status':'PASS','mode':args.mode,'seconds':time.monotonic()-start,
               'result':result,'scope':'replay of the specified finite computation, not a new semantic review or upper682 proof'}
    (out/'REPLAY_RESULT.json').write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps(receipt, indent=2))

if __name__ == '__main__':
    main()
