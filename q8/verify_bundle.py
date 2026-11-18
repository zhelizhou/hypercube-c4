#!/usr/bin/env python3
"""Check current compiled files and distinguish original from presentation-adapted audit bindings."""
from pathlib import Path
import hashlib, json, argparse

ROOT = Path(__file__).resolve().parent
BASE = ROOT/'research/ex_qn_c4/coevolve/launches/near-extremal-20261115'

def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(2**20), b''):
            h.update(block)
    return h.hexdigest()

def mapped(path):
    text = str(path).replace('\\', '/')
    if not Path(text).is_absolute():
        return ROOT / text
    # Archived paths may point at either the source project or this bundle.
    rel = text.split('/project/', 1)[1]
    prefix = ROOT.name + '/'
    if rel.startswith(prefix):
        rel = rel[len(prefix):]
    return ROOT / rel

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--all', action='store_true', help='also check every copied material')
    ap.add_argument('--out', type=Path)
    args = ap.parse_args()
    checked = []; errors = []
    edits = json.loads((ROOT/'PRESENTATION_EDITS.json').read_text())
    adapted = {entry['path']: entry for entry in edits['files']}
    def check(p, expected, scope):
        rel = p.relative_to(ROOT).as_posix()
        original = expected.removeprefix('sha256:')
        actual = sha(p) if p.is_file() else None
        identical = actual == original
        edit = adapted.get(rel, {})
        via_edit = (scope == 'whole-theorem-audit' and not identical
                    and edit.get('before_sha256') == original
                    and edit.get('after_sha256') == actual and actual is not None)
        ok = identical or via_edit
        checked.append({'path': rel, 'scope': scope, 'match': ok,
                        'original_byte_identity': identical, 'via_presentation_edit': via_edit})
        if not ok:
            errors.append(str(p))
    audit = json.loads((BASE/'finite8_degree_augmentation/pool_B684plus_enriched8/PROOF_AUDIT.json').read_text())
    for path, h in audit['audited_input_hashes'].items():
        check(mapped(path), h, 'whole-theorem-audit')
    q6 = json.loads((BASE/'finite8_q6_import_audit/FRESH_REPLAYS.json').read_text())
    for case in q6['cases']:
        check(mapped(case['command'][1]), case['cnf_sha256'], 'Q6-CNF')
        check(mapped(case['command'][2]), case['proof_sha256'], 'Q6-full-trace')
    if args.all:
        data = json.loads((ROOT/'MATERIALS_MANIFEST.json').read_text())
        for item in data['files']:
            check(ROOT/item['path'], item['sha256'], 'collection')
    result = {'status': 'PASS' if not errors else 'FAIL', 'checks': len(checked),
              'whole_theorem_audited_files': len(audit['audited_input_hashes']),
              'Q6_pairs': len(q6['cases']), 'mismatches': errors,
              'presentation_adapted_audit_files': sum(x['via_presentation_edit'] for x in checked),
              'scope': 'current file hashes, original certificate bytes, and explicitly recorded presentation adaptations; not a new mathematical proof review'}
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))
    raise SystemExit(bool(errors))

if __name__ == '__main__':
    main()
