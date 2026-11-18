from pathlib import Path
import json,subprocess,shutil
R=Path(__file__).resolve().parent;P=R.parent
source=P/'pricing_master050/INPUT_POINT.json'; script=P/'price_point.py'; results={}
def run(label,point,run_dir,rounds=None,expected=None):
    args=['python3',str(script),str(point),str(run_dir)]+([] if rounds is None else [str(rounds)])
    out=subprocess.run(args,capture_output=True,text=True)
    assert out.returncode!=0 and (expected is None or expected in out.stdout+out.stderr),(label,out.returncode,out.stdout,out.stderr)
    assert not list(run_dir.glob('query_*.txt')) and not (run_dir/'CONDITIONAL_VERTEX_CUT.json').exists()
    results[label]={'returncode':out.returncode,'diagnostic':(out.stdout+out.stderr).strip(),'no_oracle_query_or_cut_written':True}
run('rounds_zero',source,R/'cli_zero',0,'MAX_ROUNDS must be in 1..80')
run('rounds_above_limit',source,R/'cli_81',81,'MAX_ROUNDS must be in 1..80')
a=R/'cli_existing_history';a.mkdir(exist_ok=True);shutil.copyfile(source,a/'INPUT_POINT.json');(a/'SEPARATION_HISTORY.json').write_text('[]\n')
run('existing_history',source,a,1,'completed/partial run exists')
a=R/'cli_different_input';a.mkdir(exist_ok=True);(a/'INPUT_POINT.json').write_text('{}\n')
run('different_existing_snapshot',source,a,1,'existing INPUT_POINT differs')
point=json.loads(source.read_text());n=point['alpha'][0][2];n[0]+=1;n[5]-=1
m=R/'degree0_mass_point.json';m.write_text(json.dumps(point)+'\n')
run('positive_degree0_mass',m,R/'cli_degree0_mass',1,'maximal-only domain requires degree-zero mass exactly zero')
(R/'CLI_CONTRACT_RESULT.json').write_text(json.dumps({'status':'PASS_EARLY_REJECTION_PATHS_NO_LP','results':results},indent=2)+'\n')
print(json.dumps({'status':'PASS_EARLY_REJECTION_PATHS_NO_LP','checks':len(results)}))
