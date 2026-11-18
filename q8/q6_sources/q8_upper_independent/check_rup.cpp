// Independent sequential RUP verifier, keeping every verified consequence.
// Deletions are ignored: a verified earlier consequence remains a consequence.
// No SAT solver library is used. RAT-only additions are deliberately rejected.
#include <algorithm>
#include <chrono>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
using namespace std;
struct Clause{vector<int>lit;int a=0,b=1;};
struct Checker{
 int nv;vector<Clause>cs;vector<vector<int>>watch;vector<int>units,assignment,queue;
 Checker(int n):nv(n),watch(2*n+2),assignment(n+1){}
 int ix(int lit){return 2*(abs(lit)-1)+(lit<0);}
 int value(int lit){return assignment[abs(lit)]*(lit>0?1:-1);}
 bool enqueue(int lit){int v=value(lit);if(v<0)return false;if(!v){assignment[abs(lit)]=lit>0?1:-1;queue.push_back(lit);}return true;}
 bool rup(const vector<int>&clause){
  fill(assignment.begin(),assignment.end(),0);queue.clear();
  for(int lit:clause)if(!enqueue(-lit))return true;
  for(int lit:units)if(!enqueue(lit))return true;
  for(size_t head=0;head<queue.size();head++){
   int f=-queue[head];auto &list=watch[ix(f)];size_t k=0;
   while(k<list.size()){
    int id=list[k];auto &c=cs[id];
    int *wf=c.lit[c.a]==f?&c.a:&c.b;
    int other=(wf==&c.a)?c.b:c.a;
    if(c.lit[*wf]!=f){cerr<<"internal watcher error\n";exit(3);}
    if(value(c.lit[other])>0){k++;continue;}
    int replacement=-1;
    for(int j=0;j<int(c.lit.size());j++)if(j!=c.a&&j!=c.b&&value(c.lit[j])>=0){replacement=j;break;}
    if(replacement>=0){*wf=replacement;list[k]=list.back();list.pop_back();watch[ix(c.lit[replacement])].push_back(id);}
    else {if(!enqueue(c.lit[other]))return true;k++;}
   }
  }
  return false;
 }
 void add(vector<int>v){
  sort(v.begin(),v.end());v.erase(unique(v.begin(),v.end()),v.end());
  for(int lit:v)if(binary_search(v.begin(),v.end(),-lit))return; // tautology
  for(int lit:v)if(abs(lit)>nv||lit==0){cerr<<"literal outside range\n";exit(4);}
  if(v.empty())return;
  if(v.size()==1){units.push_back(v[0]);return;}
  int id=cs.size();cs.push_back({move(v),0,1});watch[ix(cs[id].lit[0])].push_back(id);watch[ix(cs[id].lit[1])].push_back(id);
 }
};
int main(int argc,char**argv){
 if(argc!=3)return 2;auto start=chrono::steady_clock::now();ifstream in(argv[1]);
 string line;int nv=0,expected=0;vector<vector<int>>input;
 while(getline(in,line)){if(line.empty()||line[0]=='c')continue;istringstream s(line);if(line[0]=='p'){string p,cnf;s>>p>>cnf>>nv>>expected;continue;}vector<int>c;int lit;bool end=false;while(s>>lit){if(lit==0){end=true;break;}c.push_back(lit);}if(!end)return 5;input.push_back(c);}
 if(nv<=0||int(input.size())!=expected)return 6;
 Checker checker(nv);for(auto c:input)checker.add(c);
 ifstream proof(argv[2]);if(!proof)return 7;long long additions=0,deletions=0,linenumber=0;bool empty=false;
 while(getline(proof,line)){
  linenumber++;if(line.empty()||line[0]=='c')continue;if(line[0]=='d'){deletions++;continue;}
  istringstream s(line);vector<int>c;int lit;bool end=false;
  while(s>>lit){if(lit==0){end=true;break;}if(abs(lit)>nv){cerr<<"bad literal\n";return 8;}c.push_back(lit);}
  if(!end)return 9;
  if(!checker.rup(c)){cerr<<"NOT RUP at proof line "<<linenumber<<" addition "<<additions+1<<'\n';return 1;}
  additions++;if(c.empty()){empty=true;break;}checker.add(c);
 }
 double seconds=chrono::duration<double>(chrono::steady_clock::now()-start).count();
 cout<<"{\"valid\":"<<(empty?"true":"false")<<",\"verified_additions\":"<<additions<<",\"ignored_deletions\":"<<deletions<<",\"final_empty_clause\":"<<(empty?"true":"false")<<",\"seconds\":"<<seconds<<"}\n";
 return empty?0:10;
}
