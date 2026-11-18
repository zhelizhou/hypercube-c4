"""Three already-authorized, genuinely enriched B column-generation rounds.

This only composes existing deterministic commands. A positive numerical
complete margin stops for exact reconstruction; it never asserts NO.
"""
from pathlib import Path
import sys,subprocess,json,datetime,os,time
P=Path(__file__).resolve().parent;scope='pool_B684plus_enriched6';env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');history=[]
state=P/'B_SEQUENCE_RUN001.json';assert not state.exists();start=time.monotonic()
def save(stage,**kw):
 d={'owner':'/root/prove_mixed_zero_row','pid':os.getpid(),'stage':stage,'current_scope':scope,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'seconds':time.monotonic()-start,'history':history,'goal':'OPEN',**kw};state.write_text(json.dumps(d,indent=2)+'\n');print(json.dumps({k:v for k,v in d.items() if k!='history'}),flush=True)
def run(cmd,out):
 with Path(str(out)+'.stdout.txt').open('w') as a,Path(str(out)+'.stderr.txt').open('w') as b:
  r=subprocess.run(cmd,cwd=P,env=env,stdout=a,stderr=b)
 if r.returncode:save('EXECUTION_ERROR',command=cmd,returncode=r.returncode,logs=str(out));raise SystemExit(r.returncode)
for no in range(7,10):
 S=P/scope/'full_oracle_001';margin=json.loads((S/'NUMERIC_FINAL_MARGIN_DIAGNOSTIC.json').read_text())['margin_before_uniform_rounding_and_exact_row_validation']
 if margin>0:save('POSITIVE_NUMERIC_MARGIN_REQUIRES_EXACT_VALIDATION',numeric_margin=margin);sys.exit(0)
 if (P/'B_SEQUENCE_STOP_AFTER_CHECKPOINT').exists():save('CALLER_REQUESTED_CHECKPOINT',numeric_margin=margin);sys.exit(0)
 save('COMPLETE_TOP8_OUTPUT_COLLECTION',numeric_margin=margin)
 if not (S/'all_positive_top8/BATCH_VERIFIED.json').exists():run([sys.executable,str(P/'collect_top8_positive.py'),str(S)],P/scope/'top8_collection')
 new=f'pool_B684plus_enriched{no}';save('EXACT_FEATURE_POOL_EXTENSION',next_scope=new)
 run([sys.executable,str(P/'extend_verified_B_pool.py'),scope,new,str(S/'all_positive_top8/BATCH_VERIFIED.json')],P/(new+'_prepare'))
 source=scope;scope=new;R=P/scope;prepared=json.loads((R/'ENRICHED_SCOPE_INPUT.json').read_text());assert prepared['new_unique_columns']>0,'No new actual feature: preserve this precise obstacle.'
 save('ACTUAL_WORKING_SET_MASTER_RUNNING',new_columns=prepared['new_unique_columns'],library=prepared['new_library'])
 cmd=[sys.executable,str(R/'RUN_CONTROLLER.py'),'--seconds','180','--max-masters','160'];live={'status':'STARTING','owner':'/root/prove_mixed_zero_row','command':cmd,'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':scope,'recovery':'read B_SEQUENCE_RUN001 plus LIVE_RUN and logs; each predecessor stays frozen','goal':'OPEN'}
 with (R/'run001.stdout.txt').open('w') as a,(R/'run001.stderr.txt').open('w') as b:
  child=subprocess.Popen(cmd,cwd=P,env=env,stdout=a,stderr=b);live.update({'status':'RUNNING','pid':child.pid});(R/'LIVE_RUN.json').write_text(json.dumps(live,indent=2)+'\n');code=child.wait()
 if code:save('MASTER_EXECUTION_ERROR',returncode=code);sys.exit(code)
 result=json.loads((R/'RESULT.json').read_text());live.update({'status':'FINISHED_CHECKPOINT','result_status':result['status'],'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()});(R/'LIVE_RUN.json').write_text(json.dumps(live,indent=2)+'\n')
 if result['status']!='NUMERIC_LIBRARY_DUAL_CANDIDATE':save('NON_DUAL_CHECKPOINT_FOR_CALLER',result_status=result['status']);sys.exit(0)
 save('COMPLETE_Q4_PRICE_OF_NEW_ACTUAL_DUAL')
 run([sys.executable,str(P/'finish_and_price_B.py'),scope],R/'complete_price001')
 m=json.loads((R/'full_oracle_001/NUMERIC_FINAL_MARGIN_DIAGNOSTIC.json').read_text());history.append({'scope':scope,'source':source,'new_features':prepared['new_unique_columns'],'library':prepared['new_library'],'numerical_library_gap':result['numeric_finite_gap'],'complete_price':m})
 if m['margin_before_uniform_rounding_and_exact_row_validation']>0:save('POSITIVE_NUMERIC_MARGIN_REQUIRES_EXACT_VALIDATION',numeric_margin=m['margin_before_uniform_rounding_and_exact_row_validation']);sys.exit(0)
save('THREE_NEW_SCOPE_CHECKPOINTS_FINISHED_NO_CLAIM')
