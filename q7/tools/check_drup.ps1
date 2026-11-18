param([Parameter(Mandatory=$true)][string]$Prefix)
$ErrorActionPreference='Stop'
$source=@'
using System;
using System.IO;
using System.Linq;
using System.Collections.Generic;
using System.Diagnostics;
using System.Security.Cryptography;
public class RethlasRupCheck {
 int n,originalEnd; bool empty=false;
 List<int[]> clauses=new List<int[]>();
 Dictionary<string,Stack<int>> ids=new Dictionary<string,Stack<int>>();
 Dictionary<int,int> units=new Dictionary<int,int>(), originals;
 List<int>[] watches; sbyte[] values; int[] trail; int tail;
 string Key(int[] c) {var d=(int[])c.Clone();Array.Sort(d);return String.Join(",",d);}
 int[] Parse(string line,bool deletion=false) {var t=line.Split((char[])null,StringSplitOptions.RemoveEmptyEntries).Skip(deletion?1:0).Select(Int32.Parse).ToArray();if(t.Length==0||t[t.Length-1]!=0||t.Take(t.Length-1).Any(z=>z==0))throw new Exception("Malformed or truncated clause");return t.Take(t.Length-1).Distinct().ToArray();}
 void Add(int[] c) {
  if(c.Length==0){empty=true;return;}
  if(c.Length==1){units[c[0]]=units.GetValueOrDefault(c[0])+1;return;}
  int k=clauses.Count;clauses.Add(c);string key=Key(c);
  if(!ids.ContainsKey(key))ids[key]=new Stack<int>();ids[key].Push(k);
  watches[c[0]+n].Add(k);watches[c[1]+n].Add(k);
 }
 void Delete(int[] c) {
  if(c.Length==1){int lit=c[0],v=units.GetValueOrDefault(lit);if(v>originals.GetValueOrDefault(lit)){if(v==1)units.Remove(lit);else units[lit]=v-1;}return;}
  string key=Key(c);if(ids.TryGetValue(key,out var s)&&s.Count>0&&s.Peek()>=originalEnd){clauses[s.Pop()]=null;if(s.Count==0)ids.Remove(key);}
 }
 bool Put(int lit){int v=Math.Abs(lit);sbyte s=(sbyte)(lit>0?1:-1);if(values[v]!=0)return values[v]==s;values[v]=s;trail[tail++]=lit;return true;}
 int Value(int lit){return values[Math.Abs(lit)]*(lit>0?1:-1);}
 bool Rup(int[] c) {
  if(empty)return true;Array.Clear(values,0,values.Length);tail=0;
  foreach(int lit in units.Keys)if(!Put(lit))return true;
  foreach(int lit in c)if(!Put(-lit))return true;
  int head=0;
  while(head<tail){int f=-trail[head++];var w=watches[f+n];int i=0;
   while(i<w.Count){int k=w[i];var cl=clauses[k];
    if(cl==null){w[i]=w[w.Count-1];w.RemoveAt(w.Count-1);continue;}
    if(cl[0]==f){int z=cl[0];cl[0]=cl[1];cl[1]=z;}
    if(cl[1]!=f)throw new Exception("Watch invariant failed");
    int other=cl[0];if(Value(other)>0){i++;continue;}
    int replacement=-1;for(int j=2;j<cl.Length;j++)if(Value(cl[j])>=0){replacement=j;break;}
    if(replacement>=0){int z=cl[1];cl[1]=cl[replacement];cl[replacement]=z;w[i]=w[w.Count-1];w.RemoveAt(w.Count-1);watches[cl[1]+n].Add(k);continue;}
    if(!Put(other))return true;i++;
   }
  }
  return false;
 }
 string Hash(string path){using(var f=File.OpenRead(path))using(var h=SHA256.Create())return BitConverter.ToString(h.ComputeHash(f)).Replace("-","").ToLowerInvariant();}
 bool FinalFromAllValidated(string prefix,long stop) {
  var fresh=new RethlasRupCheck();fresh.n=n;fresh.watches=Enumerable.Range(0,2*n+1).Select(_=>new List<int>()).ToArray();fresh.values=new sbyte[n+1];fresh.trail=new int[n+1];
  foreach(string l in File.ReadLines(prefix+".cnf"))if(l.Length>0&&l[0]!='c'&&l[0]!='p')fresh.Add(fresh.Parse(l));
  long k=0;foreach(string l in File.ReadLines(prefix+".drup")){k++;if(k>=stop)break;if(String.IsNullOrWhiteSpace(l)||l.StartsWith("d "))continue;fresh.Add(fresh.Parse(l));}
  return fresh.Rup(new int[0]);
 }
 public Dictionary<string,object> Run(string prefix){
  var cnf=File.ReadLines(prefix+".cnf");string header=cnf.First(s=>s.StartsWith("p "));var hh=header.Split(' ',StringSplitOptions.RemoveEmptyEntries);n=Int32.Parse(hh[2]);int count=Int32.Parse(hh[3]),seen=0;
  watches=Enumerable.Range(0,2*n+1).Select(_=>new List<int>()).ToArray();values=new sbyte[n+1];trail=new int[n+1];
  foreach(string line in File.ReadLines(prefix+".cnf")){if(line.Length==0||line[0]=='p'||line[0]=='c')continue;var c=Parse(line);if(c.Any(z=>Math.Abs(z)>n))throw new Exception("Invalid variable");Add(c);seen++;}
  if(seen!=count)throw new Exception("Wrong input count");originalEnd=clauses.Count;originals=new Dictionary<int,int>(units);
  long lineNo=0,checkedCount=0,deleted=0;bool derivedEmpty=false;var sw=Stopwatch.StartNew();
  foreach(string line in File.ReadLines(prefix+".drup")){lineNo++;if(String.IsNullOrWhiteSpace(line))continue;
   if(line.StartsWith("d ")){Delete(Parse(line,true));deleted++;continue;}
   var c=Parse(line);if(c.Any(z=>Math.Abs(z)>n))throw new Exception("Proof variable out of range");
   if(!Rup(c)){
    if(c.Length!=0 || !FinalFromAllValidated(prefix,lineNo))throw new Exception("Non-RUP addition at line "+lineNo);
   }
   Add(c);checkedCount++;if(c.Length==0)derivedEmpty=true;
   if(checkedCount%100000==0)Console.WriteLine("RUP checked "+checkedCount+" additions in "+sw.Elapsed.TotalSeconds.ToString("F1")+" s");
  }
  if(!derivedEmpty)throw new Exception("No validated empty clause");
  return new Dictionary<string,object>{{"valid",true},{"method","C# watched-literal RUP; retain original axioms; final empty may use all previously validated clauses"},{"checked_additions",checkedCount},{"deletions",deleted},{"seconds",sw.Elapsed.TotalSeconds},{"cnf_sha256",Hash(prefix+".cnf")},{"proof_sha256",Hash(prefix+".drup")}};
 }
}
'@
Add-Type -TypeDefinition $source -Language CSharp
$taskPrefix=(Resolve-Path -LiteralPath ($Prefix+'.cnf')).Path -replace '\.cnf$',''
$result=[RethlasRupCheck]::new().Run($taskPrefix)
$json=$result | ConvertTo-Json
$json | Set-Content -LiteralPath ($taskPrefix+'.checked_cs.json') -Encoding utf8
Write-Output $json
