"""Run complete unchanged traversal, then exact-check every positive-class best."""
from pathlib import Path
import sys,subprocess,json,time,hashlib
P=Path(__file__).resolve().parent;S=Path(sys.argv[1]).resolve();O=S/'all_positive_classes';O.mkdir(exist_ok=False)
root=P.parent/'finite8_flags/oracle';t=time.monotonic();cmd=[str(P/'oracle_batch/finite8_batch_all'),str(S/'oracle_matrices.txt'),'--linear',str(S/'oracle_linear.txt')]
r=subprocess.run(cmd,cwd=root,capture_output=True,text=True);(O/'batch.stdout.txt').write_text(r.stdout);(O/'batch.stderr.txt').write_text(r.stderr);assert r.returncode==0
check=subprocess.run([sys.executable,str(P/'oracle_batch/verify_all_batch.py'),str(S),str(O)],cwd=P,capture_output=True,text=True);(O/'verify.stdout.txt').write_text(check.stdout);(O/'verify.stderr.txt').write_text(check.stderr);assert check.returncode==0,check.stderr
receipt={'status':'COMPLETE_POSITIVE_CLASS_BATCH_EXACT_REPLAY_PASS','seconds':time.monotonic()-t,'command':cmd,'checker_stdout':check.stdout,'root_cwd_readonly':str(root),'is_Q8_counterexample':False,'goal':'OPEN'};(O/'COLLECTION_RUN.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt))
