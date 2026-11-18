"""Rebuild the integer certificate. Python uses only its standard library."""
from pathlib import Path
from fractions import Fraction
from array import array
import json, os, struct, subprocess, sys
root=Path(__file__).resolve().parent
os.chdir(root)
os.environ.setdefault("OMP_NUM_THREADS","8")
assert sys.byteorder=="little"
def run(args):
    return subprocess.check_output([str(x) for x in args],text=True)
def build(n):
    subprocess.run(["g++","-std=c++20","-O3","-march=native","-fopenmp","-fsanitize=undefined",
                    "-fno-sanitize-recover=all",n+".cpp","-o",n],check=True)
def get(n):
    return json.loads(Path(n).read_text())
def exact(q,f,r):
    found=json.loads(run(["./exact","full_masks.bin",q,f,"62","cop_terms_general.txt","cubic_terms.txt"]))
    assert found==get(r)
def mixed(a,b,m,d):
    assert 0<=m<=d and d>0
    return -((-(d-m)*a-m*b)//d)
def rebuild_base(r):
    for n in ("complete","exact","arm_integer","change_unary","high5","high6","five_features",
              "six_profile","six_check","seven_mix","seven_conflict"):
        build(n)
    coverage=json.loads(run(["./complete","full_masks.bin"]))
    assert coverage["representatives"]==3212821 and coverage["labelled_graphs_direct"]==1226436381
    exact("q128.bin","factors.bin","four.json")
    run(["./arm_integer","arm_factors.txt","full_masks.bin","scaled_scores.bin","unary.bin","gaps.bin"])
    exact("q128-first.bin","factors-first.bin","four-first.json")
    run(["./change_unary","unary.bin","scaled_scores.bin","gaps.bin",r["first_m"],r["first_d"],
         "mixed_unary.bin","mixed_gap.bin"])
    assert r["threshold5"]%10==0
    print(run(["./high5","mixed_unary.bin",r["threshold5"]//10,"all","mixed_gap.bin"]).strip(),flush=True)
    with open("high5.bin","rb") as src, open("residual_high5.bin","wb") as dest:
        for record in struct.iter_unpack("<q8H",src.read()):
            if record[0]>=r["residual_threshold5"]:
                dest.write(struct.pack("<q8H",*record))
    assert r["residual_threshold5"]>=r["threshold5"]
    assert Path("high5.bin").stat().st_size==r["n5_raw"]*24
    assert max(row[0] for row in struct.iter_unpack("<q8H",Path("high5.bin").read_bytes()))==r["max5"]
    print(run(["./high6","high5.bin",r["threshold5"],r["threshold6"],"high6.bin"]).strip(),flush=True)
    # Validate the catalogue up to isometry regardless of output order.
    unweighted=run(["./seven_mix","high6.bin",r["threshold6"]])
    assert int(unweighted.split()[3])==r["n6_orbits"]
    run(["./five_features","high5.bin","primary_fives.bin"])
    run(["./six_profile","high5.bin","high6.bin","primary_sixes.bin"])
    five_vals=[row[0] for row in struct.iter_unpack("<q10i",Path("primary_fives.bin").read_bytes())]
    for score,*ids in struct.iter_unpack("<q12i",Path("primary_sixes.bin").read_bytes()):
        assert sum(five_vals[j] if j>=0 else r["threshold5"] for j in ids)==score
    run(["./five_features","residual_high5.bin","fives.bin"])
    run(["./six_profile","residual_high5.bin","high6.bin","sixes.bin"])
def finish(r):
    if not r["top_m"]:
        ans=run(["./seven_mix","high6.bin",r["threshold6"]])
        assert int(ans.split()[1])==r["upper7"]
        second=run(["./seven_conflict","high6.bin",r["threshold6"]]);assert int(second.split()[1])==r["upper7"]
        assert Fraction(r["upper_fraction"])==Fraction(r["upper7"],1680*(1<<46))
        print(ans.strip(),flush=True)
        print("PASS upper =",r["upper_fraction"],"=",float(Fraction(r["upper_fraction"])),flush=True)
        return
    exact("q128-second.bin","factors-second.bin","four-second.json")
    q=array("q");q.frombytes(Path("scaled_scores.bin").read_bytes())
    z5=mixed(r["residual_threshold5"],10*max(q),r["second_m"],r["second_d"])
    v5=[]
    for ns,*idx in struct.iter_unpack("<q10i",Path("fives.bin").read_bytes()):
        v5.append(max(z5,mixed(ns,sum(q[j] for j in idx),r["second_m"],r["second_d"])))
    assert len(v5)==34153
    result=run(["./six_check","residual_high5.bin",r["residual_threshold5"],"scaled_scores.bin",
                r["second_m"],r["second_d"],r["residual_upper6"]-1])
    assert int(result.split()[1])==r["residual_upper6"] and int(result.split()[3])==z5
    print(result.strip(),flush=True)
    z6=mixed(r["threshold6"],r["residual_upper6"],r["top_m"],r["top_d"])
    values=array("q",[z6])
    for ns,*idx in struct.iter_unpack("<q12i",Path("sixes.bin").read_bytes()):
        vs=sum(z5 if j==-1 else v5[j] for j in idx)
        assert vs<=r["residual_upper6"]
        values.append(mixed(ns,vs,r["top_m"],r["top_d"]))
    Path("mixed_six.bin").write_bytes(values.tobytes())
    result=run(["./seven_mix","high6.bin",r["threshold6"],"mixed_six.bin"])
    assert int(result.split()[1])==r["upper7"]
    second=run(["./seven_conflict","high6.bin",r["threshold6"],"mixed_six.bin"]);assert int(second.split()[1])==r["upper7"]
    assert Fraction(r["upper_fraction"])==Fraction(r["upper7"],1680*(1<<46))
    print(result.strip(),flush=True)
    print("PASS upper =",r["upper_fraction"],"=",float(Fraction(r["upper_fraction"])),flush=True)
if __name__=="__main__":
    receipt=get("receipt.json")
    rebuild_base(receipt)
    finish(receipt)
