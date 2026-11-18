"""Run complete unchanged traversal, then exact-check every positive-class best."""
from pathlib import Path
import sys,subprocess,json,time,hashlib,os
from fractions import Fraction
os.environ['PYTHONDONTWRITEBYTECODE']='1'
P=Path(__file__).resolve().parent;S=Path(sys.argv[1]).resolve();O=S/'all_positive_top8';O.mkdir(exist_ok=False)
root=P.parent/'finite8_flags/oracle';t=time.monotonic();delta=Fraction(str(json.loads((S.parent/'RESULT.json').read_text())['numeric_delta']));den=json.loads((S/'LOCAL_PRICE_SCORE.json').read_text())['integer_score_positive_denominator'];v=delta*den/16;threshold=max(0,(v.numerator+v.denominator-1)//v.denominator);cmd=[str(P/'oracle_batch/finite8_batch_top8'),str(S/'oracle_matrices.txt'),'--linear',str(S/'oracle_linear.txt'),str(threshold)]
r=subprocess.run(cmd,cwd=root,capture_output=True,text=True);(O/'batch.stdout.txt').write_text(r.stdout);(O/'batch.stderr.txt').write_text(r.stderr);assert r.returncode==0
check=subprocess.run([sys.executable,str(P/'oracle_batch/verify_top8_batch.py'),str(S),str(O)],cwd=P,capture_output=True,text=True);(O/'verify.stdout.txt').write_text(check.stdout);(O/'verify.stderr.txt').write_text(check.stderr);assert check.returncode==0,check.stderr
receipt={'status':'COMPLETE_POSITIVE_CLASS_BATCH_EXACT_REPLAY_PASS','seconds':time.monotonic()-t,'command':cmd,'checker_stdout':check.stdout,'root_cwd_readonly':str(root),'supplement_threshold_integer':threshold,'all_positive_class_single_best_retained':True,'additional_Aut_distinct_actual_graphs_per_class_limit':8,'is_Q8_counterexample':False,'goal':'OPEN'};(O/'COLLECTION_RUN.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt))
