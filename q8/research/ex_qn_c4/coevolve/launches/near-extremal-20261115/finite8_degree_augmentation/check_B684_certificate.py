"""Check the final rational criterion against an actual full-oracle transcript.

The row-validity, reconstruction and full-domain coverage proofs remain
separate inputs; no LP status or numerical feasibility is used here.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse,json,re,hashlib
ap=argparse.ArgumentParser();ap.add_argument('OUT',type=Path);ap.add_argument('ORACLE_STDOUT',type=Path);a=ap.parse_args();O=a.OUT.resolve();log=a.ORACLE_STDOUT.resolve();d=json.loads((O/'RESULT.json').read_text());q=json.loads((O/'LOCAL_PRICE_SCORE.json').read_text());text=log.read_text()
m=re.search(r'EXACT_RAW_MAX\s+(-?\d+)',text)
if m:
 assert 'LEGAL_MARKED_COMPLETIONS 13150453' in text and 'STATUS COMPLETE_LEGAL_Q4_MAXIMUM' in text
else:
 m=re.search(r'EXACT_MAX\s+(-?\d+)\s*/\s*64512',text);assert m and 'all 13150453 legal marked completions enumerated' in text
raw=int(m.group(1));M=F(raw,int(q['integer_score_positive_denominator']));delta=F(d['delta_exact']);am=F(d['alpha_max_exact']);bm=F(d['beta_max_exact']);eps=F(d['uniform_error_exact']);margin=delta-M-eps-am-bm
assert d['valid_inequality_weight_signs'] is True
assert margin>0,(delta,M,eps,am,bm,margin)
out={'status':'STRICT_EXACT_CRITERION_PASS_PENDING_WHOLE_PROOF_ACCEPTANCE','scope':'B684..688 only, hence candidate global upper683; upper682 OPEN','delta':str(delta),'query_max':str(M),'uniform_error':str(eps),'alpha_max':str(am),'beta_max':str(bm),'exact_safe_margin':str(margin),'oracle_raw_maximum':raw,'oracle_stdout_sha256':hashlib.sha256(log.read_bytes()).hexdigest(),'matrix_sha256':hashlib.sha256((O/'oracle_matrices.txt').read_bytes()).hexdigest(),'linear_sha256':hashlib.sha256((O/'oracle_linear.txt').read_bytes()).hexdigest(),'solver_status_is_not_premise':True,'whole_B_proof_acceptance':'PENDING'}
(O/'FINAL_CRITERION_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
