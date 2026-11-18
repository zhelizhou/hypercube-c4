"""Mechanical checkpoint and complete pricing; all mathematical acceptance separate."""
from pathlib import Path
import sys,json,datetime,subprocess,os,time
P=Path(__file__).resolve().parent;R=(P/sys.argv[1]).resolve();t=time.monotonic()
d=json.loads((R/'RESULT.json').read_text());assert d['status']=='NUMERIC_LIBRARY_DUAL_CANDIDATE'
live=json.loads((R/'LIVE_RUN.json').read_text());live.update({'status':'FINISHED_CHECKPOINT','finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result_status':d['status']});(R/'LIVE_RUN.json').write_text(json.dumps(live,indent=2)+'\n')
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
before=set(R.glob('full_oracle_*'))
with (R/'extract_latest.stdout.txt').open('w') as out, (R/'extract_latest.stderr.txt').open('w') as err:
 run=subprocess.run([sys.executable,str(P/'extract_active_dual_oracle.py'),str(R)],stdout=out,stderr=err,env=env)
assert run.returncode==0
created=set(R.glob('full_oracle_*'))-before;assert len(created)==1;S=created.pop()
with (S/'adapter.stdout.txt').open('w') as out, (S/'adapter.stderr.txt').open('w') as err:
 run=subprocess.run([sys.executable,str(P/'run_local_score_oracle.py'),str(S/'LOCAL_PRICE_SCORE.json')],stdout=out,stderr=err,env=env)
assert run.returncode==0
o=json.loads((S/'OWN_ORACLE_RUN.json').read_text());q=json.loads((S/'LOCAL_PRICE_SCORE.json').read_text());L=o['exact_max_integer_numerator']/q['integer_score_positive_denominator']
v={'status':'NUMERIC_COMPLETE_ORACLE_MARGIN_DIAGNOSTIC_ONLY','numeric_delta':d['numeric_delta'],'numeric_full_lambda_max_of_rounded_query':L,'numeric_finite_alpha_max':d['numeric_alpha_max'],'numeric_finite_beta_max':d['numeric_beta_max'],'margin_before_uniform_rounding_and_exact_row_validation':d['numeric_delta']-L-d['numeric_alpha_max']-d['numeric_beta_max'],'is_exact_fullNO':False,'query_dir':str(S),'exact_max':o['exact_max_integer_numerator'],'actual_Q4_mask':o['worst_graph'],'seconds':time.monotonic()-t}
(S/'NUMERIC_FINAL_MARGIN_DIAGNOSTIC.json').write_text(json.dumps(v,indent=2)+'\n');print(json.dumps(v))
